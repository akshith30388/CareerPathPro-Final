from django import forms
from .models import Appointment, Feedback
from users.models import CustomUser
import datetime


class BookAppointmentForm(forms.ModelForm):
    """Form for booking an appointment."""
    class Meta:
        model = Appointment
        fields = ['counselor', 'date', 'time_slot', 'notes']
        widgets = {
            'counselor': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any specific topics you want to discuss...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['counselor'].queryset = CustomUser.objects.filter(role='counselor')
        self.fields['counselor'].label_from_instance = lambda obj: f"{obj.get_full_name() or obj.username}"
        # Set minimum date to today
        self.fields['date'].widget.attrs['min'] = datetime.date.today().isoformat()

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError('Appointment date cannot be in the past.')
        return date


class FeedbackForm(forms.ModelForm):
    """Feedback form after completed appointment."""
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Share your experience with this counseling session...'}),
        }

