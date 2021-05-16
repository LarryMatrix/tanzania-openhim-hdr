from datetime import datetime
from dateutil.parser import parse
from Core.models import FieldValidationMapping, ValidationRule, TransactionSummary, TransactionSummaryLine
import json


# Custom Validators
def convert_date_formats(date):
    for date_format in ('%Y-%m-%d', '%Y%m%d', '%d.%m.%Y', '%d/%m/%Y', '%Y.%m.%d'):
        try:
            date = datetime.strptime(date, date_format).strftime('%Y-%m-%d')
            return date
        except ValueError:
            pass


def check_if_future_date(date):
    formatted_date = convert_date_formats(date)
    now = datetime.now().date()

    if formatted_date > now:
        return True
    else:
        return False


def check_if_past_date(date):
    formatted_date = convert_date_formats(date)
    now = datetime.now().date()

    if formatted_date < now:
        return True
    else:
        return False


def check_if_present_date(date):
    formatted_date = convert_date_formats(date)
    now = datetime.now().date()

    if formatted_date == now:
        return True
    else:
        return False


def check_if_valid_date(date):
    if date:
        try:
            parse(date)
            return True
        except:
            return False
    return False


def validate_received_payload(data):
    message_type = data["messageType"]
    org_name = data["orgName"]
    facility_hfr_code = data["facilityHfrCode"]
    data_items = data["items"]

    instance_transaction_summary = TransactionSummary()
    instance_transaction_summary.message_type = message_type
    instance_transaction_summary.org_name = org_name
    instance_transaction_summary.facility_hfr_code = facility_hfr_code
    instance_transaction_summary.save()

    validation_rule_failed = 0
    transaction_status = True
    error_message = []
    transaction_status_array = []
    total_payload_transactions_status_array = []

    for val in data_items:
        rules = FieldValidationMapping.objects.filter(message_type=message_type)
        for rule in rules:
            field = rule.field
            predefined_rule = ValidationRule.objects.get(id=rule.validation_rule_id)
            rule_name = predefined_rule.rule_name

            print(val[field])
            # Convert date format
            try:
                if rule_name == "convert_date_formats":
                    date = convert_date_formats(val[field])
                    if date is None:
                        raised_error = "Failed to convert " + field + " with value of " + val[
                            field] + " to a valid date format."
                        transaction_status = False
                        validation_rule_failed += 1
                        error_message.append(raised_error)
                    else:
                        transaction_status = True
            except (NameError, TypeError, RuntimeError, KeyError, ValueError):
                raised_error = "Failed to convert "+field+" with value of "+val[field]+" to a valid date format."
                transaction_status = False
                validation_rule_failed += 1
                error_message.append(raised_error)


            # Check if it is a future date. Will return True if future date
            try:
                if rule_name == "check_if_future_date":
                    response = check_if_future_date(val[field])

                    if response is True:
                        transaction_status = True
                    else:
                        raised_error = "Field " + field + " with value of " + val[
                            field] + " seems to be a present date"
                        transaction_status = False
                        validation_rule_failed += 1
                        error_message.append(raised_error)
            except (NameError, TypeError, RuntimeError, KeyError, ValueError):
                raised_error = "Date Field " + field + " with value of " + val[
                    field] + " is invalid."
                transaction_status = False
                validation_rule_failed += 1
                error_message.append(raised_error)


            # Check if it is a past date. Will return True if past date
            try:
                if rule_name == "check_if_past_date":
                    response = check_if_past_date(val[field])

                    if response is True:
                        transaction_status = True
                    else:
                        raised_error = "Date Field " + field + " with value of " + val[
                            field] + " seems to be a present date"
                        transaction_status = False
                        validation_rule_failed += 1
                        error_message.append(raised_error)
            except (NameError, TypeError, RuntimeError, KeyError, ValueError):
                raised_error = "Field " + field + " with value of " + val[
                    field] + " is invalid."
                transaction_status = False
                validation_rule_failed += 1
                error_message.append(raised_error)

            # Check if it is a present date. Will return True if present date
            try:
                if rule_name == "check_if_present_date":
                    response = check_if_present_date(val[field])

                    if response is True:
                        transaction_status = True
                    else:
                        raised_error = "Date Field " + field + " with value of " + val[
                            field] + " seems to be a present date"
                        transaction_status = False
                        validation_rule_failed += 1
                        error_message.append(raised_error)
            except (NameError, TypeError, RuntimeError, KeyError, ValueError):
                raised_error = "Field " + field + " with value of " + val[
                    field] + " is invalid."
                transaction_status = False
                validation_rule_failed += 1
                error_message.append(raised_error)

            # Check if it is a valid date. Will return True if valid
            try:
                if rule_name == "check_if_valid_date":
                    response = check_if_valid_date(val[field])

                    if response is True:
                        transaction_status = True
                    else:
                        raised_error = "Date Field " + field + " with value of " + val[
                            field] + " is invalid"
                        transaction_status = False
                        validation_rule_failed += 1
                        error_message.append(raised_error)
            except (NameError, TypeError, RuntimeError, KeyError, ValueError):
                raised_error = "Date Field " + field + " with value of " + val[
                    field] + " is invalid."
                transaction_status = False
                validation_rule_failed += 1
                error_message.append(raised_error)

            transaction_status_array.append(transaction_status)
            total_payload_transactions_status_array.append(transaction_status)

        previous_transaction = TransactionSummary.objects.get(
            id=instance_transaction_summary.id)

        if validation_rule_failed > 0:
            previous_transaction.total_failed += 1
        else:
            previous_transaction.total_passed += 1

        previous_transaction.save()

        instance_transaction_summary_lines = TransactionSummaryLine()
        instance_transaction_summary_lines.transaction_id = instance_transaction_summary.id
        instance_transaction_summary_lines.payload_object = json.dumps(val)

        if False in transaction_status_array:
            instance_transaction_summary_lines.transaction_status = False
        else:
            instance_transaction_summary_lines.transaction_status = True
        instance_transaction_summary_lines.error_message = error_message

        instance_transaction_summary_lines.save()

        # initialize check
        validation_rule_failed = 0
        transaction_status_array = []
        error_message = []

    return total_payload_transactions_status_array