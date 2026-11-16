from django.db import models

# Create your models here.
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Armazenará código HTML
    post_date = models.DateTimeField(auto_now_add=True)  # Campo DateTimeField

    def __str__(self):
        return self.title