from django import forms
from django.forms import DateInput, NumberInput, ClearableFileInput, HiddenInput
from ideas.models import Idea
import datetime
from decimal import Decimal

class IdeaForm(forms.ModelForm):
    dynamic_fields = []

    class Meta:
        model = Idea
        fields = ['title', 'description', 'program', 'prototype_file', 'related_image']

    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)

        self.dynamic_fields = []

        if program:
            self.fields['program'].initial = program.id
            self.fields['program'].widget = HiddenInput()

            # Agregar campos personalizados definidos en `form_config`
            if program.form_config:
                extra_fields = program.form_config.get("extra_fields", [])
                for field_def in extra_fields:
                    field_name = field_def['name']
                    field_type = field_def.get('type', 'text')
                    required = field_def.get('required', False)
                    label = field_def.get('label', field_name.capitalize())

                    if field_type == 'number':
                        self.fields[field_name] = forms.DecimalField(
                            required=required, label=label, widget=NumberInput()
                        )
                    elif field_type == 'date':
                        self.fields[field_name] = forms.DateField(
                            required=required, label=label, widget=DateInput(attrs={'type': 'date'})
                        )
                    elif field_type == 'file':
                        self.fields[field_name] = forms.FileField(
                            required=required, label=label, widget=ClearableFileInput()
                        )
                    elif field_type == 'image':
                        self.fields[field_name] = forms.ImageField(
                            required=required, label=label
                        )
                    else:
                        self.fields[field_name] = forms.CharField(
                            required=required, label=label
                        )
                    self.dynamic_fields.append(self[field_name])

    def save(self, commit=True):
        instance = super().save(commit=False)

        dynamic_fields = {
            key: self.cleaned_data[key]
            for key in self.cleaned_data
            if key not in self.Meta.fields
        }

        def make_json_serializable(value):
            if isinstance(value, Decimal):
                return float(value)
            if isinstance(value, (datetime.date, datetime.datetime)):
                return value.isoformat()
            return value

        serialized_data = {key: make_json_serializable(value) for key, value in dynamic_fields.items()}
        instance.extra_data = serialized_data

        if commit:
            instance.save()

        return instance

class IdeaReviewForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['coordinator_review_comments', 'state']
        widgets = {
            'coordinator_review_comments': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'coordinator_review_comments': 'Comentarios del Coordinador',
            'state': 'Estado',
        }