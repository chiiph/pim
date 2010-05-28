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
from core.editor import Editor

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
	
	def load(self, fileName):
		""" Loads the fileName text """
		self.fileName= fileName
		self.fd= open(fileName, "rw+")
		self.text= self.fd.read()
		self.lines= self.text.split(linesep)
	
	def getText(self, lineInit, lineEnd):
		""" Returns the cropped text from lineInit to lineEnd """

		return linesep.join(self.lines[lineInit-1:lineEnd-lineInit])
	
	def setText(self, str):
		self.text= str
		self.lines= self.text.split(linesep)
	
	def debug(self, init, end):
		i= 0
		print self.text
		for l in self.getText(init, end):
			print str(i)+" | "+l
			i+=1
