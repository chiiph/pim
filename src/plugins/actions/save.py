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

class Save(EditCommand):
	def __init__(self, edt):
		self.editor= edt
		self.name= "Save"
		self.mode= 0

		self.stage= 0

		self.message= ""
	
	def run(self,text):
		active= self.editor.texts[self.editor.activeText]
		if active.fileName == "":
			self.message= "Nothing to do here..."
			return
		
		file= open(active.fileName, "w")
		file.write(active.text)
		file.close()
		self.editor.activateDefaultMode()

		self.editor.status_message= "Saved"
	
	def register(self):
		self.editor.activation["meta a"]= self
