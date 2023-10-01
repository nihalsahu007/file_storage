from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    random_string = models.CharField(max_length=50, blank=True, null=True)

class Storage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to ='file', 
                            validators=[FileExtensionValidator(allowed_extensions=[
                                'pptx', 'docx', 'xlsx'])])