from django import forms
from .models import Quiz

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz', None)
        super().__init__(*args, **kwargs)
        if quiz:
            self.fields['answer'] = forms.ChoiceField(
                label=quiz.question,
                choices=[(ans, ans) for ans in quiz.get_shuffled_answers()],
                widget=forms.RadioSelect
            )
