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

from core import keys
from core.text import Text
from core.editor import Editor
from plugins.base.editcommand import EditCommand

class Open(EditCommand):
	def __init__(self, edt):
		self.editor= edt
		self.name= "Open"
		self.mode= 1

		self.message= ""

		self.stage= 0
	
	def run(self,text):
		if len(self.editor.texts)==0:
			self.editor.texts.append(Text(self.editor))
		active= self.editor.texts[self.editor.activeText]
		if self.stage== 0: # Check what's the name to save the file
			super(Open, self).run(text)
			self.stage= 1
		elif self.stage== 1 and self.editor.lastKey != "enter":
			super(Open, self).run(text)
		elif self.stage== 1:
			active.load(text.text)
#            self.tab(active)
			self.editor.activateDefaultMode()
			self.editor.status_message= "Opened file "+text.text
			text.setText("")
	
#    def tab(self, text):
#        tabs = []
#        text.cursor = 0
#        while text.cursor<len(text.text):
#            self.editor.logger.log(str(text.cursor)+","+str(len(text.text)))
#            pos = 1
#            if text.text[text.cursor]=='\t':
#                self.editor.logger.log("TAB!!")
#                (line, chars) = self.editor.getLine(text)
#                col= text.cursor-chars
#                pos = self.editor.tabsize-(col%self.editor.tabsize)
#                text.setText(text.text[:text.cursor]+(" "*pos)+text.text[text.cursor+1:])
#                tabs.append(text.cursor)
#            text.cursor += pos
#        text.cursor = 0
#        text.properties["tabs"] = tabs
#        self.editor.logger.log(str(tabs))
	
	def register(self):
		self.editor.activation["meta o"] = self
