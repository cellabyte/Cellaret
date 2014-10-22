#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.1 Markdown Browser & Editor
main.py
'''

licence = '''
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

description = '''
Cellaret is a software program 
that browse and edit Markdown text.
'''

import wx
import wx.stc
import os
import sys
import codecs
import markdown
import wx.html as html
import gettext
from browser import cellaHtmlWindow, cellaPrinter
from editor import cellaStyledTextCtrl
from preferences import CellaretPreferences
from environment import *

gettext.install('cellaret', os.path.join(EXEC_PATH, 'translations'), unicode=True)

# Markdown Browser (parent wx.Frame)
#==============================================================================
class MarkdownBrowser(wx.Frame):

	def __init__(self, title):
		wx.Frame.__init__(self, None, size = (BROWSER_WIDTH, BROWSER_HEIGHT), title = title)
		favicon = Cellaret_24.GetIcon()
		self.SetIcon(favicon)
		self.Centre()
		self.Bind(wx.EVT_CLOSE, self.OnExit)

		# BROWSER STATE VARS
		#====================
		self.child = None

		# Browser cellaBrowser
		#======================
		self.cellaBrowser = cellaHtmlWindow(self) # HTML Window subclass
		self.Show(True)

		if MD_FILE_ARGV:
			self.filePath = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
			self.mdText = self.filePath.read() # read Markdown file
			self.filePath.close() # close the file
			self.mdHtml = markdown.markdown(self.mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(self.mdHtml) # deduce the content as html
			self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')
			global MD_PRINT_DATA
			MD_PRINT_DATA = self.mdHtml

		# Menu menuBar
		#==============
		self.fileMenu = wx.Menu()
		self.editMenu = wx.Menu()
		self.viewMenu = wx.Menu()
		helpMenu = wx.Menu()
		exportSubMenu = wx.Menu()
		self.contextMenu = wx.Menu()

		ID_HTML = wx.NewId()
		ID_FULLSCREEN = wx.NewId()
		self.ID_STATUSBAR = wx.NewId()

		self.fileMenu.Append(wx.ID_NEW, _('&New\tCtrl-N'), _('Creates a new document'))
		self.fileMenu.Append(wx.ID_OPEN, _('&Open\tCtrl-O'), _('Open an existing file'))
		self.fileMenu.AppendSeparator()
		self.fileMenu.AppendMenu(wx.ID_ANY, _('&Export to'), exportSubMenu)
		exportSubMenu.Append(ID_HTML, _('&HTML file'), '')
		self.fileMenu.AppendSeparator()
		self.fileMenu.Append(wx.ID_PREVIEW, _('Print Pre&view\tShift-Ctrl-P'), '')
		self.fileMenu.Append(wx.ID_PRINT, _('&Print\tCtrl-P'), '')
		self.fileMenu.AppendSeparator()
		self.fileMenu.Append(wx.ID_EXIT, _('&Quit Cellaret\tCtrl-Q'), _('Close window and exit program.'))

		self.editMenu.Append(wx.ID_EDIT, _('&Editor...\tCtrl-E'), _('Markdown text editor'))
		self.editMenu.AppendSeparator()
		self.editMenu.Append(wx.ID_COPY, _('&Copy\tCtrl-C'), '')
		self.editMenu.Append(wx.ID_SELECTALL, _('Select &All\tCtrl-A'), '')
		self.editMenu.AppendSeparator()
		self.editMenu.Append(wx.ID_PREFERENCES, _('Prefere&nces...'), '')

		self.viewMenu.Append(wx.ID_REFRESH, _('&Refresh\tF5'), '')
		self.viewMenu.AppendSeparator()
		self.viewMenu.Append(ID_FULLSCREEN, _('F&ull Screen\tF11'), _('Toggles Full Screen Mode'), wx.ITEM_CHECK)
		self.viewMenu.Append(self.ID_STATUSBAR, _('Status &Bar\tCtrl-B'), '', wx.ITEM_CHECK)

		helpMenu.Append(wx.ID_HELP, _('&Contents...\tF1'), _('Help about this program'))
		helpMenu.Append(wx.ID_ABOUT, _('&About'), _('Information about this program'))

		self.viewMenu.Check(self.ID_STATUSBAR, True)

		menuBar = wx.MenuBar()
		menuBar.Append(self.fileMenu, _('&File'))
		menuBar.Append(self.editMenu, _('&Edit'))
		menuBar.Append(self.viewMenu, _('&View'))
		menuBar.Append(helpMenu, _('&Help'))
		self.SetMenuBar(menuBar)

		# Context Menu
		#==============
		self.contextMenu.Append(wx.ID_REFRESH, _('Refresh'), '')
		self.contextMenu.Append(wx.ID_COPY, _('Copy selection'), '')
		self.contextMenu.AppendSeparator()
		self.contextMenu.Append(wx.ID_SELECTALL, _('Select All'), '')

		# Menu Event
		#============
		wx.EVT_MENU(self, wx.ID_NEW, self.OnNew)
		wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)
		wx.EVT_MENU(self, ID_HTML, self.OnSaveAsHtml)
		wx.EVT_MENU(self, wx.ID_PREVIEW, self.OnPreview)
		wx.EVT_MENU(self, wx.ID_PRINT, self.OnPrint)
		wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)
		wx.EVT_MENU(self, wx.ID_EDIT, self.OnEdit)
		wx.EVT_MENU(self, wx.ID_COPY, self.OnCopySelected)
		wx.EVT_MENU(self, wx.ID_SELECTALL, self.OnSelectAll)
		wx.EVT_MENU(self, wx.ID_PREFERENCES, self.OnPreferences)
		wx.EVT_MENU(self, wx.ID_REFRESH, self.OnRefresh)
		wx.EVT_MENU(self, ID_FULLSCREEN, self.OnFullScreen)
		wx.EVT_MENU(self, self.ID_STATUSBAR, self.OnStatusBar)
		wx.EVT_MENU(self, wx.ID_HELP, self.OnContents)
		wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)

		# Context Menu Event
		#====================
		wx.EVT_CONTEXT_MENU(self.cellaBrowser, self.OnShowPopup)

		# StatusBar for HtmlWindow
		#==========================
		self.statusbar = self.CreateStatusBar()
		self.cellaBrowser.SetRelatedFrame(self, '') # Sets the frame in which page title will be displayed.
		self.cellaBrowser.SetRelatedStatusBar(0) # After calling SetRelatedFrame, this sets statusbar slot where messages will be displayed.

	# Toggle Full Screen
	#====================
	def OnFullScreen(self, event):
		self.ShowFullScreen(not self.IsFullScreen(), wx.FULLSCREEN_NOCAPTION)

	# Show Status Bar
	#=================
	def OnStatusBar(self, event):
		if self.viewMenu.IsChecked(self.ID_STATUSBAR):
			self.statusbar.Show()
		else:
			self.statusbar.Hide()

	# Show Context Menu
	#===================
	def OnShowPopup(self, event):
		pos = event.GetPosition()
		pos = self.cellaBrowser.ScreenToClient(pos)
		self.cellaBrowser.PopupMenu(self.contextMenu, pos)

	def OnOpen(self, event):
		global MD_PATH_FILE
		global MD_DIR_NAME
		global MD_BASE_NAME
		if MD_PATH_FILE:
			dir = MD_DIR_NAME
		elif SELECT_DIRECTORY:
			dir = WORKING_DIRECTORY
		else:
			dir = ''

		wildcardStr = 'Markdown (*.md, *.mkd, *.markdown)|*.md;*.mkd;*.markdown'
		fileOpenDlg = wx.FileDialog(self, _('Choose a file to open'), defaultDir=dir, wildcard=wildcardStr, style=wx.OPEN)
		if fileOpenDlg.ShowModal() == wx.ID_OK:
			MD_PATH_FILE = fileOpenDlg.GetPath()
			MD_DIR_NAME = os.path.dirname(MD_PATH_FILE)
			MD_BASE_NAME = os.path.basename(MD_PATH_FILE)
			try:
				file = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
				mdText = file.read() # read Markdown file
				file.close() # close the file

				mdHtml = markdown.markdown(mdText) # convert Markdown to html
				self.cellaBrowser.SetPage(mdHtml) # deduce the content as html
				self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')

				global MD_PRINT_DATA
				MD_PRINT_DATA = mdHtml

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error opening file\n') + str(error))
				dlg.ShowModal()
			except UnicodeDecodeError, error:
				dlg = wx.MessageDialog(self, _('Error opening file\n') + str(error))
				dlg.ShowModal()
		fileOpenDlg.Destroy()

	def OnRefresh(self, event):
		if MD_PATH_FILE:
			filePath = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
			mdText = filePath.read() # read Markdown file
			filePath.close() # close the file

			mdHtml = markdown.markdown(mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(mdHtml) # deduce the content as html
			self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')

			global MD_PRINT_DATA
			MD_PRINT_DATA = mdHtml

	def SetTitlePlus(self, event):
		self.SetTitle('+ ' + MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')

	def OnSaveAsHtml(self, event):
		if MD_PATH_FILE:
			dir = os.path.dirname(MD_PATH_FILE)
			shortName, extName = os.path.splitext(MD_BASE_NAME)
			htmlFile = shortName + '.html'
		elif SELECT_DIRECTORY:
			dir = WORKING_DIRECTORY
			htmlFile = _('new.html')
		else:
			dir = os.getcwd()
			htmlFile = _('new.html')

		wildcardStr = 'HTML (*.html)|*.html'
		save_dlg = wx.FileDialog(self, message=_('Save file As...'), defaultDir=dir, defaultFile=htmlFile, wildcard=wildcardStr, style=wx.SAVE | wx.OVERWRITE_PROMPT)
		if save_dlg.ShowModal() == wx.ID_OK:
			startHtml = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html>\n<head>\n\t<meta http-equiv="content-type" content="text/html; charset=utf-8">\n\t<meta name="generator" content="Cellaret (linux)">\n</head>\n<body>\n'
			endHtml = '\n</body>\n</html>\n'
			htmlFile = startHtml + MD_PRINT_DATA + endHtml
			htmlPathFile = save_dlg.GetPath()
			try:
				file = codecs.open(htmlPathFile, 'w', encoding='utf-8')
				file.write(htmlFile)
				file.close()

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error saving file\n') + str(error))
				dlg.ShowModal()
		save_dlg.Destroy()

	def OnSelectAll(self, event):
		self.cellaBrowser.SelectsAllText()

	def OnCopySelected(self, event):
		self.cellaBrowser.SelectionToClipboard()

	# Printer dialog
	#================
	def OnPreview(self, event):
		printer = cellaPrinter() # Printer subclass
		printer.PreviewText(MD_PRINT_DATA, MD_PATH_FILE)
		return True

	def OnPrint(self, event):
		printer = cellaPrinter() # Printer subclass
		printer.Print(MD_PRINT_DATA, MD_PATH_FILE)
		return True

	# Open Editor frame
	#===================
	def OnEdit(self, event):
		if MD_PATH_FILE:
			self.DisableMenuBrowser(self)
			global markdownNew
			markdownNew = False
			self.child = MarkdownEditor(self)
			self.child.Show()
		else:
			self.OnNew(event)

	def OnNew(self, event):
		self.DisableMenuBrowser(self)
		global markdownNew
		markdownNew = True
		self.child = MarkdownEditor(self)
		self.child.Show()

	# Disable menu items
	#====================
	def DisableMenuBrowser(self, event):
		self.fileMenu.Enable(wx.ID_NEW, False) # Disable menu item New
		self.fileMenu.Enable(wx.ID_OPEN, False) # Disable menu item Open
		self.editMenu.Enable(wx.ID_EDIT, False) # Disable menu item Editor

	# Enable menu items
	#===================
	def EnableMenuBrowser(self, event):
		self.fileMenu.Enable(wx.ID_NEW, True) # Enable menu item New
		self.fileMenu.Enable(wx.ID_OPEN, True) # Enable menu item Open
		self.editMenu.Enable(wx.ID_EDIT, True) # Enable menu item Editor

	# Open Properties frame
	#=======================
	def OnPreferences(self, event):
		self.preferences = CellaretPreferences(self)
		self.preferences.Show()

	# Open Help frame
	#=================
	def OnContents(self, event):
		self.contents = MarkdownHelp(self)
		self.contents.ShowContents()
		self.contents.Show()

	# About dialog
	#==============
	def OnAbout(self, event):
		info = wx.AboutDialogInfo()
		getCellaret_32Icon = Cellaret_32.GetIcon()

		info.SetIcon(getCellaret_32Icon)
		info.SetName('Cellaret')
		info.SetVersion('0.1.1')
		info.SetDescription(description)
		info.SetCopyright('Copyright 2014 Roman Verin')
		info.SetWebSite('http://cellabyte.com')
		info.SetLicence(licence)
		info.AddDeveloper('Roman A. Verin <roman@cellabyte.com>')
		#info.AddDocWriter('')
		info.AddArtist('Roman A. Verin <roman@cellabyte.com>')
		info.AddTranslator('')

		wx.AboutBox(info)

	def OnExit(self, event):
		if self.child:
			self.child.OnQuitApplication(self) # if open editor, OnQuitApplication (child wx.Frame)
		else:
			wx.Exit()

# Markdown Help
#==============================================================================
class MarkdownHelp(wx.Frame):

	title = _('Cellaret Help')

	def __init__(self, parent):
		wx.Frame.__init__(self, None, size = (800, 600), title=self.title)
		favicon = Cellaret_24.GetIcon()
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

# Markdown Editor (child wx.Frame)
#==============================================================================
class MarkdownEditor(wx.Frame):

	title = _('New File - Cellaret File Editor')

	def __init__(self, parent):
		wx.Frame.__init__(self, None, size = (EDITOR_WIDTH, EDITOR_HEIGHT), title = self.title)
		self.parent = parent
		favicon = Cellaret_24.GetIcon()
		self.SetIcon(favicon)
		self.Centre()
		self.Bind(wx.EVT_CLOSE, self.OnCloseEditor)

		self.iconToolbar = self.CreateIconToolbar()

		# EDITOR STATE VARS
		#==================
		self.markdownTextIsModified = False # file is changed (Modified)
		self.edLastFilenameSaved = False # No path to the file (new file)
		self.fileOpenDir = os.getcwd()
		self.edOverwriteMode = False # For the future implementation of the overwrite.

		# Editor cellaEditor (Scintilla)
		#===============================
		self.cellaEditor = cellaStyledTextCtrl(self) # Text editor subclass
		self.cellaEditor.SetBackgroundColour(wx.WHITE)
		self.cellaEditor.WrapMode = True # Scintilla Wrap mode
#		self.cellaEditor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d" % EDITOR_FONT_SIZE) # Style for the default text

		if not markdownNew:
			filePath = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
			self.cellaEditor.AppendText(filePath.read()) # read and deduce Markdown text
			self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - ' + _('Cellaret File Editor'))
			filePath.close() # close the file
			self.cellaEditor.EmptyUndoBuffer() # clear the Undo buffer
			self.edLastFilenameSaved = MD_PATH_FILE # path to the file (for saving)
			self.imagePathFile = MD_PATH_FILE # path to the image file (for the beginning)
		else:
			self.imagePathFile = None

		self.markdownTextIsModified = False # Set False, because the text was changed.
		self.statusbar = self.CreateStatusBar()

		self.cellaEditor.Bind(wx.stc.EVT_STC_MODIFIED, self.IfTextChanged)
		self.cellaEditor.Bind(wx.EVT_KEY_DOWN, self.IfKeyDown)
#		self.Bind(wx.EVT_UPDATE_UI, self.IfKeyDown, self.cellaEditor)

		# Positioning iconToolbar & Scintilla
		#=====================================
		edPanelSizer = wx.BoxSizer(wx.VERTICAL)
		edPanelSizer.Add(self.iconToolbar, proportion=0, flag=wx.EXPAND)
		edPanelSizer.Add(self.cellaEditor, proportion=1, flag=wx.EXPAND)
		self.SetSizer(edPanelSizer) # Assigns Sizer for container management.

	# Toolbar iconToolbar
	#====================
	def CreateIconToolbar(self):

		self.toolbar = wx.ToolBar(self, wx.ID_ANY)

		ID_NAMEDHYPERLINK = wx.NewId()
		ID_HYPERLINK = wx.NewId()
		ID_INSERTIMAGE = wx.NewId()

		self.toolbar.AddSimpleTool(wx.ID_OPEN, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN), _('Append to File'), '')
		self.toolbar.AddSimpleTool(wx.ID_SAVE, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE), _('Save'), '')
		self.toolbar.AddSimpleTool(wx.ID_SAVEAS, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS), _('Save as...'), '')
		self.toolbar.AddSeparator()
		self.toolbar.AddSimpleTool(wx.ID_COPY, wx.ArtProvider.GetBitmap(wx.ART_COPY), _('Copy'), '')
		self.toolbar.AddSimpleTool(wx.ID_CUT, wx.ArtProvider.GetBitmap(wx.ART_CUT), _('Cut'), '')
		self.toolbar.AddSimpleTool(wx.ID_PASTE, wx.ArtProvider.GetBitmap(wx.ART_PASTE), _('Paste'), '')
		self.toolbar.AddSeparator()
		self.toolbar.AddSimpleTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO), _('Undo'), '')
		self.toolbar.AddSimpleTool(wx.ID_REDO, wx.ArtProvider.GetBitmap(wx.ART_REDO), _('Redo'), '')
		self.toolbar.AddSeparator()
		self.toolbar.AddSimpleTool(wx.ID_BOLD, wx.Image('/usr/share/icons/gnome/16x16/actions/format-text-bold.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Bold'), '')
		self.toolbar.AddSimpleTool(wx.ID_ITALIC, wx.Image('/usr/share/icons/gnome/16x16/actions/format-text-italic.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Italic'), '')
		self.toolbar.AddSeparator()
		self.toolbar.AddSimpleTool(ID_NAMEDHYPERLINK, wx.Image('/usr/share/icons/gnome/16x16/actions/insert-link.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Named Hyperlink'), '')
		self.toolbar.AddSimpleTool(ID_HYPERLINK, wx.Image('/usr/share/icons/gnome/16x16/actions/insert-link.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Hyperlink'), '')
		self.toolbar.AddSimpleTool(ID_INSERTIMAGE, wx.Image('/usr/share/icons/gnome/16x16/actions/insert-image.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Insert Image'), '')
		self.toolbar.AddSeparator()
		self.toolbar.AddSimpleTool(wx.ID_CLOSE, wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK), _('Close Editor'), '')
		self.toolbar.AddSimpleTool(wx.ID_EXIT, wx.ArtProvider.GetBitmap(wx.ART_QUIT), _('Quit Cellaret'), '')

		self.toolbar.EnableTool(wx.ID_SAVE, False)
		self.toolbar.EnableTool(wx.ID_UNDO, False)
		self.toolbar.EnableTool(wx.ID_REDO, False)

		# Toolbar Event
		#===============
		wx.EVT_TOOL(self, wx.ID_OPEN, self.OnAppendToFile)
		wx.EVT_TOOL(self, wx.ID_SAVE, self.OnSaveFile)
		wx.EVT_TOOL(self, wx.ID_SAVEAS, self.OnSaveAsFile)
		wx.EVT_TOOL(self, wx.ID_COPY, self.OnCopy)
		wx.EVT_TOOL(self, wx.ID_CUT, self.OnCut)
		wx.EVT_TOOL(self, wx.ID_PASTE, self.OnPaste)
		wx.EVT_TOOL(self, wx.ID_UNDO, self.OnUndo)
		wx.EVT_TOOL(self, wx.ID_REDO, self.OnRedo)
		wx.EVT_TOOL(self, wx.ID_BOLD, self.OnBold)
		wx.EVT_TOOL(self, wx.ID_ITALIC, self.OnItalic)
		wx.EVT_TOOL(self, ID_NAMEDHYPERLINK, self.OnNamedHyperlink)
		wx.EVT_TOOL(self, ID_HYPERLINK, self.OnHyperlink)
		wx.EVT_TOOL(self, ID_INSERTIMAGE, self.OnInsertImage)
		wx.EVT_TOOL(self, wx.ID_CLOSE, self.OnCloseEditor)
		wx.EVT_TOOL(self, wx.ID_EXIT, self.OnQuitApplication)

		self.toolbar.Realize()
		return self.toolbar

	def IfTextChanged(self, event):
		if not markdownNew:
			self.SetTitle('*' + MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - ' + _('Cellaret File Editor'))
		self.markdownTextIsModified = True
		self.toolbar.EnableTool(wx.ID_SAVE, True) # Save highlight
		self.toolbar.EnableTool(wx.ID_UNDO, True) # Undo highlight
		event.Skip()

	def IfKeyDown(self, event):
		keycode = event.GetKeyCode()
#		print keycode
		if keycode == 340:
			self.contents = MarkdownHelp(self)
			self.contents.ShowHelp('Markdown')
			self.contents.Show()
		event.Skip()

	def OnAppendToFile(self, event):
		wildcardStr = 'Markdown (*.md)|*.md|All files (*)|*'
		fileOpenDlg = wx.FileDialog(self, _('Choose a file to open'), wildcard=wildcardStr, style=wx.OPEN)
		if fileOpenDlg.ShowModal() == wx.ID_OK:
			PathFile = fileOpenDlg.GetPath()
			try:
				file = codecs.open(PathFile, 'r', encoding='utf-8') # open the file and encoding
				mdText = file.read()
				file.close()

				self.cellaEditor.AddText(mdText) # Add text at cursor position
				self.markdownTextIsModified = True

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error opening file\n') + str(error))
				dlg.ShowModal()
			except UnicodeDecodeError, error:
				dlg = wx.MessageDialog(self, _('Error opening file\n') + str(error))
				dlg.ShowModal()
		fileOpenDlg.Destroy()

	def OnSaveFile(self, event):
		if self.edLastFilenameSaved:
			try:
				file = codecs.open(MD_PATH_FILE, 'w', encoding='utf-8') # open to the write and encoding
				mdText = self.cellaEditor.GetText()
				file.write(mdText)
				file.close()

				self.edLastFilenameSaved = MD_BASE_NAME
				self.statusbar.SetStatusText(self.edLastFilenameSaved + _(' Saved'), 0)
				self.statusbar.SetStatusText('', 1)
				self.markdownTextIsModified = False
				self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - ' + _('Cellaret File Editor'))

				self.parent.OnRefresh(self) # Refresh browser (parent wx.Frame)
				self.parent.SetTitlePlus(self) # Setting "+" on Title browser (parent wx.Frame)
				self.toolbar.EnableTool(wx.ID_SAVE, False)

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error saving file\n') + str(error))
				dlg.ShowModal()
		else:
			self.OnSaveAsFile(event)

	def OnSaveAsFile(self, event):
		global MD_PATH_FILE
		global MD_DIR_NAME
		global MD_BASE_NAME
		if MD_PATH_FILE:
			dir = MD_DIR_NAME
			saveAs = MD_BASE_NAME
		elif SELECT_DIRECTORY:
			dir = WORKING_DIRECTORY
			saveAs = _('new.md')
		else:
			dir = os.getcwd()
			saveAs = _('new.md')

		wildcardStr = 'Markdown (*.md)|*.md'
		save_dlg = wx.FileDialog(self, message=_('Save file As...'), defaultDir=dir, defaultFile=saveAs, wildcard=wildcardStr, style=wx.SAVE | wx.OVERWRITE_PROMPT)
		if save_dlg.ShowModal() == wx.ID_OK:
			MD_PATH_FILE = save_dlg.GetPath()
			MD_DIR_NAME = os.path.dirname(MD_PATH_FILE)
			MD_BASE_NAME = os.path.basename(MD_PATH_FILE)
			try:
				file = codecs.open(MD_PATH_FILE, 'w', encoding='utf-8') # open to the write and encoding
				mdText = self.cellaEditor.GetText()
				file.write(mdText)
				file.close()

				global markdownNew
				markdownNew = False

				self.edLastFilenameSaved = MD_BASE_NAME
				self.statusbar.SetStatusText(self.edLastFilenameSaved + _(' Saved'), 0)
				self.statusbar.SetStatusText('', 1)
				self.markdownTextIsModified = False
				self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - ' + _('Cellaret File Editor'))

				self.parent.OnRefresh(self) # Refresh browser (parent wx.Frame)
				self.toolbar.EnableTool(wx.ID_SAVE, False)

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error saving file\n') + str(error))
				dlg.ShowModal()
		save_dlg.Destroy()

	def OnCut(self, event):
		self.cellaEditor.Cut()
		self.markdownTextIsModified = True

	def OnCopy(self, event):
		self.cellaEditor.Copy()

	def OnPaste(self, event):
		self.cellaEditor.Paste()
		self.markdownTextIsModified = True

	def OnUndo(self, event):
		if self.cellaEditor.CanUndo():
			self.cellaEditor.Undo()
			self.toolbar.EnableTool(wx.ID_REDO, True)
		else:
			self.toolbar.EnableTool(wx.ID_UNDO, False)

	def OnRedo(self, event):
		if self.cellaEditor.CanRedo():
			self.cellaEditor.Redo()
			self.toolbar.EnableTool(wx.ID_UNDO, True)
		else:
			self.toolbar.EnableTool(wx.ID_REDO, False)

	def OnBold(self, event):
		self.InsertTags('**', '**')
		self.markdownTextIsModified = True

	def OnItalic(self, event):
		self.InsertTags('_', '_')
		self.markdownTextIsModified = True

	def OnHyperlink(self, event):
		self.InsertTags('<', '>')
		self.markdownTextIsModified = True

	def OnNamedHyperlink(self, event):
		dlg = wx.TextEntryDialog(self, _('Enter Hyperlink'), _('URL Entry'))
#		dlg.SetValue('URL')
		if dlg.ShowModal() == wx.ID_OK:
			self.InsertTags('[', '](%s "")' % dlg.GetValue())
			self.markdownTextIsModified = True
		dlg.Destroy()

	def OnInsertImage(self, event):
		if self.imagePathFile:
			dir = os.path.dirname(self.imagePathFile)
		elif SELECT_DIRECTORY:
			dir = WORKING_DIRECTORY
		else:
			dir = ''

		wildcardStr = 'Images (*.jpg, *.gif, *.png)|*.jpg;*.gif;*.png|All files (*)|*'
		insertImageDlg = wx.FileDialog(self, message = _('Choose image file'), defaultDir = dir, wildcard = wildcardStr, style=wx.OPEN)
		if insertImageDlg.ShowModal() == wx.ID_OK:
			self.imagePathFile = insertImageDlg.GetPath()

			imageFile = os.path.basename(self.imagePathFile)
			self.cellaEditor.AddText('!['+ imageFile +'](%s)' % self.imagePathFile)
			self.markdownTextIsModified = True

		insertImageDlg.Destroy()

	def InsertTags(self, starttag, stoptag):
		start, to = self.cellaEditor.GetSelection()
		to += len(starttag)
		self.cellaEditor.GotoPos(start)
		self.cellaEditor.AddText(starttag)
		self.cellaEditor.GotoPos(to)
		self.cellaEditor.AddText(stoptag)
		self.cellaEditor.GotoPos(to+len(stoptag))

	#def OnDelete(self, event):
		#start, to = self.cellaEditor.GetSelection()
		#self.cellaEditor.Remove(start, to)
		#self.markdownTextIsModified = True

	def OnCloseEditor(self, event):
		''' If there were changes, request save the file. '''
		if self.markdownTextIsModified:
			dlg = wx.MessageDialog(self, _('File is modified. Save before exit?'), '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.OnSaveFile(event)
				if not self.markdownTextIsModified:
					self.Destroy() # Destroy MarkdownEditor(wx.Frame)
					self.parent.EnableMenuBrowser(self) # Enable menu items (parent wx.Frame)
			elif val == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.Destroy() # Destroy MarkdownEditor(wx.Frame)
				self.parent.EnableMenuBrowser(self) # Enable menu items (parent wx.Frame)
		else:
			self.Destroy() # Destroy MarkdownEditor(wx.Frame)
			self.parent.EnableMenuBrowser(self) # Enable menu items (parent wx.Frame)

	def OnQuitApplication(self, event):
		''' If there were changes, request save the file. '''
		if self.markdownTextIsModified:
			dlg = wx.MessageDialog(self, _('File is modified. Save before exit?'), '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.OnSaveFile(event)
				if not self.markdownTextIsModified:
					wx.Exit() # Exit wx.App.MainLoop()
			elif val == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				wx.Exit() # Exit wx.App.MainLoop()
		else:
			wx.Exit() # Exit wx.App.MainLoop()
