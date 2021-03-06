# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.3 Markdown Browser & Editor
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
import os
import codecs
import markdown
import gettext
from browser import CellaHtmlWindow, CellaPrinter, MarkdownHelp
from editor import MarkdownEditor
from preferences import CellaretPreferences
from environment import CONFIG, PNG_CELLARET_24, PNG_CELLARET_32, SELECT_DIRECTORY, WORKING_DIRECTORY, BROWSER_WIDTH, BROWSER_HEIGHT, BROWSER_STATUSBAR, EXEC_PATH

gettext.install('cellaret', os.path.join(EXEC_PATH, 'translations'), unicode = True)

# Markdown Browser (parent wx.Frame)
#==============================================================================
class MarkdownBrowser(wx.Frame):

	def __init__(self, mdFileArgv, mdPathFile):
		wx.Frame.__init__(self, None, size = (BROWSER_WIDTH, BROWSER_HEIGHT), title = 'Cellaret')
		favicon = PNG_CELLARET_24.GetIcon()
		self.SetIcon(favicon)
		self.Centre()
		self.Bind(wx.EVT_CLOSE, self.OnExit)

		# BROWSER STATE VARS
		#====================
		global MD_PATH_FILE
		global MD_DIR_NAME
		global MD_BASE_NAME
		global MD_PRINT_DATA
		MD_FILE_ARGV = mdFileArgv
		MD_PATH_FILE = mdPathFile
		MD_PRINT_DATA = None
		MD_DIR_NAME = None
		self.child = None

		# Browser cellaBrowser
		#======================
		self.cellaBrowser = CellaHtmlWindow(self) # HTML Window subclass
		self.Show(True)

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

		self.viewMenu.Check(self.ID_STATUSBAR, BROWSER_STATUSBAR)
		self.fileMenu.Enable(wx.ID_PREVIEW, False)
		self.fileMenu.Enable(wx.ID_PRINT, False)

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
		if not BROWSER_STATUSBAR:
			self.statusbar.Hide()

		# Open file from CLI
		#====================
		if MD_FILE_ARGV:
			MD_DIR_NAME = os.path.dirname(MD_PATH_FILE)
			MD_BASE_NAME = os.path.basename(MD_PATH_FILE)
			self.filePath = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
			self.mdText = self.filePath.read() # read Markdown file
			self.filePath.close() # close the file
			self.mdHtml = markdown.markdown(self.mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(self.mdHtml) # deduce the content as html
			self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')
			MD_PRINT_DATA = self.mdHtml
			self.fileMenu.Enable(wx.ID_PREVIEW, True)
			self.fileMenu.Enable(wx.ID_PRINT, True)

	# Toggle Full Screen
	#====================
	def OnFullScreen(self, event):
		self.ShowFullScreen(not self.IsFullScreen(), wx.FULLSCREEN_NOCAPTION)

	# Show Status Bar
	#=================
	def OnStatusBar(self, event):
		global BROWSER_STATUSBAR
		CONFIG.SetPath('Browser')
		if self.viewMenu.IsChecked(self.ID_STATUSBAR):
			self.statusbar.Show()
			CONFIG.WriteInt('show_statusbar', True)
			BROWSER_STATUSBAR = True
		else:
			self.statusbar.Hide()
			CONFIG.WriteInt('show_statusbar', False)
			BROWSER_STATUSBAR = False
		CONFIG.SetPath('')

	# Show Context Menu
	#===================
	def OnShowPopup(self, event):
		pos = event.GetPosition()
		pos = self.cellaBrowser.ScreenToClient(pos)
		self.cellaBrowser.PopupMenu(self.contextMenu, pos)

	# Open file
	#===========
	def OnOpen(self, event):
		global MD_PATH_FILE
		global MD_DIR_NAME
		global MD_BASE_NAME
		global MD_PRINT_DATA
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

				MD_PRINT_DATA = mdHtml
				self.fileMenu.Enable(wx.ID_PREVIEW, True)
				self.fileMenu.Enable(wx.ID_PRINT, True)

			except IOError, error:
				dlg = wx.MessageDialog(self, _('Error opening file\n') + str(error))
				dlg.ShowModal()
			except UnicodeDecodeError, error:
				dlg = wx.MessageDialog(self, _('Error opening file\n') + str(error))
				dlg.ShowModal()
		fileOpenDlg.Destroy()

	# Refresh
	#=========
	def OnRefresh(self, event):
		global MD_PRINT_DATA
		if MD_PATH_FILE:
			filePath = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
			mdText = filePath.read() # read Markdown file
			filePath.close() # close the file

			mdHtml = markdown.markdown(mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(mdHtml) # deduce the content as html
			self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')

			MD_PRINT_DATA = mdHtml
			self.fileMenu.Enable(wx.ID_PREVIEW, True)
			self.fileMenu.Enable(wx.ID_PRINT, True)

	def OnSaveRefresh(self, mdPathFile, mdDirName, mdBaseName):
		global MD_PATH_FILE
		global MD_DIR_NAME
		global MD_BASE_NAME
		global MD_PRINT_DATA
		MD_PATH_FILE = mdPathFile
		MD_DIR_NAME = mdDirName
		MD_BASE_NAME = mdBaseName
		if MD_PATH_FILE:
			filePath = codecs.open(MD_PATH_FILE, mode='r', encoding='utf-8') # open the file and encoding
			mdText = filePath.read() # read Markdown file
			filePath.close() # close the file

			mdHtml = markdown.markdown(mdText) # convert Markdown to html
			self.cellaBrowser.SetPage(mdHtml) # deduce the content as html
			self.SetTitle(MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')

			MD_PRINT_DATA = mdHtml
			self.fileMenu.Enable(wx.ID_PREVIEW, True)
			self.fileMenu.Enable(wx.ID_PRINT, True)

	def SetTitlePlus(self, event):
		self.SetTitle('+ ' + MD_BASE_NAME + ' (' + MD_DIR_NAME + ') - Cellaret')

	# Save as HTML
	#==============
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

	# Select & Copy
	#===============
	def OnSelectAll(self, event):
		self.cellaBrowser.SelectsAllText()

	def OnCopySelected(self, event):
		self.cellaBrowser.SelectionToClipboard()

	# Printer dialog
	#================
	def OnPreview(self, event):
		printer = CellaPrinter() # Printer subclass
		printer.PreviewText(MD_PRINT_DATA, MD_PATH_FILE)

	def OnPrint(self, event):
		printer = CellaPrinter() # Printer subclass
		printer.Print(MD_PRINT_DATA, MD_PATH_FILE)

	# Open Editor frame
	#===================
	def OnEdit(self, event):
		if MD_PATH_FILE:
			self.DisableMenuBrowser(self)
			self.child = MarkdownEditor(self, MD_PATH_FILE, MD_DIR_NAME, MD_BASE_NAME, False)
			self.child.Show()
		else:
			self.OnNew(event)

	def OnNew(self, event):
		self.DisableMenuBrowser(self)
		self.child = MarkdownEditor(self, None, MD_DIR_NAME, None, True)
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
		getCellaret_32Icon = PNG_CELLARET_32.GetIcon()

		info.SetIcon(getCellaret_32Icon)
		info.SetName('Cellaret')
		info.SetVersion('0.1.3')
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
