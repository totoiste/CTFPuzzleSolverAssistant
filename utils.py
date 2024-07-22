import numpy as np
from PIL import Image

### Functions ###
def display_image(title,image):
	img = Image.fromarray(image)
	img.show(title)
	
def euclidian_distance(np1,np2):
	if np1.size != np2.size:
		return 1
	else:
		np1 = np1.astype(np.int16) #before this conversion, values are : uint8
		np2 = np2.astype(np.int16)
		#https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
		return np.linalg.norm(np.subtract(np1,np2))
		
def opposite_side(side):
	if side == 'N':
		return 'S'
	elif side == 'S':
		return 'N'
	elif side == 'E':
		return 'W'
	elif side == 'W':
		return 'E'
	else:
		return side