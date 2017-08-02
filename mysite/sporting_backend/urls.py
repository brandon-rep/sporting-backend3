"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from sporting_backend.views import (
    profile_leaderboard,
    district_leaderboard,
    sign_up,
    personal_info,
    who_is_my
)

urlpatterns = [
    url(r'^profile_leaderboard/', profile_leaderboard),
    url(r'^district-leaderboard/', district_leaderboard),
    url(r'^sign-up/', sign_up),
    url(r'^personal-info/', personal_info),
    url(r'^who_is_my/', who_is_my),
]
