from typing import List, Any, Tuple

import random
import wx
import threading
import webbrowser

from story_teller.ui.wx.ui_helper import decorate_required, decorate_required_label
from story_teller.ui.wx.ui_helper import layout_label_and_control, create_text_field
from story_teller.service.simple_chain_service import develop_story
from story_teller.service.story_callback import StoryCallbackMixin
from story_teller.test.provider.novel_content_provider import create_novel_content_list


class TabMain(wx.Panel):
    def __init__(self, parent):
        super(TabMain, self).__init__(parent)

        self.novel_content = parent.Parent.novel_content
        self.layout = wx.BoxSizer(wx.VERTICAL)

        # Create the form elements
        self.story_title_label, self.story_title_textctrl = create_text_field(
            self, "Story Title", "Please enter a story title here"
        )
        self.story_sub_title_label, self.story_sub_title_textctrl = create_text_field(
            self, "Story Subtitle", "Please enter a story subtitle here"
        )

        self.story_description_label = wx.StaticText(
            self, label=decorate_required_label("Story Description")
        )
        self.story_description_textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.story_description_textctrl.SetHint(
            "Please enter the full story description here"
        )
        decorate_required(self.story_description_textctrl)

        self.generate_random_content_button = wx.Button(
            self, label="Generate random novel content"
        )
        # Bind the button to an event handler
        self.generate_random_content_button.Bind(
            wx.EVT_BUTTON, self.generate_random_content
        )

        self.literary_author_label = wx.StaticText(self, label="Literary Author :")
        self.literary_author_textctrl = wx.TextCtrl(self)
        self.literary_author_textctrl.SetValue(self.novel_content.style_info.author)

        self.book_name_label = wx.StaticText(self, label="Book Name:")
        self.book_name_textctrl = wx.TextCtrl(self)
        self.book_name_textctrl.SetValue(self.novel_content.style_info.book)

        self.cleanup_checkbox = wx.CheckBox(
            self, label="Cleanup texts after generation"
        )

        self.gauge = wx.Gauge(self, range=100, pos=(50, 100), size=(100, 25))

        # Create submit button
        self.submit_button = wx.Button(self, label="Start novel generation")
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)

        self.layout_components()

    def layout_components(self):
        # Add the form elements to the layout
        layout_label_and_control(
            self.layout, self.story_title_label, self.story_title_textctrl
        )
        layout_label_and_control(
            self.layout, self.story_sub_title_label, self.story_sub_title_textctrl
        )
        self.layout.Add(self.story_description_label, 0, wx.ALL, 5)
        self.layout.Add(self.story_description_textctrl, 1, wx.EXPAND | wx.ALL, 5)

        self.layout.Add(self.generate_random_content_button, 0, wx.ALL, 5)

        layout_label_and_control(
            self.layout, self.literary_author_label, self.literary_author_textctrl
        )
        layout_label_and_control(
            self.layout, self.book_name_label, self.book_name_textctrl
        )

        self.layout.Add(self.cleanup_checkbox, 0, wx.ALL, 5)

        self.layout.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.submit_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.layout)
        self.parent_frame = self.Parent.Parent

    def on_submit(self, event):
        # Collect data from the form

        validation_messages = []
        self.novel_content.title = self.story_title_textctrl.GetValue()
        title_min_length = 3
        validate(
            self.story_title_textctrl,
            title_min_length,
            f"The novel title is too short. It should be more than {title_min_length} characters.",
            validation_messages,
        )
        self.novel_content.subtitle = self.story_sub_title_textctrl.GetValue()
        subtitle_min_length = 10
        validate(
            self.story_sub_title_textctrl,
            subtitle_min_length,
            f"The novel subtitle is too short. It should be more than {subtitle_min_length} characters.",
            validation_messages,
        )
        self.novel_content.details = self.story_description_textctrl.GetValue()
        details_min_length = 20
        validate(
            self.story_description_textctrl,
            details_min_length,
            f"The novel description is too short. It should be more than {details_min_length} characters.",
            validation_messages,
        )
        self.novel_content.style_info.author = self.literary_author_textctrl.GetValue()
        self.novel_content.style_info.book = self.book_name_textctrl.GetValue()

        # You can process the data here
        if len(validation_messages) > 0:
            dlg = wx.MessageDialog(
                None,
                "\n".join(validation_messages),
                "Could not generate story",
                wx.OK | wx.ICON_WARNING,
            )
            dlg.ShowModal()
            dlg.Destroy()
            self.parent_frame.SetStatusText(validation_messages[0])
        else:
            self.submit_button.Disable()
            self.generate_random_content_button.Disable()
            self.parent_frame.SetStatusText(
                "Novel generation has started. This should take some minutes. Please wait ..."
            )
            threading.Thread(target=self.develop_story).start()

    def develop_story(self):
        tab_main = self

        class SimpleStoryCallback(StoryCallbackMixin):
            def on_chapters_generated(self, chapters: List[str]) -> Any:
                wx.CallAfter(tab_main.update_chapters_generated, (chapters))

            def on_chapter_finish(
                self, chapter_name: str, completed: int, total: int
            ) -> Any:
                wx.CallAfter(tab_main.update_progress, (chapter_name, completed, total))

            def on_chapter_cleanup(self, chapter_name: str) -> Any:
                wx.CallAfter(tab_main.update_chapter_cleanup, chapter_name)

            def on_html_finished(self, file_location) -> Any:
                if file_location is not None and file_location.exists():
                    webbrowser.open(file_location)

        simple_story_callback = SimpleStoryCallback()

        novel_result = develop_story(
            self.novel_content,
            simple_story_callback,
            cleanup_text=self.cleanup_checkbox.GetValue(),
        )
        wx.CallAfter(self.submit_button.Enable, True)
        wx.CallAfter(self.generate_random_content_button.Enable, True)
        wx.CallAfter(
            self.parent_frame.SetStatusText,
            f"Novel generation is finished. Please check the generated file: {novel_result.html_file}",
        )

    def update_chapters_generated(self, chapters: List[str]):
        self.parent_frame.SetStatusText(f"Generated {len(chapters)} chapter(s)")

    def update_progress(self, progress_data: Tuple[str, int, int]):
        (name, completed, total) = progress_data
        progress = completed / total * self.gauge.Range
        self.gauge.SetValue(int(progress))
        self.parent_frame.SetStatusText(f"Chapter: {name}")

    def update_chapter_cleanup(self, chapter_name: str):
        self.parent_frame.SetStatusText(f"Cleaning chapter: {chapter_name}")

    def generate_random_content(self, _event):
        novel_list = create_novel_content_list()
        novel_data = random.choice(novel_list)
        self.story_title_textctrl.SetValue(novel_data.title)
        self.story_sub_title_textctrl.SetValue(novel_data.subtitle)
        self.story_description_textctrl.SetValue(novel_data.details)


def validate(
    field: wx.TextCtrl,
    min_length: int,
    error_message: str,
    validation_messages: List[str],
):
    if len(field.GetValue()) < min_length:
        validation_messages.append(error_message)
        field.SetFocus()
