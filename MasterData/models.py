from django.db import models

# Create your models here.
class Client(models.Model):
    def __str__(self):
        return '%d' % self.id

    json = models.TextField()
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'client'


class ClientMetadata(models.Model):
    def __str__(self):
        return '%d' % self.id

    client_id = models.CharField( max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    document_id = models.TextField(null=True, blank=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'client_metadata'


class Event(models.Model):
    def __str__(self):
        return '%d' %self.id

    json = models.TextField(null=True, blank=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'event'


class EventMetadata(models.Model):
    def __str__(self):
        return '%d' %self.id

    event_type = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.CharField(max_length=255,null=True, blank=True)
    open_him_client_id = models.CharField(max_length=255,null=True, blank=True)
    mediator_version = models.CharField(max_length=255,null=True, blank=True)

    class Meta:
        db_table = 'event_metadata'


class Location(models.Model):
    def __str__(self):
        return '%d' % self.id

    json = models.TextField()

    class Meta:
        db_table = 'location'


class LocationMetadata(models.Model):
    def __str__(self):
        return '%d' % self.id

    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    geojson_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    parent_id = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    server_version = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "location_metadata"


class Department(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_department_id = models.IntegerField()
    department_name = models.CharField(max_length=255)

    class Meta:
        db_table = "department"


class Ward(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_ward_id = models.IntegerField()
    ward_name = models.CharField(max_length=255)
    department_id = models.IntegerField()
    number_of_beds = models.IntegerField()

    class Meta:
        db_table = "ward"


class Payer(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_payer_id = models.IntegerField()
    payer_name = models.CharField(max_length=255)

    class Meta:
        db_table = "payer"


class Exemption(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_exemption_id = models.IntegerField()
    exemption_name = models.CharField(max_length=255)

    class Meta:
        db_table = "exemption"







