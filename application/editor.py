#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.1 Markdown Browser & Editor
editor.py
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
#import wx.stc
import codecs
from environment import *

# Text editor subclass Scintilla
#==============================================================================
class cellaStyledTextCtrl(wx.stc.StyledTextCtrl):
	def __init__(self, parent):
		wx.stc.StyledTextCtrl.__init__(self, parent, style = 0)

		self.encoder = codecs.getencoder("utf-8")

		if wx.Platform == '__WXMSW__':
			faces = {'times': 'Times New Roman', 'mono': 'Courier New', 'helv': 'Arial', 'other': 'Comic Sans MS', 'size': 10, 'size2': 8}
			#self.SetEOLMode(wx.stc.STC_EOL_CRLF)
		else:
			faces = {'times': 'Times', 'mono': 'Courier', 'helv': 'Helvetica', 'other': 'new century schoolbook', 'size': 10, 'size2': 8}
			#self.SetEOLMode(wx.stc.STC_EOL_LF)

		# Global default styles
		self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, "back:#EDECEB,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
		self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#808080") # Style for matching brackets
		self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000") # Style to unpaired brackets (erroneous) - red background

		# Defining styles Markdown
		self.MARKDOWN_DEFAULT = 0
		self.MARKDOWN_LINE_BEGIN = 1
		self.MARKDOWN_STRONG1 = 2
		self.MARKDOWN_STRONG2 = 3
		self.MARKDOWN_EM1 = 4
		self.MARKDOWN_EM2 = 5
		self.MARKDOWN_HEADER1 = 6
		self.MARKDOWN_HEADER2 = 7
		self.MARKDOWN_HEADER3 = 8
		self.MARKDOWN_HEADER4 = 9
		self.MARKDOWN_HEADER5 = 10
		self.MARKDOWN_HEADER6 = 11
		self.MARKDOWN_PRECHAR = 12
		self.MARKDOWN_ULIST_ITEM = 13
		self.MARKDOWN_OLIST_ITEM = 14
		self.MARKDOWN_BLOCKQUOTE = 15
		self.MARKDOWN_STRIKEOUT = 16
		self.MARKDOWN_HRULE = 17
		self.MARKDOWN_LINK = 18
		self.MARKDOWN_CODE = 19
		self.MARKDOWN_CODE2 = 20
		self.MARKDOWN_CODEBK = 21

		'''		colors
		#86ABD9	#EDECEB	#BEBEBE	#FF0000	#ffff00	#6C8EA2	#0000FF	#FF00FF
		#A52A2A	#2E8B57	#008A8C	#A020F0	#6A5ACD	#008B8B			#7F0000
		'''

		self.StyleSetSpec(self.MARKDOWN_DEFAULT, "fore:#404040,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_LINE_BEGIN, "fore:#0000FF,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_STRONG1, "fore:#000000,face:%(helv)s,size:%(size)d,bold" % faces)
		self.StyleSetSpec(self.MARKDOWN_STRONG2, "fore:#A52A2A,face:%(mono)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_EM1, "fore:#A52A2A,face:%(mono)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_EM2, "fore:#000000,face:%(helv)s,size:%(size)d,italic" % faces)
		self.StyleSetSpec(self.MARKDOWN_HEADER1, "fore:#007F00,face:%(helv)s,size:%(size)d,bold" % faces)
		self.StyleSetSpec(self.MARKDOWN_HEADER2, "fore:#2E8B57,face:%(helv)s,size:%(size)d,bold" % faces)
		self.StyleSetSpec(self.MARKDOWN_HEADER3, "fore:#008A8C,face:%(helv)s,size:%(size)d,bold" % faces)
		self.StyleSetSpec(self.MARKDOWN_HEADER4, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_HEADER5, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_HEADER6, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_PRECHAR, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_ULIST_ITEM, "fore:#0000FF,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_OLIST_ITEM, "fore:#0000FF,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_BLOCKQUOTE, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_STRIKEOUT, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_HRULE, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_LINK, "fore:#007F00,face:%(helv)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_CODE, "fore:#FF00FF,face:%(mono)s,size:%(size)d" % faces)
		self.StyleSetSpec(self.MARKDOWN_CODEBK, "fore:#FF00FF,face:%(mono)s,size:%(size)d" % faces)

#		self.SetLexer(wx.stc.STC_LEX_CONTAINER)

		# Other useful attributes for the editing window
#		self.SetWhitespaceForeground(True,wx.Colour(240,210,210))

		self.SetMargins(2, 2) # Set left and right margin widths in pixels
		self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER) # Margin #1 - Set up the numbers in the margin
		self.SetMarginMask(1, 0) # only show line numbers
		self.SetMarginWidth(1, 40)

		self.EmptyUndoBuffer()

#		self.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEALWAYS)
#		self.SetIndentationGuides(True)
#		self.SetWrapMode(False)
#		self.SetEOLMode(wx.stc.STC_EOL_CRLF)
#		self.SetViewEOL(True)

		if STYLE_HIGHLIGHTING:
			self.Bind(wx.stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded) # Event triggered when you want to set the highlighting style.

		#if CHECK_BRACE:
			#self.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnCheckBrace) # Get the handler, where we will check pairing brackets.

	def calcByteLen(self, text):
		return len(self.encoder(text)[0]) # Calculate the length of the string in bytes (not characters).

	def calcBytePos(self, text, pos):
		return len(self.encoder(text[: pos])[0]) # Convert position in characters in the byte position.

	# Markdown Highlight
	#===================
	def OnStyleNeeded(self, event):
		text = self.GetText()
		''' Apply to all text, default style. '''
		self.StartStyling(0, 0xff)
		self.SetStyling(self.calcByteLen(text), self.MARKDOWN_DEFAULT)

		''' Highlight the text, using indicators. '''
		self.HighlightWord(u'*', self.MARKDOWN_EM1)
		self.HighlightPhrase(u'_', self.MARKDOWN_EM2)

		self.HighlightPhrase(u'**', self.MARKDOWN_STRONG1)
		#self.HighlightWord(u'__', self.MARKDOWN_STRONG2)

		self.HighlightLine(u'#', self.MARKDOWN_HEADER1)
		self.HighlightLine(u'##', self.MARKDOWN_HEADER2)
		self.HighlightLine(u'###', self.MARKDOWN_HEADER3)
		#self.HighlightLine(u'####', self.MARKDOWN_HEADER4)

		self.HighlightWord(u'-', self.MARKDOWN_ULIST_ITEM)
		self.HighlightWord(u'+', self.MARKDOWN_ULIST_ITEM)

		#self.HighlightWord(u'~~', self.MARKDOWN_STRIKEOUT)

		self.HighlightPhrase(u'`', self.MARKDOWN_CODE)
		#self.HighlightWord(u'~~~', self.MARKDOWN_CODEBK)

	# Handlers highlighting
	#======================
	def HighlightWord(self, highlight, style):
		text = self.GetText()
		pos = text.find(highlight)
		while pos != -1:
			bytepos = self.calcBytePos(text, pos) # Get the current position in bytes.
			text_byte_len = self.calcByteLen(highlight) # Calculate the length of the search string in bytes.

			''' Apply Style. '''
			self.StartStyling(bytepos, 0xff)
			self.SetStyling(text_byte_len, style)

			pos = text.find(highlight, pos + len(highlight) + 1)

	def HighlightLine(self, highlight, style):
		text = self.GetText()
		pos = text.find(highlight)

		while pos != -1:
			endLine = text.find("\n", pos)
			bytepos = self.calcBytePos(text, pos) # Get the current position in bytes.
			byte_len = self.calcByteLen(highlight) # Calculate the length of the search string in bytes.

			byteEndpos = self.calcBytePos(text, endLine)

			text_byte_len = byte_len + (byteEndpos - bytepos) - 2

			''' Apply Style. '''
			if text.find("\n", pos - 2):
				self.StartStyling(bytepos, 0xff)
				self.SetStyling(text_byte_len, style)

			pos = text.find(highlight, endLine)

	def HighlightPhrase(self, highlight, style):
		text = self.GetText()
		pos = text.find(highlight)

		while pos != -1:
			endLine = text.find(highlight, pos + 1)
			bytepos = self.calcBytePos(text, pos) # Get the current position in bytes.
			byte_len = self.calcByteLen(highlight) # Calculate the length of the search string in bytes.

			byteEndpos = self.calcBytePos(text, endLine)
#			print byteEndpos
#			print bytepos
			text_byte_len = byte_len + (byteEndpos - bytepos)
#			print ''
#			print text_byte_len
			''' Apply Style. '''
			self.StartStyling(bytepos, 0xff)
			if endLine < 1:
				self.SetStyling(byte_len, style)
				pos = text.find(highlight, pos + len(highlight) + 1)
			else:
				self.SetStyling(text_byte_len, style)
				pos = text.find(highlight, endLine + 2)

	# Markdown Brace
	#===============
	#def OnCheckBrace(self, event):
		#
