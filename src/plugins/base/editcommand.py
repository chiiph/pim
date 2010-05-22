from core.text import Text
from core.editor import Editor

import curses

class EditCommand(object):
	def __init__(self, edt):
		self.editor= edt
		self.key= 0 # Activation key
		self.name= "EditCommand"
		self.mode= 0
	
	def run(self,text):
		if self.editor.lastKey == curses.KEY_BACKSPACE or self.editor.lastKey == 127:
			if text.cursor > 0:
				text.setText(text.text[:text.cursor-1]+text.text[text.cursor:])
				text.cursor-= 1
				self.editor.updateRowCol(text)
		elif self.editor.lastKey == curses.KEY_DC:
			text.setText(text.text[:text.cursor]+text.text[text.cursor+1:])
#		TODO: history
#        elif self.editor.lastKey == curses.KEY_UP:
#            if self.editor.row>0:
#                self.editor.row-= 1
#                if self.editor.col>len(text.lines[self.editor.row]):
#                    self.editor.col= len(text.lines[self.editor.row])
#                self.editor.updateCursor(text)
#        elif self.editor.lastKey == curses.KEY_DOWN:
#            if self.editor.row<len(text.lines)-1:
#                self.editor.row+= 1
#                if self.editor.col>len(text.lines[self.editor.row]):
#                    self.editor.col= len(text.lines[self.editor.row])
#                self.editor.updateCursor(text)
		elif self.editor.lastKey == curses.KEY_LEFT:
			if self.editor.col>0:
				self.editor.col-= 1
				self.editor.updateCursor(text)
		elif self.editor.lastKey == curses.KEY_RIGHT:
			if self.editor.col<self.editor.maxcol and self.editor.col<(len(text.lines[self.editor.row])):
				self.editor.col+= 1
				self.editor.updateCursor(text)
		else:
			if 0<self.editor.lastKey<255 and self.editor.lastKey!=ord('\n'):
				text.setText(text.text[:text.cursor]+chr(self.editor.lastKey)+text.text[text.cursor:])
				text.cursor+=1
				self.editor.updateRowCol(text)
