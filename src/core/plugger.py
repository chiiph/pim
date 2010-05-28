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

import sys,os,re
class Plugger:
	def __init__(self):
		self.actions= dict()
		self.states= dict()

		self.classes= dict()
		self.loadAll()

	def loadAll(self):
		""" Loads all the plugins in the base path """

		self.load("actions", self.actions)
		self.load("states", self.states)
		print self.classes

	def load(self, dir, var):
		""" Loads all the plugins in dir to var and saves them to classes """
		
		filt= re.compile(".py$", re.IGNORECASE)
		files= filter(filt.search,os.listdir("plugins/"+dir+"/"))
		for f in files:
			file= f.replace(".py", "")
			if file!= "__init__":
				var[file]= file.capitalize()

		for act in var:
			print "Loading "+act+"..."
			res = __import__("plugins."+dir+"."+act, globals(), locals(), [var[act]], -1)
			self.classes[act]= getattr(res, var[act])
