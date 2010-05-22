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
		self.fd= open(fileName, "r+")
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
