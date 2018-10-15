from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from server.modelers import Computers, Types, Categories, Testers
import datetime
import json
from urllib.parse import parse_qs, unquote



@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        print("Before parser")
        print(request.__dict__)
        data = JSONParser().parse(request)
        print(data)
        try:
            dt = datetime.datetime.now()
            try:
                print("trying to get record with the same serial")
                existing_computer = Computers.objects.get(serial=data['Serial'])
                print("computer with the same serial was found. Updating existing record")
                computer = Computers(
                    id_computer=existing_computer.id_computer,
                    serial=data['Serial'],
                    manufacturer=data['Manufacturer'],
                    model=data['Model'],
                    cpu=data['CPU'],
                    ram=data['RAM'],
                    gpu=data['GPU'],
                    hdd=data['HDD'],
                    diagonal=data['Diagonal'],
                    license=data['License'],
                    camera=data['Camera'],
                    cover=data['Cover'],
                    display=data['Display'],
                    bezel=data['Bezel'],
                    keyboard=data['Keyboard'],
                    mouse=data['Mouse'],
                    sound=data['Sound'],
                    cdrom=data['CD-ROM'],
                    hdd_cover=data['HDD Cover'],
                    ram_cover=data['RAM Cover'],
                    other=data['Other'],
                    tester=data['Tester'],
                    date=dt,
                    bios=data['BIOS'],
                    computer_type=data['Computer type'],
                    motherboard_serial=data['motherboard_serial'],
                    hdd_serial1=data['hdd_serial1'],
                    hdd_serial2=data['hdd_serial2'],
                    hdd_serial3=data['hdd_serial3'],
                    ram_serial1=data['ram_serial1'],
                    ram_serial2=data['ram_serial2'],
                    ram_serial3=data['ram_serial3'],
                    ram_serial4=data['ram_serial4'],
                    ram_serial5=data['ram_serial5'],
                    ram_serial6=data['ram_serial6'],
                    bat1_wear_out=data['Bat1 wear'],
                    bat1_expected_time=data['Bat1 expected time'],
                    bat1_serial=data['Bat1 serial'],
                    bat2_wear_out=data['Bat2 wear'],
                    bat2_expected_time=data['Bat2 expected time'],
                    bat2_serial=data['Bat2 serial'],
                )
                print("updating")
                computer.save()
                print("update was succesful")
                response = HttpResponse("Matching serial was found. Previous record updated.", status=200)
                return response
            except Exception as e:
                print(str(e))
                if str(e) == 'Computers matching query does not exist.':
                    computer = Computers(
                        serial=data['Serial'],
                        manufacturer=data['Manufacturer'],
                        model=data['Model'],
                        cpu=data['CPU'],
                        ram=data['RAM'],
                        gpu=data['GPU'],
                        hdd=data['HDD'],
                        diagonal=data['Diagonal'],
                        license=data['License'],
                        camera=data['Camera'],
                        cover=data['Cover'],
                        display=data['Display'],
                        bezel=data['Bezel'],
                        keyboard=data['Keyboard'],
                        mouse=data['Mouse'],
                        sound=data['Sound'],
                        cdrom=data['CD-ROM'],
                        hdd_cover=data['HDD Cover'],
                        ram_cover=data['RAM Cover'],
                        other=data['Other'],
                        tester=data['Tester'],
                        date=dt,
                        bios=data['BIOS'],
                        computer_type=data['Computer type'],
                        motherboard_serial=data['motherboard_serial'],
                        hdd_serial1=data['hdd_serial1'],
                        hdd_serial2=data['hdd_serial2'],
                        hdd_serial3=data['hdd_serial3'],
                        ram_serial1=data['ram_serial1'],
                        ram_serial2=data['ram_serial2'],
                        ram_serial3=data['ram_serial3'],
                        ram_serial4=data['ram_serial4'],
                        ram_serial5=data['ram_serial5'],
                        ram_serial6=data['ram_serial6'],
                        bat1_wear_out=data['Bat1 wear'],
                        bat1_expected_time=data['Bat1 expected time'],
                        bat1_serial=data['Bat1 serial'],
                        bat2_wear_out=data['Bat2 wear'],
                        bat2_expected_time=data['Bat2 expected time'],
                        bat2_serial=data['Bat2 serial'],
                    )
                    computer.save()
                    response = HttpResponse("No matching serials were found. New record has been made.", status=200)
                    return response
                else:
                    response = HttpResponse(status=404)
                    response.write(str(e))
                    return response
        except Exception as e:
            return HttpResponse(str(e), status=404)
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']
        datastring = unquote(query_string)
        data = json.loads(datastring)
        print(type(data["Serial"]))
        data["Serial"] = str(data["Serial"]).strip()
        print(type(data["Serial"]))
        try:
            print("trying to get record with the same serial")
            existing_computer = Computers.objects.get(serial=data["Serial"])
            dict_to_send = {}
            dict_to_send['License'] = existing_computer.license
            dict_to_send['Camera'] = existing_computer.camera
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


@csrf_exempt
def aux_data(request):
    print("aux_data called")
    if request.method == "GET":
        print("GET aux_data")
        print("___________________________")
        categories = Categories.objects.all()
        cat_dict = dict()
        for category in categories:
            print(category.id_category)
            print(category.category_name)
            cat_dict[category.id_category] = category.category_name
        print(cat_dict)
        print("___________________________")
        types = Types.objects.all()
        typ_dict = dict()
        for type in types:
            print(type.id_types)
            print(type.type_name)
            typ_dict[type.id_types] = type.type_name
        print(typ_dict)
        print("___________________________")
        testers = Testers.objects.all()
        test_dict = dict()
        for tester in testers:
            test_dict[tester.id_tester] = tester.tester_name
        dict_dict = dict()
        dict_dict["cat_dict"] = cat_dict
        dict_dict["typ_dict"] = typ_dict
        dict_dict["tes_dict"] = test_dict
        print(dict_dict)
        return JsonResponse(dict_dict)

