from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ExtendedUser, Question


# Create your forms here.
class NewQuestionForm(forms.Form):
    class Meta:
        model = Question
        fields = ('question', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct_answer')

    def save(self, commit=True):
        question = super(NewQuestionForm, self).save(commit=False)
        if commit:
            question.save()
        return question

    def clean(self):
        cleaned_data = super(NewQuestionForm, self).clean()
        # do your custom validations / transformations here
        # and some more


class NewUserForm(UserCreationForm):
    class Meta:
        model = ExtendedUser
        fields = ("user_role", "rel")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
