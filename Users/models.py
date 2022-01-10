import json

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question = models.CharField(max_length=200, null=False)
    answer_1 = models.TextField(default="")
    answer_2 = models.TextField(default="")
    answer_3 = models.TextField(default="")
    answer_4 = models.TextField(default="")
    correct_answer = models.TextField(default="")
    theme = models.CharField(max_length=200, null=False, default="")

    def set_possible_answers(self, answers):
        self.possible_answers = json.dumps(answers)

    def get_possible_asnwers(self):
        return json.loads(self.possible_answers)


class Level(models.Model):
    repetition = models.PositiveSmallIntegerField()
    questions = models.ManyToManyField(Question)


class ExtendedUser(models.Model):
    STUDENT = 1
    TEACHER = 2
    ROLE = (
        (STUDENT, "Student"), (TEACHER, "Teacher")
    )

    rel = models.OneToOneField(User, on_delete=models.CASCADE, related_name="related_user")
    user_role = models.PositiveSmallIntegerField(choices=ROLE, blank=False)
    levels = models.ManyToManyField(Level, default=None)
