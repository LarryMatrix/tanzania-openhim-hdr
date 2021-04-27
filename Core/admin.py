from django.contrib import admin
from .models import TransactionSummary,ValidationRule , FieldValidationMapping, TransactionSummaryLine
from django.contrib.admin import helpers

# Register your models here.
class TransactionSummaryAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_date_time','message_type','org_name','facility_hfr_code',
                    'total_passed','total_failed','facility_hfr_code')
    search_fields = ['facility_hfr_code',]


class TransactionSummaryLinesAdmin(admin.ModelAdmin):
    list_display = ('id','transaction','payload_object','has_failed','has_passed',
                    'error_message')
    search_fields = []


class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ('id','description','rule_name')
    search_fields = ['description',]

    def has_delete_permission(self, request, obj=None):
        return False


class FieldValidationMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_type','field','validation_rule')
    search_fields = ['message_type', ]


admin.site.register(TransactionSummary, TransactionSummaryAdmin)
admin.site.register(TransactionSummaryLine, TransactionSummaryLinesAdmin)
admin.site.register(ValidationRule, ValidationRuleAdmin)
admin.site.register(FieldValidationMapping, FieldValidationMappingAdmin)