from django.urls import path
from .views import qrcodesearch

urlpatterns = [
    path(route='qrcodesearch', view=qrcodesearch, name="qrcodesearch"),
]