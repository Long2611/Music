from django.shortcuts import render

from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, FormView
from .models import Song, SongRating
from django.urls import reverse_lazy
#import login required mixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
#import forms
from django import forms

class SongListView(ListView):
    model = Song

    # add context so we can show average rating for each Song using the @property average_rating
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Songs'] = Song.objects.all()
        return context

class SongDetailView(DetailView):
    model = Song

class SongDeleteView(DeleteView):
    model = Song
    success_url = reverse_lazy('Songs:list')

class SongCreateView(CreateView):
    model = Song
    # use custom template
    template_name = 'Songs/Song_create_view.html'
    success_url = reverse_lazy('Songs:list')

class SongUpdateView(UpdateView):
    model = Song
    template_name = 'Songs/Song_update_view.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('Songs:list')



class SongRateView(LoginRequiredMixin, FormView):
    template_name = 'Songs/Song_rate_view.html'
    success_url = reverse_lazy('Songs:list')
    



