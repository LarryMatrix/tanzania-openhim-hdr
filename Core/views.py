import csv
import json
from .models import TransactionSummaryLine
from django.http import HttpResponse


# Create your views here.
def convert_to_csv(request):
    if request.method == "POST":
        transaction_id = request.POST["item_pk"]
        transaction_lines = TransactionSummaryLine.objects.filter(transaction_id = transaction_id)
        model_fields = TransactionSummaryLine._meta.fields + TransactionSummaryLine._meta.many_to_many
        field_names = [field.name for field in model_fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response, delimiter=",")
        fields = []
        # Write a first row with header information

        json_object = transaction_lines.first().payload_object

        jsonObject = json.loads(json_object)
        for key in jsonObject:
            fields.append(key)
        writer.writerow(fields)

        for row in transaction_lines:
            json_object = row.payload_object
            values = []
            fields = []
            # for field in field_names:
            jsonObject = json.loads(json_object)
            for key in jsonObject:
                value = jsonObject[key]
                fields.append(key)
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(value)
            writer.writerow(values)
            values = []
        data = response

        return  HttpResponse(data, content_type='text/csv')


