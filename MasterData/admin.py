from django.contrib import admin
from MasterData.models import Department, Ward, Payer, Exemption, Facility

# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('local_department_id', 'department_name')
    search_fields = ['department_name']

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id','facility_name', 'facility_code')
    search_fields = ['facility_name']

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

class WardAdmin(admin.ModelAdmin):
    list_display = ('local_ward_id','ward_name','facility', 'department', 'number_of_beds')
    search_fields = ['health_commodity_category_name']

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


class PayerAdmin(admin.ModelAdmin):
    list_display = ('local_payer_id','payer_name')
    search_fields = ['payer_name',]

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


class ExemptionAdmin(admin.ModelAdmin):
    list_display = ('local_exemption_id','exemption_name')
    search_fields = ['exemption_name',]

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(Exemption, ExemptionAdmin)
admin.site.register(Facility, FacilityAdmin)

