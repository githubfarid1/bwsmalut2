from django.urls import path
from .views import irigasi, pdfdownload, air_baku, sungai, pantai, keuangan, statistics
#tes2, tes1

urlpatterns = [
    path(route='irigasi', view=irigasi, name="irigasi"),
    path(route='air_baku', view=air_baku, name="air_baku"),
    path(route='pantai', view=pantai, name="pantai"),
    path(route='sungai', view=sungai, name="sungai"),
    path(route='keuangan', view=keuangan, name="keuangan"),
    path(route='pdfdownload/<str:link>/<str:doc_id>', view=pdfdownload, name='pdfdownload'),
    path(route='statistics', view=statistics, name="statistics"),
    # path(route='tes1', view=tes1, name="tes1"),
    # path(route='tes2', view=tes2, name="tes2"),




]