from django.db import models


class Face(models.Model):
    name = models.CharField(max_length=100)

class FaceRecognitionResult(models.Model):
    time = models.DateTimeField()
    student_attend = models.ManyToManyField(Face)
