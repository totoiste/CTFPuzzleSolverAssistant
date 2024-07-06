from PIL import Image

### Functions ###
def display_image(title,image):
	img = Image.fromarray(image)
	img.show(title)