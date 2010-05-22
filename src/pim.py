import string,curses,sys,traceback
import curses.panel
from core.editor import Editor
from core.text import Text

def ctrl(key):
	return ord(key)-64
	
def _ctoi(c):
    if type(c) == type(""):
        return ord(c)
    else:
        return c

def alt(c):
    if type(c) == type(""):
        return chr(_ctoi(c) | 0x80)
    else:
        return _ctoi(c) | 0x80

class Pim:
	def __init__(self, scr):
		self.stdscr= scr
		(self.my,self.mx)= stdscr.getmaxyx()
		self.topLine= 1

		self.editor= Editor()
		self.editor.maxrow= self.my
		self.editor.maxcol= self.mx

		txt= Text(self.editor)
		txt.load("test")
		self.editor.texts.append(txt)
		self.editor.lineText= Text(self.editor)

		self.createUi()
		
		while 1:
			if self.editor.activeMode.mode == 1:
				self.cmdLine.addstr(0, 0, self.editor.lineText.text)
			elif self.editor.activeMode.mode == 0:
				self.display.addstr(0, 0, self.editor.getText(self.topLine, self.topLine+self.my))
#            self.display.addstr(0, 0, self.editor.texts[0].getText(1, 20))
#            self.cmdLine.addstr(0, 0, "Mode:"+curses.keyname(self.editor.lastKey)+":")
			self.status.addstr(0, 0, "Mode: "+self.editor.activeMode.name)
#            self.display.addstr(0, 0, self.editor.texts[0].text)
			
			self.refresh()
			self.editor.lastKey= self.stdscr.getch()
			if not self.editor.changeMode():
				if self.editor.activeMode.mode == 1:
					self.editor.runLine()
				elif self.editor.activeMode.mode == 0:
					self.editor.run()

			if self.editor.lastKey == ord('q'): # FIXME: provisory exit
				break  # Exit the while()

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
		else:
			self.display.move(self.editor.row, self.editor.col)

#        self.stdscr.refresh()
#        self.cmdLine.refresh()
#        self.display.refresh()
		curses.panel.update_panels()
		curses.doupdate()
	
	def test(self):
		self.cmdLine.addstr(0,0,"test cmdline")
		self.display.addstr(0,0,"test display")
	
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

#    ed= Editor()
#    text= Text()
#    text.text= "Este es un texto de prueba"
#    text.cursor= 3
#    ed.lastKey= ord('y')
#    text.debug(0,1)
#    print "Editing: Add char y..."
#    ed.actions["edit"].run(text).debug(0,1)
#    ed.lastKey= 263
#    print "Editing: Erease char with backspace..."
#    ed.actions["edit"].run(text).debug(0,1)
#    ed.lastKey= 330
#    print "Editing: Erease char with delete..."
#    ed.actions["edit"].run(text).debug(0,1)
