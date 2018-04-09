from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from ULCDTinterface.modelers import Categories, Types, Testers, Computers
from ULCDTinterface.logic import Computer_record

# Create your views here.
@csrf_exempt
def aux_data(request):
    print("aux_data called")
    if request.method == "GET":
        print("GET aux_data")
        dict_dict = dict()
        dict_dict["cat_dict"] = Categories.get_values()
        dict_dict["typ_dict"] = Types.get_values()
        dict_dict["tes_dict"] = Testers.get_values()
        return JsonResponse(dict_dict)

@csrf_exempt
def process_data(request):
    print("proccess_data called")
    if request.method == "POST":
        print("POST proccess_data")
        data = JSONParser().parse(request)
        print(data)
        record = Computer_record(data)

        """
        try:
            existing_computer = Computers.objects.get(computer_serial=data['Serial'])
            print("Does exist")
        except Exception as e:
            print(str(e))
        """