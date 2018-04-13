from django.shortcuts import render
from django.http import HttpResponse
# from server.modelers import Computers
from ULCDTinterface.modelers import Computers, BatToComp
from django.template import loader
from website.logic import *
import re
import os
from django.views.decorators.csrf import csrf_exempt
# from website.form_classes import Computers_form
"""
# Create your views here.
def index(request):
    print("INDEX")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('index.html')
    computers = Computers.objects.all()
    return HttpResponse(template.render({'computers': computers}, request))

def look(request, int_index):
    print("LOOK ")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    print(request)
    print(int_index)
    template = loader.get_template('computer_look.html')
    computer = Computers.objects.get(id_computer=int_index)
    return HttpResponse(template.render({'computer': computer}, request))

@csrf_exempt
def edit(request, int_index):
    print("EDIT ")
    if request.method == 'POST':
        print("This was POST request")
        computer = Computers(
            id_computer=data_dict.pop("id_computer", "")[0],
            serial=data_dict.pop("serial", "")[0],
            manufacturer=data_dict.pop("manufacturer", "")[0],
            model=data_dict.pop("model", "")[0],
            cpu=data_dict.pop("cpu", "")[0],
            ram=data_dict.pop("ram", "")[0],
            gpu=data_dict.pop("gpu", "")[0],
            hdd=data_dict.pop("hdd", "")[0],
            diagonal=data_dict.pop("diagonal", "")[0],
            license=data_dict.pop("camera", "")[0],
            camera=data_dict.pop("camera", "")[0],
            cover=data_dict.pop("cover", "")[0],
            display=data_dict.pop("display", "")[0],
            bezel=data_dict.pop("bezel", "")[0],
            keyboard=data_dict.pop("keyboard", "")[0],
            mouse=data_dict.pop("mouse", "")[0],
            sound=data_dict.pop("sound", "")[0],
            cdrom=data_dict.pop("cdrom", "")[0],
            battery=data_dict.pop("battery", "")[0],
            hdd_cover=data_dict.pop("hdd_cover", "")[0],
            ram_cover=data_dict.pop("ram_cover", "")[0],
            other=data_dict.pop("other", "")[0],
            tester=data_dict.pop("tester", "")[0],
            date=data_dict.pop("date", "")[0],
            bios=data_dict.pop("bios", "")[0]
        )
        computer.save()
        template = loader.get_template('status.html')
        return HttpResponse(template.render({'status': "Success",
                                             'color': "green",
                                             'message': "Record with serial \""+computer.serial+"\" has been updated"},
                                            request))

    if request.method == 'GET':
        print("This was GET request")
        template = loader.get_template('computer_edit.html')
        computer = Computers.objects.get(id_computer=int_index)
        return HttpResponse(template.render({'computer': computer}, request))

@csrf_exempt
def delete(request, int_index):
    print("DELETE")
    if request.method == 'POST':
        print("This was POST request")
        computer = Computers.objects.get(id_computer=int_index)
        computer.delete()
        template = loader.get_template('status.html')
        return HttpResponse(template.render({'status': "Success",
                                             'color': "green",
                                             'message': "Record with serial \"" + computer.serial + "\" has been deleted"},
                                            request))
        # return HttpResponse("Object with an index " + str(int_index) + " deleted")

    if request.method == 'GET':
        print("This was GET request")
        template = loader.get_template('computer_delete.html')
        computer = Computers.objects.get(id_computer=int_index)
        return HttpResponse(template.render({'computer': computer}, request))
"""

def index(request):
    print("INDEX")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('index2.html')
    computers = Computers.objects.all()
    return HttpResponse(template.render({'computers': computers}, request))

def look(request, int_index):
    print("LOOK ")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
        template = loader.get_template('computer_look2.html')
        computer = Computers.objects.get(id_computer=int_index)
        batteries = get_batteries(int_index)
        rams = get_rams(int_index)
        hdds = get_hdds(int_index)
        return HttpResponse(
            template.render({'computer': computer,
                             'bat_list': batteries,
                             "ram_list": rams,
                             "hdd_list": hdds}, request))

@csrf_exempt
def edit(request, int_index):
    print("EDIT ")
    if request.method == 'POST':
        print("This was POST request")
        ecr = Edit_computer_record(request.POST.copy())
        return HttpResponse("Success", request)

    if request.method == 'GET':
        print("This was GET request")
        template = loader.get_template('computer_edit2.html')
        computer = Computers.objects.get(id_computer=int_index)
        batteries = get_batteries(int_index)
        rams = get_rams(int_index)
        hdds = get_hdds(int_index)
        return HttpResponse(template.render({'computer': computer,
                                             'bat_list': batteries,
                                             "ram_list": rams,
                                             "hdd_list": hdds}, request))

@csrf_exempt
def delete(request, int_index):
    print("DELETE")
    if request.method == 'POST':
        print("This was POST request")
        print(int_index)
        existing_computer = Computers.objects.get(id_computer=int_index)
        motherboard = existing_computer.f_motherboard
        existing_computer.delete()
        motherboard.delete()
    if request.method == 'GET':
        print("This was GET request")
        print(int_index)