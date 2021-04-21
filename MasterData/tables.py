import django_tables2 as tables
from MasterData import models as master_data_models
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-sm"><i class="la la-trash"></i>Delete</button> '% (escape(record.id)))


class PayerMappingTable(tables.Table):
    Actions = Actions()
    class Meta:
        model = master_data_models.PayerMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('payer','local_payer_id','local_payer_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }


class ExemptionMappingTable(tables.Table):
    Actions = Actions()
    class Meta:
        model = master_data_models.ExemptionMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('exemption','local_exemption_id','local_exemption_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }


class DepartmentMappingTable(tables.Table):
    Actions = Actions()
    class Meta:
        model = master_data_models.DepartmentMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','department','local_department_id','local_department_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }


class WardMappingTable(tables.Table):
    Actions = Actions()
    class Meta:
        model = master_data_models.Ward
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','description','local_ward_id','local_ward_description', 'number_of_beds','department' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }


class GenderMappingTable(tables.Table):
    Actions = Actions()
    class Meta:
        model = master_data_models.GenderMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','gender','local_gender_description' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }


class ServiceProviderRankingMappingTable(tables.Table):

    class Meta:
        model = master_data_models.ServiceProviderRankingMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','service_provider_ranking', 'local_service_provider_ranking_id','local_service_provider_ranking_description')
        row_attrs = {
            'data-id': lambda record: record.pk
        }


class PlaceODeathMappingTable(tables.Table):

    class Meta:
        model = master_data_models.PlaceOfDeathMapping
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','place_of_death', 'local_place_of_death_id','local_place_of_death_description')
        row_attrs = {
            'data-id': lambda record: record.pk
        }