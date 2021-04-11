from django.db import models


# Support for nifi flow.
class Client(models.Model):
    def __str__(self):
        return '%d' % self.id

    json = models.TextField()

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

    json = models.TextField()

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



# models for mapping
class Facility(models.Model):
    def __str__(self):
        return '%s' % self.description

    description = models.CharField(max_length=255)
    hfr_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = "Facilities"


class PayerCategory(models.Model):
    def __str__(self):
        return '%s' % self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'payer_category'
        verbose_name_plural = "PayerCategories"


class Payer(models.Model):
    def __str__(self):
        return '%s' %self.description

    payer_category = models.ForeignKey(PayerCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Payers'


class PayerMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, null=True, blank=True)
    local_payer_id = models.IntegerField()
    local_payer_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "PayerMappings"


class ExemptionCategory(models.Model):
    def __str__(self):
        return '%s' % self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'exemption_category'
        verbose_name_plural = "ExemptionCategories"


class Exemption(models.Model):
    def __str__(self):
        return '%s' %self.description

    exemption_category = models.ForeignKey(ExemptionCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Exemptions"


class ExemptionMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    exemption = models.ForeignKey(Exemption, on_delete=models.CASCADE, null=True, blank=True)
    local_exemption_id = models.IntegerField()
    local_exemption_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "ExemptionMappings"


class Department(models.Model):
    def __str__(self):
        return '%s' %self.description

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Departments"


class DepartmentMapping(models.Model):
    def __str__(self):
        return '%d' % self.id

    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    local_department_id = models.IntegerField()
    local_department_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "DepartmentMappings"


class Ward(models.Model):
    def __str__(self):
        return '%d' %self.id

    description = models.CharField(max_length=255)
    local_ward_id = models.IntegerField()
    local_ward_description = models.CharField(max_length=255)
    number_of_beds = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Wards"


class Gender(models.Model):
    def __str__(self):
        return '%d' %self.id

    description = models.CharField(max_length=50)

    class Meta:
        db_table = "Gender"


class GenderMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    local_gender_description = models.CharField(max_length=50)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "GenderMappings"


class ICD10Code(models.Model):
    def __str__(self):
        return '%d' %self.id

    icd10_code = models.CharField(max_length=255)
    icd10_description = models.CharField(max_length=255)

    class Meta:
        db_table="ICD10Codes"


class CPTCode(models.Model):
    def __str__(self):
        return '%d' %self.id

    cpt_code = models.CharField(max_length=255)
    cpt_description = models.CharField(max_length=255)

    class Meta:
        db_table = "CPTCodes"


class ServiceProviderRanking(models.Model):
    def __str__(self):
        return '%d' %self.id

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "ServiceProviderRankings"


class ServiceProviderRankingMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    service_provider_ranking = models.ForeignKey(ServiceProviderRanking, on_delete=models.CASCADE, null=True, blank=True)
    local_service_provider_ranking_id = models.IntegerField()
    local_service_provider_ranking_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "ServiceProviderRankingMappings"


class PlaceOfDeath(models.Model):
    def __str__(self):
        return "%d" %self.id

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "PlacesOfDeath"
        verbose_name_plural = "PlacesOfDeath"


class PlaceOfDeathMapping(models.Model):
    def __str__(self):
        return '%d' %self.id

    place_of_death = models.ForeignKey(PlaceOfDeath, on_delete=models.CASCADE, null=True, blank=True)
    local_place_of_death_id = models.IntegerField()
    local_place_of_death_description = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "PlaceOfDeathMappings"


