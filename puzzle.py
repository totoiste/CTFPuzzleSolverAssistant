import numpy as np
import time
import random
import itertools
from PIL import Image
from piece import Piece
from utils import display_image

### Class Puzzle ###
#Puzzle is a set of pieces
class Puzzle:
	def __init__(self, name, image, nb_rows, nb_cols):
		self.name = name
		self.nb_rows = nb_rows
		self.nb_cols = nb_cols
		self.Pieces = []
		(self.image_height, self.image_width, self.rgb) = image.shape
		self.piece_width = int(self.image_width/self.nb_cols)
		self.piece_height = int(self.image_height/self.nb_rows)

		#Handle Exceptions before splitting in images in pieces
		if ((self.image_width % nb_cols)|(self.image_height % nb_rows)) != 0:
			print(f"Image size (width x height) = {self.image_width} x {self.image_height}")
			raise ValueError('Number of cols or rows must be a multiple of image heigth and width')
		else:
			self.split(image)

	def split(self,image):
		number = 0
		for y, x in itertools.product(range(self.nb_rows), range(self.nb_cols)):
			#print(f"Add Piece {number} with {x = } and {y = } and pixels {y*self.piece_height}:{y*self.piece_height+self.piece_height},{x*self.piece_width}:{x*self.piece_width+self.piece_width}")
			self.add(x, y, number, image[y*self.piece_height:y*self.piece_height+self.piece_height,x*self.piece_width:x*self.piece_width+self.piece_width])
			number += 1

	def add(self, x, y, number, pixels):
		self.Pieces.append(Piece(x, y, number, pixels))

	def save(self):
		display_image(f"Puzzle {self.name}",self.snap())

	def move(self,piece0,piece1):
		(X,Y) = (piece0.x, piece0.y)
		piece0.change_coord(piece1.x,piece1.y)
		piece1.change_coord(X,Y)

	def snap(self):
		image = np.empty((self.image_width,self.image_height,self.rgb), dtype="uint8")
		for y, x in itertools.product(range(self.nb_rows), range(self.nb_cols)):
			number = self.get_piece_number_by_coord(x,y)
			image[y*self.piece_height:y*self.piece_height+self.piece_height,x*self.piece_width:x*self.piece_width+self.piece_width] = self.Pieces[number].pixels
		return(image)

	def get_piece_number_by_coord(self,x,y):
		for piece in self.Pieces:
			if(piece.x == x and piece.y == y):
				return(piece.number)
		return(False)

	def find_piece_ready_to_move(self):
		for piece in self.Pieces:
			if(piece.selected_to_move is not False):
				return(piece.number)
		return(False)

	def find_piece_selected_as_match(self):
		for piece in self.Pieces:
			if(piece.selected_as_match is not False):
				return(piece.number)
		return(False)

	def find_piece_selected_as_blocked(self,row_or_col,num):
		blocked_pieces = []
		if row_or_col == 'row':
			for c in range(self.nb_cols):
				piece_num = self.get_piece_number_by_coord(c,num)
				if self.Pieces[piece_num].blocked is not False:
					blocked_pieces.append(piece_num)

		if row_or_col == 'col':
			for r in range(self.nb_rows):
				piece_num = self.get_piece_number_by_coord(num,r)
				if self.Pieces[piece_num].blocked is not False:
					blocked_pieces.append(piece_num)
		return(blocked_pieces)
		
	def euclidian_distance(self,np1,np2):
		if np1.size != np2.size:
			return 1
		else:
			np1 = np1.astype(np.int16) #before this conversion, values are : uint8
			np2 = np2.astype(np.int16)
			#https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
			return np.linalg.norm(np.subtract(np1,np2)) 

	def search_match(self,number,side):
		(best_index,best_piece) = (10000,0)
		border = self.Pieces[number].border(side)
		opp = self.Pieces[number].opposite_side(side)
		for piece in self.Pieces:
			if piece.number == number or piece.blocked is not False :
				next
			else:
				index = self.euclidian_distance(piece.border(opp),border)
				if index < best_index :
					(best_index,best_piece) = (index,piece.number)
		return (best_index,best_piece,opp)