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
        self.chatgpt_key_textctrl.Bind(wx.EVT_TEXT, self.onKeyChanged)

        # List of choices for the dropdown
        choices = [cfg.openai_model, "gpt-4", "gpt-4-0613", "gpt-3.5-turbo"]

        # Create a wx.ComboBox dropdown for the models
        self.combo_models_label = wx.StaticText(
            self, label=decorate_required_label("Model")
        )
        self.openai_models = wx.ComboBox(self, choices=choices)
        self.openai_models.SetValue(choices[0])
        self.openai_models.Bind(wx.EVT_COMBOBOX, self.onModelChanged)
        decorate_required(self.openai_models)

        # Create a temperature spin control
        self.temperature_label = wx.StaticText(
            self, label=decorate_required_label("Temperature")
        )
        self.spinCtrl = wx.SpinCtrlDouble(self, value="0", min=0, max=2, inc=0.1)
        self.spinCtrl.SetValue(cfg.openai_temperature)  # Set initial value
        self.spinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.onTemperatureChanged)

        # Layout
        layout_label_and_control(
            self.layout, self.chatgpt_key_label, self.chatgpt_key_textctrl
        )
        layout_label_and_control(
            self.layout, self.combo_models_label, self.openai_models
        )
        layout_label_and_control(self.layout, self.temperature_label, self.spinCtrl)

        self.SetSizer(self.layout)

    def onModelChanged(self, _event):
        cfg.openai_model = self.openai_models.GetValue()

    def onKeyChanged(self, _event):
        cfg.openai_api_key = self.chatgpt_key_textctrl.GetValue()

    def onTemperatureChanged(self, _event):
        cfg.openai_temperature = self.spinCtrl.GetValue()


def set_openai_api_key(input_textctrl: wx.TextCtrl):
    if cfg.openai_api_key is not None:
        input_textctrl.SetValue(cfg.openai_api_key)
