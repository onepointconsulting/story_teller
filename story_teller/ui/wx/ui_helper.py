from typing import Tuple


import wx


def decorate_required(input_textctrl: wx.TextCtrl):
    input_textctrl.SetToolTip("This field is required.")


def decorate_required_label(label: str):
    return f"{label} *:"


def layout_label_and_control(
    layout: wx.BoxSizer, label: wx.StaticText, control: wx.Control
):
    layout.Add(label, 0, wx.ALL, 5)
    layout.Add(control, 0, wx.EXPAND | wx.ALL, 5)


def create_text_field(
    parent: wx.Panel, title: str, hint: str
) -> Tuple[wx.StaticText, wx.TextCtrl]:
    parent.label = wx.StaticText(parent, label=decorate_required_label(title))
    parent.textctrl = wx.TextCtrl(parent)
    parent.textctrl.SetHint(hint)
    decorate_required(parent.label)
    return parent.label, parent.textctrl
