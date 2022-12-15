from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class GenreListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView GenreListCreateView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def post(self, request):
        try:
            response = super(GenreListCreateView, self).post(request)
            return Response(response.data, HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)


class TrackListView(generics.ListAPIView):
    """
    ListAPIView TrackListView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = [
        SearchFilter
    ]
    search_fields = [
        '$title',
    ]
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class TrackListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView TrackListCreateView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = [
        SearchFilter
    ]
    search_fields = [
        '$name',
    ]
    serializer_class = TrackSerializer
    queryset = Track.objects.all()

    def post(self, request):
        try:
            response = super(TrackListCreateView, self).post(request)
            return Response(response.data, HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)


class TrackDetailView(generics.RetrieveAPIView):
    """
    RetrieveAPIView TrackDetailView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_url_kwarg = 'id'
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class AlbumListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView AlbumListCreateView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    def post(self, request):
        try:
            response = super(AlbumListCreateView, self).post(request)
            return Response(response.data, HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)


class AlbumDetailView(generics.RetrieveAPIView):
    """
    RetrieveAPIView AlbumDetailView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_url_kwarg = 'id'
    serializer_class = AlbumDetailSerializer
    queryset = Album.objects.all()


class AlbumFanCreateView(APIView):
    """
    APIView AlbumFanCreateView
    """
    def post(self, request, id):
        user = request.user
        artist = self.kwargs.get('id')
        try:
            data_send = AlbumFan.objects.get_or_create(user=user, artist_id=artist)
            return Response(status=HTTP_200_OK, data={"message": "New fan registered"})
        except:
            return Response(status=HTTP_400_BAD_REQUEST, data={"message": "Could not add new fan"})


class ArtistListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView ArtistListCreateView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

    def post(self, request):
        try:
            response = super(ArtistListCreateView, self).post(request)
            return Response(response.data, HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)


class ArtistDetailView(generics.RetrieveAPIView):
    """
    RetrieveAPIView ArtistDetailView
    """
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_url_kwarg = 'id'
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()


class ArtistFanCreateView(APIView):
    """
    APIView ArtistFanCreateView
    """
    def post(self, request, id):
        user = request.user
        artist = self.kwargs.get('id')
        try:
            data_send = ArtistFan.objects.get_or_create(user=user, artist_id=artist)
            return Response(status=HTTP_200_OK, data={"message": "New fan registered"})
        except:
            return Response(status=HTTP_400_BAD_REQUEST, data={"message": "Could not add new fan"})