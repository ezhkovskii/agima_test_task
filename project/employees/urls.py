from django.urls import path, include
from employees.routers import router


urlpatterns = [
    path('', include(router.urls)),
]
