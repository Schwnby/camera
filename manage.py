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

from django.http import HttpResponse
from picamera2 import Picamera2
from PIL import Image
import io

def index(request):
    picam2 = Picamera2()

    picam2.start()

    frame = picam2.capture_array()

    picam2.close()

    image = Image.fromarray(frame)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


from django.urls import path

urlpatterns = [
    path('', index),
]


from django.core.wsgi import get_wsgi_application

def configure():
    print("Hello World!")
    
configure()
application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)
