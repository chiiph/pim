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

from core.editor import Editor
from core.text import Text
from urwid import Edit, Text as urText, Frame, Filler, \
                  Pile, MainLoop, ExitMainLoop,\
				  raw_display
from os import linesep

class Display(Edit):
	def __init__(self, caption='', edit_text='', multiline=False, 
		align='left', wrap='space', allow_tab=False, edit_pos=None, layout=None):
		super(Display, self).__init__()

	def keypress(self,size,key):
		return key
	
	def set_filler_text(self, text, height):
		fill= height-(len(text.split(linesep)))
		str= text+("\n"*fill)
		super(Display, self).set_edit_text(str)

class Pim:
	def __init__(self):
		self.topLine= 1

		self.urscreen= raw_display.Screen()
		(self.mx,self.my)= self.urscreen.get_cols_rows()

		self.editor= Editor()
		self.editor.maxrow= self.my
		self.editor.maxcol= self.mx

		self.display= Display()
		self.status_line= urText("")
		self.command_line= Display()

		self.frame= Frame(body=Filler(self.display), footer=Pile([self.status_line, self.command_line]))

		self.loop = MainLoop(self.frame, screen=self.urscreen, input_filter=self.keypress, unhandled_input=self.keypress)

		self.update()

		self.loop.run()
	
	def keypress(self, key, raw):
		self.editor.lastKey= key[0] # get the last key pressed

		self.editor.logger.log(self.editor.lastKey)

		# change the mode if needed
		changed= self.editor.changeMode()
		if changed:
			self.editor.lastKey= ""

		if self.editor.activeMode.mode == 1:
			self.editor.runLine()
		elif self.editor.activeMode.mode == 0:
			self.editor.run()
		
		### DEBUG CODE ###
		if self.editor.lastKey == 'meta q': # FIXME: provisory exit
			raise ExitMainLoop()  # Exit the while()
		### DEBUG CODE ###

		self.update()

	def update(self):
#        self.display.move_cursor_to_coords((self.mx,), self.editor.col, self.editor.row)
		if self.editor.activeMode.mode == 1:
			self.frame.set_focus("footer")
			self.command_line.set_edit_pos(self.editor.lineText.cursor)
		elif self.editor.activeMode.mode == 0:
			self.frame.set_focus("body")
			self.display.set_edit_pos(self.editor.texts[self.editor.activeText].cursor)
		(self.editor.col,self.editor.row)= self.display.get_cursor_coords((self.mx,))
#        self.editor.pref_col= self.display.get_pref_col((self.mx,))
		self.command_line.set_edit_text(self.editor.lineText.text)
		self.display.set_filler_text(self.editor.getText(self.topLine, self.topLine+self.my), self.mx)
		
		status_text= "["+self.editor.activeMode.name+"]"
		if self.editor.status_message != "":
			status_text+= " - "+self.editor.status_message
		self.status_line.set_text(status_text) # Debug for now, may be it'll stay as status
		

if __name__=='__main__':
	pim = Pim()
