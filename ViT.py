from PIL import Image
import pytesseract

print(pytesseract.get_languages())

# To get text from image
print(pytesseract.image_to_string(Image.open('pdf_images/page_0.jpg')))
