from django import forms

TOPIC_CHOICES =[
    ('mechanics', 'Mechanics'),
    ('optic','Optics'),
    ('direct current electricity', 'Direct Current Electricity'),
    ('heat and thermodynamics', 'Heat and Thermodynamics'),
    ('waves and oscillations', 'Waves and Oscillations'),
    ('modern physics', 'Modern Physics'),
    ('electromagnetism', 'Electromagnetism'),
    ('electrostatics', 'Electrostatics'),

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