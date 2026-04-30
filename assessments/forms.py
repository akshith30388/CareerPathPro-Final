from django import forms
from .models import AssessmentQuestion


class AssessmentAnswerForm(forms.Form):
    """Dynamic form for assessment MCQ answers."""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                choices = [
                    ('a', q.option_a),
                    ('b', q.option_b),
                    ('c', q.option_c),
                    ('d', q.option_d),
                ]
                self.fields[f'question_{q.id}'] = forms.ChoiceField(
                    label=q.question_text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=True,
                )

