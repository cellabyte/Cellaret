#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.1 Markdown Browser & Editor
dater.py
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
import wx.calendar
import environment
from environment import pngCellaret_24
#from environment import *

class CellaCalendar(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, size = (200, 160), title = _('Calendar'))
		self.parent = parent
		favicon = pngCellaret_24.GetIcon()
		self.SetIcon(favicon)
		self.Centre()

		calendar = wx.calendar.CalendarCtrl(self, wx.ID_ANY, wx.DateTime_Now(), style = wx.calendar.CAL_SHOW_HOLIDAYS | wx.calendar.CAL_MONDAY_FIRST | wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
		self.calendar = calendar
		self.Bind(wx.calendar.EVT_CALENDAR, self.OnCalSelected, id = calendar.GetId())

		# Setup to display a set of holidays.
		#====================================
		self.holidays = [(1,1), (10,31), (12,25)] # These dates, don't move around.
		self.Bind(wx.calendar.EVT_CALENDAR_MONTH, self.OnChangeMonth, calendar)
		self.OnChangeMonth()

	def OnChangeMonth(self, event = None):
		currentMonth = self.calendar.GetDate().GetMonth() + 1 # Convert wx.DateTime 0-11 to 1-12.
		for month, day in self.holidays:
			if month == currentMonth:
				self.calendar.SetHoliday(day)
		if currentMonth == 8:
			attr = wx.calendar.CalendarDateAttr(border = wx.calendar.CAL_BORDER_SQUARE, colBorder = 'red')
			self.calendar.SetAttr(14, attr)
		else:
			self.calendar.ResetAttr(14)
 
	def OnCalSelected(self, event):
		self.parent.cellaEditor.AddText(event.GetDate().Format('%d.%m.%Y'))
		self.Destroy()
