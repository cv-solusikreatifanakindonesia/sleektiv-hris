from django.apps import AppConfig


class SleektivApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sleektiv_api"

    def ready(self):
        from django.urls import include, path

        from sleektiv.urls import urlpatterns

        urlpatterns.append(
            path("api/", include("sleektiv_api.urls")),
        )
        super().ready()
