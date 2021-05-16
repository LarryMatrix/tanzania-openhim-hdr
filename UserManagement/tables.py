import django_tables2 as tables
from Core import models as core_models
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_view_more btn btn-success'
                         ' btn-xs"><i class="la la"></i>View More Details</button> '
                         '<button id="%s" class="btn_download btn btn-primary'
                         ' btn-xs"><i class="la la-down"></i>Download CSV</button> '  % (escape(record.id), escape(record.id)))


class TransactionSummaryTable(tables.Table):
    Actions = Actions()
    id = tables.Column(
        attrs={
            "th": {"id": "id"},
            "td": {"align": "center"}
        }
    )
    total_failed = tables.Column(
        attrs={
            "th": {"id": "total_failed"},
            "td": {"align": "center"}
        }
    )

    total_passed = tables.Column(
        attrs={
            "th": {"id": "total_passed"},
            "td": {"align": "center"}
        }
    )

    class Meta:
        model = core_models.TransactionSummary
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','message_type','org_name', 'facility_hfr_code','total_passed', 'total_failed')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

class TransactionSummaryLineTable(tables.Table):

    class Meta:
        model = core_models.TransactionSummaryLine
        template_name = "django_tables2/bootstrap.html"
        fields = ('transaction', 'payload_object', 'transaction_status', 'error_message')
        row_attrs = {
            'data-id': lambda record: record.pk
        }