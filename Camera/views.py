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
