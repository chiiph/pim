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

alt= str(0x1b)
modif= alt+str(0x5b)

beggining= modif+str(0x37)+str(0x7e)
end= modif+str(0x38)+str(0x7e)

ctrlright= modif+str(0x31)+str(0x3b)+str(0x35)+str(0x43)
ctrlleft= modif+str(0x31)+str(0x3b)+str(0x35)+str(0x44)
#ctrlright= "kRIT5"
#ctrlleft= "kLFT5"
