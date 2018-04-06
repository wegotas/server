from django.shortcuts import render
from django.http import HttpResponse
from server.modelers import Computers
from django.template import loader
import re
import os
from django.views.decorators.csrf import csrf_exempt
# from website.form_classes import Computers_form

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
            id_computer=request.POST.get("id_computer", ""),
            serial=request.POST.get("serial", ""),
            manufacturer=request.POST.get("manufacturer", ""),
            model=request.POST.get("model", ""),
            cpu=request.POST.get("cpu", ""),
            ram=request.POST.get("ram", ""),
            gpu=request.POST.get("gpu", ""),
            hdd=request.POST.get("hdd", ""),
            diagonal=request.POST.get("diagonal", ""),
            license=request.POST.get("camera", ""),
            camera=request.POST.get("camera", ""),
            cover=request.POST.get("cover", ""),
            display=request.POST.get("display", ""),
            bezel=request.POST.get("bezel", ""),
            keyboard=request.POST.get("keyboard", ""),
            mouse=request.POST.get("mouse", ""),
            sound=request.POST.get("sound", ""),
            cdrom=request.POST.get("cdrom", ""),
            battery=request.POST.get("battery", ""),
            hdd_cover=request.POST.get("hdd_cover", ""),
            ram_cover=request.POST.get("ram_cover", ""),
            other=request.POST.get("other", ""),
            tester=request.POST.get("tester", ""),
            date=request.POST.get("date", ""),
            bios=request.POST.get("bios", "")
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