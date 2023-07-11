import os
import time
import requests

from amazon_rekognition import AmazonRekognition
from line_notify import LineNotify
import soracam

SORACOM_AUTH_KEY_ID = os.environ.get("SORACOM_AUTH_KEY_ID")
SORACOM_AUTH_KEY = os.environ.get("SORACOM_AUTH_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
EVENT_RETRIEVE_INTERVAL_SEC = os.environ.get("EVENT_RETRIEVE_INTERVAL_SEC")

REKOGNITION_REGION = os.environ.get("REKOGNITION_REGION")
TARGET_LABEL_NAME = os.environ.get("TARGET_LABEL_NAME")
TARGET_CONFIDENCE = int(os.environ.get("TARGET_CONFIDENCE"))

LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

REQUESTS_TIMEOUT = 5


def lambda_handler(event, context):
    if all([SORACOM_AUTH_KEY_ID, SORACOM_AUTH_KEY,
            DEVICE_ID, EVENT_RETRIEVE_INTERVAL_SEC,
            REKOGNITION_REGION, TARGET_LABEL_NAME,
            TARGET_CONFIDENCE, LINE_NOTIFY_TOKEN]) is False:
        raise Exception("You didn't set some environment variables")

    print("Begin listing events and download images.")
    image_urls = get_image_urls(DEVICE_ID)

    if image_urls is None:
        print("No event images.")
        return

    rekognition = AmazonRekognition(
        region=REKOGNITION_REGION)
    line_notify = LineNotify(LINE_NOTIFY_TOKEN)

    for image_url in image_urls:
        exported_image_bytes = download_image(image_url)
        print("Image downloaded. Detect labels.")
        labels = rekognition.detect_labels(
            image_bytes=exported_image_bytes)
        print("label list: " + str(labels))
        target_label = AmazonRekognition.find_target_label(
            labels=labels,
            target_label_name=TARGET_LABEL_NAME,
            target_confidence=TARGET_CONFIDENCE)

        if not target_label:
            print("There was no label with target name in the image.")
            continue

        if target_label.get('Instances') == []:
            notification_image_bytes = exported_image_bytes
        else:
            notification_image_bytes = AmazonRekognition.display_bounding_boxes(
                image_bytes=exported_image_bytes, label=target_label)

        print("Notify to LINE.")
        message_text = 'Found ' + TARGET_LABEL_NAME.lower() + ' in the image.'
        line_notify.notify_to_line_with_image(
            message=message_text,
            image_bytes=notification_image_bytes)
    return


def get_image_urls(device_id):
    soracam_api_client = soracam.SoraCamClient(
        coverage_type='jp',
        auth_key_id=SORACOM_AUTH_KEY_ID,
        auth_key=SORACOM_AUTH_KEY)

    current_unix_time_ms = int(time.time() * 1000)
    event_retrieve_interval_sec = int(EVENT_RETRIEVE_INTERVAL_SEC)
    delta_ms = event_retrieve_interval_sec * 1000
    from_unix_time_ms = current_unix_time_ms - delta_ms

    motion_events = soracam_api_client.get_devices_events(
        device_id=device_id, from_t=from_unix_time_ms, to_t=current_unix_time_ms)

    if len(motion_events) == 0:
        print("There was no events.")
        return

    image_urls = []
    for motion_event in motion_events:
        event_detected_epoch_ms = motion_event.get("time", None)

        if event_detected_epoch_ms is None:
            print("There was event but no timestamp.")
            return

        image_url = motion_event.get('eventInfo', {}).get(
            'atomEventV1', []).get('picture', None)

        if image_url is None:
            print("There was event but no url")
            continue

        image_urls.append(image_url)

    return image_urls


def download_image(image_url):
    image_data_bytes = requests.get(
        image_url, timeout=REQUESTS_TIMEOUT).content
    return image_data_bytes
