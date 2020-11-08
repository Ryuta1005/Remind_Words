from django.urls import path
from django.conf.urls import url
from .views import Index
from .views import Addition
from .views import WordList
from .views import RemindList
from .views import Details
from . import views


urlpatterns = [
    path(r'', Index.as_view(), name='index'),
    path(r'addition', Addition.as_view(), name='addition'),
    path(r'word_list', WordList.as_view(), name='word_list'),
    path(r'remind_list', RemindList.as_view(), name='remind_list'),
    path("details/<int:num>/",Details.as_view(),name="details"),
]