# -*- coding: utf-8 -*-
"""
quoations.urls module
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('genres/', GenreListCreateView.as_view()),
    path('albums/', AlbumListCreateView.as_view()),
    path('albums/<int:id>/', AlbumDetailView.as_view()),
    path('albums/<int:id>/new-fan/', AlbumFanCreateView.as_view()),
    path('artists/', ArtistListCreateView.as_view()),
    path('artists/<int:id>/', ArtistDetailView.as_view()),
    path('artists/<int:id>/new-fan/', ArtistFanCreateView.as_view()),
    path('search/', TrackListView.as_view()),
    path('tracks/', TrackListCreateView.as_view()),
    path('tracks/<int:id>/', TrackDetailView.as_view()),
]