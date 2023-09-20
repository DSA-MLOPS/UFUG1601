import logging
import os
import requests
import io
import logging
import json
import time
from mask import mask_inappropriate_words
from upstage.api import OCR


OCR_BACKEND_URL = os.environ["OCR_BACKEND_URL"]
OCR_SECRET = os.environ["OCR_SECRET"]
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()


logger = logging.getLogger(__name__)
logger.setLevel(level=LOGLEVEL)

client = OCR(OCR_BACKEND_URL, OCR_SECRET, redact=True, log_level="DEBUG", timeout=10)


def condense_results(ocr_results):
    result = ""
    for item in ocr_results:
        if 'text' in item and 'coordinates' in item:
            x1, y1 = item['coordinates'][0]
            x2, y2 = item['coordinates'][2]
            text = item['text']
            result += f"{text}[{x1},{y1}],"

    return result


if __name__ == '__main__':

    with open('i.png', 'rb') as f:
        img_data = f.read()

    ocr_results = client.request(img_data, "text_with_coords")
    print("ocr results: ", ocr_results)
        
    con_results = condense_results(ocr_results)
    print("condensed results: ", con_results)

    coords = mask_inappropriate_words(ocr_results)
    print("coords: ", coords)