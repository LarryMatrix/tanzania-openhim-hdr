from django.db import models

# Create your models here.
class Client(models.Model):
    def __str__(self):
        return '%d' % self.id

    json = models.JSONField()

    class Meta:
        db_table = 'client'


class ClientMetadata(models.Model):
    def __str__(self):
        return '%d' % self.id

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    open_him_client_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'client_metadata'


class Event(models.Model):
    def __str__(self):
        return '%d' %self.id

    json = models.JSONField()

    class Meta:
        db_table = 'event'


class EventMetadata(models.Model):
    def __str__(self):
        return '%d' %self.id

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
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
        return '%s' % self.department_name

    local_department_id = models.IntegerField()
    department_name = models.CharField(max_length=255)

    class Meta:
        db_table = "department"


class Facility(models.Model):
    def __str__(self):
        return '%s' % self.facility_name

    facility_name = models.CharField(max_length=255)
    facility_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = "Facilities"


class Ward(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_ward_id = models.IntegerField()
    ward_name = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    number_of_beds = models.IntegerField()

    class Meta:
        db_table = "ward"


class HdrPayerCategory(models.Model):
    def __str__(self):
        return '%s' % self.hdr_payer_category_description

    hdr_payer_category_description = models.CharField(max_length=255)
    hdr_payer_category_local_id = models.IntegerField()

    class Meta:
        db_table = 'hdr_payer_category'
        verbose_name_plural = "HDR Payer Categories"


class HdrExemptionCategory(models.Model):
    def __str__(self):
        return '%s' % self.hdr_exemption_category_description

    hdr_exemption_category_description = models.CharField(max_length=255)
    hdr_exemption_category_local_id = models.IntegerField()

    class Meta:
        db_table = 'hdr_exemption_category'
        verbose_name_plural = "HDR Exemption Categories"



class Payer(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_payer_id = models.IntegerField()
    payer_name = models.CharField(max_length=255)
    hdr_payer_category = models.ForeignKey(HdrPayerCategory, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "payer"


class Exemption(models.Model):
    def __str__(self):
        return '%d' % self.id

    local_exemption_id = models.IntegerField()
    exemption_name = models.CharField(max_length=255)
    hdr_exemption_category = models.ForeignKey(HdrExemptionCategory, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "exemption"


class Icd10Code(models.Model):
    def __str__(self):
        return '%d' % self.id

    icd10_code = models.CharField(max_length=255)
    icd10_name = models.CharField(max_length=255)

    class Meta:
        db_table = "icd10_code"


class CPTCode(models.Model):
    def __str__(self):
        return '%d' % self.id

    cpt_code = models.BigIntegerField()
    cpt_name = models.CharField(max_length=255)

    class Meta:
        db_table = "cpt_code"






