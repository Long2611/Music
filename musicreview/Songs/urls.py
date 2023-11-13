from django.urls import path
from . import views

app_name = "Songs"
urlpatterns = [
    path(
        route='',
        view=views.SongListView.as_view(),
        name='list'
    ),
    path(
        route='create/',
        view=views.SongCreateView.as_view(),
        name='create'
    ),
    path(
        route='<slug:slug>/',
        view=views.SongDetailView.as_view(),
        name='detail'
    ),
    path(
        route='<slug:slug>/delete/',
        view=views.SongDeleteView.as_view(),
        name='delete'
    ),
    path(
        route='<slug:slug>/update/',
        view=views.SongUpdateView.as_view(),
        name='update'
    ),
    path(
        route='<slug:slug>/rate/',
        view=views.SongRateView.as_view(),
        name='rate'
    ),
]