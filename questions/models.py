from django.db import models

# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    subtopic = models.CharField(max_length=100, blank=True)
    question_text = models.TextField()
    answer_text = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[
        ('Easy','Easy'),
        ('Medium', 'Medium'),
        ('Hard','Hard'),
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.subject} - {self.topic}: {self.question_text[:50]}..."

