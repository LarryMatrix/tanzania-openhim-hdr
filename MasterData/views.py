from django.shortcuts import render, redirect
from .tables import PayerMappingTable, ExemptionMappingTable, DepartmentMappingTable, WardMappingTable,\
    GenderMappingTable, ServiceProviderRankingMappingTable, PlaceODeathMappingTable
from .models import PayerMapping, DepartmentMapping, ExemptionMapping, Ward, GenderMapping, \
    ServiceProviderRankingMapping, PlaceOfDeathMapping
from .forms import DepartmentMappingForm, ExemptionMappingForm, PayerMappingForm, WardMappingForm, GenderMappingForm, \
    ServiceProviderRankingMappingForm, PlaceODeathMappingForm
from django_tables2 import RequestConfig


def get_departments_page(request):
    if request.method == "POST":
        department_mapping_form = DepartmentMappingForm(request.POST)

        if department_mapping_form.is_valid():
            department_mapping_form.full_clean()
            department_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        department_mappings = DepartmentMapping.objects.filter(facility=facility)
        department_mappings_table = DepartmentMappingTable(department_mappings)
        department_mapping_form = DepartmentMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(department_mappings_table)
        return render(request, 'MasterData/Features/Departments.html',{"department_mappings_table": department_mappings_table,
                                                                       "department_mapping_form" : department_mapping_form})


def get_exemptions_page(request):
    if request.method == "POST":
        exemption_mapping_form = ExemptionMappingForm(request.POST)

        if exemption_mapping_form.is_valid():
            exemption_mapping_form.full_clean()
            exemption_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        exemption_mappings = ExemptionMapping.objects.filter(facility=facility)
        exemption_mappings_table = ExemptionMappingTable(exemption_mappings)
        exemption_mapping_form = ExemptionMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(exemption_mappings_table)
        return render(request, 'MasterData/Features/Exemptions.html',{"exemption_mappings_table":exemption_mappings_table,
                                                                      "exemption_mapping_form":exemption_mapping_form})


def get_payers_page(request):
    if request.method == "POST":
        payer_mapping_form = PayerMappingForm(request.POST)

        if payer_mapping_form.is_valid():
            payer_mapping_form.full_clean()
            payer_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        payer_mappings = PayerMapping.objects.filter(facility=facility)
        payer_mappings_table = PayerMappingTable(payer_mappings)
        payer_mapping_form = PayerMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(payer_mappings_table)
        return render(request, 'MasterData/Features/Payers.html', {"payer_mappings_table":payer_mappings_table,
                                                                   "payer_mapping_form":payer_mapping_form})


def get_wards_page(request):
    if request.method == "POST":
        ward_mapping_form = WardMappingForm(request.POST)

        if ward_mapping_form.is_valid():
            ward_mapping_form.full_clean()
            ward_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        ward_mappings = Ward.objects.filter(facility=facility)
        ward_mappings_table = WardMappingTable(ward_mappings)
        ward_mapping_form = WardMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(ward_mappings_table)
        return render(request, 'MasterData/Features/Wards.html',{"ward_mappings_table":ward_mappings_table,
                                                                 "ward_mapping_form":ward_mapping_form})


def get_gender_page(request):
    if request.method == "POST":
        gender_mapping_form = GenderMappingForm(request.POST)

        if gender_mapping_form.is_valid():
            gender_mapping_form.full_clean()
            gender_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        gender_mappings = GenderMapping.objects.filter(facility=facility)
        gender_mappings_table = GenderMappingTable(gender_mappings)
        gender_mapping_form = GenderMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(gender_mappings_table)
        return render(request, 'MasterData/Features/Gender.html', {"gender_mappings_table": gender_mappings_table,
                                                                  "gender_mapping_form": gender_mapping_form})


def get_service_provider_rankings_page(request):
    if request.method == "POST":
        service_provider_ranking_mapping_form = ServiceProviderRankingMappingForm(request.POST)

        if service_provider_ranking_mapping_form.is_valid():
            service_provider_ranking_mapping_form.full_clean()
            service_provider_ranking_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        service_provider_ranking_mappings = ServiceProviderRankingMapping.objects.filter(facility=facility)
        service_provider_ranking_mappings_table = ServiceProviderRankingMappingTable(service_provider_ranking_mappings)
        service_provider_ranking_mapping_mapping_form = ServiceProviderRankingMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(service_provider_ranking_mappings_table)
        return render(request, 'MasterData/Features/ServiceProviderRankings.html',
                      {"service_provider_ranking_mappings_table": service_provider_ranking_mappings_table,
                        "service_provider_ranking_mappings_form": service_provider_ranking_mapping_mapping_form})


def get_places_of_death_page(request):
    if request.method == "POST":
        place_of_death_mapping_form = PlaceODeathMappingForm(request.POST)

        if place_of_death_mapping_form.is_valid():
            place_of_death_mapping_form.full_clean()
            place_of_death_mapping_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        facility = request.user.profile.facility
        place_of_death_mappings = PlaceOfDeathMapping.objects.filter(facility=facility)
        place_of_death_mappings_table = PlaceODeathMappingTable(place_of_death_mappings)
        place_of_death_mapping_form = PlaceODeathMappingForm(initial={'facility': request.user.profile.facility})
        RequestConfig(request, paginate={"per_page": 10}).configure(place_of_death_mappings_table)
        return render(request, 'MasterData/Features/PlacesOfDeath.html',
                      {"place_of_death_mappings_table": place_of_death_mappings_table,
                                                "place_of_death_mapping_form": place_of_death_mapping_form})