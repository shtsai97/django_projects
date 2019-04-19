from django import forms
from cats.models import Cat
from django.core.files.uploadedfile import InMemoryUploadedFile
from cats.humanize import naturalsize

from django.core.exceptions import ValidationError
from django.core import validators

# https://docs.djangoproject.com/en/2.1/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/2.1/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other

# Create the form class.
class CreateForm(forms.ModelForm):

    class Meta:
        model = Cat
        fields = ['name', 'foods', 'weight']  # Picture is manual


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
