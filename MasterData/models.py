from django.db import models

# Create your models here.
class Client(models.Model):
    def __str__(self):
        return '%d' % self.id

    json = models.TextField()
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "client"


class ClientMetadata(models.Model):
    def __str__(self):
        return '%d' % self.id

    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    document_id = models.TextField()
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "client_metadata"


class Event(models.Model):
    def __str__(self):
        return '%d' %self.id

    json = models.TextField()
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "event"


class EventMetadata(models.Model):
    def __str__(self):
        return '%d' %self.id

    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    server_version = models.TextField()
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    document_id = models.TextField()
    date_created = models.DateTimeField(null=True, blank=True)
    date_edited = models.DateTimeField(null=True, blank=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "event_metadata"


class Location(models.Model):
    def __str__(self):
        return '%d' % self.id

    json = models.TextField()
    active = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "location"


class LocationMetadata(models.Model):
    def __str__(self):
        return '%d' % self.id

    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    parent_id = models.TextField()
    uuid = models.TextField()
    status = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    version = models.TextField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    class Meta:
        db_table = "location_metadata"


class LocationTag(models.Model):
    def __str__(self):
        return '%d' % self.id

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    active = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "location_tag"


class LocationTagMap(models.Model):
    def __str__(self):
        return '%d' % self.id

    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    location_tag_id = models.ForeignKey(LocationTag, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "location_tag_map"
