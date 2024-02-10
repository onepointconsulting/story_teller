import wx

from story_teller.model.novel_content import NovelContent, create_empty_novel_content
from story_teller.ui.wx.tab_config import TabConfig
from story_teller.ui.wx.tab_main import TabMain
from story_teller.config.config import cfg


class StoryTeller(wx.App):
    def OnInit(self):
        screenWidth, screenHeight = wx.DisplaySize()
        initial_width = screenWidth
        initial_height = screenHeight * 0.8
        self.frame = StoryTellerConfigFrame(
            parent=None,
            title="Story Submission Form",
            size=(initial_width, initial_height),
        )
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

        show_input_openai_key_dialogue(self)


def show_input_openai_key_dialogue(parent):
    if cfg.openai_api_key is None or cfg.openai_api_key == "":
        dialog = wx.TextEntryDialog(
            parent,
            "This tool requires an Open API key which you can get from https://platform.openai.com/api-keys. Please enter the OpenAI API key",
            "OpenAI API Key",
            "",
        )
        if dialog.ShowModal() == wx.ID_OK:
            cfg.openai_api_key = dialog.GetValue()
            parent.tab_config.set_my_open_api_key(cfg.openai_api_key)
            dialog.Destroy()
            if len(cfg.openai_api_key) > 0:
                try:
                    cfg.init_llms()
                except:
                    show_error_message(parent)
            else:
                dialog.Destroy()
                show_input_openai_key_dialogue(parent)    
        else:
            # User cancelled the dialog
            dialog.Destroy()
            show_input_openai_key_dialogue(parent)
        


def show_error_message(parent):
    dialog = wx.MessageDialog(parent, "Could not create LLM connection", "Error", wx.OK | wx.ICON_ERROR)
    dialog.ShowModal()
    dialog.Destroy()

if __name__ == "__main__":
    app = StoryTeller()
    app.MainLoop()
