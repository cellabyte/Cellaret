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
		#===================
		self.child = None

		# Browser cellaBrowser
		#=====================
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
		#=============
		menuBar = wx.MenuBar()

		menu = wx.Menu()
		self.newItem = menu.Append(wx.ID_NEW, _('&New\tCtrl-N'), _('Creates a new document'))
		self.Bind(wx.EVT_MENU, self.OnNew, self.newItem)
		self.openItem = menu.Append(wx.ID_OPEN, _('&Open\tCtrl-O'), _('Open an existing file'))
		self.Bind(wx.EVT_MENU, self.OnOpen, self.openItem)
		menu.AppendSeparator()
		export = wx.Menu()
		menu.AppendMenu(wx.ID_ANY, _('Export to'), export)
		htmlItem = export.Append(wx.ID_ANY, _('HTML file'), '')
		self.Bind(wx.EVT_MENU, self.OnSaveAsHtml, htmlItem)
		menu.AppendSeparator()
		previewItem = menu.Append(wx.ID_PREVIEW, _('Print &Preview\tShift-Ctrl-P'), '')
		self.Bind(wx.EVT_MENU, self.OnPreview, previewItem)
		printItem = menu.Append(wx.ID_PRINT, _('&Print\tCtrl-P'), '')
		self.Bind(wx.EVT_MENU, self.OnPrint, printItem)
		menu.AppendSeparator()
		exitItem = menu.Append(wx.ID_EXIT, _('&Quit Cellaret\tCtrl-Q'), _('Close window and exit program.'))
		self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
		menuBar.Append(menu, _('&File'))

		menu = wx.Menu()
		self.editItem = menu.Append(wx.ID_EDIT, _('&Editor...\tCtrl-E'), _('Markdown text editor'))
		self.Bind(wx.EVT_MENU, self.OnEdit, self.editItem)
		#selectAllItem = menu.Append(wx.ID_SELECTALL, _('Select &All\tCtrl-A'), '')
		#self.Bind(wx.EVT_MENU, self.OnSelectAll, selectAllItem)
		#copySelectedItem = menu.Append(wx.ID_COPY, _('&Copy selected\tCtrl-C'), '')
		#self.Bind(wx.EVT_MENU, self.OnCopySelected, copySelectedItem)
		menu.AppendSeparator()
		preferencesItem = menu.Append(wx.ID_PREFERENCES, _('Preferences...'), '')
		self.Bind(wx.EVT_MENU, self.OnPreferences, preferencesItem)
		menuBar.Append(menu, _('E&dit'))

		menu = wx.Menu()
		refreshItem = menu.Append(wx.ID_REFRESH, _('Refresh\tF5'), '')
		self.Bind(wx.EVT_MENU, self.OnRefresh, refreshItem)
		menu.AppendSeparator()
		fullscreenItem = menu.Append(wx.ID_ANY, _('Full Screen\tF11'), _('Toggles Full Screen Mode'), wx.ITEM_CHECK)
		self.Bind(wx.EVT_MENU, self.OnFullScreen, fullscreenItem)
		self.statusbarItem = menu.Append(wx.ID_ANY, _('Show Status &Bar\tCtrl-B'), '', wx.ITEM_CHECK)
		menu.Check(self.statusbarItem.GetId(), True)
		self.Bind(wx.EVT_MENU, self.OnStatusBar, self.statusbarItem)
		menuBar.Append(menu, _('&View'))

		menu = wx.Menu()
		contentsItem = menu.Append(wx.ID_HELP, _('Contents...\tF1'), _('Help about this program'))
		self.Bind(wx.EVT_MENU, self.OnContents, contentsItem)
		aboutItem = menu.Append(wx.ID_ABOUT, _('About'), _('Information about this program'))
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
		menuBar.Append(menu, _('&Help'))

		self.SetMenuBar(menuBar)

		# Context Menu
		self.popupmenu = wx.Menu()
		refreshContextItem = self.popupmenu.Append(wx.ID_REFRESH, _('Refresh'), '')
		self.Bind(wx.EVT_MENU, self.OnRefresh, refreshContextItem)

		#selectAllContextItem = self.popupmenu.Append(wx.ID_SELECTALL, _('Select &All\tCtrl-A'), '')
		#self.Bind(wx.EVT_MENU, self.OnSelectAll, selectAllContextItem)

		copySelectedContextItem = self.popupmenu.Append(wx.ID_COPY, _('&Copy selected\tCtrl-C'), '')
#		self.Bind(wx.EVT_MENU, self.OnCopySelected, copySelectedContextItem)

		# Context Menu Event
		self.cellaBrowser.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

		# StatusBar for HtmlWindow
		self.statusbar = self.CreateStatusBar()
		self.cellaBrowser.SetRelatedFrame(self, '') # Sets the frame in which page title will be displayed.
		self.cellaBrowser.SetRelatedStatusBar(0) # After calling SetRelatedFrame, this sets statusbar slot where messages will be displayed.

	# Toggle Full Screen
	def OnFullScreen(self, event):
		self.ShowFullScreen(not self.IsFullScreen(), wx.FULLSCREEN_NOCAPTION)

	# Show Status Bar
	def OnStatusBar(self, event):
		if self.statusbarItem.IsChecked():
			self.statusbar.Show()
		else:
			self.statusbar.Hide()

	# Show Context Menu
	def OnShowPopup(self, event):
		pos = event.GetPosition()
		pos = self.cellaBrowser.ScreenToClient(pos)
		self.cellaBrowser.PopupMenu(self.popupmenu, pos)

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

	#def OnSelectAll(self, event):
		#

	#def OnCopySelected(self, event):
		#

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
		self.newItem.Enable(False) # Disable menu item New
		self.openItem.Enable(False) # Disable menu item Open
		self.editItem.Enable(False) # Disable menu item Editor

	# Enable menu items
	#===================
	def EnableMenuBrowser(self, event):
		self.newItem.Enable(True) # Enable menu item New
		self.openItem.Enable(True) # Enable menu item Open
		self.editItem.Enable(True) # Enable menu item Editor

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

		# Append to file
		self.toolbar.AddSimpleTool(wx.ID_OPEN, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN), _('Append to File'), '')
		self.Bind(wx.EVT_TOOL, self.OnAppendToFile, id=wx.ID_OPEN)

		# SAVE TO FILE editor's current text
		self.toolbar.AddSimpleTool(wx.ID_SAVE, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE), _('Save'), '')
		self.toolbar.EnableTool(wx.ID_SAVE, False)
		self.Bind(wx.EVT_TOOL, self.OnSaveFile, id=wx.ID_SAVE)

		# SAVE TO FILE AS... editor's current text
		self.toolbar.AddSimpleTool(wx.ID_SAVEAS, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS), _('Save as...'), '')
		self.Bind(wx.EVT_TOOL, self.OnSaveAsFile, id=wx.ID_SAVEAS)

		self.toolbar.AddSeparator()

		# COPY
		self.toolbar.AddSimpleTool(wx.ID_COPY, wx.ArtProvider.GetBitmap(wx.ART_COPY), _('Copy'), '')
		self.Bind(wx.EVT_TOOL, self.OnCopy, id=wx.ID_COPY)

		# CUT
		self.toolbar.AddSimpleTool(wx.ID_CUT, wx.ArtProvider.GetBitmap(wx.ART_CUT), _('Cut'), '')
		self.Bind(wx.EVT_TOOL, self.OnCut, id=wx.ID_CUT)

		# PASTE any text previously copied text
		self.toolbar.AddSimpleTool(wx.ID_PASTE, wx.ArtProvider.GetBitmap(wx.ART_PASTE), _('Paste'), '')
		self.Bind(wx.EVT_TOOL, self.OnPaste, id=wx.ID_PASTE)

		self.toolbar.AddSeparator()

		# UNDO
		self.toolbar.AddSimpleTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO), _('Undo'), '')
		self.toolbar.EnableTool(wx.ID_UNDO, False)
		self.Bind(wx.EVT_TOOL, self.OnUndo, id=wx.ID_UNDO)

		# REDO
		self.toolbar.AddSimpleTool(wx.ID_REDO, wx.ArtProvider.GetBitmap(wx.ART_REDO), _('Redo'), '')
		self.toolbar.EnableTool(wx.ID_REDO, False)
		self.Bind(wx.EVT_TOOL, self.OnRedo, id=wx.ID_REDO)

		self.toolbar.AddSeparator()

		# BOLD
		self.toolbar.AddSimpleTool(wx.ID_BOLD, wx.Image('/usr/share/icons/gnome/16x16/actions/format-text-bold.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Bold'), '')
		self.Bind(wx.EVT_TOOL, self.OnBold, id=wx.ID_BOLD)

		# ITALIC
		self.toolbar.AddSimpleTool(wx.ID_ITALIC, wx.Image('/usr/share/icons/gnome/16x16/actions/format-text-italic.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Italic'), '')
		self.Bind(wx.EVT_TOOL, self.OnItalic, id=wx.ID_ITALIC)

		self.toolbar.AddSeparator()

		# Hyperlink
		hyperlinkID = wx.NewId()
		self.toolbar.AddSimpleTool(hyperlinkID, wx.Image('/usr/share/icons/gnome/16x16/actions/insert-link.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Hyperlink'), '')
		self.Bind(wx.EVT_TOOL, self.OnHyperlink, id=hyperlinkID)

		# Named Hyperlink
		namedHyperlinkID = wx.NewId()
		self.toolbar.AddSimpleTool(namedHyperlinkID, wx.Image('/usr/share/icons/gnome/16x16/actions/insert-link.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Named Hyperlink'), '')
		self.Bind(wx.EVT_TOOL, self.OnNamedHyperlink, id=namedHyperlinkID)

		# Insert Image
		insertImageID = wx.NewId()
		self.toolbar.AddSimpleTool(insertImageID, wx.Image('/usr/share/icons/gnome/16x16/actions/insert-image.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), _('Insert Image'), '')
		self.Bind(wx.EVT_TOOL, self.OnInsertImage, id=insertImageID)

		self.toolbar.AddSeparator()

		# CLOSE this frame.
		self.toolbar.AddSimpleTool(wx.ID_CLOSE, wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK), _('Close Editor'), '')
		self.Bind(wx.EVT_TOOL, self.OnCloseEditor, id=wx.ID_CLOSE)

		# EXIT this app.
		self.toolbar.AddSimpleTool(wx.ID_EXIT, wx.ArtProvider.GetBitmap(wx.ART_QUIT), _('Quit Cellaret'), '')
		self.Bind(wx.EVT_TOOL, self.OnQuitApplication, id=wx.ID_EXIT)

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
		(start, to) = self.cellaEditor.GetSelection()
		to += len(starttag)
		self.cellaEditor.GotoPos(start)
		self.cellaEditor.AddText(starttag)
		self.cellaEditor.GotoPos(to)
		self.cellaEditor.AddText(stoptag)
		self.cellaEditor.GotoPos(to+len(stoptag))

	#def OnDelete(self, event):
		#frm, to = self.cellaEditor.GetSelection()
		#self.cellaEditor.Remove(frm, to)
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
