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

from os import linesep

class Line:
	def __init__(self, text, mark= False):
		self.data= text
		# if a line is marked, then it means that it belongs to the line above
		# this applies recursively and matters only for saving/line numbering
		# in editing it should be treated as a normal line
		self.marked= mark 
	
	def __len__(self):
		return len(self.data)

class Text:
	def __init__(self, edt):
		self.editor= edt
		self.text= ""
		self.mode= None
		# self.postAction
		self.selected= (0,0)
		self.cursor= 0
		self.fileName= ""
		self.fd= None
		self.lines= []

		self.properties= dict()
	
	def load(self, fileName):
		""" Loads the fileName text """
		self.fileName= fileName
		self.fd= open(fileName, "r")
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
		self.lines.append(Line(tmp))
		# if the string is longer, add it as marked
		while tmpl!="":
			tmp= tmpl[:size]
			tmpl= tmpl[size:]
			self.lines.append(Line(tmp, True))
	
	def getText(self, lineInit, lineEnd):
		""" Returns the cropped text from lineInit to lineEnd """
		trimmed= self.lines[lineInit-1:lineEnd-lineInit]
		txt= ""
		for l in trimmed:
			txt+= l.data+linesep

		return txt
	
	def setText(self, str):
		self.text= str
		self.splitText()
	
#    def whichLine(self):
#        there= False
#        i= 0
#        chars= 0
#        row= 0
#        col= 0
#        while not there:
#            if i<len(self.lines):
#                tmp= chars+len(self.lines[i])+1
#                if tmp>text.cursor and tmp<self.maxcol:
#                    col= text.cursor-chars
#                    there= True
#                else:
#                    row+= 1
#                    chars+=(len(self.lines[i])+1)
#                    i+=1
#            else:
#                there= True
#        return (row, col)

	def debug(self, init, end):
		i= 0
		print self.text
		for l in self.getText(init, end):
			print str(i)+" | "+l
			i+=1
