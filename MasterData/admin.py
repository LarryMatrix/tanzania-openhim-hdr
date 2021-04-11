from django.contrib import admin
from MasterData.models import Department, Ward, Payer, Exemption, Facility, ExemptionCategory, PayerCategory, \
    ICD10Code, CPTCode,PayerMapping, ExemptionMapping, DepartmentMapping, Gender, GenderMapping, ServiceProviderRanking, \
    ServiceProviderRankingMapping, PlaceOfDeath, PlaceOfDeathMapping

# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','description',)
    search_fields = ['description',]


class DepartmentMappingsAdmin(admin.ModelAdmin):
    list_display = ('id','department','local_department_id', 'local_department_description', 'facility')
    search_fields = ['local_department_description',]


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id','description', 'hfr_code')
    search_fields = ['description',]


class WardAdmin(admin.ModelAdmin):
    list_display = ('description','local_ward_id','local_ward_description', 'number_of_beds', 'department','facility')
    search_fields = ['local_ward_description']


class PayerCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description',]


class PayerAdmin(admin.ModelAdmin):
    list_display = ('id','payer_category','description')
    search_fields = ['description',]


class PayerMappingsAdmin(admin.ModelAdmin):
    list_display = ('id','payer','local_payer_id','local_payer_description', 'facility')
    search_fields = ['local_payer_description',]


class ExemptionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description',]


class ExemptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exemption_category','description')
    search_fields = ['description', ]


class ExemptionMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'exemption','local_exemption_id','local_exemption_description','facility')
    search_fields = ['local_exemption_description', ]


class GenderAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    search_fields = ['description', ]


class GenderMappingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender','local_gender_description','facility')
    search_fields = ['local_gender_description', ]


class ICD10MappingAdmin(admin.ModelAdmin):
    list_display = ('icd10_code', 'icd10_description')
    search_fields = ['icd10_description', ]


class CPTCodeAdmin(admin.ModelAdmin):
    list_display = ('cpt_code', 'cpt_description')
    search_fields = ['cpt_description', ]


class ServiceProviderRankingAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ['description', ]


class ServiceProviderRankingMappingAdmin(admin.ModelAdmin):
    list_display = ('service_provider_ranking','local_service_provider_ranking_id',
                    'local_service_provider_ranking_description','facility')
    search_fields = ['local_service_provider_ranking_description', ]


class PlaceOfDeathAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ['description', ]


class PlaceOfDeathMappingAdmin(admin.ModelAdmin):
    list_display = ('place_of_death','local_place_of_death_id',
                    'local_place_of_death_description','facility')
    search_fields = ['local_place_of_death_description', ]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentMapping, DepartmentMappingsAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(PayerCategory, PayerCategoryAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(PayerMapping, PayerMappingsAdmin)
admin.site.register(Exemption, ExemptionAdmin)
admin.site.register(ExemptionMapping, ExemptionMappingsAdmin)
admin.site.register(ExemptionCategory, ExemptionCategoryAdmin)
admin.site.register(ICD10Code, ICD10MappingAdmin)
admin.site.register(CPTCode, CPTCodeAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(GenderMapping, GenderMappingsAdmin)
admin.site.register(ServiceProviderRanking, ServiceProviderRankingAdmin)
admin.site.register(ServiceProviderRankingMapping, ServiceProviderRankingMappingAdmin)
admin.site.register(PlaceOfDeath, PlaceOfDeathAdmin)
admin.site.register(PlaceOfDeathMapping, PlaceOfDeathMappingAdmin)

