import io

import boto3
from PIL import Image, ImageDraw


class AmazonRekognition(object):
    def __init__(self, region: str = 'ap-northeast-1'):
        self.client = boto3.client('rekognition', region)

    def detect_labels(self, image_bytes):
        """Returns detected labels in an image using Amazon Rekognition"""
        response = self.client.detect_labels(Image={'Bytes': image_bytes})
        return response.get('Labels')

    @staticmethod
    def find_target_label(labels, target_label_name, target_confidence):
        """Returns a label with a specific name and high confidence from a list"""
        for label in labels:
            if label.get('Name') == target_label_name and \
                    label.get('Confidence') > target_confidence:
                print("Found " + target_label_name + " in the image")
                return label
        print("There was no " + target_label_name + " in the image")
        return

    @staticmethod
    def display_bounding_boxes(image_bytes, label):
        """Returns a image with bounding boxes using detected label"""
        image = Image.open(io.BytesIO(image_bytes))
        imgWidth, imgHeight = image.size
        draw = ImageDraw.Draw(image)
        for instance in label.get('Instances'):
            box = instance.get("BoundingBox")
            left = imgWidth * box.get('Left')
            top = imgHeight * box.get('Top')
            width = imgWidth * box.get('Width')
            height = imgHeight * box.get('Height')
            points = (
                (left, top),
                (left + width, top),
                (left + width, top + height),
                (left, top + height),
                (left, top)

            )
            draw.line(points, fill='#00d400', width=2)
        image_with_boxes_jpg = io.BytesIO()
        image.save(image_with_boxes_jpg, format='JPEG')
        image_with_boxes_bytes = image_with_boxes_jpg.getvalue()

        return image_with_boxes_bytes
