from django.db import models
from django.contrib.auth.models import User

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date = models.DateTimeField()
    duration_minutes = models.IntegerField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"
class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Sınav Adı (Örn: Kalkülüs Vize)
    date = models.DateTimeField() # Sınav Tarihi ve Saati

    def __str__(self):
        return self.name