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

import string,curses,sys,traceback
import curses.panel
from core.editor import Editor
from core.text import Text

# list of modifier keys to handle multiple keystrokes
modifierkeys= [0x1b #alt
	]

class Pim:
	def __init__(self, scr):
		self.stdscr= scr
		(self.my,self.mx)= stdscr.getmaxyx()
		self.topLine= 1

		self.editor= Editor()
		self.editor.maxrow= self.my
		self.editor.maxcol= self.mx

		### DEBUGGING CODE ###
		txt= Text(self.editor)
		txt.load("test")
		self.editor.texts.append(txt)
		self.editor.lineText= Text(self.editor)
		### END DEBUGGING  ###

		self.createUi()
		
		while 1:
			if self.editor.activeMode.mode == 1: # mode 1 interacts with the cmdLine window
				self.cmdLine.addstr(0, 0, self.editor.lineText.text)
			elif self.editor.activeMode.mode == 0: # mode 0 interacts with the display window
				self.display.addstr(0, 0, self.editor.getText(self.topLine, self.topLine+self.my))
			
			self.status.addstr(0, 0, "Mode: "+self.editor.activeMode.name) # Debug for now, may be it'll stay as status
			
			self.refresh() # refreshes the content in all the windows
			self.editor.lastKey= self.stdscr.getch() # get the last key pressed
			
			# concat the last key with the sequence that could mean to change the mode
			self.editor.lastKeys+= str(self.editor.lastKey) 
			# if the last key pressed is in the modifier list (alt, ...) the clean the sequence
			if self.editor.lastKey in modifierkeys:
				self.editor.lastKeys= str(self.editor.lastKey)
				self.editor.lastKey= ""

			# change the mode if needed
			changed= self.editor.changeMode()
			if not changed:
				# if we don't change the mode, then pass the keys to the current mode
				if self.editor.activeMode.mode == 1:
					self.editor.runLine()
				elif self.editor.activeMode.mode == 0:
					self.editor.run()
			else:
				# if we change the mode, then the sequence must be clear
				self.editor.lastKeys= ""
			
			### DEBUG CODE ###
			if self.editor.lastKey == ord('q'): # FIXME: provisory exit
				break  # Exit the while()
			### DEBUG CODE ###

	def createUi(self):
		self.display = curses.newwin(self.my-2, self.mx-1, 0, 0)
		self.setwin(self.display)
	
		self.status = curses.newwin(1, self.mx-1, self.my-2, 0)
		self.setwin(self.status)
	
		self.cmdLine = curses.newwin(1, self.mx-1, self.my-1, 0)
		self.setwin(self.cmdLine)

		self.pstatus= curses.panel.new_panel(self.status)
		self.pcmdLine= curses.panel.new_panel(self.cmdLine)
		self.pdisplay= curses.panel.new_panel(self.display)

	def setwin(self, win):
		win.clear()
		win.refresh()
	
	def refresh(self):
		if self.editor.activeMode.mode == 1:
			self.cmdLine.move(self.editor.row, self.editor.col)
			self.cmdLine.clrtoeol()
		elif self.editor.activeMode.mode == 0:
			self.display.move(self.editor.row, self.editor.col)

		curses.panel.update_panels()
		curses.doupdate()
	
if __name__=='__main__':
	stdscr=curses.initscr()
	try:
		curses.noecho()
		curses.cbreak()
		curses.raw()
		curses.meta(1)
		stdscr.keypad(1)
		curses.curs_set(1)
		pim = Pim(stdscr)

		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin() 

	except:
		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin() 
		traceback.print_exc()           # Print the exception
