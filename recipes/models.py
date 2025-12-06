from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from tag.models import Tag
from django.conf import settings
import os
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True, blank=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    @staticmethod
    def resize_image_before_save(image_file, new_width=840):
        image = Image.open(image_file)
        original_width, original_height = image.size

        if original_width <= new_width:
            return image_file

        new_height = round((new_width * original_height) / original_width)
        resized = image.resize((new_width, new_height), Image.LANCZOS)

        buffer = BytesIO()
        resized.save(buffer, format=image.format, optimize=True, quality=50)
        buffer.seek(0)

        return ContentFile(buffer.read(), name=image_file.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}"
        
        if self.cover:
            self.cover = self.resize_image_before_save(self.cover, 1254)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=[self.slug])
