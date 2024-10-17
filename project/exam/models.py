from django.db import models
from courses.models import Video
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=255)  # Поле для текста вопроса
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='questions')  # Связь с видео

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.question.question_text}'
