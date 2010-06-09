#    Pim: A vim/emacs like text editor
#    Copyright (C) 2010 Tomas Touceda
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as 
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import linesep, open, fdopen, O_RDONLY, O_CREAT
from string import count, expandtabs

class Line:
	def __init__(self, text, edt, mark= False):
		self.data= text
		self.editor = edt
		# if a line is marked, then it means that it belongs to the line above
		# this applies recursively and matters only for saving/line numbering
		# in editing it should be treated as a normal line
		self.marked= mark 
	
	def __len__(self):
		return len(self.getData())
	
	def getData(self):
		return expandtabs(self.data, self.editor.tabsize)

class Text:
	def __init__(self, edt):
		self.editor= edt
		self.text= ""
		self.mode= None
		# self.postAction
		self.selected= (0,0)

		# Navigation marks
		self.cursor = 0 # cursor for the tab expanded text
		self.inner_cursor = 0 # cursor for the actual text
		self.line_pos = 0 # cursor for the line

		self.fileName= ""
		self.fd= None
		self.lines= []

		self.properties= dict()
	
	def load(self, fileName):
		""" Loads the fileName text """
		self.fileName= fileName
		self.fd= open(fileName, O_RDONLY | O_CREAT)
		self.fd = fdopen(self.fd)
		self.text= self.fd.read()
		self.splitText()
	
	def splitText(self):
		self.lines= []
		tmp= self.text.split(linesep)
		for l in tmp:
			self.addLine(l)
	
	def addLine(self, l):
		size= self.editor.maxcol-2
		tmpl= l
		# Add the first part without mark
		tmp= tmpl[:size]
		tmpl= tmpl[size:]
		self.lines.append(Line(l, self.editor))
		return
		# if the string is longer, add it as marked
		while tmpl!="":
			tmp= tmpl[:size]
			tmpl= tmpl[size:]
			self.lines.append(Line(tmp, self.editor,True))
	
	def getText(self, lineInit, lineEnd):
		""" Returns the cropped text from lineInit to lineEnd """
		trimmed= self.lines[lineInit-1:lineEnd-lineInit]
		txt= ""
		for l in trimmed:
			txt+= l.getData()+linesep

		return txt
	
	def getAllText(self):
		txt= ""
		for l in self.lines:
			txt+= l.getData()+linesep

		return txt
	
	def setText(self, str):
		self.text= str
		self.splitText()
	
	def debug(self, init, end):
		i= 0
		print self.text
		for l in self.getText(init, end):
			print str(i)+" | "+l
			i+=1
	
	def updateCursor(self):
		""" Sets the cursor from the inner_cursor """

		tmp_cursor = self.inner_cursor
		self.inner_cursor = 0
		self.cursor = 0

		expanded = expandtabs(self.text, self.editor.tabsize)

		while True:
			if self.inner_cursor == tmp_cursor:
				break

			# The only "problem" are tabs, so first we handle those
			if self.inner_cursor < len(self.text) and self.text[self.inner_cursor] == "\t":
				# Find out how much tabs are in a role, if any
				while self.inner_cursor != tmp_cursor and self.inner_cursor < len(self.text) and self.text[self.inner_cursor] == "\t":
					self.inner_cursor += 1

				# if there are any spaces after the tab chars, we need
				# to advance inner_cursor properly
				while self.inner_cursor != tmp_cursor and self.inner_cursor < len(self.text) and self.text[self.inner_cursor] == " ":
					self.inner_cursor += 1

				if self.inner_cursor >= len(self.text):
					# If the cursor's at the end of the text
					# then just push to the end both cursors
					self.cursor = len(expanded)-1
					self.inner_cursor = tmp_cursor
					break

				# else advance the spaces that correspond to the
				# tab expantion + the spaces after the tabs
				while self.cursor < len(expanded) and expanded[self.cursor] != self.text[self.inner_cursor]:
					self.cursor += 1
			elif self.cursor < len(expanded) and self.inner_cursor < len(self.text):
				# Otherwise, it's another char, and just advance both cursors
				self.cursor += 1
				self.inner_cursor += 1
			else:
				self.cursor = tmp_cursor
				self.inner_cursor = len(self.text)-1
	
	def updateInnerCursor(self):
		""" Sets the inner_cursor from cursor """

		tmp_cursor = self.cursor
		self.inner_cursor = 0
		self.cursor = 0

		expanded = expandtabs(self.text, self.editor.tabsize)

		while True:
			if self.cursor == tmp_cursor:
				break

			if self.inner_cursor < len(self.text) and self.text[self.inner_cursor] == "\t":
				# The only "problem" are tabs, so first we handle those
				# Find out how much tabs are in a role, if any
				while self.inner_cursor < len(self.text) and self.text[self.inner_cursor] == "\t":
					self.inner_cursor += 1

				# if there are any spaces after the tab chars, we need
				# to advance inner_cursor properly
				while self.inner_cursor < len(self.text) and self.text[self.inner_cursor] == " ":
					self.inner_cursor += 1

				if self.inner_cursor >= len(self.text):
					# If the cursor's at the end of the text
					# then just push to the end both cursors
					self.cursor = tmp_cursor
					self.inner_cursor = len(self.text)-1
				else:
					# else advance the spaces that correspond to the
					# tab expantion + the spaces after the tabs
					while self.cursor < len(expanded) and expanded[self.cursor] != self.text[self.inner_cursor]:
						self.cursor += 1
			elif self.cursor < len(expanded) and self.inner_cursor < len(self.text):
				# Otherwise, it's another char, and just advance both cursors
				self.cursor += 1
				self.inner_cursor += 1
			else:
				self.cursor = tmp_cursor
				self.inner_cursor = len(self.text)-1
