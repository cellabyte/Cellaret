# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.3 Markdown Browser & Editor
environment.py
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
import locale
from wx.lib.embeddedimage import PyEmbeddedImage

config = wx.Config('cellabyte/cellaret.conf')

config.SetPath('General')
if config.Exists('select_directory'):
	SELECT_DIRECTORY = config.ReadInt('select_directory')
	WORKING_DIRECTORY = config.Read('working_directory')
else:
	SELECT_DIRECTORY = False # Select Working directory, default False.
	config.WriteInt('select_directory', SELECT_DIRECTORY)
	WORKING_DIRECTORY = ''
	config.Write('working_directory', WORKING_DIRECTORY)
config.SetPath('')

config.SetPath('Browser')
if config.Exists('width'):
	BROWSER_WIDTH, BROWSER_HEIGHT = config.ReadInt('width'), config.ReadInt('height')
else:
	(BROWSER_WIDTH, BROWSER_HEIGHT) = (1024, 768)
	config.WriteInt('width', BROWSER_WIDTH)
	config.WriteInt('height', BROWSER_HEIGHT)
if config.Exists('font_size'):
	BROWSER_FONT_SIZE = config.ReadInt('font_size')
else:
	BROWSER_FONT_SIZE = 10 # Font size, default 10
	config.WriteInt('font_size', BROWSER_FONT_SIZE)
if config.Exists('print_filename'):
	PRINT_FILENAME = config.ReadInt('print_filename')
else:
	PRINT_FILENAME = False # Print the filename on the printer page.
	config.WriteInt('print_filename', PRINT_FILENAME)
if config.Exists('open_link'):
	WEBBROWSER_OPEN_LINK = config.ReadInt('open_link')
else:
	WEBBROWSER_OPEN_LINK = False # Open link in a web browser.
	config.WriteInt('open_link', WEBBROWSER_OPEN_LINK)

if config.Exists('show_statusbar'):
	BROWSER_STATUSBAR = config.ReadInt('show_statusbar')
else:
	BROWSER_STATUSBAR = True # Show Status Bar, default True.
	config.WriteInt('show_statusbar', BROWSER_STATUSBAR)
config.SetPath('')

config.SetPath('Editor')
if config.Exists('width'):
	EDITOR_WIDTH, EDITOR_HEIGHT = config.ReadInt('width'), config.ReadInt('height')
else:
	(EDITOR_WIDTH, EDITOR_HEIGHT) = (800, 600)
	config.WriteInt('width', EDITOR_WIDTH)
	config.WriteInt('height', EDITOR_HEIGHT)
if config.Exists('style_highlighting'):
	STYLE_HIGHLIGHTING = config.ReadInt('style_highlighting')
else:
	STYLE_HIGHLIGHTING = False # Style highlighting, default False.
	config.WriteInt('style_highlighting', STYLE_HIGHLIGHTING)
if config.Exists('datetime_format'):
	DATETIME_FORMAT = config.Read('datetime_format')
else:
	DATETIME_FORMAT = '\[%Y-%m-%d\] %H:%M'
	config.Write('datetime_format', DATETIME_FORMAT)

if config.Exists('wrap_mode'):
	WRAP_MODE = config.ReadInt('wrap_mode')
else:
	WRAP_MODE = True # Wrap mode, default True.
	config.WriteInt('wrap_mode', WRAP_MODE)
if config.Exists('white_space'):
	WHITE_SPACE = config.ReadInt('white_space')
else:
	WHITE_SPACE = True # Show White Space, default True.
	config.WriteInt('white_space', WHITE_SPACE)
if config.Exists('indentation_guides'):
	INDENTATION_GUIDES = config.ReadInt('indentation_guides')
else:
	INDENTATION_GUIDES = False # Show Indentation Guides, default False.
	config.WriteInt('indentation_guides', INDENTATION_GUIDES)
if config.Exists('line_endings'):
	LINE_ENDINGS = config.ReadInt('line_endings')
else:
	LINE_ENDINGS = False # Show Line Endings, default False.
	config.WriteInt('line_endings', LINE_ENDINGS)

if config.Exists('show_toolbar'):
	EDITOR_TOOLBAR = config.ReadInt('show_toolbar')
else:
	EDITOR_TOOLBAR = True # Show Tool Bar, default True.
	config.WriteInt('show_toolbar', EDITOR_TOOLBAR)
if config.Exists('show_statusbar'):
	EDITOR_STATUSBAR = config.ReadInt('show_statusbar')
else:
	EDITOR_STATUSBAR = True # Show Status Bar, default True.
	config.WriteInt('show_statusbar', EDITOR_STATUSBAR)
config.SetPath('')

OS_LANGUAGE, OS_ENCODING = locale.getdefaultlocale()

# Images
#==============================================================================

pngCellaret_24 = PyEmbeddedImage(
	"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAAlwSFlz"
	"AAALEwAACxMBAJqcGAAAAAd0SU1FB94EFQ8ONbXLeAIAAAAZdEVYdENvbW1lbnQAQ3JlYXRl"
	"ZCB3aXRoIEdJTVBXgQ4XAAACw0lEQVRIx5WWv04cVxTGf98IRcgNcqrIBSRVXBCEgvwEIcgU"
	"PILpkEhi1l1mY3NnPTOy2CmQYuxiJXdBeQKkYAm6NJEimsALRI5SWk4qCsznYgazf2ZYONJo"
	"NDP3fufc3z3nnhEN1smLKeMFoXVgBZjs/244Be8BPaGjNMT/1emo7mWSdVuS1oDZQc2P4z00"
	"9wR4lYZ450oHSVZMSOwDiw1CdWZANkg+BC2nIT4bcZBk3QmkY8HdahLXEMfYWJKMrf/BbyTN"
	"XziJ+hazL7gD7JbCps9RU+iVOOe23tv+0eYW8PpiTASQ5EULsQh+m4Z4FTgG9fNu8OBK3JHN"
	"PeCppC/A3yR50QKIkrw7JVgr1UrRNMRzpRNUXR7GUjIHG9v6GvyHpM+k6husJVkxFQkWqmwZ"
	"EKmcHPiSlBuwfAf+TdInpbiQZGBWeCFymee1G5qGeEkawjWKJRuIXB9XjdF6VBVRo/XjslET"
	"FpAkDQQpsRLJTI7LlgtcErZ1Zvv7YSz1GcxkVIEZm+9piJeAd7bnG7CMFrFggmtaSLcenp+f"
	"35L0O+h2uY9qEmegDsYhCunWD5JeSNrOkvankg9KLFcWowEim9OrEIV0qyPpJfAsS9pPSlzt"
	"0eyqP0hPI8TemMif2t7Nkvbm8MYbH7uhGCu3exG4VxdFSLceXkSed35arQsgC+051RTj5YN7"
	"EeaoOs/lciRJ1u0ALyosm+OyaxhXlbcnoCNV3asFPLf9t+3Hkn61vdsUeW2Tyrt/CX3V10Me"
	"pSHeuewHeXGAvQj8A/ycJe1tbmidvPgFeGA4zEL8LQzWwbKkE9tfAhudvNjwDcSrBnIb+Ff4"
	"/nAdkIX4zPaspENJM4YZwbTK+1XXtGDG9ufAn5hpj236edES3KjpG7/KQnunD5fSEFvNm1ZM"
	"Vb1i3WZFGv1tEewBPZujLBn9benkRfQB9vt0OEUhz8AAAAAASUVORK5CYII="
	)

pngCellaret_32 = PyEmbeddedImage(
	"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAAlwSFlz"
	"AAALEwAACxMBAJqcGAAAAAd0SU1FB94EFQ8zDfchiCIAAAAZdEVYdENvbW1lbnQAQ3JlYXRl"
	"ZCB3aXRoIEdJTVBXgQ4XAAACCklEQVRYw8WXPVIbQRBGX48ccwLbVa6iyr6CExHhRFJE5NQJ"
	"RxiS0Wq0AewNrMAxkRJQRmALO8CHAIfOiZxYTTJSLUIrzc4uRae7Ne+br6t/RoiMLC8+A0fA"
	"IbBX8ds9cAVMvbPnMedKBDgDRqTFyDvrkwRkedEF5rQTB97Z600fTAX8a4twgHk4c7cDWV5c"
	"AANAY1IUGarKPxF+eWc/VToQVA6AmxZvr6oIyAdVfbPuhFnL+TGAd/YjcBdcaAP+FhbfQd4D"
	"x4H1xIFHOffO7jcUUYb/AHknskrp/JGAUGpPooGIbfByea8cqKzzBBE74WWmCR1ua9QQEQtf"
	"dVcT2istiKgFD3FkQm+noYgUOMCh2TJYYkWkwgH2TEp9lUQsVFkkwqtnQQ0RBnidCgd4lSrA"
	"+dOZqqoIf1VlkQJPdmA4PrswxvSAO+9ORIQ/qR3TJMAvgYGq3o6HJ/tN27YJa1Q0XET6IrKC"
	"N2zb9ybscLE376vqbYC10bavDDCNhW+6eUMRU7Nre3X+dLaEV908VYR39nzrNAw57wHR8Boi"
	"Rqsq2LQ6D8dnM6AP7LQ9RcSSWS7DgxL8G9CLyXlNEbrOMqUfr4EJgIh8AW7q2r5DxO+wZU/K"
	"b4RNa/llsP454qd3tru1E3pnB0snWo6Jd7ab5UXnxZ9mWV50vLP/X/RxuhQRPUKf43me5UXn"
	"AWzYJuaY/UW0AAAAAElFTkSuQmCC"
	)

# pngCellaret_32.GetBitmap().SaveFile('cellaret.png', wx.BITMAP_TYPE_PNG)
