#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.3 Markdown Browser & Editor
cellaret.py
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
import sys
import codecs
from application.main import MarkdownBrowser

if len(sys.argv) > 1:
	MD_PATH_FILE = os.path.abspath(sys.argv[1])
	MD_FILE_ARGV = True

	try:
		MD_PATH_FILE = MD_PATH_FILE.decode('utf-8') # omit in Python 3.x
	except UnicodeEncodeError:
		pass

	if not os.path.isfile(MD_PATH_FILE):
		MD_FILE_ARGV = False
		MD_PATH_FILE = None
else:
	MD_FILE_ARGV = False
	MD_PATH_FILE = None

if __name__ == '__main__':

	app = wx.App()
	MarkdownBrowser(MD_FILE_ARGV, MD_PATH_FILE)
	app.MainLoop()
