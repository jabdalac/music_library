from rest_framework import serializers
from .utils import get_file_path
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(write_only=True, required=False)
    picture_path = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        fields = '__all__'

    def get_picture_path(self,obj):
        request = self.context.get('request')
        file_path = get_file_path(request, obj.picture)
        return file_path


class ArtistSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(write_only=True, required=False)
    picture_path = serializers.SerializerMethodField()
    nb_album = serializers.IntegerField()
    nb_fan = serializers.IntegerField()
    class Meta:
        model = Artist
        fields = '__all__'
        extra_kwargs = {
            'nb_album': {'read_only': True},
            'nb_fan': {'read_only': True}
        }

    def get_picture_path(self,obj):
        request = self.context.get('request')
        file_path = get_file_path(request, obj.picture)
        return file_path


class AlbumSerializer(serializers.ModelSerializer):
    cover = serializers.FileField(write_only=True, required=False)
    cover_path = serializers.SerializerMethodField()    
    artist = ArtistSerializer(read_only=True, many=False)
    artist_id = serializers.IntegerField(write_only=True, required=True)
    nb_fan = serializers.IntegerField(required=False)
    genre_id = serializers.ListField(write_only=True, required=False)
    contributor_id = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Album
        fields = '__all__'
        extra_kwargs = {
            'nb_fan': {'read_only': True},
            'artist_id': {'write_only': True},
        }

    def get_cover_path(self,obj):
        request = self.context.get('request')
        file_path = get_file_path(request, obj.cover)
        return file_path

    def create(self, validated_data):    
        genre_id = validated_data.pop("genre_id",[])   
        contributor_id = validated_data.pop("contributor_id",[])   
        for i in genre_id: 
            genre = Genre.objects.filter(pk=i)
            if not genre.exists():
                raise serializers.ValidationError(
                    f'pk={i} not registered in Genre table'
                )
        for j in contributor_id: 
            artist = Artist.objects.filter(pk=j)
            if not artist.exists():
                raise serializers.ValidationError(
                    f'pk={j} not registered in Artist table'
                )
        album = Album.objects.create(**validated_data)
        album.genres.set(genre_id)
        album.contributors.set(contributor_id)
        album.save()
        return album


class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True, many=False)
    artist_id = serializers.IntegerField(write_only=True)
    album = AlbumSerializer(read_only=True, many=False)
    album_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Track
        fields = '__all__'


class AlbumDetailSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(write_only=True, required=False)
    cover_path = serializers.SerializerMethodField()
    contributors = ArtistSerializer(read_only=True, many=True)
    tracks = TrackSerializer(source="album_track", read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)
    nb_fan = serializers.IntegerField()
    class Meta:
        model = Album
        fields = '__all__'
        extra_kwargs = {
            'nb_fan': {'read_only': True}
        }

    def get_cover_path(self,obj):
        request = self.context.get('request')
        file_path = get_file_path(request, obj)
        return file_path
