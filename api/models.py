from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    date=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    options=(
        ("published","published"),
        ("unpublished","unpublished"),       
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="unpublished")
    options=(
        ("like","like"),
        ("dislike","dislike"),
    )
    like=models.CharField(max_length=200,choices=options,default="order-placed")

    def __str__(self):
        return self.title
