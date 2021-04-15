import django_tables2 as tables
from Core import models as core_models
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-sm"><i class="la la-trash"></i>Delete</button> '
                         '<button id="%s" class="btn_update btn btn-primary'
                         ' btn-sm"><i class="la la-pencil"></i>Edit</button>  '% (escape(record.id),escape(record.id)))


class TransactionSummaryTable(tables.Table):
    id = tables.Column(
        attrs={
            "th": {"id": "id"},
            "td": {"align": "center"}
        }
    )
    failed_records = tables.Column(
        attrs={
            "th": {"id": "failed_records"},
            "td": {"align": "center"}
        }
    )

    passed_records = tables.Column(
        attrs={
            "th": {"id": "passed_records"},
            "td": {"align": "center"}
        }
    )

    class Meta:
        model = core_models.TransactionSummary
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','error_message','failed_records','passed_records', 'payload' )
        row_attrs = {
            'data-id': lambda record: record.pk
        }