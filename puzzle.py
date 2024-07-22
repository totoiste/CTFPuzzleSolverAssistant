import numpy as np
import time
import random
import itertools
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from piece import Piece, Tk_Piece
from utils import display_image, euclidian_distance, opposite_side


### Class Puzzle ###
# Puzzle is a set of pieces
class Puzzle:
	def __init__(self, name, image, nb_rows, nb_cols):
		self._name = name
		self._nb_rows = nb_rows
		self._nb_cols = nb_cols
		self.Pieces = []
		(self._image_height, self._image_width, self._rgb) = image.shape
		self._piece_width = int(self._image_width / self._nb_cols)
		self._piece_height = int(self._image_height / self._nb_rows)

		# Handle Exceptions before splitting in images in pieces
		if (
			(self._image_width % self._nb_cols) | (self._image_height % self._nb_rows)
		) != 0:
			print(
				f"Image size (width x height) = {self._image_width} x {self._image_height}"
			)
			raise ValueError(
				"Number of cols or rows must be a multiple of image heigth and width"
			)
		else:
			self.split(image)

	def split(self, image):
		for index, (y, x) in zip(
			itertools.count(start=0, step=1),
			itertools.product(range(self._nb_rows), range(self._nb_cols)),
		):
			# print(f"Add Piece {number} with {x = } and {y = } and pixels {y*self.piece_height}:{y*self.piece_height+self.piece_height},{x*self.piece_width}:{x*self.piece_width+self.piece_width}")
			self.add_piece(
				index,
				image[
					y * self._piece_height : y * self._piece_height
					+ self._piece_height,
					x * self._piece_width : x * self._piece_width + self._piece_width,
				],
			)

	def add_piece(self, id, pixels):
		self.Pieces.append(Piece(id, pixels))

#	def switch_pieces(self, piece0, piece1):
#		print(f"Switching piece {piece0._id} and piece {piece1._id}")
#		self.Pieces[piece0._id], self.Pieces[piece1._id] = self.Pieces[piece1._id], self.Pieces[piece0._id]

class Tk_Puzzle(Puzzle):
	def __init__(self, puzzle, window):
		self._Puzzle = puzzle
		self._window = window
		self.Tk_Pieces = []
		
		self.side_rectangle = (
			False  # used to manage the rectangle of selection of piece and side
		)
		
		for piece in self._Puzzle.Pieces:
			tk_piece = Tk_Piece(piece)
			self.Tk_Pieces.append(tk_piece)

	def init_canvas(self):
		for tk_piece in self.Tk_Pieces:
			(x, y) = self.get_coord(tk_piece)
			image = ImageTk.PhotoImage(Image.fromarray(tk_piece._piece._pixels))
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas = tk.Canvas(self._window.frame_grid, width=self._Puzzle._piece_width, height=self._Puzzle._piece_height, borderwidth=0, highlightthickness=1)
			self.Tk_Pieces[tk_piece._piece._original_pos].fd_image = self.Tk_Pieces[tk_piece._piece._original_pos].canvas.create_image((self._Puzzle._piece_width/2,self._Puzzle._piece_height/2),image=image)
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.image = image
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.grid(row=y,column=x)
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.bind('<Button-1>',			lambda event, arg=tk_piece: self.event_mouse_left_click(event, arg))
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.bind('<Double-Button-1>',	lambda event, arg=tk_piece: self.event_mouse_left_doubleclick(event, arg))
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.bind('<Button-3>',			lambda event, arg=tk_piece: self.event_mouse_right_click(event, arg))
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.bind('<Motion>',			lambda event, arg=tk_piece: self.event_mouse_motion(event, arg))
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.bind('<Enter>',				lambda event, arg=tk_piece: self.event_mouse_motion_enter(event, arg))
			self.Tk_Pieces[tk_piece._piece._original_pos].canvas.bind('<Leave>',				lambda event, arg=tk_piece: self.event_mouse_motion_leave(event, arg))
	
	def get_pos(self, tk_piece):
		positions = [element._piece._original_pos for element in self.Tk_Pieces]
		#print(f"Piece with original pos {piece._original_pos} is at pos = {positions.index(piece._piece._original_pos)}")
		return positions.index(tk_piece._piece._original_pos)

	def set_pos(self, piece, pos):
		pos_original = self.get_pos(piece)
		self.switch_pieces(self.Tk_Pieces[pos], self.Tk_Pieces[pos_original])
		
	def get_coord(self, piece):
		pos = self.get_pos(piece)
		x = pos % self._Puzzle._nb_cols
		y = pos // self._Puzzle._nb_rows
		#print(f"Piece with original pos {piece._original_pos} is at coord = {(x,y)}")
		return (x,y)

	def get_piece_by_coord(self, x, y):
		pos = y * self._Puzzle._nb_cols + x
		return self.Tk_Pieces[pos]

	def save(self):
		display_image(f"Puzzle {self._Puzzle._name}", self.snap())

	def snap(self):
		image = np.empty(
			(self._Puzzle._image_width, self._Puzzle._image_height, self._Puzzle._rgb), dtype="uint8"
		)
		for index, (y, x) in zip(
			itertools.count(start=0, step=1),
			itertools.product(range(self._Puzzle._nb_rows), range(self._Puzzle._nb_cols)),
		):
			image[
				y * self._Puzzle._piece_height : y * self._Puzzle._piece_height + self._Puzzle._piece_height,
				x * self._Puzzle._piece_width : x * self._Puzzle._piece_width + self._Puzzle._piece_width,
			] = self.Tk_Pieces[index]._pixels
		return image

	def shuffle(self):
		np.random.shuffle(self.Tk_Pieces)
		self._window.print_log(f"Puzzle shuffled !")

	def search_match(self, piece, side):
		(best_index, best_piece) = (float("+inf"), 0)
		border = piece._piece.border(side)
		opp = opposite_side(side)

		for candidate in self.Tk_Pieces:
			if piece == candidate or candidate.blocked is not False:
				next
			else:
				match = euclidian_distance(candidate.border(opp), border)
				if match < best_index:
					(best_index, best_piece) = (match, candidate)
		return (best_index, best_piece, opp)
		
	def switch_pieces(self, piece0, piece1):
		piece0_pos = self.get_pos(piece0)
		piece1_pos = self.get_pos(piece1)
		print(f"Before Switching : piece at pos {piece0_pos} is at {self.get_coord(piece0)} and piece at pos {piece1_pos} is at {self.get_coord(piece1)}")
		self.unmark_piece_moved(piece0)
		if piece0.blocked is not False or piece1.blocked is not False:
			self._window.print_log(f"Exchange KO : piece is blocked !")
		else:
			#self._Puzzle.switch_pieces(piece0, piece1)
			self.unmark_piece_matched(piece0)
			self.unmark_piece_matched(piece1)
			self.Tk_Pieces[piece0_pos], self.Tk_Pieces[piece1_pos] = self.Tk_Pieces[piece1_pos], self.Tk_Pieces[piece0_pos]
			self.display_refresh()
			self._window.print_log(f"Exchange OK : piece at pos {piece0_pos} and piece at pos {piece1_pos}")
		print(f"After Switching : piece at pos {piece0_pos} is at {self.get_coord(piece0)} and piece at pos {piece1_pos} is at {self.get_coord(piece1)}")		

	def get_neighbor_piece(self, piece, side):
		pos = self.get_pos(piece)
		(x, y) = self.get_coord(piece)
		neighbor = False

		if side == "W":
			if x > 0:
				x = x - 1
				neighbor = True
		if side == "E":
			if x < self._Puzzle._nb_cols - 1:
				x = x + 1
				neighbor = True
		if side == "N":
			if y > 0:
				y = y - 1
				neighbor = True
		if side == "S":
			if y < self._Puzzle._nb_rows - 1:
				y = y + 1
				neighbor = True

		if neighbor is not False:
			return self.get_piece_by_coord(x,y)
		else:
			return False

	def get_first_piece_by_line(self, line, number):
		if line == "row": 
			piece = self.Tk_Pieces[number * self._Puzzle._nb_cols]
		elif line == "col":
			piece = self.Tk_Pieces[number]
		return piece

	def find_piece_ready_to_move(self):
		for piece in self.Tk_Pieces:
			if piece.selected_to_move is not False:
				return piece
		return False

	def find_piece_selected_as_match(self):
		for piece in self.Tk_Pieces:
			if piece.selected_as_match is not False:
				return piece
		return False

	def find_pieces_selected_as_blocked_by_line(self, line, number):
		blocked_pieces = []
		if line == "row": 
			for piece in self.Tk_Pieces[number * self._Puzzle._nb_cols:(number+1) * self._Puzzle._nb_cols]:
				if piece.blocked is not False:
					blocked_pieces.append(piece)
		elif line == "col":
			for piece in self.Tk_Pieces[number::self._Puzzle._nb_rows]:
				if piece.blocked is not False:
					blocked_pieces.append(piece)
		return blocked_pieces

	def display_refresh(self):
		for index, (y, x) in zip(
			itertools.count(start=0, step=1),
			itertools.product(range(self._Puzzle._nb_rows), range(self._Puzzle._nb_cols))
		):
			self.Tk_Pieces[index].canvas.grid(row=y, column=x)

	# Manage Events
	# Mouse Motion
	def event_mouse_motion(self, event, piece):
		piece_pos = self.get_pos(piece)
		self.Tk_Pieces[piece_pos].canvas.delete(self.side_rectangle)
		
		rectangle_color = "white"
		rectangle_thickness = self._Puzzle._piece_width / 5

		side = self.determine_side(event.x, event.y)
		if side == "N":
			self.side_rectangle = self.Tk_Pieces[piece_pos].canvas.create_rectangle(
				0,
				0,
				self._Puzzle._piece_width,
				rectangle_thickness,
				fill=rectangle_color
			)
		elif side == "S":
			self.side_rectangle = self.Tk_Pieces[piece_pos].canvas.create_rectangle(
				0,
				self._Puzzle._piece_height - rectangle_thickness,
				self._Puzzle._piece_width,
				self._Puzzle._piece_height,
				fill=rectangle_color,
			)
		elif side == "W":
			self.side_rectangle = self.Tk_Pieces[piece_pos].canvas.create_rectangle(
				0,
				0,
				rectangle_thickness,
				self._Puzzle._piece_height,
				fill=rectangle_color,
			)
		elif side == "E":
			self.side_rectangle = self.Tk_Pieces[piece_pos].canvas.create_rectangle(
				self._Puzzle._piece_width - rectangle_thickness,
				0,
				self._Puzzle._piece_width,
				self._Puzzle._piece_height,
				fill=rectangle_color,
			)

	def event_mouse_motion_enter(self, event, piece):
		piece_pos = self.get_pos(piece)
		self.Tk_Pieces[piece_pos].canvas.config(highlightthickness=0)

	def event_mouse_motion_leave(self, event, piece):
		piece_pos = self.get_pos(piece)
		self.Tk_Pieces[piece_pos].canvas.config(highlightthickness=1)
		self.Tk_Pieces[piece_pos].canvas.delete(self.side_rectangle)

	# Mouse right click - MOVE
	def event_mouse_right_click(self, event, piece):
		piece_pos = self.get_pos(piece)
		piece_to_move = self.find_piece_ready_to_move()
		if piece_to_move is not False:
			# self._window.print_log(f"Found {piece_to_move = } ready to move")
			self.unmark_piece_moved(
				piece_to_move
			)  # Only one piece can be marked to move
		self.mark_piece_ready_to_move(piece)
		self._window.print_log(f"Piece Selected to move is at pos {piece_pos}")

	def mark_piece_ready_to_move(self, piece):
		piece_pos = self.get_pos(piece)
		radius = int(self._Puzzle._piece_width / 3)
		color = "green"
		piece.selected_to_move = self.Tk_Pieces[piece_pos].canvas.create_oval(
			1, 1, radius + 1, radius + 1, fill=color
		)
		print(f"Mark Piece at pos {piece_pos} ready to move with canvas ID = {piece.selected_to_move}")

	def unmark_piece_moved(self, piece):
		piece_pos = self.get_pos(piece)
		print(f"Piece at pos {piece_pos} will be unselect to move soon")
		if piece.selected_to_move is not False:
			self.Tk_Pieces[piece_pos].canvas.delete(piece.selected_to_move)
			print(f"Piece at pos {piece_pos} with canvas id = {piece.selected_to_move} unselected to move")
			piece.selected_to_move = False

	# Mouse Left click
	def event_mouse_left_click(self, event, piece):
		piece_pos = self.get_pos(piece)
		piece_to_move = self.find_piece_ready_to_move()
		if piece_to_move is False:	# No piece has been activated before by right click
			side = self.determine_side(event.x, event.y)
			if side is not False:
				piece_as_match = self.find_piece_selected_as_match()
				if piece_as_match is not False:
					self.unmark_piece_matched(piece_as_match)
				(score, match, opp_side) = self.search_match(piece, side)
				match_pos = self.get_pos(match)
				self._window.print_log(f"Best match for {piece_pos}/{side} = {match_pos}/{opp_side}")
				self.mark_piece_as_match(match)
			else:
				self._window.print_log(f"Piece at pos {piece_pos} clicked on {event.x = } and {event.y = }")
		else:
			piece_to_move_pos = self.get_pos(piece_to_move)
			self._window.print_log(f"Preparing exchange between piece at pos {piece_pos} and piece {piece_to_move_pos}")
			self.switch_pieces(piece_to_move, piece)

	def mark_piece_as_match(self, piece):
		piece_pos = self.get_pos(piece)
		radius = int(self._Puzzle._piece_width / 3)
		color = "blue"
		piece.selected_as_match = self.Tk_Pieces[piece_pos].canvas.create_oval(
			1, 1, radius + 1, radius + 1, fill=color
		)

	def unmark_piece_matched(self, piece):
		piece_pos = self.get_pos(piece)
		if piece.selected_as_match is not False:
			self.Tk_Pieces[piece_pos].canvas.delete(piece.selected_as_match)
			piece.selected_as_match = False

	# Mouse double click
	def event_mouse_left_doubleclick(self, event, piece):
		if piece.blocked is False:
			self.mark_piece_blocked(piece)
		else:
			self.unmark_piece_blocked(piece)

	def mark_piece_blocked(self, piece):
		piece_pos = self.get_pos(piece)
		radius = int(self._Puzzle._piece_width / 3)
		color = "red"
		piece.block(
			self.Tk_Pieces[piece_pos].canvas.create_oval(
				self._Puzzle._piece_width - radius - 1,
				1,
				self._Puzzle._piece_width - 1,
				radius + 1,
				fill=color,
			)
		)
		self._window.print_log(f"Piece at pos {piece_pos} is blocked")

	def unmark_piece_blocked(self, piece):
		if piece.blocked is not False:
			piece_pos = self.get_pos(piece)
			self.Tk_Pieces[piece_pos].canvas.delete(piece.blocked)
			piece.unblock()
			self._window.print_log(f"Piece at pos {piece_pos} is unblocked")
			self.unmark_piece_moved(piece)

	def unblock_all(self):
		for piece in self.Tk_Pieces:
			self.unmark_piece_blocked(piece)

	# Mouse wheel
	def event_mouse_wheel(self, event):
		self._window.frame_menu.Console.yview_scroll(int(-1 * (event.delta / 120)), "units")

	def determine_side(self, x, y):
		if (
			y < self._Puzzle._piece_height / 5
			and x > self._Puzzle._piece_width / 5
			and x < self._Puzzle._piece_width * 4 / 5
		):
			return "N"
		elif (
			y > self._Puzzle._piece_height * 4 / 5
			and x > self._Puzzle._piece_width / 5
			and x < self._Puzzle._piece_width * 4 / 5
		):
			return "S"
		elif (
			x < self._Puzzle._piece_width / 5
			and y > self._Puzzle._piece_height / 5
			and y < self._Puzzle._piece_height * 4 / 5
		):
			return "W"
		elif (
			x > self._Puzzle._piece_width * 4 / 5
			and y > self._Puzzle._piece_height / 5
			and y < self._Puzzle._piece_height * 4 / 5
		):
			return "E"
		else:
			return False
