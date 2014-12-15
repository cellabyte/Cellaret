# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.3 Markdown Browser & Editor
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
from environment import CONFIG, PNG_CELLARET_24, SELECT_DIRECTORY, WORKING_DIRECTORY, BROWSER_WIDTH, BROWSER_HEIGHT, BROWSER_FONT_SIZE, PRINT_FILENAME, WEBBROWSER_OPEN_LINK, EDITOR_WIDTH, EDITOR_HEIGHT, STYLE_HIGHLIGHTING, DATETIME_FORMAT

# Cellaret Preferences (child wx.Frame)
#==============================================================================
class CellaretPreferences(wx.Frame):

	def __init__(self, parent):
		wx.Frame.__init__(self, None, size = (440, 340), title = _('Cellaret Preferences'), style = wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
		self.parent = parent
		favicon = PNG_CELLARET_24.GetIcon()
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

		# Main Panel (Path 'General')
		#=============================
		wx.StaticText(self.main, wx.ID_ANY, _('Select Working directory'), (20, 20))
		self.cb1SelectDirectory = wx.CheckBox(self.main, wx.ID_ANY, '', (20, 40))
		self.cb1SelectDirectory.SetValue(SELECT_DIRECTORY)
		self.workingDirectory = wx.TextCtrl(self.main, wx.ID_ANY, str(WORKING_DIRECTORY), (40, 40), (385, -1))

		closeButton = wx.Button(self.main, wx.ID_CLOSE, pos=(225, 240))
		self.okMainButton = wx.Button(self.main, wx.ID_OK, pos=(325, 240))
		self.okMainButton.SetDefault()

		# Browser Panel (Path 'Browser')
		#================================
		self.cb1Browser = wx.CheckBox(self.browser, wx.ID_ANY, _('Print Filename'), (200, 15))
		self.cb2Browser = wx.CheckBox(self.browser, wx.ID_ANY, _('Open link in a web browser'), (200, 45))
		self.cb1Browser.SetValue(PRINT_FILENAME)
		self.cb2Browser.SetValue(WEBBROWSER_OPEN_LINK)

		wx.StaticText(self.browser, wx.ID_ANY, _('Width:'), (20, 20))
		wx.StaticText(self.browser, wx.ID_ANY, _('Height:'), (20, 50))
		wx.StaticText(self.browser, wx.ID_ANY, _('Font size:'), (20, 80))
		self.sc1Browser = wx.SpinCtrl(self.browser, wx.ID_ANY, str(BROWSER_WIDTH), (100, 15), (60, -1), min=200, max=2000)
		self.sc2Browser = wx.SpinCtrl(self.browser, wx.ID_ANY, str(BROWSER_HEIGHT), (100, 45), (60, -1), min=200, max=2000)
		self.sc3Browser = wx.SpinCtrl(self.browser, wx.ID_ANY, str(BROWSER_FONT_SIZE), (100, 75), (60, -1), min=8, max=24)

		closeButton = wx.Button(self.browser, wx.ID_CLOSE, pos=(225, 240))
		self.okBrowserButton = wx.Button(self.browser, wx.ID_OK, pos=(325, 240))
		self.okBrowserButton.SetDefault()

		# Editor Panel (Path 'Editor')
		#==============================
		self.cb1Editor = wx.CheckBox(self.editor, wx.ID_ANY, _('Style highlighting'), (200, 15))
		self.cb1Editor.SetValue(STYLE_HIGHLIGHTING)

		wx.StaticText(self.editor, wx.ID_ANY, _('Width:'), (20, 20))
		wx.StaticText(self.editor, wx.ID_ANY, _('Height:'), (20, 50))
		self.sc1Editor = wx.SpinCtrl(self.editor, wx.ID_ANY, str(EDITOR_WIDTH), (100, 15), (60, -1), min=200, max=2000)
		self.sc2Editor = wx.SpinCtrl(self.editor, wx.ID_ANY, str(EDITOR_HEIGHT), (100, 45), (60, -1), min=200, max=2000)

		wx.StaticText(self.editor, wx.ID_ANY, _('Format Date and Time:'), (20, 80))
		self.datetimeFormat = wx.TextCtrl(self.editor, wx.ID_ANY, str(DATETIME_FORMAT), (200, 75), (225, -1))

		closeButton = wx.Button(self.editor, wx.ID_CLOSE, pos=(225, 240))
		self.okEditorButton = wx.Button(self.editor, wx.ID_OK, pos=(325, 240))
		self.okEditorButton.SetDefault()

		# Buttons
		#=========
		self.okMainButton.Bind(wx.EVT_BUTTON, self.OnSaveMain, id=wx.ID_OK)
		self.okBrowserButton.Bind(wx.EVT_BUTTON, self.OnSaveBrowser, id=wx.ID_OK)
		self.okEditorButton.Bind(wx.EVT_BUTTON, self.OnSaveEditor, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CLOSE)

		self.statusbar = self.CreateStatusBar()

	def OnSaveMain(self, event):
		CONFIG.SetPath('General')
		CONFIG.WriteInt('select_directory', self.cb1SelectDirectory.GetValue())
		CONFIG.Write('working_directory', self.workingDirectory.GetValue())
		CONFIG.SetPath('')
		self.statusbar.SetStatusText(_('Main Configuration saved. Program restart required.'))

	def OnSaveBrowser(self, event):
		CONFIG.SetPath('Browser')
		CONFIG.WriteInt('width', self.sc1Browser.GetValue())
		CONFIG.WriteInt('height', self.sc2Browser.GetValue())
		CONFIG.WriteInt('font_size', self.sc3Browser.GetValue())
		CONFIG.WriteInt('print_filename', self.cb1Browser.GetValue())
		CONFIG.WriteInt('open_link', self.cb2Browser.GetValue())
		CONFIG.SetPath('')
		self.statusbar.SetStatusText(_('Browser Configuration saved. Program restart required.'))

	def OnSaveEditor(self, event):
		CONFIG.SetPath('Editor')
		CONFIG.WriteInt('width', self.sc1Editor.GetValue())
		CONFIG.WriteInt('height', self.sc2Editor.GetValue())
		CONFIG.WriteInt('style_highlighting', self.cb1Editor.GetValue())
		CONFIG.Write('datetime_format', self.datetimeFormat.GetValue())
		CONFIG.SetPath('')
		self.statusbar.SetStatusText(_('Editor Configuration saved. Program restart required.'))

	def OnCancel(self, event):
		self.Destroy()
