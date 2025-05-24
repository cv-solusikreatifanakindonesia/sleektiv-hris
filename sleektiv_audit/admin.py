"""
admin.py
"""

from django.contrib import admin

from sleektiv_audit.models import AuditTag, HorillaAuditInfo, HorillaAuditLog

# Register your models here.

admin.site.register(AuditTag)
