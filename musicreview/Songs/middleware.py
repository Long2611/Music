import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urljoin

class SpotifyAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the access token is expired
        # exclude spotify auth urls
        if request.path.startswith('/Songs/spotify-auth-redirect/'):
            return self.get_response(request)
        
        # also exclude the callback
        if request.path.startswith('/Songs/spotify-callback/'):
            return self.get_response(request)
        print('middleware')
        access_token = request.session.get('spotify_access_token')
        if access_token:
            response = requests.get('https://api.spotify.com/v1/me', headers={
                'Authorization': f'Bearer {access_token}'
            })

            if response.status_code == 401 or response.status_code == 400:
                # Token has expired, re-authenticate
                return HttpResponseRedirect(urljoin(reverse('Songs:spotify-auth-redirect'), f'?next=list'))
        else:
            return HttpResponseRedirect(urljoin(reverse('Songs:spotify-auth-redirect'), f'?next=list'))

        return self.get_response(request)