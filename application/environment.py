#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Cellaret v0.1.1 Markdown Browser & Editor
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
from wx.lib.embeddedimage import PyEmbeddedImage

config = wx.Config('config/cellaret.conf')

config.SetPath('Browser')
if config.Exists('Width'):
	BROWSER_WIDTH, BROWSER_HEIGHT = config.ReadInt('Width'), config.ReadInt('Height')
else:
	(BROWSER_WIDTH, BROWSER_HEIGHT) = (1024, 768)
	config.WriteInt('Width', BROWSER_WIDTH)
	config.WriteInt('Height', BROWSER_HEIGHT)
if config.Exists('Font_size'):
	BROWSER_FONT_SIZE = config.ReadInt('Font_size')
else:
	BROWSER_FONT_SIZE = 10 # Font size, default 10
	config.WriteInt('Font_size', BROWSER_FONT_SIZE)
if config.Exists('Print_filename'):
	PRINT_FILENAME = config.ReadInt('Print_filename')
else:
	PRINT_FILENAME = False # Print the filename on the printer page.
	config.WriteInt('Print_filename', PRINT_FILENAME)
if config.Exists('Navigate_through'):
	NAVIGATE_THROUGH_LINK = config.ReadInt('Navigate_through')
else:
	NAVIGATE_THROUGH_LINK = False # Navigate through the all links.
	config.WriteInt('Navigate_through', NAVIGATE_THROUGH_LINK)
config.SetPath('')

config.SetPath('Editor')
if config.Exists('Width'):
	EDITOR_WIDTH, EDITOR_HEIGHT = config.ReadInt('Width'), config.ReadInt('Height')
else:
	(EDITOR_WIDTH, EDITOR_HEIGHT) = (800, 600)
	config.WriteInt('Width', EDITOR_WIDTH)
	config.WriteInt('Height', EDITOR_HEIGHT)
if config.Exists('Check_brace'):
	CHECK_BRACE = config.ReadInt('Check_brace')
else:
	CHECK_BRACE = True # Check brace, default True.
	config.WriteInt('Check_brace', CHECK_BRACE)
if config.Exists('Style_highlighting'):
	STYLE_HIGHLIGHTING = config.ReadInt('Style_highlighting')
else:
	STYLE_HIGHLIGHTING = False # Style highlighting, default True.
	config.WriteInt('Style_highlighting', STYLE_HIGHLIGHTING)
config.SetPath('')

# Don't edit these variables
#============================
MD_PATH_FILE = ''
MD_PRINT_DATA = ''
MD_FILE_ARGV = False

# Images
#==============================================================================

Cellaret_24 = PyEmbeddedImage(
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

Cellaret_32 = PyEmbeddedImage(
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

# Cellaret_32.GetBitmap().SaveFile('cellaret.png', wx.BITMAP_TYPE_PNG)
