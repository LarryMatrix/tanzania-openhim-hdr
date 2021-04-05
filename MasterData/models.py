from django.db import models


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
        return '%d' % self.id

    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'payer_category'
        verbose_name_plural = "Payer Categories"


class Payer(models.Model):
    def __str__(self):
        return '%d' %self.id

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
        verbose_name_plural = "Exemption Categories"


class Exemption(models.Model):
    def __str__(self):
        return '%d' %self.id

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
        return '%d' %self.id

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "Departments"


class DepartmentMappings(models.Model):
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
