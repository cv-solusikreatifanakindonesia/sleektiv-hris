from django.apps import AppConfig


class BackupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sleektiv_backup"

    def ready(self):
        from django.urls import include, path

        from sleektiv.urls import urlpatterns

        urlpatterns.append(
            path("backup/", include("sleektiv_backup.urls")),
        )
        super().ready()
