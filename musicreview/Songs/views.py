# Standard library imports
from urllib.parse import urlencode, urljoin
import json
import requests

# Django imports
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView, DetailView, DeleteView, CreateView, UpdateView, FormView, TemplateView
)

# Local imports from the current application
from .models import Song, SongRating
from .forms import SongRatingForm, EditReviewForm


class SongListView(ListView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs = Song.objects.values('id', 'spotify_song_id')

        # Enhance song data with user's review status if the user is logged in
        if self.request.user.is_authenticated:
            enhanced_songs = []
            for song in songs:
                song_id = song['id']
                user_has_reviewed = SongRating.objects.filter(Song_id=song_id, creator=self.request.user).exists()
                enhanced_song = song.copy()
                enhanced_song['user_has_reviewed'] = str(user_has_reviewed)
                enhanced_songs.append(enhanced_song)

            #associate the average rating with each song
            for song in enhanced_songs:
                song_id = song['id']
                song_obj = Song.objects.get(id=song_id)
                song['average_rating'] = song_obj.average_rating()

            context['songs'] = enhanced_songs
        else:
            songs = Song.objects.values('id', 'spotify_song_id')
            songs = list(songs)
            #associate the average rating with each song
            for song in songs:
                song_id = song['id']
                song_obj = Song.objects.get(id=song_id)
                song['average_rating'] = song_obj.average_rating()
            context['songs'] = list(songs)
        return context


class SongDetailView(DetailView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add the Spotify song ID to the context
        spotify_song_id = self.object.spotify_song_id
        context['spotify_song_id'] = spotify_song_id


        return context
    
class ReviewView(LoginRequiredMixin, FormView):
    template_name = 'songs/song_rate_view.html'
    form_class = SongRatingForm

    def form_valid(self, form):
        song_rating = form.save(commit=False)
        song_rating.creator = self.request.user
        song_id = self.kwargs.get('pk')
        song_rating.Song = Song.objects.get(pk=song_id)
        song_rating.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect after a successful submission
        return reverse('Songs:detail', kwargs={'pk': self.kwargs['pk']})

class EditReviewView(LoginRequiredMixin, UpdateView):
    model = SongRating
    template_name = 'songs/song_rate_view.html'
    form_class = EditReviewForm

    def get_success_url(self):
        # Redirect after a successful submission
        return reverse('Songs:detail', kwargs={'pk': self.object.Song_id})

    def get_object(self, queryset=None):
        # Only get the SongRating object for the current user and song
        # if multiple (shouldn't be but just in case) then get the first one
        obj = SongRating.objects.filter(Song_id=self.kwargs['pk'], creator=self.request.user).first()
        return obj
    
    #context for auto populating the form rating and comment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating'] = self.object.rating
        context['comment'] = self.object.comment
        return context
    
class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = SongRating
    template_name = 'songs/song_delete_review.html'

    def get_success_url(self):
        # Redirect after a successful submission
        return reverse('Songs:detail', kwargs={'pk': self.object.Song_id})

    def get_object(self, queryset=None):
        # Only get the SongRating object for the current user and song
        # if multiple (shouldn't be but just in case) then get the first one
        obj = SongRating.objects.filter(Song_id=self.kwargs['pk'], creator=self.request.user).first()
        return obj
    
def delete_review(request, pk):
    review = SongRating.objects.get(id=pk)
    if request.method == "POST":
        review.delete()
        return redirect('Songs:detail', pk=review.Song_id)
    context = {'review': review}
    return render(request, 'songs/song_delete_review.html', context)

class SongDeleteView(UserPassesTestMixin, DeleteView):
    model = Song
    success_url = reverse_lazy('Songs:list')

    def test_func(self):
        return self.request.user.is_superuser

class SongCreateView(CreateView):
    model = Song
    fields = ['spotify_song_id']
    template_name = 'Songs/Song_create_view.html'
    success_url = reverse_lazy('Songs:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spotify_access_token'] = self.request.session.get('spotify_access_token', '')
        return context

def song_reviews(request, pk):
    reviews_query = SongRating.objects.filter(Song_id=pk).values(
        'id', 'rating', 'comment', 'creator__username', 'Song'
    )

    reviews = list(reviews_query)
    if request.user.is_authenticated:
        user_review = next((r for r in reviews if r['creator__username'] == request.user.username), None)
        if user_review:
            reviews.remove(user_review)
            reviews.insert(0, user_review)

    return JsonResponse(reviews, safe=False)

def user_reviews(request, pk):
    reviews_query = SongRating.objects.filter(creator_id=pk).values(
        'id', 'rating', 'comment', 'creator__username', 'Song'
    )

    reviews = list(reviews_query)
    if request.user.is_authenticated:
        user_review = next((r for r in reviews if r['creator__username'] == request.user.username), None)
        if user_review:
            reviews.remove(user_review)
            reviews.insert(0, user_review)

    return JsonResponse(reviews, safe=False)

def get_spotify_song_id(request, pk):
    song = Song.objects.get(id=pk)
    spotify_song_id = song.spotify_song_id
    return JsonResponse({'spotify_song_id': spotify_song_id})

def spotify_auth_redirect(request):
    next_url = request.GET.get('next', settings.DEFAULT_RETURN_URL)
    #prepend "Songs:" to the next_url
    next_url = "Songs:" + next_url
    full_next_url = request.build_absolute_uri(reverse(next_url))

    params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'scope': 'user-read-private',
        'state': next_url,  # Use state parameter to pass the next_url
    }
    url = f'https://accounts.spotify.com/authorize?{urlencode(params)}'
    return redirect(url)

def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    next_url = request.GET.get('state', settings.DEFAULT_RETURN_URL)
    #next_url = "Songs:" + next_url

    if error:
        # Handle the scenario where the user denied the request or some other error occurred.
        return HttpResponseRedirect(reverse('error_view_name'))  # Redirect to an error page or similar.

    if code:
        # Exchange the code for an access token
        response = requests.post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        })

        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            # Optionally handle refresh_token and save them for later use.
            request.session['spotify_access_token'] = access_token  # Save the access token in the session or user's profile

            # Ensure the next_url is safe to redirect to
            #if not is_safe_url(url=next_url, allowed_hosts={request.get_host()}):
            #    return HttpResponseRedirect(reverse('Songs:list'))  # Redirect to a safe default page

            return HttpResponseRedirect(reverse(next_url))
        else:
            # Handle failure in obtaining an access token.
            return HttpResponseRedirect(reverse('error_view_name'))  # Redirect to an error page or similar.

    # Handle scenarios where there's neither code nor error.
    return HttpResponseRedirect(reverse('default_view_name'))  # Redirect to a default page or an error page.

@csrf_exempt  # Consider using CSRF protection for production
@require_POST
def save_song(request):
    data = json.loads(request.body)
    spotify_song_id = data.get('spotify_song_id')

    if spotify_song_id:
        # Create and save the new song
        song = Song(spotify_song_id=spotify_song_id)
        song.save()
        return JsonResponse({'status': 'success', 'message': 'Song added successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)





