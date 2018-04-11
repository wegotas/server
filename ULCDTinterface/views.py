from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from ULCDTinterface.modelers import Categories, Types, Testers, Computers, CameraOptions, Licenses
from ULCDTinterface.logic import Computer_record
import json
from urllib.parse import unquote

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
        if record.success == True:
            status_code = 200
        elif record.success == False:
            status_code = 404
        else:
            status_code = 202
            record.message += "Something gone wrong. Notify administrator of this problem."
        return HttpResponse(record.message, status=status_code)
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']
        datastring = unquote(query_string)
        data = json.loads(datastring)
        data["Serial"] = str(data["Serial"]).strip()
        try:
            print("trying to get record with the same serial")
            existing_computer = Computers.objects.get(computer_serial=data["Serial"])
            dict_to_send = {}
            dict_to_send['License'] = existing_computer.f_license.license_name
            dict_to_send['Camera'] = existing_computer.f_camera.option_name
            dict_to_send['Cover'] = existing_computer.cover
            dict_to_send['Display'] = existing_computer.display
            dict_to_send['Bezel'] = existing_computer.bezel
            dict_to_send['Keyboard'] = existing_computer.keyboard
            dict_to_send['Mouse'] = existing_computer.mouse
            dict_to_send['Sound'] = existing_computer.sound
            dict_to_send['CD-ROM'] = existing_computer.cdrom
            dict_to_send['HDD Cover'] = existing_computer.hdd_cover
            dict_to_send['RAM Cover'] = existing_computer.ram_cover
            dict_to_send['Other'] = existing_computer.other
            return JsonResponse(dict_to_send)
        except Exception as e:
            if str(e) == 'Computers matching query does not exist.':
                print("No such computer")
                return HttpResponse("No such computer", status=404)
            else:
                print("Something else")
                return HttpResponse(str(e), status=404)

def check_if_exists(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']
        datastring = unquote(query_string)
        data = json.loads(datastring)
        data["Serial"] = str(data["Serial"]).strip()
        exists = Computers.objects.filter(computer_serial=data["Serial"])
        if exists:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=404)