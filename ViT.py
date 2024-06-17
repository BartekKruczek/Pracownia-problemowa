from PIL import Image
import pytesseract
import json

print(pytesseract.get_languages(config=''))

# To get text from image
image = pytesseract.image_to_string(Image.open('pdf_images/page_0.jpg'))

image_text = pytesseract.image_to_string(Image.open('pdf_images/page_0.jpg'))
# print(type(image_text))

# use LLM model to get text structure and dump it to json
image_text_structure = pytesseract.image_to_string(Image.open('pdf_images/page_0.jpg'), output_type=pytesseract.Output.DICT)
# print(json.dumps(image_text_structure, indent=2))

image_data = pytesseract.image_to_data(Image.open('pdf_images/page_0.jpg'), output_type=pytesseract.Output.DICT)
print(image_data.keys())
print(image_data["text"])
print(type(image_data["text"]))

image_structure = pytesseract.image_to_osd(Image.open('pdf_images/page_0.jpg'))
# print(image_structure)

image_hocr = pytesseract.image_to_pdf_or_hocr(Image.open('pdf_images/page_0.jpg'), extension='hocr')
# print(image_hocr)