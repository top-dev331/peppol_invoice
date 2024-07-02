from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class MyProfile(models.Model):
    company_name = models.CharField(max_length=255, default='Default Company')
    address = models.CharField(max_length=255, default='123 Default St')
    postcode = models.CharField(max_length=20, default='00000')
    city = models.CharField(max_length=100, default='Default City')
    coc_number = models.CharField(max_length=50, default='00000000')  # Chamber of Commerce Number
    iban = models.CharField(max_length=34, default='DE89370400440532013000')
    peppol_sender_id = models.CharField(max_length=50, default='1234567890')
    first_name = models.CharField(max_length=50, default='John')
    last_name = models.CharField(max_length=50, default='Doe')
    email_address = models.EmailField(default='john.doe@example.com')

    def __str__(self):
        return self.company_name


class CustomerInfo(models.Model):
    company_name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    postcode = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=100, default='')
    peppol_receiver_id = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.company_name