from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from ULCDTinterface.modelers import * # Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Clients, Sales, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, RamSizes, Rams, Testers, Types, BatToComp, RamToComp, HddToComp, CompOrd, OrdTes, Orders
from ULCDTinterface.logic import *
import json
from urllib.parse import unquote


# Create your views here.


@csrf_exempt
def aux_data(request):
    print("aux_data called")
    if request.method == "GET":
        def _get_formed_observations_dict():
            variables = Observations.objects.all()
            observation_dict = dict()
            for variable in variables:
                cat_name = variable.f_id_observation_category.category_name
                sub_cat_name = variable.f_id_observation_subcategory.subcategory_name
                full_name = variable.full_name
                shortcode = variable.shortcode

                if not cat_name in observation_dict:
                    observation_dict[cat_name] = {}
                if not sub_cat_name in observation_dict[cat_name]:
                    observation_dict[cat_name][sub_cat_name] = {}
                observation_dict[cat_name][sub_cat_name][full_name] = shortcode
            return observation_dict

        print("GET aux_data")
        dict_dict = dict()
        dict_dict["Categories"] = list(Categories.objects.values_list('category_name', flat=True))
        dict_dict["Types"] = list(Types.objects.values_list('type_name', flat=True))
        dict_dict["Testers"] = list(Testers.objects.values_list('tester_name', flat=True))
        dict_dict['Received batches'] = list(Receivedbatches.objects.values_list('received_batch_name', flat=True))
        dict_dict['Form factors'] = list(ComputerFormFactors.objects.values_list('form_factor_name', flat=True))
        dict_dict['Form factors'].insert(0, '')
        dict_dict['Observations'] = _get_formed_observations_dict()
        return JsonResponse(dict_dict)


@csrf_exempt
def process_data(request):
    print("proccess_data 2 called")
    if request.method == "POST":
        print("POST proccess_data2")
        data = JSONParser().parse(request)
        record = ComputerRecord(data)
        if record.success == True:
            status_code = 200
        elif record.success == False:
            status_code = 404
        else:
            status_code = 202
            record.message += "Something gone wrong. Notify administrator of this problem."
        if status_code == 200:
            data = {}
            print(type(record.computer))
            print(record.computer)
            data["Index"] = record.computer.id_computer
            json_data = json.dumps(data)
            return HttpResponse(json_data, status=status_code)
        else:
            return HttpResponse(record.message, status=status_code)
    if request.method == 'GET':
        print("GET proccess_data2")
        query_string = request.META['QUERY_STRING']
        datastring = unquote(query_string)
        data = json.loads(datastring)
        try:
            csb = ComputerDataDictBuilder(str(data["Serial"]).strip())
            return JsonResponse(csb.data_dict)
        except Exception as e:
            if str(e) == 'Computers matching query does not exist.':
                print("No such computer")
                return HttpResponse("No such computer", status=404)
            else:
                print("Something else")
                return HttpResponse(str(e), status=404)


@csrf_exempt
def process_pictures(request, int_index):
    print(int_index)
    # print(request.FILES)
    variable = request.FILES



def check_if_exists(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']
        datastring = unquote(query_string)
        data = json.loads(datastring)
        data["Serial"] = str(data["Serial"]).strip()
        exists = Computers.objects.filter(computer_serial=data["Serial"]).exists()
        if exists:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=404)
