"""
admin.py
"""

from django.contrib import admin

from sleektiv_audit.models import AuditTag, SleektivAuditInfo, SleektivAuditLog

# Register your models here.

admin.site.register(AuditTag)
