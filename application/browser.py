# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.3 Markdown Browser & Editor
browser.py
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
import os
import webbrowser
import wx.html as html
from wx.html import HtmlEasyPrinting
from environment import PNG_CELLARET_24, BROWSER_FONT_SIZE, PRINT_FILENAME, WEBBROWSER_OPEN_LINK, EXEC_PATH, OS_LANGUAGE

# HTML Window subclass
#==============================================================================
class CellaHtmlWindow(html.HtmlWindow):

	def __init__(self, parent):
		html.HtmlWindow.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.SUNKEN_BORDER)
		if 'gtk2' in wx.PlatformInfo:
			self.SetStandardFonts(BROWSER_FONT_SIZE)
			self.SetBackgroundColour(wx.WHITE)

	def SelectsAllText(self):
		html.HtmlWindow.SelectAll(self)

	def SelectionToClipboard(self):
		textSelection = self.SelectionToText()
		if wx.TheClipboard.Open():
			wx.TheClipboard.Clear()
			wx.TheClipboard.SetData(wx.TextDataObject(textSelection))
			wx.TheClipboard.Close()

	def OnLinkClicked(self, linkinfo):
		if WEBBROWSER_OPEN_LINK:
			ahref = linkinfo.GetHref()
			if ahref.startswith('#'):
				self.base_OnLinkClicked(linkinfo) # Navigate through the link.
			else:
				webbrowser.open(ahref) # Open link in a web browser.
		else:
			textLink = linkinfo.GetHref()
			if wx.TheClipboard.Open():
				wx.TheClipboard.Clear()
				wx.TheClipboard.SetData(wx.TextDataObject(textLink))
				wx.TheClipboard.Close()

				messageDlg = wx.MessageDialog(self, '('+ textLink +') '+_('copied to the Clipboard'), _('Link copy to Clipboard'), wx.OK|wx.ICON_INFORMATION)
				messageDlg.ShowModal()
				messageDlg.Destroy()

# Printer subclass
#==============================================================================
class CellaPrinter(HtmlEasyPrinting):

	def __init__(self):
		HtmlEasyPrinting.__init__(self)

	def PreviewText(self, html, docName):
		if PRINT_FILENAME:
			self.SetHeader(docName)
		HtmlEasyPrinting.PreviewText(self, html)

	def Print(self, html, docName):
		if PRINT_FILENAME:
			self.SetHeader(docName)
		self.PrintText(html)

# Markdown Help
#==============================================================================
class MarkdownHelp(wx.Frame):

	def __init__(self, parent):
		wx.Frame.__init__(self, None, size = (800, 600), title = _('Cellaret Help'))
		favicon = PNG_CELLARET_24.GetIcon()
		self.SetIcon(favicon)
		self.Centre()

		if os.path.isdir(os.path.join(EXEC_PATH, 'help', OS_LANGUAGE)):
			helpPath = os.path.join(EXEC_PATH, 'help', OS_LANGUAGE)
		else:
			helpPath = os.path.join(EXEC_PATH, 'help', 'en_US')

		self.helpWindow = html.HtmlHelpWindow(self, wx.ID_ANY, wx.DefaultPosition, self.GetClientSize(), wx.TAB_TRAVERSAL | wx.BORDER_NONE, html.HF_DEFAULT_STYLE)
		self.helpController = html.HtmlHelpController(html.HF_EMBEDDED)
		self.helpController.SetHelpWindow(self.helpWindow)
		self.helpController.AddBook(os.path.join(helpPath, 'contents.hhp'))

	def ShowContents(self):
		self.helpController.DisplayContents()

	def ShowHelp(self, subHelp):
		self.helpController.Display(subHelp)
