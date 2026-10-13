from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name