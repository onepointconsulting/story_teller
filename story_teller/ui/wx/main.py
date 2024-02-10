from pathlib import Path

import wx

from story_teller.model.novel_content import NovelContent, create_empty_novel_content
from story_teller.ui.wx.tab_config import TabConfig
from story_teller.ui.wx.tab_main import TabMain
from story_teller.config.config import cfg

env_path = Path("./.env")


class StoryTeller(wx.App):
    def OnInit(self):
        screenWidth, screenHeight = wx.DisplaySize()
        initial_width = screenWidth
        initial_height = screenHeight - 50
        self.frame = StoryTellerConfigFrame(
            parent=None,
            title="Story Submission Form",
            size=(initial_width, initial_height),
        )
        self.frame.Maximize(True)
        self.frame.Show()
        return True


class StoryTellerConfigFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super(StoryTellerConfigFrame, self).__init__(parent, title=title, size=size)

        self.novel_content: NovelContent = create_empty_novel_content()

        # Create a Notebook widget
        notebook = wx.Notebook(self)

        # Create the tab windows
        tab_main = TabMain(notebook)
        self.tab_config = TabConfig(notebook)

        # Add the tabs to the notebook with the respective names
        notebook.AddPage(tab_main, "Main")
        notebook.AddPage(self.tab_config, "Configuration")

        self.CreateStatusBar()
        self.SetStatusText("Ready")

        self.Centre()

        self.show_input_openai_key_dialogue()
        self.specify_output_folder()

    def show_input_openai_key_dialogue(self):
        if cfg.openai_api_key is None or cfg.openai_api_key == "":
            dialog = wx.TextEntryDialog(
                self,
                "This tool requires an Open API key which you can get from https://platform.openai.com/api-keys. Please enter the OpenAI API key",
                "OpenAI API Key",
                "",
            )
            if dialog.ShowModal() == wx.ID_OK:
                cfg.openai_api_key = dialog.GetValue()
                # Ensure the UI knows about the temporary path.
                self.tab_config.set_my_open_api_key(cfg.openai_api_key)
                # Write the .env file
                write_to_env("OPENAI_API_KEY", cfg.openai_api_key)
                dialog.Destroy()
                if len(cfg.openai_api_key) > 0:
                    try:
                        cfg.init_llms()
                    except:
                        show_error_message(self)
                else:
                    # No key entered
                    dialog.Destroy()
                    self.show_input_openai_key_dialogue()
            else:
                # User cancelled the dialog
                dialog.Destroy()
                self.show_input_openai_key_dialogue()

    def specify_output_folder(self):
        if cfg.tmp_folder_str is None or cfg.tmp_folder_str == "":
            # Create and show the DirDialog
            with wx.DirDialog(
                self,
                "Choose a directory for generating the story",
                style=wx.DD_DEFAULT_STYLE,
            ) as dirDialog:
                if dirDialog.ShowModal() == wx.ID_CANCEL:
                    self.specify_output_folder()
                    return  # User cancelled the dialog
                # Proceed to use the selected directory
                pathname = dirDialog.GetPath()
                try:
                    cfg.tmp_folder_str = pathname
                    write_to_env("TMP_FOLDER", pathname)
                    cfg.init_temp_folders()
                except IOError:
                    wx.LogError(f"Cannot open directory '{pathname}'.")


def show_error_message(parent):
    dialog = wx.MessageDialog(
        parent, "Could not create LLM connection", "Error", wx.OK | wx.ICON_ERROR
    )
    dialog.ShowModal()
    dialog.Destroy()


def write_to_env(var_name: str, value: str):
    with open(env_path, "a", encoding="utf-8") as f:
        f.write(f"\n{var_name}={value}")


if __name__ == "__main__":
    app = StoryTeller()
    app.MainLoop()
