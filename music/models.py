from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
from users.models import User
from django.utils.translation import gettext_lazy as _

class Genre(models.Model):
    """
    Genre Model Class
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    ) 
    picture	= models.ImageField(      
        max_length=10**7,  
        upload_to="media/genre_picture/",
        null=True,
        blank=True,
        verbose_name=_("Picture")
    )

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Artist(models.Model):
    """
    Artist Model Class
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    ) 
    picture	= models.ImageField(      
        max_length=10**7,   
        upload_to="media/artist_picture/",
        null=True,
        blank=True,
        verbose_name=_("Picture")
    )
    radio = models.BooleanField(
        default=False,
        verbose_name=_("Smartradio")
    )
    fans = models.ManyToManyField(
        User,
        through='ArtistFan',
        through_fields=('artist', 'user'),
        related_name='artist_fan',
        verbose_name=_("Fans"),
    )

    @property
    def nb_album(self):
        albums = Album.objects.filter(artist_id=self.pk).count()
        return albums   

    @property
    def nb_fan(self):
        fans = self.fans.count()
        return fans

    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")


class ArtistFan(models.Model):
    """
    ArtistFan Model Class
    """
    artist	= models.ForeignKey(
        Artist,
        related_name='artist_fan',
        verbose_name=_("Artist"),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='user_artist',
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Artist Fan")
        verbose_name_plural = _("Artist Fans")


class Album(models.Model):
    """
    Album Model Class
    """
    EXPLICIT_TYPE = [
        (0, _("Not Explicit")), 
        (1, _("Explicit")), 
        (2, _("Unknown")),
        (3, _("Edited")),
        (4, _("Partially Explicit (Album 'lyrics' only)")), 
        (5, _("Partially Unknown (Album 'lyrics' only)")),
        (6, _("No Advice Available")),
        (7, _("Partially No Advice Available (Album 'lyrics' only)"))
    ]
    title	= models.CharField(
        max_length=255,
        verbose_name=_("Title")
    ) 
    upc	= models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name=_("Universal Product Code")
    )
    cover = models.ImageField(
        max_length=10**7, 
        upload_to="media/album_cover/",
        null=True,
        blank=True,
        verbose_name=_("Cover")
    )
    label = models.CharField(
        max_length=255,
        verbose_name=_("Label")
    ) 
    duration = models.PositiveIntegerField(
        verbose_name=_("Explicit Content Lyrics")
    )
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Release Date")
    )
    record_type	= models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Record Type")
    )
    available = models.BooleanField(
        default=True, 
        verbose_name=_("Available")
    )	
    alternative	= models.ForeignKey(
        'self',
        null=True,
        related_name='alternative_album',
        verbose_name=_("Alternative"),
        on_delete=models.SET_NULL
    )
    explicit_lyrics = models.BooleanField(
        default=False,
        verbose_name=_("Explicit lyrics")
    )	
    explicit_content_lyrics = models.IntegerField(
        choices=EXPLICIT_TYPE,
        default=0,
        verbose_name=_("Explicit Content Lyrics")
    )
    explicit_content_cover = models.IntegerField(
        choices=EXPLICIT_TYPE,
        default=0,
        verbose_name=_("Explicit Content Cover")
    ) 
    artist = models.ForeignKey(
        Artist,
        related_name='artist_album',
        verbose_name=_("Artist"),
        on_delete=models.CASCADE
    )
    fans = models.ManyToManyField(
        User,
        through='AlbumFan',
        through_fields=('album', 'user'),
        related_name='album_fan',
        verbose_name=_("Fans"),
    )
    contributors = models.ManyToManyField(
        Artist,
        through='Contributor',
        through_fields=('album','artist'),
        related_name='album_contributor',
        verbose_name=_("Contributors"),
    )
    genres = models.ManyToManyField(
        Genre,
        through='AlbumGenre',
        through_fields=('album', 'genre'),
        related_name='album_genre',
        verbose_name=_("Genres"),
    )
    @property
    def nb_fan(self):
        fans = self.fans.count()
        return fans

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")


class AlbumFan(models.Model):
    """
    AlbumFan Model Class
    """
    album	= models.ForeignKey(
        Album,
        related_name='album_fan',
        verbose_name=_("Artist"),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='user_album',
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Album Fan")
        verbose_name_plural = _("Album Fans")


class Contributor(models.Model):
    """
    Contributor Model Class
    """
    artist = models.ForeignKey(
        Artist,
        verbose_name=_("Artist"),
        on_delete=models.CASCADE
    )
    album = models.ForeignKey(
        Album,
        verbose_name=_("Album"),
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = _("Contributor")
        verbose_name_plural = _("Contributors")


class AlbumGenre(models.Model):
    """
    AlbumGenre Model Class
    """
    album = models.ForeignKey(
        Album,
        related_name='album_genre',
        verbose_name=_("Artist"),
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        related_name='genre_album',
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Track(models.Model):
    """
    Track Model Class
    """
    EXPLICIT_TYPE = [
        (0, _("Not Explicit")), 
        (1, _("Explicit")), 
        (2, _("Unknown")),
        (3, _("Edited")),
        (4, _("Partially Explicit (Album 'lyrics' only)")), 
        (5, _("Partially Unknown (Album 'lyrics' only)")),
        (6, _("No Advice Available")),
        (7, _("Partially No Advice Available (Album 'lyrics' only)"))
    ]
    file = models.FileField(
        max_length=50**7, 
        validators=[FileExtensionValidator(allowed_extensions=[
            "mp3","wav", "aac", 'wma'
        ])],
        upload_to="media/track_file/",
        verbose_name=_("File")
    )
    readable = models.BooleanField(
        default=True,
        verbose_name=_("Readable")
    )
    title =  models.CharField(
        max_length=255,
        verbose_name=_("Title")
    ) 
    title_short	= models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Title Short")
    ) 
    title_version = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Title Version")
    ) 
    isrc = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("International Standard Recording Code")
    ) 
    duration = models.IntegerField(
        verbose_name=_("Duration")
    )
    track_position	= models.IntegerField(
        verbose_name=_("Track Position")
    )
    disk_number	= models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Disk Number")
    ) 
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Release Date")
    )
    explicit_lyrics = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Explicit lyrics")
    )	
    explicit_content_lyrics = models.IntegerField(
        choices=EXPLICIT_TYPE,
        null=True,
        blank=True,
        verbose_name=_("Explicit Content Lyrics")
    )
    explicit_content_cover = models.IntegerField(
        choices=EXPLICIT_TYPE,
        null=True,
        blank=True,
        verbose_name=_("Explicit Content Cover")
    )
    bpm	= models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,        
        validators=[
            MinValueValidator(0.0)
        ],
        verbose_name=_("Beats Per Minute (BPM)")
    )
    gain = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.0,
        validators=[
            MinValueValidator(0.0)
        ],
        verbose_name=_("Gain")
    )
    alternative = models.ForeignKey(
        'self',
        null=True,
        related_name='alternative_track',
        verbose_name=_("Alternative"),
        on_delete=models.SET_NULL
    )
    album = models.ForeignKey(
        Album,
        related_name='album_track',
        verbose_name=_("Album"),
        on_delete=models.CASCADE
    )
    artist = models.ForeignKey(
        Artist,
        related_name='artist_track',
        verbose_name=_("Artist"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
