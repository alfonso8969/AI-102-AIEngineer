import os
import sys
import time
from array import array

import numpy as np
# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import \
    VisualFeatureTypes
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw


def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Computer Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Analyze image
        AnalyzeImage(image_file)

        # Generate thumbnail
        GetThumbnail(image_file)

    except Exception as ex:
        print(ex)


def AnalyzeImage(image_file):
    print('Analyzing', image_file)

    # Specify features to be retrieved
    features: list[VisualFeatureTypes] = [VisualFeatureTypes.description,
                                          VisualFeatureTypes.tags,
                                          VisualFeatureTypes.categories,
                                          VisualFeatureTypes.brands,
                                          VisualFeatureTypes.objects,
                                          VisualFeatureTypes.adult]

    # Get image analysis
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data, features)

        # Get image description
        for caption in analysis.description.captions:
            print("Description: '{}' (confidence: {:.2f}%)".format(
                caption.text, caption.confidence * 100))


def GetThumbnail(image_file):
    print('Generating thumbnail')

    # Generate a thumbnail


if __name__ == "__main__":
    main()
