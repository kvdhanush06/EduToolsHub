from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import HomeWork, Notes, Todo


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "description"]


class DateInput(forms.DateInput):
    input_type = "date"


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        widgets = {"due": DateInput()}
        fields = ["subject", "title", "description", "due", "is_finished"]


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=200, label="Enter Your Search:", required=False)

    def clean_text(self):
        value = self.cleaned_data.get("text", "") or ""
        return value.strip()


class ToDoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "is_finished"]


class ConversionForm(forms.Form):
    CHOICES = [("length", "Length"), ("mass", "Mass")]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversationLengthForm(forms.Form):
    CHOICES = [("yard", "Yard"), ("foot", "Foot")]
    input = forms.IntegerField(
        required=False,
        label=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Enter the number"}),
    )
    measure1 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))


class ConversationMassForm(forms.Form):
    CHOICES = [("pound", "Pound"), ("kilogram", "Kilogram")]
    input = forms.IntegerField(
        required=False,
        label=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Enter the number"}),
    )
    measure1 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
