from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "helpdesk"

    def ready(self):
        from django.urls import include, path

        from sleektiv.sleektiv_settings import APPS
        from sleektiv.urls import urlpatterns

        APPS.append("helpdesk")
        urlpatterns.append(
            path("helpdesk/", include("helpdesk.urls")),
        )
        super().ready()
