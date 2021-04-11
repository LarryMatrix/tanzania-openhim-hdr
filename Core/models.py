from django.db import models

# Create your models here.
# class ServicesReceived(models.Model):
#     def __str__(self):
#         return '%d' %self.id
#
#     message_type = models.CharField(max_length=255)
#     org_name = models.CharField(max_length=255)
#     facility_hfr_code = models.CharField(max_length=255)
#     department_name = models.CharField(max_length=255)
#     department_id = models.CharField(max_length=255)
#     patient_id = models.CharField(max_length=255)
#     gender = models.CharField(max_length=50)
#     date_of_birth = models.DateField(null=True, blank=True)
#     med_svc_code = models.CharField(max_length=255)
#     icd_10_code = models.CharField(max_length=255,null=True, blank=True)
#     service_date = models.DateField()
#     service_provider_ranking_id = models.CharField(max_length=255)
#     visit_type = models.CharField(max_length=255)
