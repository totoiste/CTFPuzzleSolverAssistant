import numpy as np
from PIL import Image
from PIL import ImageTk
import itertools
import tkinter as tk
from piece import Piece, Tk_Piece
#from canvas import Canvas
from puzzle import Puzzle, Tk_Puzzle
from utils import opposite_side, euclidian_distance


### Class Window ###
class Window:
	def __init__(self, window, Puzzle):
		self._window = window
		self._Tk_Puzzle = Tk_Puzzle(Puzzle, self)
		self._window_width = self._Tk_Puzzle._Puzzle._image_width + self._Tk_Puzzle._Puzzle._nb_cols * 2
		self._window_height = self._Tk_Puzzle._Puzzle._image_height + self._Tk_Puzzle._Puzzle._nb_rows * 4
		self._window.title("Puzzle Solver Assistant")

		self.menu_width = 200
		self.bar_finder_size = 40
		self._window.geometry(
			f"{self._window_width+self.menu_width+self.bar_finder_size}x{self._window_height+self.bar_finder_size}"
		)
		self._window.resizable(width=False, height=False)

		# Frames Definition
		self.frame_finder_corner = tk.Frame(
			self._window, width=self.bar_finder_size, height=self.bar_finder_size, bd=0
		)
		self.frame_finder_cols = tk.Frame(
			self._window, width=self._window_width, height=self.bar_finder_size, bd=0
		)
		self.frame_finder_rows = tk.Frame(
			self._window, width=self.bar_finder_size, height=self._window_height, bd=0
		)
		self.frame_grid = tk.Frame(
			self._window, width=self._window_width, height=self._window_height, bd=0
		)
		self.frame_menu = tk.Frame(
			self._window,
			width=self.menu_width,
			height=self._window_height + self.bar_finder_size,
			bd=0,
		)

		# Frames Positioning
		self.frame_finder_corner.grid(row=0, column=0)
		self.frame_finder_cols.grid(row=0, column=1)
		self.frame_finder_rows.grid(row=1, column=0)
		self.frame_grid.grid(row=1, column=1)
		self.frame_menu.grid(row=0, column=2, rowspan=2)

		# Log in console
		self.console_log = ""
		self.frame_menu.Console = tk.Canvas(
			self.frame_menu,
			width=self.menu_width - 15,
			height=self.menu_width,
			bg="#e0e0e0",
			scrollregion=(0, 0, self.menu_width, self.menu_width),
		)
		self.frame_menu.Console_text = self.frame_menu.Console.create_text(
			(6, 6),
			text=self.console_log,
			anchor="nw",
			justify=tk.LEFT,
			width=self.menu_width - 15,
			fill="black",
			font=("Courier", 6, "italic"),
		)
		self.frame_menu.console_scroll = tk.Scrollbar(
			self.frame_menu, orient="vertical", command=self.frame_menu.Console.yview
		)
		self.frame_menu.Console["yscrollcommand"] = self.frame_menu.console_scroll.set
		self.frame_menu.Console.bind("<MouseWheel>", self._Tk_Puzzle.event_mouse_wheel)
		self.frame_menu.Console_lines = 0

		self.buttons = []
		self.checkbutton_num = tk.IntVar()

		self._Tk_Puzzle.init_canvas()
		self.init_buttons()
		self.init_menu()

	def print_log(self, log):
		self.frame_menu.Console_lines += 1
		self.console_log = str(log) + "\n" + self.console_log
		self.frame_menu.Console.configure(
			scrollregion=(
				0,
				0,
				self.menu_width,
				self.menu_width + self.frame_menu.Console_lines * 8,
			)
		)
		self.frame_menu.Console.itemconfig(
			self.frame_menu.Console_text,
			text=self.console_log,
		)

	# Manage Windows and Frames Init
	def init_menu(self):
		fg_color = "black"
		radius = 15

		self.frame_menu.Title = tk.Label(
			self.frame_menu,
			fg=fg_color,
			text="PUZZLE\nSOLVER\nASSISTANT",
			anchor="nw",
			height=3,
			font=("Courier", 24, "bold"),
		)
		self.frame_menu.legend = tk.Label(
			self.frame_menu,
			fg=fg_color,
			text="Colors Legend",
			anchor="nw",
			justify=tk.LEFT,
			font=("Courier", 10, "bold"),
		)
		self.frame_menu.legend1 = tk.Label(
			self.frame_menu,
			fg=fg_color,
			text="	  Blocked / Unmovable",
			anchor="nw",
			justify=tk.LEFT,
			font=("Courier", 8),
		)
		self.frame_menu.legend1_canvas = tk.Canvas(
			self.frame_menu, width=20, height=20, borderwidth=0, highlightthickness=1
		)
		self.frame_menu.legend1_circle = self.frame_menu.legend1_canvas.create_oval(
			1, 1, radius + 1, radius + 1, fill="red"
		)
		self.frame_menu.legend2 = tk.Label(
			self.frame_menu,
			fg=fg_color,
			text="	  Ready to Move",
			anchor="nw",
			justify=tk.LEFT,
			font=("Courier", 8),
		)
		self.frame_menu.legend2_canvas = tk.Canvas(
			self.frame_menu, width=20, height=20, borderwidth=0, highlightthickness=1
		)
		self.frame_menu.legend2_circle = self.frame_menu.legend2_canvas.create_oval(
			1, 1, radius + 1, radius + 1, fill="green"
		)
		self.frame_menu.legend3 = tk.Label(
			self.frame_menu,
			fg=fg_color,
			text="	  Possible Match",
			anchor="nw",
			justify=tk.LEFT,
			font=("Courier", 8),
		)
		self.frame_menu.legend3_canvas = tk.Canvas(
			self.frame_menu, width=20, height=20, borderwidth=0, highlightthickness=1
		)
		self.frame_menu.legend3_circle = self.frame_menu.legend3_canvas.create_oval(
			1, 1, radius + 1, radius + 1, fill="blue"
		)

		self.frame_menu.console = tk.Label(
			self.frame_menu,
			fg=fg_color,
			text="\n\nConsole >",
			anchor="nw",
			justify=tk.LEFT,
			font=("Courier", 10, "bold"),
		)

		self.frame_menu.chekbutton_num = tk.Checkbutton(
			self.frame_menu,
			text="View Pieces Indexes",
			variable=self.checkbutton_num,
			command=self.view_indexes,
		)
		self.frame_menu.button_unblock = tk.Button(
			self.frame_menu, text="Unblock all", command=self._Tk_Puzzle.unblock_all
		)
		self.frame_menu.button_shuffle = tk.Button(
			self.frame_menu, text="Shuffle", command=self.shuffle
		)
		self.frame_menu.button_save = tk.Button(
			self.frame_menu, text="Save", command=self._Tk_Puzzle.save
		)
		self.frame_menu.button_quit = tk.Button(
			self.frame_menu, text="Quit", command=self._window.destroy
		)
		self.frame_menu.button_help = tk.Button(
			self.frame_menu, text="Help", command=self.help
		)

		self.frame_menu.Title.grid(row=0, column=0, columnspan=3, sticky=tk.N + tk.S)
		self.frame_menu.legend.grid(row=1, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.legend1_canvas.grid(row=2, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.legend1.grid(row=2, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.legend2_canvas.grid(row=3, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.legend2.grid(row=3, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.legend3_canvas.grid(row=4, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.legend3.grid(row=4, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.console.grid(row=5, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.Console.grid(row=6, column=0, columnspan=2, sticky=tk.W)
		self.frame_menu.console_scroll.grid(row=6, column=2, sticky=tk.N + tk.S)
		self.frame_menu.chekbutton_num.grid(row=9, column=0, columnspan=3, sticky=tk.W)
		self.frame_menu.button_unblock.grid(
			row=11, column=0, columnspan=3, sticky=tk.W + tk.E
		)
		self.frame_menu.button_shuffle.grid(
			row=12, column=0, columnspan=3, sticky=tk.W + tk.E
		)
		self.frame_menu.button_save.grid(row=13, column=0, sticky=tk.W + tk.E)
		self.frame_menu.button_quit.grid(
			row=13, column=1, columnspan=2, sticky=tk.W + tk.E
		)
		self.frame_menu.button_help.grid(
			row=18, column=0, columnspan=3, sticky=tk.W + tk.E, pady=50
		)

	def init_buttons(self):
		number = 0

		# Bouton Corner
		button = self.buttons.append(
			tk.Button(
				self.frame_finder_corner,
				text="$",
				font=("Courier", 6, "bold"),
				command=lambda: self.search_match_grid(),
			)
		)
		self.buttons[number].grid(row=0, column=0)
		number += 1

		# Boutons columns
		for c in range(self._Tk_Puzzle._Puzzle._nb_cols):
			self.frame_finder_cols.grid_columnconfigure(
				c, minsize=self._Tk_Puzzle._Puzzle._piece_width + 2
			)
			button = self.buttons.append(
				tk.Button(
					self.frame_finder_cols,
					text="V",
					font=("Courier", 6, "bold"),
					command=lambda arg=c: self.search_match_line("col", arg),
				)
			)
			self.buttons[number].grid(row=0, column=c, sticky=tk.E + tk.W)
			number += 1

		# Boutons rows
		for r in range(self._Tk_Puzzle._Puzzle._nb_rows):
			self.frame_finder_rows.grid_rowconfigure(
				r, minsize=self._Tk_Puzzle._Puzzle._piece_height + 2
			)
			button = self.buttons.append(
				tk.Button(
					self.frame_finder_rows,
					text=">",
					font=("Courier", 6, "bold"),
					command=lambda arg=r: self.search_match_line("row", arg),
				)
			)
			self.buttons[number].grid(row=r, column=0, sticky=tk.N + tk.S)
			number += 1

	# Manage Pieces
	def search_match_line(self, line, number):
		blocked_pieces = self._Tk_Puzzle.find_pieces_selected_as_blocked_by_line(line, number)

		#Define a ref to compare
		if not blocked_pieces:	# Taking first piece of line as reference
			piece_ref = self._Tk_Puzzle.get_first_piece_by_line(line, number)
			blocked_pieces.append(piece_ref)
		else:  # Taking first blocked piece as reference
			piece_ref = blocked_pieces[0]
		piece_ref_pos = self._Tk_Puzzle.get_pos(piece_ref)	
		self.print_log(f"Piece at pos {piece_ref_pos} is a ref to sort {line} {number}")

		# Manage Pieces on the left or the top of ref piece then on the right or the bottom of ref piece
		if line == "row":
			sides = ["W","E"]
		elif line == "col":
			sides = ["N", "S"]

		for side in sides :
			piece_last = piece_ref
			piece_last_pos = self._Tk_Puzzle.get_pos(piece_last)
			while piece_neighbor := self._Tk_Puzzle.get_neighbor_piece(piece_last,side) :
				if piece_neighbor not in blocked_pieces:
					(best_index, piece_match, opp) = self._Tk_Puzzle.search_match(piece_last, side)
					piece_match_pos = self._Tk_Puzzle.get_pos(piece_match)
					self.print_log(f"best match for piece at pos {piece_last_pos}/{side} = {piece_match_pos}")
					self._Tk_Puzzle.switch_pieces(piece_neighbor,piece_match)
					blocked_pieces.append(piece_match)
					piece_last = piece_match
				else:
					piece_last = piece_neighbor
					piece_neighbor_pos = self._Tk_Puzzle.get_pos(piece_neighbor)
					self.print_log(f"Piece {piece_neighbor_pos} is unmovable")

	def find_border(self, side):
		""" This function try to find the best pieces which could be a border of the puzzle.
		As there are 4 borders, it is necessary to distinguish them with side : N,S,E,W
		"""
		
		# First we check if a piece is already mark as precedent match
		piece_match = self._Tk_Puzzle.find_piece_selected_as_match()
		if piece_match is not False:
			self._Tk_Puzzle.unmark_piece_matched(piece_match)

		scores = []

		for piece_corner in self._Tk_Puzzle.Tk_Pieces:
			best_index = 0
			for piece in self._Tk_Puzzle.Tk_Pieces:
				if piece_corner == piece:
					next
				else:
					index = euclidian_distance(
						piece_corner._piece.border(side), piece._piece.border(opposite_side(side))
					)
					if index > best_index:
						best_index = index
			scores.append((piece_corner,best_index))
		
		for element in sorted(scores, key=lambda x: x[1], reverse=True)[:10]:
			(piece, score) = element
			print(f"Score of piece @pos {piece._piece._original_pos} = {score}")

		
		#self.print_log(f"Best matches for corner {side} = {best_piece._piece._original_pos}")
		#self._Tk_Puzzle.mark_piece_as_match(best_piece)

	def find_corner(self, side1, side2):
		""" This function try to find the best piece which could be a corner of the puzzle.
		As there are 4 corners, it is necessary to distinguish them with side1 and side 2 : NW, NE, SE, SW
		"""
		
		# First we check if a piece is already mark as precedent match
		piece_match = self._Tk_Puzzle.find_piece_selected_as_match()
		if piece_match is not False:
			self._Tk_Puzzle.unmark_piece_matched(piece_match)

		(best_index, best_piece) = (0, 0)
		for piece_corner in self._Tk_Puzzle.Tk_Pieces:
			for piece in self._Tk_Puzzle.Tk_Pieces:
				if piece_corner == piece:
					next
				else:
					index1 = euclidian_distance(
						piece_corner._piece.border(side1), piece._piece.border(opposite_side(side1))
					)
					index2 = euclidian_distance(
						piece_corner._piece.border(side2), piece._piece.border(opposite_side(side2))
					)
					print(f"{piece_corner._piece._original_pos}/{piece_corner._piece._original_pos} has a score of {int(index1)} x {int(index2)} = {int(index1*index2)}")
					if index1 * index2 > best_index:
						(best_index, best_piece) = (
							index1 * index2,
							piece_corner
						)

		self.print_log(f"Best match for corner {side1}{side2} = {best_piece._piece._original_pos}")
		self._Tk_Puzzle.mark_piece_as_match(best_piece)

	def search_match_grid(self):
		#self.find_corner("N", "W")
		self.find_border("N")

	def view_indexes(self):
		if self.checkbutton_num.get() == 1:	 # Selected
			for piece in self._Tk_Puzzle.Tk_Pieces:
				if piece.view_index is False:
					piece.view_index = piece.canvas.create_text(
						(self._Tk_Puzzle._Puzzle._piece_width / 2, self._Tk_Puzzle._Puzzle._piece_height / 2),
						text=piece._piece._original_pos,
						fill="red",
						font=("Courier", 10, "bold"),
					)
				else:
					print(
						f"Unexpected Error ! Number is already printed... for piece {piece._piece._original_pos}"
					)
			self.print_log(f"Pieces Indexes are visible")
		else:  # UnSelected
			for piece in self._Tk_Puzzle.Tk_Pieces:
				if piece.view_index is not False:
					piece.canvas.delete(piece.view_index)
					piece.view_index = False
			self.print_log(f"Pieces Indexes are hidden")

	def shuffle(self):
		self._Tk_Puzzle.shuffle()
		self._Tk_Puzzle.display_refresh()
		self.print_log(f"Puzzle shuffled !")

	def help(self):
		helptext = """
		Actions : 
		
		1- Right click to select a piece to move then left click to the correct place
		2- Double click to block a piece to move
		3- Find a match by clicking on the border rectangle of each piece
		4- Try to solve line by line with left '>' and top buttons 'V'
		
		Contact and comments : 
		https://github.com/totoiste/CTFPuzzleSolverAssistant/"""

		help_window = tk.Toplevel()
		help_window.title("Help")
		help_window.config(width=800, height=200)

		help_window.canvas1 = tk.Canvas(
			help_window, width=800, height=180, bg="#e0e0e0"
		)
		help_window.canvas1.create_text(
			(6, 6),
			text=helptext,
			anchor="nw",
			justify=tk.LEFT,
			fill="black",
			font=("Courier", 8),
		)
		button_close = tk.Button(
			help_window, text="Close window", command=help_window.destroy
		)
		help_window.canvas1.pack()
		button_close.pack()
