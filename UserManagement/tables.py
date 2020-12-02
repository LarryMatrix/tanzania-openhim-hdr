from django.contrib.auth.models import User
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-xs"><i class="la la-trash"></i></button> '
                         '<button id="%s" class="btn_update btn btn-success '
                         'btn-xs"><i class="la la-pencil"></i></button> ' % (escape(record.id), escape(record.id)))

class UserTable(tables.Table):
    Actions = Actions()
    gender = tables.Column(accessor='profile.gender')

    class Meta:
        model = User
        row_attrs = {
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'first_name','last_name', 'gender', 'is_staff')



