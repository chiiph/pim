from core.text import Text
from core.editor import Editor
from plugins.base.editcommand import EditCommand

class Save(EditCommand):
	def __init__(self, edt):
		self.editor= edt
		self.name= "Save"
		self.mode= 1

		self.stage= 0
	
	def run(self,text):
		active= self.editor.texts[self.editor.activeText]
		if self.stage== 0: # Check what's the name to save the file
			text.setText(active.fileName)
			text.cursor= len(active.fileName)
			self.stage= 1
		elif self.stage== 1 and self.editor.lastKey != ord('\n'): # and 
			super(Save, self).run(text)
		elif self.stage== 1:
			active.fd.write(active.text)
			active.fd.close()
			active.load(active.fd.fileName)
			text.setText("SAVED!")
	
	def register(self):
		self.editor.activation["M-^_"]= self
		return
