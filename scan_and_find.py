from typing import Text
from VisionDemo import find_text, print_texts
from document_scanner import scan_image

def scan_and_find(path):
	texts = find_text(scan_image(path))
	print_texts(texts)
	return texts

# scan_and_find("IMG_7737.jpg")