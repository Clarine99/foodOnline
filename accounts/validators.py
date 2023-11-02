from django.core.exceptions import ValidationError
import os

def allow_only_images_validator (value):
    ext = os.path.splitext (value.name)[1]
    print(ext)

    valid_ext = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_ext :
        raise ValidationError('Unsupported file extension. Allowed '+ str(valid_ext))


