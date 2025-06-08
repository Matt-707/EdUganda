from django import forms

TOPIC_CHOICES =[
    ('mechanics', 'Mechanics'),
    ('optic','Optics'),
    ('electricity', 'Electricity'),
]

DIFFICULTY_CHOICES = [
    ('easy','Easy'),
    ('medium','Medium'),
    ('hard','Hard'),
    ('balanced','Balanced'),
]

class PaperGenerationForm(forms.Form):
    topics = forms.MultipleChoiceField(
        choices=TOPIC_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Select Topics"
    )
    difficulty=forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.RadioSelect,
        label="Select Difficulty",
        required=True,
    )