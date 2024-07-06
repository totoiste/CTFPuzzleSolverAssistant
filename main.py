import argparse
import numpy as np
import tkinter as tk
from PIL import Image
from puzzle import Puzzle
from window import MyWindow


### Manage command line Arguments ###
parser = argparse.ArgumentParser(prog='pict_puzzle.py', description='Solve and Generate Picture Puzzle')
parser.add_argument('-f', '--file', required=True)
parser.add_argument('-r', '--rows', type=int, required=True)
parser.add_argument('-c', '--cols', type=int, required=True)
args = parser.parse_args()

### MAIN ###
if __name__ == "__main__":
	try:
		img = Image.open(args.file)
		img_rgb = np.asarray(img)

		Puzzle = Puzzle(args.file,img_rgb,args.rows,args.cols)
		MainWindow = tk.Tk()
		window = MyWindow(MainWindow,Puzzle)
	except Exception as err:
		 print(f"Unexpected {err=}, {type(err)=}")