from django.http import HttpResponse
from ULCDTinterface.modelers import Computers, BatToComp
from django.template import loader
from website.logic import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def index(request):
    print("Paging")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    qty = getQty(request)
    qtySelect = QtySelect()
    qtySelect.setDefaultSelect(qty)
    computers = Computers.objects.all()
    paginator = Paginator(computers, qty)

    page = getPage(request)
    computers = paginator.get_page(page)
    counter = Counter()
    counter.count = qty*(page-1)
    cattyp = CatTyp()
    autoFilters = AutoFilters()

    return render(request, 'index3.html', {
        'computers': computers,
        "counter": counter,
        "qtySelect": qtySelect,
        "autoFilters": autoFilters,
        "cattyp": cattyp})

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
        bats_to_comp = BatToComp.objects.filter(f_id_computer_bat_to_com=int_index)
        for bat_to_comp in bats_to_comp:
            bat_to_comp.delete()
        hdds_to_comp = HddToComp.objects.filter(f_id_computer_hdd_to_com=int_index)
        for hdd_to_comp in hdds_to_comp:
            hdd_to_comp.delete()
        rams_to_comp = RamToComp.objects.filter(f_id_computer_ram_to_com=int_index)
        for ram_to_comp in rams_to_comp:
            ram_to_comp.delete()
        existing_computer = Computers.objects.get(id_computer=int_index)

        motherboard = existing_computer.f_motherboard
        cpu = existing_computer.f_cpu
        diagonal = existing_computer.f_diagonal
        hdd_size = existing_computer.f_hdd_size
        ram_size = existing_computer.f_ram_size
        gpu = existing_computer.f_gpu
        model = existing_computer.f_model
        manufacturer = existing_computer.f_manufacturer

        existing_computer.delete()
        motherboard_deletion_if_exists(motherboard)
        cpu_deletion_if_exists(cpu)
        diagonal_deletion_if_exists(diagonal)
        hdd_size_deletion_if_exists(hdd_size)
        ram_size_deletion_if_exists(ram_size)
        gpu_deletion_if_exists(gpu)
        model_deletion_if_exists(model)
        manufacturer_deletion_if_exists(manufacturer)


        return HttpResponse("If you see this message that means after deletion post update on JS side page reload has failed")
    if request.method == 'GET':
        print("This was GET request")
        print(int_index)

def motherboard_deletion_if_exists(motherboard):
    if motherboard is not None:
        motherboard.delete()

def cpu_deletion_if_exists(cpu):
    if cpu is not None:
        if not Computers.objects.filter(f_cpu=cpu.id_cpu).exists():
            cpu.delete()

def diagonal_deletion_if_exists(diagonal):
    if diagonal is not None:
        if not Computers.objects.filter(f_diagonal=diagonal.id_diagonal).exists():
            diagonal.delete()

def hdd_size_deletion_if_exists(hdd_size):
    if hdd_size is not None:
        if not Computers.objects.filter(f_hdd_size=hdd_size.id_hdd_sizes).exists():
            hdd_size.delete()

def ram_size_deletion_if_exists(ram_size):
    if ram_size is not None:
        if not Computers.objects.filter(f_ram_size=ram_size.id_ram_size).exists():
            ram_size.delete()

def gpu_deletion_if_exists(gpu):
    if gpu is not None:
        if not Computers.objects.filter(f_gpu=gpu.id_gpu).exists():
            gpu.delete()

def model_deletion_if_exists(model):
    if model is not None:
        if not Computers.objects.filter(f_model=model.id_model).exists():
            model.delete()

def manufacturer_deletion_if_exists(manufacturer):
    if manufacturer is not None:
        print(manufacturer)
        if not Computers.objects.filter(f_manufacturer=manufacturer.id_manufacturer).exists():
            print("Does not exist")
            manufacturer.delete()
            print("Deletion accomplished")
        else:
            print("Does exist")