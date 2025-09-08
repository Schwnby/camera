
import os
import sys

from django.conf import settings

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

ALLOWED_HOSTS = ['*']

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY=SECRET_KEY,
        ALLOWED_HOSTS=ALLOWED_HOSTS,
        ROOT_URLCONF=__name__,
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
    )

format = 'JPG'
content_type = 'image/jpg'

from django.http import HttpResponse
from picamera2 import Picamera2
from PIL import Image
import io
import cv2
import json

def take_picture():
    picam2 = Picamera2()

    picam2.set_controls({"ExposureTime": 500})
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.start()

    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite('test.png', frame)

    picam2.stop()
    picam2.close()

    return frame

def index(request):
    frame = take_picture()

    image = Image.fromarray(frame)
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type=content_type)


from django.urls import path

urlpatterns = [
    path('', index),
]


from django.core.wsgi import get_wsgi_application

def configure():
    image = take_picture()

    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(image)

    if bbox is not None:
        global format
        global content_type
        print(f"data: {data}")
        parsed = json.loads(data)
        format = parsed["format"]
        content_type = parsed["content_type"]
    else:
        print("No QR code found")

configure()
application = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
