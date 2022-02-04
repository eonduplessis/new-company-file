import logging
import requests
import gc
import os

import io

from pdf2image import convert_from_bytes

import azure.functions as func

API_PATH = 'https://pngocr.azurewebsites.net/api/png-ocr?code=8ia5MihwBZcv6LlgA0DN4pENERqQPo33HKnSl95NIJJk4MoOpllSkQ=='

def png_ocr(png_file):

    ocr_file = [
    ('images', ('ocr_image.png', png_file, 'image/png')),]

    response = requests.post(API_PATH, files=ocr_file)
    
    return response.text

def png_ocr_path(png_file_path):
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

def pdf_ocr(company_name, pdf_file_blob):
    pages = convert_from_bytes(pdf_file_blob.read(), fmt='png')

    result = ""

    i = 0
    for page in pages:
        # Save pages as images in the pdf
        image_name = company_name + 'page'+ str(i)
        logging.info(f"Performing OCR on image: {image_name}")

        buf = io.BytesIO()
        page.save(buf, 'PNG')
        
        result = result + png_ocr(buf)
        
        length = len(result)
        logging.info(f"Performing OCR on image complete: {image_name}, content length: {length}")

        i = i + 1

    del pdf_file_blob
    del pages

    return result

def clean_up_files(file_list):
    for file in file_list:
        os.remove(file)

async def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    logging.info(f"Converting blob bytestream to PNG")
    pdf_content = pdf_ocr(myblob.name[15:-4], myblob)
    logging.info(f"Converting blob bytestream to PNG complete")

    del myblob
    gc.collect()


    logging.info(f"Processing PDF complete. \n"
                 f"Document content size: {len(pdf_content)}")
