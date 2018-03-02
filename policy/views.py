from django.shortcuts import render, HttpResponse
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit

# Create your views here.

def policy(request):
    return render(request, 'login/policy.html')