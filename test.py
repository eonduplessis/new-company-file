import logging
import requests
import gc
import os 

from pdf2image import convert_from_bytes


def png_ocr(png_file_path):
    with open(png_file_path, 'rb') as png_file:
        ocr_file = [
        ('images', ('ocr_image.png', png_file, 'image/png')),]

        response = requests.post('https://pngocr.azurewebsites.net/api/png-ocr?code=8ia5MihwBZcv6LlgA0DN4pENERqQPo33HKnSl95NIJJk4MoOpllSkQ==', files=ocr_file)
        
        return response.text

def pdf_to_png(company_name, companies_house_pdf_file_blob):
    # Store Pdf with convert_from_path function
    pages = convert_from_bytes(companies_house_pdf_file_blob.read())

    image_list = []

    i = 0     
    for page in pages:
        # Save pages as images in the pdf
        image_name = company_name + 'page'+ str(i) +'.png'
        logging.info(f"Saving image: {image_name}")
        page.save(image_name, 'PNG')
        logging.info(f"Saving image complete: {image_name}")
        image_list.append(image_name)
        i = i + 1

    del companies_house_pdf_file_blob
    del pages

    return image_list

def clean_up_files(file_list):
    for file in file_list:
        os.remove(file)

with open('companies-house-12345-test1.pdf', 'rb') as f:
    image_list = pdf_to_png('test-pdf.pdf', f)
    logging.info(f"Converting blob bytestream to PNG complete")

logging.info(f"Executing OCR on PNG payload")
for image in image_list:
    logging.info(f"Processing image: {image}")
    text = png_ocr(image)
    logging.info(f"Processing image complete: {image} \n"
                    f"Content size: {len(text)}")
    content = content + text

logging.info(f"Cleaning up temporary files")
clean_up_files(image_list)

logging.info(f"Processing PDF complete. \n"
                f"Document content size: {len(content)}")
