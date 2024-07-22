import numpy as np
import itertools
from utils import display_image
import tkinter as tk

### Class Piece ###
class Piece:
	def __init__(self, original_pos, pixels):
		self._original_pos = original_pos
		self._pixels = pixels

	#Return a row or a column of pixels - Used to compare and find approaching piece
	def border(self,side):
		if side == 'N':
			return self._pixels[0,:]
		if side == 'W':
			return self._pixels[:,0]
		if side == 'E':
			return self._pixels[:,-1]
		if side == 'S':
			return self._pixels[-1,:]

class Tk_Piece(Piece):
	def __init__(self,piece):
		self._piece = piece
		self._pixels = piece._pixels
		self.selected_to_move = False
		self.selected_as_match = False
		self.blocked = False
		self.view_index = False

	def display(self):
		display_image(f"Piece with original pos {self._piece._original_pos = }",self._pixels)

	def block(self,value):
		self.blocked = value
		
	def unblock(self):
		self.blocked = False
