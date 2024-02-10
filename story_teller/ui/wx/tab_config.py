import wx

from story_teller.config.config import cfg
from story_teller.ui.wx.ui_helper import decorate_required, decorate_required_label
from story_teller.ui.wx.ui_helper import layout_label_and_control


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
        choices = [cfg.openai_model, "gpt-4", "gpt-4-0613", "gpt-3.5-turbo"]

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

        self.image_intermediate_prompt = wx.CheckBox(
            self, label="Use intermediate prompt to generate images"
        )
        self.image_intermediate_prompt.SetValue(cfg.image_intermediate_prompt)
        self.image_intermediate_prompt.Bind(
            wx.EVT_CHECKBOX, self.image_intermediate_prompt_checked
        )

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
        self.layout.Add(self.image_intermediate_prompt, 0, wx.ALL, 5)

        self.SetSizer(self.layout)

    def on_model_changed(self, _event):
        cfg.openai_model = self.openai_models.GetValue()

    def on_key_changed(self, _event):
        cfg.openai_api_key = self.chatgpt_key_textctrl.GetValue()

    def on_temperature_changed(self, _event):
        cfg.openai_temperature = self.spinCtrl.GetValue()

    def image_intermediate_prompt_checked(self, event):
        cfg.image_intermediate_prompt = self.image_intermediate_prompt.GetValue()

    def set_my_open_api_key(self, key: str):
        self.chatgpt_key_textctrl.SetValue(key)


def set_openai_api_key(input_textctrl: wx.TextCtrl):
    if cfg.openai_api_key is not None:
        input_textctrl.SetValue(cfg.openai_api_key)
