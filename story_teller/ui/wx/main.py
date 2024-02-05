import wx

from story_teller.model.novel_content import NovelContent, create_empty_novel_content
from story_teller.ui.wx.tab_config import TabConfig
from story_teller.ui.wx.tab_main import TabMain


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
        tab_config = TabConfig(notebook)

        # Add the tabs to the notebook with the respective names
        notebook.AddPage(tab_main, "Main")
        notebook.AddPage(tab_config, "Configuration")

        self.CreateStatusBar()
        self.SetStatusText("Ready")

        self.Centre()


if __name__ == "__main__":
    app = StoryTeller()
    app.MainLoop()
