"""
sleektiv_multi_select_field.py
This module is used to write cutom multiple select field
"""

from django import forms


class SleektivMultiSelectField(forms.ModelMultipleChoiceField):
    """
    SleektivMultiSelectField
    """
