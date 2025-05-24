from django.urls import include, path

urlpatterns = [
    path("auth/", include("sleektiv_api.api_urls.auth.urls")),
    path("asset/", include("sleektiv_api.api_urls.asset.urls")),
    path("base/", include("sleektiv_api.api_urls.base.urls")),
    path("employee/", include("sleektiv_api.api_urls.employee.urls")),
    path("notifications/", include("sleektiv_api.api_urls.notifications.urls")),
    path("payroll/", include("sleektiv_api.api_urls.payroll.urls")),
    path("attendance/", include("sleektiv_api.api_urls.attendance.urls")),
    path("leave/", include("sleektiv_api.api_urls.leave.urls")),
]
