"""
sleektiv_automations/filters.py
"""

from sleektiv.filters import SleektivFilterSet, django_filters
from sleektiv_automations.models import MailAutomation


class AutomationFilter(SleektivFilterSet):
    """
    AutomationFilter
    """

    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = MailAutomation
        fields = "__all__"
