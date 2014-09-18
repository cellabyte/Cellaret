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

gettext.install('cellaret', './translations', unicode=True)

# GLOBAL VARS
#==============================================================================
from environment import *

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
			self.filePath = codecs.open(os.path.join(MD_PATH_FILE), mode="r", encoding="utf-8") # open the file and encoding
			self.mdText = self.filePath.read() # read Markdown file
			self.filePath.close() # close the file
			self.mdHtml = markdown.markdown(self.mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(self.mdHtml) # deduce the content as html
			self.SetTitle(MD_PATH_FILE + " - Cellaret")
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
		exportID = wx.NewId()
		menu.AppendMenu(exportID, _('Export to'), export)
		htmlID = wx.NewId()
		htmlItem = export.Append(htmlID, _('HTML file'), '')
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
		refreshItem = menu.Append(wx.ID_REFRESH, _('Refresh\tF5'), '')
		self.Bind(wx.EVT_MENU, self.OnRefresh, refreshItem)
		#copySelectedItem = menu.Append(wx.ID_COPY, _('&Copy selected\tCtrl-C'), '')
		#self.Bind(wx.EVT_MENU, self.OnCopySelected, copySelectedItem)
		self.editItem = menu.Append(wx.ID_EDIT, _('&Editor\tCtrl-E'), '')
		self.Bind(wx.EVT_MENU, self.OnEdit, self.editItem)
		menu.AppendSeparator()
		self.preferencesItem = menu.Append(wx.ID_PREFERENCES, _('Preferences...'), '')
		self.Bind(wx.EVT_MENU, self.OnPreferences, self.preferencesItem)
		menuBar.Append(menu, _('E&dit'))

		menu = wx.Menu()
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

#		self.statusbar = self.CreateStatusBar()

	# Show Context Menu
	def OnShowPopup(self, event):
		pos = event.GetPosition()
		pos = self.cellaBrowser.ScreenToClient(pos)
		self.cellaBrowser.PopupMenu(self.popupmenu, pos)

	def OnOpen(self, event):
		if SELECT_DIRECTORY:
			dir = WORKING_DIRECTORY
		else:
			dir = ''

		wildcardStr = 'Markdown (*.md, *.mkd, *.markdown)|*.md;*.mkd;*.markdown'
		fileOpenDlg = wx.FileDialog(self, _('Choose a file to open'), defaultDir=dir, wildcard=wildcardStr, style=wx.OPEN)
		if (fileOpenDlg.ShowModal() == wx.ID_OK) :
			global MD_PATH_FILE
			MD_PATH_FILE = fileOpenDlg.GetPath()
			try:
				file = codecs.open(os.path.join(MD_PATH_FILE), mode="r", encoding="utf-8") # open the file and encoding
				mdText = file.read() # read Markdown file
				file.close() # close the file

				mdHtml = markdown.markdown(mdText) # convert Markdown to html
				self.cellaBrowser.SetPage(mdHtml) # deduce the content as html
				self.SetTitle(MD_PATH_FILE + " - Cellaret")

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
			filePath = codecs.open(os.path.join(MD_PATH_FILE), mode="r", encoding="utf-8") # open the file and encoding
			mdText = filePath.read() # read Markdown file
			filePath.close() # close the file

			mdHtml = markdown.markdown(mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(mdHtml) # вdeduce the content as html
			self.SetTitle(MD_PATH_FILE + " - Cellaret")

			global MD_PRINT_DATA
			MD_PRINT_DATA = mdHtml

	def OnSaveAsHtml(self, event):
		if MD_PATH_FILE:
			dir = os.path.dirname(MD_PATH_FILE)
		else:
			dir = os.getcwd()

		#print os.getcwd()
		#print os.path.abspath(os.path.dirname(MD_PATH_FILE))
		#print os.path.dirname(MD_PATH_FILE)

		wildcardStr = 'HTML (*.html)|*.html'
		save_dlg = wx.FileDialog(self, message=_('Save file As...'), defaultDir=dir, defaultFile=_('new.html'), wildcard=wildcardStr, style=wx.SAVE | wx.OVERWRITE_PROMPT)
		if save_dlg.ShowModal() == wx.ID_OK:
			startHtml = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html>\n<head>\n\t<meta http-equiv="content-type" content="text/html; charset=utf-8">\n\t<meta name="generator" content="Cellaret (linux)">\n</head>\n<body>\n'
			endHtml = '\n</body>\n</html>\n'
			htmlFile = startHtml + MD_PRINT_DATA + endHtml
			htmlPathFile = save_dlg.GetPath()
			try:
				file = codecs.open(htmlPathFile, 'w', encoding="utf-8") # utf-8
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
			global MarkdownNew
			MarkdownNew = False
			self.child = MarkdownEditor(self)
			self.child.Show()
		else:
			self.OnNew(event)

	def OnNew(self, event):
		self.DisableMenuBrowser(self)
		global MarkdownNew
		MarkdownNew = True
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
			self.child.QuitApplication(self) # if open editor, QuitApplication (child wx.Frame)
		else:
			wx.Exit()

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
		self.Bind(wx.EVT_CLOSE, self.CloseEditor)

		self.iconToolbar = self.CreateIconToolbar()

		# EDITOR STATE VARS
		#==================
		self.markdownTextIsModified = False # file is changed (Modified)
		self.edLastFilenameSaved = False # No path to the file (new file)
		self.fileOpenDir = os.getcwd()
		self.edOverwriteMode = False # For the future implementation of the overwrite.

		# Editor cellaEditor
		#===================
		self.cellaEditor = cellaStyledTextCtrl(self) # Text editor subclass

		self.cellaEditor.SetBackgroundColour(wx.WHITE)

		# Scintilla
		self.cellaEditor.WrapMode = True # Scintilla Wrap mode
#		self.cellaEditor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d" % EDITOR_FONT_SIZE) # Style for the default text

		if not MarkdownNew:
			filePath = codecs.open(MD_PATH_FILE, mode="r", encoding="utf-8") # open the file and encoding
			self.cellaEditor.AppendText(filePath.read()) # read and deduce Markdown text
			self.SetTitle(MD_PATH_FILE + _(' - Cellaret File Editor'))
			filePath.close() # close the file
			self.cellaEditor.EmptyUndoBuffer() # clear the Undo buffer
			self.edLastFilenameSaved = MD_PATH_FILE # path to the file (for saving)

		self.markdownTextIsModified = False # Set False, because the text was changed.
		self.statusbar = self.CreateStatusBar()

		self.cellaEditor.Bind(wx.stc.EVT_STC_MODIFIED, self.OnTextChanged)
#		self.cellaEditor.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
#		self.Bind(wx.EVT_UPDATE_UI, self.OnKeyDown, self.cellaEditor)

		# Positioning iconToolbar & textCtrl
		#=====================================
		edPanelSizer = wx.BoxSizer(wx.VERTICAL)
		edPanelSizer.Add(self.iconToolbar, proportion=0, flag=wx.EXPAND)
		edPanelSizer.Add(self.cellaEditor, proportion=1, flag=wx.EXPAND)
		self.SetSizer(edPanelSizer) # Assigns Sizer for container management.

	# Toolbar iconToolbar
	#====================
	def CreateIconToolbar(self):

		self.toolbar = wx.ToolBar(self, -1)

		# Append to file
		self.toolbar.AddSimpleTool(wx.ID_OPEN, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN), _('Append to File'), '')
		self.Bind(wx.EVT_TOOL, self.OnOpenFile, id=wx.ID_OPEN)

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
		self.Bind(wx.EVT_TOOL, self.CloseEditor, id=wx.ID_CLOSE)

		# EXIT this app.
		self.toolbar.AddSimpleTool(wx.ID_EXIT, wx.ArtProvider.GetBitmap(wx.ART_QUIT), _('Quit Cellaret'), '')
		self.Bind(wx.EVT_TOOL, self.QuitApplication, id=wx.ID_EXIT)

		self.toolbar.Realize()

		return self.toolbar

	def OnTextChanged(self, event):
		self.markdownTextIsModified = True
		self.toolbar.EnableTool(wx.ID_SAVE, True) # Save highlight
		self.toolbar.EnableTool(wx.ID_UNDO, True) # Undo highlight
		event.Skip()

	#def OnKeyDown(self, event):
		#keycode = event.GetKeyCode()
		#print keycode
		#event.Skip()

	def OnOpenFile(self, event):
		wildcardStr = 'Markdown (*.md)|*.md|All files (*)|*'
		fileOpenDlg = wx.FileDialog(self, _('Choose a file to open'), wildcard=wildcardStr, style=wx.OPEN)
		if (fileOpenDlg.ShowModal() == wx.ID_OK) :
			PathFile = fileOpenDlg.GetPath()
			try:
				file = codecs.open(PathFile, 'r', encoding="utf-8") # utf-8
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
				file = codecs.open(MD_PATH_FILE, 'w', encoding="utf-8") # utf-8
				mdText = self.cellaEditor.GetText()
				file.write(mdText)
				file.close()

				self.statusbar.SetStatusText(os.path.basename(self.edLastFilenameSaved) + _(' Saved'), 0)
				self.markdownTextIsModified = False

				self.parent.OnRefresh(self) # Refresh browser (parent wx.Frame)
				self.toolbar.EnableTool(wx.ID_SAVE, False)

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error saving file\n') + str(error))
				dlg.ShowModal()
		else:
			self.OnSaveAsFile(event)

	def OnSaveAsFile(self, event):
		global MD_PATH_FILE
		if MD_PATH_FILE:
			dir = os.path.dirname(MD_PATH_FILE)
		elif SELECT_DIRECTORY:
			dir = WORKING_DIRECTORY
		else:
			dir = os.getcwd()

		wildcardStr = 'Markdown (*.md)|*.md'
		save_dlg = wx.FileDialog(self, message=_('Save file As...'), defaultDir=dir, defaultFile=_('new.md'), wildcard=wildcardStr, style=wx.SAVE | wx.OVERWRITE_PROMPT)
		if save_dlg.ShowModal() == wx.ID_OK:
			MD_PATH_FILE = save_dlg.GetPath()
			try:
				file = codecs.open(MD_PATH_FILE, 'w', encoding="utf-8") # utf-8
				mdText = self.cellaEditor.GetText()
				file.write(mdText)
				file.close()

				self.edLastFilenameSaved = os.path.basename(MD_PATH_FILE)
				self.statusbar.SetStatusText(self.edLastFilenameSaved + _(' Saved'), 0)
				self.markdownTextIsModified = False
				self.statusbar.SetStatusText('', 1)
				self.SetTitle(MD_PATH_FILE + _(' - Cellaret File Editor'))

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
		self._insertTags('**', '**')
		self.markdownTextIsModified = True

	def OnItalic(self, event):
		self._insertTags('_', '_')
		self.markdownTextIsModified = True

	def OnHyperlink(self, event):
		self._insertTags('<', '>')
		self.markdownTextIsModified = True

	def OnNamedHyperlink(self, event):
		self._insertTags('[', '](URL "")')
		self.markdownTextIsModified = True

	def OnInsertImage(self, event):
		dir = os.path.dirname(MD_PATH_FILE)
		wildcardStr = 'Images (*.jpg, *.gif, *.png)|*.jpg;*.gif;*.png|All files (*)|*'
		dlg = wx.FileDialog(self, message = _('Choose image file'), defaultDir = dir, defaultFile = "", wildcard = wildcardStr, style=wx.OPEN | wx.FILE_MUST_EXIST)
		dlgResult = dlg.ShowModal()
		imagePathFile = dlg.GetPath()
		dlg.Destroy()
		if  dlgResult != wx.ID_OK: return

		self.cellaEditor.AddText('![altText](%s)' % imagePathFile)
		self.markdownTextIsModified = True

	def _insertTags(self, starttag, stoptag):
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

	def CloseEditor(self, event):
		''' If there were changes, request save the file. '''
		if self.markdownTextIsModified:
			dlg = wx.MessageDialog(self, _('File is modified. Save before exit?'), '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if (val == wx.ID_YES):
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

	def QuitApplication(self, event):
		''' If there were changes, request save the file. '''
		if self.markdownTextIsModified:
			dlg = wx.MessageDialog(self, _('File is modified. Save before exit?'), '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if (val == wx.ID_YES):
				self.OnSaveFile(event)
				if not self.markdownTextIsModified:
					wx.Exit() # Exit wx.App.MainLoop()
			elif val == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				wx.Exit() # Exit wx.App.MainLoop()
		else:
			wx.Exit() # Exit wx.App.MainLoop()
