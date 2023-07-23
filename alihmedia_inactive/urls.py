from django.urls import path
from .views import irigasi, pdfdownload, airbaku, sungai, pantai, keuangan

urlpatterns = [
    path(route='irigasi', view=irigasi, name="irigasi"),
    path(route='airbaku', view=airbaku, name="airbaku"),
    path(route='pantai', view=pantai, name="pantai"),
    path(route='sungai', view=sungai, name="sungai"),
    path(route='keuangan', view=keuangan, name="keuangan"),
    path(route='pdfdownload/<str:link>/<str:doc_id>', view=pdfdownload, name='pdfdownload')



]