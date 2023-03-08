from django import forms
from django.core.validators import RegexValidator

from forum.models import Question, Answer

tagsValidator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Tags should contain letters")


class NewQuestionForm(forms.ModelForm):
    tags = forms.CharField(validators=[tagsValidator])

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')


class AnswerForm(forms.Form):
    text = forms.CharField()

    class Meta:
        model = Answer
        fields = ('title', 'text')


