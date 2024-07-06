import numpy as np
from PIL import Image
from PIL import ImageTk
from puzzle import Puzzle
import itertools
import tkinter as tk
from piece import Piece
from puzzle import Puzzle

### Class MyWindow ###
class MyWindow:
	def __init__(self,window,Puzzle):
		self.menu_width 			= 200
		self.bar_finder_length	 	= 40
		self.window 				= window
		self.Puzzle 				= Puzzle
		window_width				= Puzzle.image_width+self.Puzzle.nb_cols*2
		window_height				= Puzzle.image_height+self.Puzzle.nb_rows*4
		self.window.title("Puzzle Solver Assistant")
		self.window.geometry(f"{window_width+self.menu_width+self.bar_finder_length}x{window_height+self.bar_finder_length}")
		self.window.resizable(width=False, height=False)

		#Frames Definition
		self.frame_finder_corner	= tk.Frame(self.window, width=self.bar_finder_length, height=self.bar_finder_length, bd=0)
		self.frame_finder_cols		= tk.Frame(self.window, width=window_width, height=self.bar_finder_length, bd=0)
		self.frame_finder_rows		= tk.Frame(self.window, width=self.bar_finder_length, height=window_height, bd=0)
		self.frame_grid				= tk.Frame(self.window, width=window_width, height=window_height, bd=0)
		self.frame_menu				= tk.Frame(self.window, width=self.menu_width, height=window_height+self.bar_finder_length, bd=0)

		#Frames Positioning
		self.frame_finder_corner.grid(	row = 0, column= 0)
		self.frame_finder_cols.grid(	row = 0, column= 1)
		self.frame_finder_rows.grid(	row = 1, column= 0)
		self.frame_grid.grid(			row = 1, column= 1)
		self.frame_menu.grid(			row = 0, column= 2, rowspan=2)
		
		#Log in console
		self.console_log = ''
		self.frame_menu.Console	= tk.Canvas(self.frame_menu, width=self.menu_width-15, height=self.menu_width, bg="#e0e0e0", scrollregion =(0, 0, self.menu_width, self.menu_width))
		self.frame_menu.Console_text = self.frame_menu.Console.create_text((6,6),text=self.console_log, anchor="nw", justify=tk.LEFT, width=self.menu_width-15, fill="black", font=("Courier", 6, "italic"))
		self.frame_menu.console_scroll	= tk.Scrollbar(self.frame_menu, orient='vertical', command=self.frame_menu.Console.yview)
		self.frame_menu.Console['yscrollcommand']=self.frame_menu.console_scroll.set
		self.frame_menu.Console.bind('<MouseWheel>',self.event_mouse_wheel)
		self.frame_menu.Console_lines = 0

		self.side_rectangle = False # used to manage the rectangle of selection of piece and side
		self.canvas = []
		self.buttons = []
		self.checkbutton_num = tk.IntVar()

		self.init_canvas()
		self.init_buttons()
		self.init_menu()
		self.window.mainloop()

	def print_log(self, log):
		self.frame_menu.Console_lines += 1
		self.console_log = str(log)+'\n'+self.console_log
		self.frame_menu.Console.configure(scrollregion=(0,0,self.menu_width,self.menu_width+self.frame_menu.Console_lines*8))
		self.frame_menu.Console.itemconfig(self.frame_menu.Console_text,text=self.console_log,)
		
	#Manage Windows and Frames Init
	def init_menu(self):
		fg_color = "black"
		radius = 15
		
		self.frame_menu.Title	 		= tk.Label(self.frame_menu, fg=fg_color, text="PUZZLE\nSOLVER\nASSISTANT", anchor="nw", height=3, font=("Courier", 24, "bold"))
		self.frame_menu.legend			= tk.Label(self.frame_menu, fg=fg_color, text="Colors Legend", anchor="nw", justify=tk.LEFT, font=("Courier", 10, "bold"))
		self.frame_menu.legend1			= tk.Label(self.frame_menu, fg=fg_color, text="    Blocked / Unmovable", anchor="nw", justify=tk.LEFT, font=("Courier", 8))
		self.frame_menu.legend1_canvas 	= tk.Canvas(self.frame_menu, width=20, height=20, borderwidth=0, highlightthickness=1)
		self.frame_menu.legend1_circle	= self.frame_menu.legend1_canvas.create_oval(1,1,radius+1,radius+1,fill="red")
		self.frame_menu.legend2			= tk.Label(self.frame_menu, fg=fg_color, text="    Ready to Move", anchor="nw", justify=tk.LEFT, font=("Courier", 8))
		self.frame_menu.legend2_canvas 	= tk.Canvas(self.frame_menu, width=20, height=20, borderwidth=0, highlightthickness=1)
		self.frame_menu.legend2_circle	= self.frame_menu.legend2_canvas.create_oval(1,1,radius+1,radius+1,fill="green")
		self.frame_menu.legend3			= tk.Label(self.frame_menu, fg=fg_color, text="    Possible Match", anchor="nw", justify=tk.LEFT, font=("Courier", 8))
		self.frame_menu.legend3_canvas 	= tk.Canvas(self.frame_menu, width=20, height=20, borderwidth=0, highlightthickness=1)
		self.frame_menu.legend3_circle	= self.frame_menu.legend3_canvas.create_oval(1,1,radius+1,radius+1,fill="blue")
		
		self.frame_menu.console			= tk.Label(self.frame_menu, fg=fg_color, text="\n\nConsole >", anchor="nw", justify=tk.LEFT, font=("Courier", 10, "bold"))

		self.frame_menu.chekbutton_num	= tk.Checkbutton(self.frame_menu, text = "View Pieces Numbers", variable = self.checkbutton_num, command = self.view_numbers)
		self.frame_menu.button_unblock	= tk.Button(self.frame_menu, text = "Unblock all", command = self.unblock_all)
		self.frame_menu.button_shuffle	= tk.Button(self.frame_menu, text = "Shuffle", command = self.shuffle)
		self.frame_menu.button_save		= tk.Button(self.frame_menu, text = "Save", command = self.Puzzle.save)
		self.frame_menu.button_quit		= tk.Button(self.frame_menu, text = "Quit", command = self.window.destroy)
		self.frame_menu.button_help		= tk.Button(self.frame_menu, text = "Help", command = self.help)

		self.frame_menu.Title.grid(				row=0,column=0,columnspan=3,sticky=tk.N+tk.S)
		self.frame_menu.legend.grid(			row=1,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.legend1_canvas.grid(	row=2,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.legend1.grid(			row=2,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.legend2_canvas.grid(	row=3,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.legend2.grid(			row=3,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.legend3_canvas.grid(	row=4,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.legend3.grid(			row=4,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.console.grid(			row=5,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.Console.grid(			row=6,column=0,columnspan=2,sticky=tk.W)
		self.frame_menu.console_scroll.grid(	row=6,column=2,				sticky=tk.N+tk.S)
		self.frame_menu.chekbutton_num.grid(	row=9,column=0,columnspan=3,sticky=tk.W)
		self.frame_menu.button_unblock.grid(	row=11,column=0,columnspan=3,sticky=tk.W+tk.E)
		self.frame_menu.button_shuffle.grid(	row=12,column=0,columnspan=3,sticky=tk.W+tk.E)
		self.frame_menu.button_save.grid(		row=13,column=0,				sticky=tk.W+tk.E)
		self.frame_menu.button_quit.grid(		row=13,column=1,columnspan=2,sticky=tk.W+tk.E)
		self.frame_menu.button_help.grid(		row=18,column=0,columnspan=3,sticky=tk.W+tk.E,pady=50)

	def init_canvas(self):
		number = 0
		for y, x in itertools.product(range(self.Puzzle.nb_rows), range(self.Puzzle.nb_cols)):
			piece = Image.fromarray(self.Puzzle.Pieces[number].pixels)
			image = ImageTk.PhotoImage(piece)
			self.canvas.append(tk.Canvas(self.frame_grid, width=self.Puzzle.piece_width, height=self.Puzzle.piece_height, borderwidth=0, highlightthickness=1))
			self.canvas[number].fd_image = self.canvas[number].create_image((self.Puzzle.piece_width/2,self.Puzzle.piece_height/2),image=image)
			#self.canvas[number].create_text((self.Puzzle.piece_width/2,self.Puzzle.piece_height/2),text=number,fill='red')
			self.canvas[number].image = image
			self.canvas[number].grid(row=y,column=x)
			self.canvas[number].bind('<Button-1>',			lambda event, arg=number: self.event_mouse_left_click(event, arg))
			self.canvas[number].bind('<Double-Button-1>',	lambda event, arg=number: self.event_mouse_left_doubleclick(event, arg))
			self.canvas[number].bind('<Button-3>',			lambda event, arg=number: self.event_mouse_right_click(event, arg))
			self.canvas[number].bind('<Motion>',			lambda event, arg=number: self.event_mouse_motion(event, arg))
			self.canvas[number].bind('<Enter>',				lambda event, arg=number: self.event_mouse_motion_enter(event, arg))
			self.canvas[number].bind('<Leave>',				lambda event, arg=number: self.event_mouse_motion_leave(event, arg))
			#Uncomment to see pieces appearing but very slow
			#self.window.update()
			number += 1

	def init_buttons(self):
		number =  0

		#Bouton Corner
		button = self.buttons.append(tk.Button(self.frame_finder_corner, text ="$", font=("Courier", 6, "bold"), command = lambda : self.search_match_grid()))
		self.buttons[number].grid(row=0,column=0)
		number += 1
		
		#Boutons columns
		for c in range(self.Puzzle.nb_cols):
			self.frame_finder_cols.grid_columnconfigure(c, minsize=self.Puzzle.piece_width+2)
			button = self.buttons.append(tk.Button(self.frame_finder_cols, text ="V", font=("Courier", 6, "bold"), command = lambda arg=c: self.search_match_line("col",arg)))
			self.buttons[number].grid(row=0, column=c, sticky=tk.E+tk.W)
			number += 1

		#Boutons rows
		for r in range(self.Puzzle.nb_rows):
			self.frame_finder_rows.grid_rowconfigure(r, minsize=self.Puzzle.piece_height+2)
			button = self.buttons.append(tk.Button(self.frame_finder_rows, text =">", font=("Courier", 6, "bold"), command = lambda arg=r: self.search_match_line("row",arg)))
			self.buttons[number].grid(row=r, column=0, sticky=tk.N+tk.S)
			number += 1

	#Manage Events
	#Mouse Motion
	def event_mouse_motion(self, event, number):
		self.canvas[number].delete(self.side_rectangle)

		rectangle_color="white"
		rectangle_thickness = self.Puzzle.piece_width / 8
		
		side = self.determine_side(event.x,event.y)
		if side == 'N':
			self.side_rectangle = self.canvas[number].create_rectangle(0,0,self.Puzzle.piece_width,rectangle_thickness,fill=rectangle_color)
		elif side == 'S':
			self.side_rectangle = self.canvas[number].create_rectangle(0,self.Puzzle.piece_height-rectangle_thickness,self.Puzzle.piece_width,self.Puzzle.piece_height,fill=rectangle_color)
		elif side == 'W':
			self.side_rectangle = self.canvas[number].create_rectangle(0,0,rectangle_thickness,self.Puzzle.piece_height,fill=rectangle_color)
		elif side == 'E':
			self.side_rectangle = self.canvas[number].create_rectangle(self.Puzzle.piece_width-rectangle_thickness,0,self.Puzzle.piece_width,self.Puzzle.piece_height,fill=rectangle_color)

	def event_mouse_motion_enter(self, event, number):
		self.canvas[number].config(highlightthickness=0)

	def event_mouse_motion_leave(self, event, number):
		self.canvas[number].config(highlightthickness=1)
		self.canvas[number].delete(self.side_rectangle)

	#Mouse right click - MOVE
	def event_mouse_right_click(self, event, number):
		piece_to_move = self.Puzzle.find_piece_ready_to_move()
		if piece_to_move is not False:
			#self.print_log(f"Found {piece_to_move = } ready to move")
			self.unmark_piece_moved(piece_to_move) # Only one piece can be marked to move
		self.mark_piece_ready_to_move(number)
		self.print_log(f"Piece Selected to move = {number}")
	
	def mark_piece_ready_to_move(self,number):
		radius = int(self.Puzzle.piece_width / 3)
		color = "green" 
		self.Puzzle.Pieces[number].selected_to_move = self.canvas[number].create_oval(1,1,radius+1,radius+1,fill=color)

	def unmark_piece_moved(self,number):
		self.canvas[number].delete(self.Puzzle.Pieces[number].selected_to_move)
		self.Puzzle.Pieces[number].selected_to_move = False

	#Mouse Left click
	def event_mouse_left_click(self, event, number):
		piece_to_move = self.Puzzle.find_piece_ready_to_move()
		if piece_to_move is False: #No piece has been activated before by right click
			side = self.determine_side(event.x,event.y)
			if side is not False:
				#self.print_log(f"image clicked on {event.x = } and {event.y = } : Piece {number = } and {side = }")
				piece_as_match = self.Puzzle.find_piece_selected_as_match()
				if piece_as_match is not False:
					self.unmark_piece_matched(piece_as_match)
				(score,match,opp_side) = self.Puzzle.search_match(number,side)
				self.print_log(f"Best match for {number}/{side} = {match}/{opp_side}")
				self.mark_piece_as_match(match)
			#else:
				#self.print_log(f"image clicked on {event.x = } and {event.y = } : Piece {number = }")
		else:
			#self.print_log(f"Preparing exchange between piece {number} and piece {piece_to_move}")
			self.move_pieces(self.Puzzle.Pieces[piece_to_move],self.Puzzle.Pieces[number])

	def mark_piece_as_match(self,number):
		radius = int(self.Puzzle.piece_width / 3)
		color = "blue" 
		self.Puzzle.Pieces[number].selected_as_match = self.canvas[number].create_oval(1,1,radius+1,radius+1,fill=color)

	def unmark_piece_matched(self,number):
		self.canvas[number].delete(self.Puzzle.Pieces[number].selected_as_match)
		self.Puzzle.Pieces[number].selected_as_match = False 
		
	#Mouse double click
	def event_mouse_left_doubleclick(self, event, number):
		if self.Puzzle.Pieces[number].blocked is False:
			self.mark_piece_blocked(number)
		else:
			self.mark_piece_unblocked(number)


	def mark_piece_blocked(self,number):
		radius = int(self.Puzzle.piece_width / 3)
		color = "red" 
		self.Puzzle.Pieces[number].block(self.canvas[number].create_oval(self.Puzzle.piece_width - radius - 1,1,self.Puzzle.piece_width - 1,radius+1,fill=color))
		self.print_log(f"Piece {number} blocked")

	def mark_piece_unblocked(self,number):
		if self.Puzzle.Pieces[number].blocked is not False:
			self.canvas[number].delete(self.Puzzle.Pieces[number].blocked)
			self.Puzzle.Pieces[number].unblock()
			self.print_log(f"Piece {number} unblocked")

	#Mouse wheel
	def event_mouse_wheel(self, event):
		self.frame_menu.Console.yview_scroll(int(-1*(event.delta/120)),"units")
		
	#Manage Pieces
	def move_pieces(self,piece0,piece1):
		if piece0.blocked is not False or piece1.blocked is not False :
			self.print_log(f"Exchange KO : piece is blocked !")
		else:
			self.Puzzle.move(piece0,piece1)
			self.canvas[piece0.number].grid(row=piece0.y,column=piece0.x)
			self.canvas[piece1.number].grid(row=piece1.y,column=piece1.x)
			self.unmark_piece_moved(piece0.number)
			self.unmark_piece_matched(piece0.number)
			self.print_log(f"Exchange OK : {piece0.number} and {piece1.number}")
		
	def search_match_line(self,row_or_col,num):
		blocked_pieces = self.Puzzle.find_piece_selected_as_blocked(row_or_col,num)

		if not blocked_pieces: #Taking first piece of line as reference
			line_ref = 0
			if row_or_col == 'row':
				piece_number_ref = self.Puzzle.get_piece_number_by_coord(line_ref,num)
			elif row_or_col == 'col':
				piece_number_ref = self.Puzzle.get_piece_number_by_coord(num,line_ref)
			blocked_pieces.append(piece_number_ref)
		else: #Taking first blocked piece as reference
			if row_or_col == 'row':
				line_ref = self.Puzzle.Pieces[blocked_pieces[0]].x
			elif row_or_col == 'col':
				line_ref = self.Puzzle.Pieces[blocked_pieces[0]].y
			piece_number_ref = blocked_pieces[0]
		self.print_log(f"Piece {piece_number_ref} is a ref to sort line {line_ref}")
			
		#Manage Pieces on the left or the top of ref piece
		piece_num = piece_number_ref
		last = piece_num
		ref = line_ref
		side = ''
		while ref >= 0:
			if row_or_col == 'row':
				piece_num = self.Puzzle.get_piece_number_by_coord(ref,num)
				side = 'W'
			elif row_or_col == 'col':
				piece_num = self.Puzzle.get_piece_number_by_coord(num,ref)
				side = 'N'
			if piece_num not in blocked_pieces:
				(best_index,piece_number_match,opp) = self.Puzzle.search_match(last,side)
				self.print_log(f"best match of {last}/{side} = {piece_number_match}")
				self.move_pieces(self.Puzzle.Pieces[piece_num],self.Puzzle.Pieces[piece_number_match])
				last = piece_number_match
			else:
				self.print_log(f"Piece {piece_num} is unmovable")
				last = piece_num
			ref = ref - 1

		#Manage Pieces on the right or the bottom of ref piece
		piece_num = piece_number_ref
		last = piece_num
		ref = line_ref
		side = ''
		while ref < self.Puzzle.nb_rows:
			if row_or_col == 'row':
				piece_num = self.Puzzle.get_piece_number_by_coord(ref,num)
				side = 'E'
			elif row_or_col == 'col':
				piece_num = self.Puzzle.get_piece_number_by_coord(num,ref)
				side = 'S'
			if piece_num not in blocked_pieces:
				(best_index,piece_number_match,opp) = self.Puzzle.search_match(last,side)
				self.print_log(f"best match of {last}/{side} = {piece_number_match}")
				self.move_pieces(self.Puzzle.Pieces[piece_num],self.Puzzle.Pieces[piece_number_match])
				last = piece_number_match
			else:
				self.print_log(f"Piece {piece_num} is unmovable")
				last = piece_num
			ref = ref + 1
		
	def find_corner(self,side1,side2):
		piece_as_match = self.Puzzle.find_piece_selected_as_match()
		if piece_as_match is not False:
			self.unmark_piece_matched(piece_as_match)

		(best_index,best_piece) = (0,0)
		for piece_corner in self.Puzzle.Pieces:
			for piece in self.Puzzle.Pieces:
				if piece_corner.number == piece.number:
					next
				else:
					index1 = self.Puzzle.euclidian_distance(piece_corner.border(side1),piece.border(piece.opposite_side(side1)))
					index2 = self.Puzzle.euclidian_distance(piece_corner.border(side2),piece.border(piece.opposite_side(side2)))
					if index1*index2 > best_index:
						(best_index,best_piece) = (index1*index2,piece_corner.number)

		self.print_log(f"Best match for corner {side1}{side2} = {best_piece}")
		self.mark_piece_as_match(best_piece)
	
	def search_match_grid(self):
		self.find_corner('N','W')

	def unblock_all(self):
		for piece in self.Puzzle.Pieces:
			self.mark_piece_unblocked(piece.number)

	def view_numbers(self):
		if self.checkbutton_num.get() == 1: #Selected
			for piece in self.Puzzle.Pieces:
				if piece.view_number is False:
					piece.view_number = self.canvas[piece.number].create_text((self.Puzzle.piece_width/2,self.Puzzle.piece_height/2),text=piece.number,fill='red',font=("Courier", 6, "bold"))
				else:
					print(f"Unexpected Error ! Number is already printed... for piece {piece.number}")
			self.print_log(f"Pieces Numbers are visible")
		else: #UnSelected
			for piece in self.Puzzle.Pieces:
				if piece.view_number is not False:
					self.canvas[piece.number].delete(piece.view_number)
					piece.view_number = False
			self.print_log(f"Pieces Numbers are hidden")

	def shuffle(self):
		# Time Management
		#time_start = time.time()
		
		number = 0
		has_moved = []
		new_order = [y for y in range(self.Puzzle.nb_rows*self.Puzzle.nb_cols)]
		random.shuffle(new_order)
		
		for y, x in itertools.product(range(self.Puzzle.nb_rows), range(self.Puzzle.nb_cols)):
			number = self.Puzzle.get_piece_number_by_coord(x,y)
			if number not in has_moved :
				self.move_pieces(self.Puzzle.Pieces[new_order[number]],self.Puzzle.Pieces[number])
				has_moved.append(number)
			#print(f"Time for {number = } : {time.time() - time_start}")
			number += 1

	def determine_side(self,x,y):
		if y < self.Puzzle.piece_height/5 and x > self.Puzzle.piece_width/5 and x < self.Puzzle.piece_width*4/5:
			return("N")
		elif y > self.Puzzle.piece_height*4/5 and x > self.Puzzle.piece_width/5 and x < self.Puzzle.piece_width*4/5:
			return("S")
		elif x < self.Puzzle.piece_width/5 and y > self.Puzzle.piece_height/5 and y < self.Puzzle.piece_height*4/5:
			return("W")
		elif x > self.Puzzle.piece_width*4/5 and y > self.Puzzle.piece_height/5 and y < self.Puzzle.piece_height*4/5:
			return("E")
		else:
			return(False)		 

	def help(self):
		helptext = '''
		Actions : 
		
		1- Right click to select a piece to move then left click to the correct place
		2- Double click to block a piece to move
		3- Find a match by clicking on the border rectangle of each piece
		4- Try to solve line by line with left '>' and top buttons 'V'
		
		Contact and comments : 
		https://github.com/totoiste/CTFPuzzleSolverAssistant/'''
		
		help_window = tk.Toplevel()
		help_window.title("Help")
		help_window.config(width=800, height=200)

		help_window.canvas1 = tk.Canvas(help_window, width = 800, height = 180, bg="#e0e0e0")
		help_window.canvas1.create_text((6,6),text=helptext, anchor="nw", justify=tk.LEFT, fill="black", font=("Courier", 8))
		button_close = tk.Button(help_window,text="Close window",command=help_window.destroy)
		help_window.canvas1.pack()
		button_close.pack()