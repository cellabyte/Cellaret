#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.1 Markdown Browser & Editor
preferences.py
'''

'''
Copyright 2014 Roman Verin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import wx
import environment
from environment import Cellaret_24

config = wx.Config('cellabyte/cellaret.conf')

# Cellaret Preferences (child wx.Frame)
#==============================================================================
class CellaretPreferences(wx.Frame):

	def __init__(self, parent):
		wx.Frame.__init__(self, None, size = (440, 340), title = _('Cellaret Preferences'))
		self.parent = parent
		favicon = Cellaret_24.GetIcon()
		self.SetIcon(favicon)
		self.Centre()

		nb = wx.Notebook(self, wx.ID_ANY, style=wx.NB_TOP)

		self.main = wx.Panel(nb)
		self.browser = wx.Panel(nb)
		self.editor = wx.Panel(nb)

		nb.AddPage(self.main, _('Main'))
		nb.AddPage(self.browser, _('Browser'))
		nb.AddPage(self.editor, _('Editor'))

		self.main.SetFocus()

		# Main Panel
		#===========
		wx.StaticText(self.main, wx.ID_ANY, _('Select Working directory'), (20, 20))
		self.cb1SelectDirectory = wx.CheckBox(self.main, wx.ID_ANY, '', (20, 40))

		config.SetPath('Main')
		self.cb1SelectDirectory.SetValue(config.ReadInt('Select_directory'))
		environment.WORKING_DIRECTORY = config.Read('Working_directory')
		config.SetPath('')

		self.WorkingDirectory = wx.TextCtrl(self.main, wx.ID_ANY, str(environment.WORKING_DIRECTORY), (40, 40), (385, -1))

		closeButton = wx.Button(self.main, wx.ID_CLOSE, pos=(225, 240))
		self.okMainButton = wx.Button(self.main, wx.ID_OK, pos=(325, 240))
		self.okMainButton.SetDefault()

		# Browser Panel
		#==============
		self.cb1Browser = wx.CheckBox(self.browser, wx.ID_ANY, _('Print Filename'), (200, 15))
		self.cb2Browser = wx.CheckBox(self.browser, wx.ID_ANY, _('Navigate through the links'), (200, 45))

		config.SetPath('Browser')
		environment.BROWSER_FONT_SIZE = config.ReadInt('Font_size')
		self.cb1Browser.SetValue(config.ReadInt('Print_filename'))
		self.cb2Browser.SetValue(config.ReadInt('Navigate_through'))
		config.SetPath('')

		wx.StaticText(self.browser, wx.ID_ANY, _('Width:'), (20, 20))
		wx.StaticText(self.browser, wx.ID_ANY, _('Height:'), (20, 50))
		wx.StaticText(self.browser, wx.ID_ANY, _('Font size:'), (20, 80))
		self.sc1Browser = wx.SpinCtrl(self.browser, wx.ID_ANY, str(environment.BROWSER_WIDTH), (100, 15), (60, -1), min=200, max=2000)
		self.sc2Browser = wx.SpinCtrl(self.browser, wx.ID_ANY, str(environment.BROWSER_HEIGHT), (100, 45), (60, -1), min=200, max=2000)
		self.sc3Browser = wx.SpinCtrl(self.browser, wx.ID_ANY, str(environment.BROWSER_FONT_SIZE), (100, 75), (60, -1), min=8, max=24)

		closeButton = wx.Button(self.browser, wx.ID_CLOSE, pos=(225, 240))
		self.okBrowserButton = wx.Button(self.browser, wx.ID_OK, pos=(325, 240))
		self.okBrowserButton.SetDefault()

		# Editor Panel
		#=============
		self.cb1Editor = wx.CheckBox(self.editor, wx.ID_ANY, _('Style highlighting'), (200, 15))
#		self.cb2Editor = wx.CheckBox(self.editor, wx.ID_ANY, _('Check brace'), (200, 45))

		config.SetPath('Editor')
		self.cb1Editor.SetValue(config.ReadInt('Style_highlighting'))
#		self.cb2Editor.SetValue(config.ReadInt('Check_brace'))
		config.SetPath('')

		wx.StaticText(self.editor, wx.ID_ANY, _('Width:'), (20, 20))
		wx.StaticText(self.editor, wx.ID_ANY, _('Height:'), (20, 50))
		self.sc1Editor = wx.SpinCtrl(self.editor, wx.ID_ANY, str(environment.EDITOR_WIDTH), (100, 15), (60, -1), min=200, max=2000)
		self.sc2Editor = wx.SpinCtrl(self.editor, wx.ID_ANY, str(environment.EDITOR_HEIGHT), (100, 45), (60, -1), min=200, max=2000)

		closeButton = wx.Button(self.editor, wx.ID_CLOSE, pos=(225, 240))
		self.okEditorButton = wx.Button(self.editor, wx.ID_OK, pos=(325, 240))
		self.okEditorButton.SetDefault()

		# Buttons
		#========
		self.okMainButton.Bind(wx.EVT_BUTTON, self.OnSaveMain, id=wx.ID_OK)
		self.okBrowserButton.Bind(wx.EVT_BUTTON, self.OnSaveBrowser, id=wx.ID_OK)
		self.okEditorButton.Bind(wx.EVT_BUTTON, self.OnSaveEditor, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CLOSE)

		self.statusbar = self.CreateStatusBar()

	def OnSaveMain(self, event):
		config.SetPath('Main')
		config.WriteInt('Select_directory', self.cb1SelectDirectory.GetValue())
		config.Write('Working_directory', self.WorkingDirectory.GetValue())
		config.SetPath('')
		self.statusbar.SetStatusText(_('Main Configuration saved. Program restart required.'))

	def OnSaveBrowser(self, event):
		config.SetPath('Browser')
		config.WriteInt('Width', self.sc1Browser.GetValue())
		config.WriteInt('Height', self.sc2Browser.GetValue())
		config.WriteInt('Font_size', self.sc3Browser.GetValue())
		config.WriteInt('Print_filename', self.cb1Browser.GetValue())
		config.WriteInt('Navigate_through', self.cb2Browser.GetValue())
		config.SetPath('')
		self.statusbar.SetStatusText(_('Browser Configuration saved. Program restart required.'))

	def OnSaveEditor(self, event):
		config.SetPath('Editor')
		config.WriteInt('Width', self.sc1Editor.GetValue())
		config.WriteInt('Height', self.sc2Editor.GetValue())
		config.WriteInt('Style_highlighting', self.cb1Editor.GetValue())
#		config.WriteInt('Check_brace', self.cb2Editor.GetValue())
		config.SetPath('')
		self.statusbar.SetStatusText(_('Editor Configuration saved. Program restart required.'))

	def OnCancel(self, event):
		self.Destroy()
