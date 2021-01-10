from logging import fatal
import os, io
from google.cloud import vision
from google.cloud.vision import types

#Check out Integromat https://www.integromat.com/en/
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

def find_text(path):
	client = vision.ImageAnnotatorClient()
	# Try with HEIC photo type

	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.text_detection(image=image)
	# f = open(OUT_FILE, "W")
	# f.write(str(response))
	# f.close()

	texts = response.text_annotations
	return texts

bounds = {
	"fname" : {
		"ul" : {
			"x" : 50,
			"y" : 580
		},
		"br" : {
			"x": 300,
			"y": 605
		}
	},
	"lname" : {
		"ul" : {
			"x": 50,
			"y": 555
		},
		"br" : {
			"x" : 300,
			"y" : 575
		}
	},
	"DOB" : {
		"ul" : {
			"x": 315,
			"y": 225
		},
		"br" : {
			"x" : 465,
			"y" : 255
		}
	},
	"EXP" : {
		"ul" : {
			"x": 312,
			"y": 192
		},
		"br" : {
			"x" : 460,
			"y" : 220
		}
	},
	"DL Number" : {
		"ul" : {
			"x": 303,
			"y": 153
		},
		"br" : {
			"x" : 463,
			"y" : 185
		}
	},
	"ADDRESS" : {
		"ul" : {
			"x": 21,
			"y": 608
		},
		"br" : {
			"x" : 75,
			"y" : 624
		}
	},
	"ZIP" : {
		"ul" : {
			"x": 171,
			"y": 623
		},
		"br" : {
			"x" : 231,
			"y" : 643
		}
	}
	,
	"SEX" : {
		"ul" : {
			"x": 189,
			"y": 654
		},
		"br" : {
			"x" : 204,
			"y" : 673
		}
	}

}


def print_texts(texts):
	# print('Texts:')
	for text in texts:
	# 	# print('\n"{}"'.format(text.description))

	# 	# vertices = (['({},{})'.format(vertex.x, vertex.y)
	# 	# 			for vertex in text.bounding_poly.vertices])

	# 	# print('bounds: {}'.format(','.join(vertices)))\
		vertices = text.bounding_poly.vertices
		for key in bounds.keys():
			bound = bounds.get(key)
			valid = False
			for vertex in vertices:
				if (
					vertex.x >= bound.get('ul').get('x') and vertex.x <= bound.get('br').get('x')
					and
					vertex.y >= bound.get('ul').get('y') and vertex.y <= bound.get('br').get('y')
				):
					valid = True
			if valid:
				print(f"{key} : {text.description}")
	
				
		