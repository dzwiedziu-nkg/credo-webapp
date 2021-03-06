from __future__ import unicode_literals

from datetime import datetime

from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(min_length=3, max_length=50)
    display_name = forms.CharField(min_length=3, max_length=50)
    team = forms.CharField(max_length=50)
    password = forms.CharField(
        min_length=6, max_length=128, widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        min_length=6, max_length=128, widget=forms.PasswordInput()
    )
    accept_rules = forms.BooleanField()

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        if not (cleaned_data.get("password") == cleaned_data.get("confirm_password")):
            self.add_error("confirm_password", "Passwords do not match")
        if not cleaned_data.get("accept_rules"):
            self.add_error("accept_rules", "Please accept the rules")


class ContestCreationForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=200, label="Contest name")
    description = forms.CharField(
        max_length=1000, label="Contest description", widget=forms.Textarea
    )
    start_time = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], initial=datetime.now()
    )
    duration = forms.IntegerField(
        min_value=1, max_value=24 * 7, initial=24, label="Duration (h)"
    )
    limit = forms.IntegerField(
        min_value=0,
        max_value=1000,
        initial=20,
        label="Limit of recent detections displayed",
    )
    blacklist = forms.CharField(
        max_length=500,
        required=False,
        label="Comma separated list of usernames to ignore",
    )
    avbrightness_max = forms.FloatField(
        min_value=0,
        max_value=1,
        initial=0.01,
        label="Average brightness",
        label_suffix=" <",
    )
    maxbrightness_min = forms.IntegerField(
        min_value=0,
        max_value=255,
        initial=120,
        label="Maximum single pixel brightness",
        label_suffix=" >",
    )
