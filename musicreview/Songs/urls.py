from django.urls import path
from . import views

app_name = "Songs"
urlpatterns = [
    path('spotify-auth-redirect/', views.spotify_auth_redirect, name='spotify-auth-redirect'),
    path('spotify-callback/', views.spotify_callback, name='spotify-callback'),
    path('save/', views.save_song, name='save'),
    path('review/<int:pk>', views.ReviewView.as_view(), name='song-review'),
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
        route='detail/<int:pk>/',
        view=views.SongDetailView.as_view(),
        name='detail'
    ),
    path(
        route='delete/<int:pk>/',
        view=views.SongDeleteView.as_view(),
        name='delete'
    ),
    path('api/<int:pk>/reviews/', views.song_reviews, name='song-reviews'),
    #edit review
    path('edit-review/<int:pk>', views.EditReviewView.as_view(), name='edit-review'),
    #confirm delete review
    path('delete-review/<int:pk>', views.DeleteReviewView.as_view(), name='delete-review'),
    #delete review
    path('delete-review/confirmed/<int:pk>', views.delete_review, name='delete-review-confirmed'),

]