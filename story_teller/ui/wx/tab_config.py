import wx

from story_teller.config.config import cfg
from story_teller.ui.wx.ui_helper import decorate_required, decorate_required_label
from story_teller.ui.wx.ui_helper import layout_label_and_control
from story_teller.mymidjourney.config import midjourney_cfg


class TabConfig(wx.Panel):
    def __init__(self, parent):
        super(TabConfig, self).__init__(parent)
        self.layout = wx.BoxSizer(wx.VERTICAL)

        self.chatgpt_key_label = wx.StaticText(
            self, label=decorate_required_label("ChatGPT Key")
        )
        self.chatgpt_key_textctrl = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        set_openai_api_key(self.chatgpt_key_textctrl)
        decorate_required(self.chatgpt_key_textctrl)
        self.chatgpt_key_textctrl.Bind(wx.EVT_TEXT, self.on_key_changed)

        # List of choices for the dropdown
        choices = [cfg.openai_model, "gpt-4", "gpt-4-0613"]

        # Create a wx.ComboBox dropdown for the models
        self.combo_models_label = wx.StaticText(
            self, label=decorate_required_label("Model")
        )
        self.openai_models = wx.ComboBox(self, choices=choices)
        self.openai_models.SetValue(choices[0])
        self.openai_models.Bind(wx.EVT_COMBOBOX, self.on_model_changed)
        decorate_required(self.openai_models)

        # Create a temperature spin control
        self.temperature_label = wx.StaticText(
            self, label=decorate_required_label("Temperature")
        )
        self.spinCtrl = wx.SpinCtrlDouble(self, value="0", min=0, max=2, inc=0.1)
        self.spinCtrl.SetValue(cfg.openai_temperature)  # Set initial value
        self.spinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_temperature_changed)

        # Create a wx.ComboBox dropdown for the image quality of Dall-E
        image_quality_choices = ["standard", "hd"]
        self.image_quality_dall_e_text = wx.StaticText(
            self, label=decorate_required_label("Dall-E image quality")
        )
        self.image_quality_dall_e_combo = wx.ComboBox(
            self, choices=image_quality_choices
        )
        self.image_quality_dall_e_combo.SetValue(image_quality_choices[0])
        self.image_quality_dall_e_combo.Bind(
            wx.EVT_COMBOBOX, self.image_quality_dall_e_combo_changed
        )

        self.image_intermediate_prompt = wx.CheckBox(
            self,
            label="Use intermediate prompt to generate images (unticking speeds up generation)",
        )
        self.image_intermediate_prompt.SetValue(cfg.image_intermediate_prompt)
        self.image_intermediate_prompt.Bind(
            wx.EVT_CHECKBOX, self.image_intermediate_prompt_checked
        )

        self.use_midjourney_check = wx.CheckBox(
            self, label="Use Midjourney image generation"
        )
        # Bind the checkbox event to the handler
        self.use_midjourney_check.Bind(wx.EVT_CHECKBOX, self.on_activate_midjourney)
        # Create a text field and initially hide it
        self.mymidjourney_key_label = wx.StaticText(
            self, label=decorate_required_label("My Midjourney Key")
        )
        self.mymidjourney_key_text = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.mymidjourney_key_text.SetValue(midjourney_cfg.bearer_token)
        self.mymidjourney_key_text.Bind(wx.EVT_TEXT, self.on_midjourney_key_changed)

        self.hide_midjourney_fields()

        self.layout_components()

    def layout_components(self):
        # Layout
        layout_label_and_control(
            self.layout, self.chatgpt_key_label, self.chatgpt_key_textctrl
        )
        layout_label_and_control(
            self.layout, self.combo_models_label, self.openai_models
        )
        layout_label_and_control(self.layout, self.temperature_label, self.spinCtrl)
        layout_label_and_control(
            self.layout, self.image_quality_dall_e_text, self.image_quality_dall_e_combo
        )
        self.layout_checkbox(self.image_intermediate_prompt)
        self.layout_checkbox(self.use_midjourney_check)

        layout_label_and_control(
            self.layout, self.mymidjourney_key_label, self.mymidjourney_key_text
        )

        self.SetSizer(self.layout)

    def on_model_changed(self, _event):
        cfg.openai_model = self.openai_models.GetValue()
        cfg.init_llms()

    def image_quality_dall_e_combo_changed(self, _event):
        cfg.image_quality_dall_e = self.image_quality_dall_e_combo.GetValue()
        cfg.init_llms()

    def on_key_changed(self, _event):
        cfg.openai_api_key = self.chatgpt_key_textctrl.GetValue()

    def on_midjourney_key_changed(self, _event):
        midjourney_cfg.bearer_token = self.mymidjourney_key_text.GetValue()

    def on_temperature_changed(self, _event):
        cfg.openai_temperature = self.spinCtrl.GetValue()

    def image_intermediate_prompt_checked(self, event):
        cfg.image_intermediate_prompt = self.image_intermediate_prompt.GetValue()

    def set_my_open_api_key(self, key: str):
        self.chatgpt_key_textctrl.SetValue(key)

    def layout_checkbox(self, element: wx.CheckBox):
        self.layout.Add(element, 0, wx.ALL, 5)

    def on_activate_midjourney(self, _event):
        if self.use_midjourney_check.IsChecked():
            self.mymidjourney_key_label.Show()
            self.mymidjourney_key_text.Show()
            cfg.use_midjourney = True
        else:
            self.hide_midjourney_fields()
            cfg.use_midjourney = False
        self.Layout()

    def hide_midjourney_fields(self):
        self.mymidjourney_key_label.Hide()
        self.mymidjourney_key_text.Hide()


def set_openai_api_key(input_textctrl: wx.TextCtrl):
    if cfg.openai_api_key is not None:
        input_textctrl.SetValue(cfg.openai_api_key)
