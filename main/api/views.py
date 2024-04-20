from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# import easyocr

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 

from paddleocr import PaddleOCR

from python_main.scan_card import scan_reader
from python_main.scan_card import util

import time

# reader = easyocr.Reader(['en'],detector='dbnet18')
reader = PaddleOCR(lang='en')

@api_view(['POST'])
def card_scan_reader(request):
    # data = JSONParser().parse(request)
    if 'image' not in  request.data:
        return Response({'error': 'No image key provided'}, status=400)
    
    try:
        in_memory_image = request.data['image']
        image = np.fromstring(in_memory_image.file.read(), np.uint8)
        image = cv.imdecode(image, cv.IMREAD_COLOR)
    except: 
        return Response({'error': 'the upload it image is not an image file'}, status=400)

    # image = util.ImageHandler.convert2grey(image)
    image = util.ImageHandler.resize_img(image)
    image = util.ImageHandler.img_blurer(image)

    # start = time.time()
    text = util.TextHandler.text_extractor(reader, image)
    # print(text)
    
    scand_r = scan_reader.ScanCardReader()
    scand_r.extract_entities(text)
    # print(start - time.time())
    return Response(scand_r.to_json())


@api_view(['GET'])
def info(request):
    data = {
        'name': 'abdulaziz',
        'id': 25
    }
    return Response(JSONRenderer().render(data))