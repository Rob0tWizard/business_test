from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render, redirect

from .models import Report


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['user', 'address', 'revenue']

    helper = FormHelper()
    helper.layout = Layout(
        Fieldset('Ежедневный отчет',
                 'user',
                 'address',
                 'revenue',
                 ),
        Submit('submit', 'Сохранить'),
    )

    def clean_revenue(self):
        revenue = self.cleaned_data['revenue']
        if not revenue:
            raise ValidationError('Введите выручку')
        try:
            float(revenue)
        except ValueError:
            raise ValidationError('Выручка должна быть числом')



