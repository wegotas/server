from django.http import HttpResponse
from ULCDTinterface.modelers import Computers, BatToComp
from django.template import loader
from website.logic import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.db.utils import IntegrityError


def index(request):
    print("Paging")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    isSold = getIsSold(request)
    isOrder = getIsOrder(request)
    data_dict = request.GET.copy()
    qty = getQty(data_dict)
    page = getPage(data_dict)
    keyword = getKeyword(data_dict)
    autoFilters = AutoFilter(data_dict)
    cattyp = CatTyp()
    if isSold:
        possible_categories = None
        qtySelect = QtySelect()
        qtySelect.setDefaultSelect(qty)
        computers = Computers.objects.exclude(f_sale__isnull=True)
        computers = autoFilters.filter(computers)
        if keyword is not None:
            computers = search(keyword, computers)
        af = AutoFiltersFromSoldComputers(computers)
        paginator = Paginator(computers, qty)
        computers = paginator.get_page(page)
        counter = Counter()
        counter.count = qty * (page - 1)
        category_querySet = Categories.objects.values_list('category_name')
        possible_categories = []
        for query_member in category_querySet:
            possible_categories.append(query_member[0])
        # cattyp = CatTyp()
        # removeKeyword(request)
        return render(request, 'sold.html', {
            'computers': computers,
            "counter": counter,
            "qtySelect": qtySelect,
            "autoFilters": af,
            "cattyp": cattyp,
            "poscat": possible_categories})
    elif isOrder:
        counter = Counter()
        orders = OrdersClass()
        return render(request, 'orders.html', {
            "counter": counter,
            "cattyp": cattyp,
            "orders": orders
        })
    else:
        typ = getType(data_dict)
        cat = getCat(data_dict)
        removeSold(data_dict)
        possible_categories = None
        if cat or typ:
            qtySelect = QtySelect()
            qtySelect.setDefaultSelect(qty)
            typeRecord = Types.objects.filter(type_name=typ)[:1].get()
            catRecord = Categories.objects.filter(category_name=cat)[:1].get()
            computers = Computers.objects.filter(f_type=typeRecord.id_type, f_category=catRecord.id_category, f_sale=None).exclude(f_id_comp_ord__isnull=False).exclude(f_sale__isnull=False)
            computers = autoFilters.filter(computers)
            if keyword is not None:
                computers = search(keyword, computers)
            af = AutoFiltersFromComputers(computers)
            paginator = Paginator(computers, qty)
            computers = paginator.get_page(page)
            counter = Counter()
            counter.count = qty*(page-1)
            category_querySet = Categories.objects.values_list('category_name')
            possible_categories = []
            for query_member in category_querySet:
                possible_categories.append(query_member[0])
            po = PossibleOrders()
        else:
            af = None
            computers = None
            counter = None
            qtySelect = None
            autoFilters = None
            possible_types = None
            po = PossibleOrders()
        # cattyp = CatTyp()
        # removeKeyword(request)
        return render(request, 'index.html', {
            'computers': computers,
            "counter": counter,
            "qtySelect": qtySelect,
            "autoFilters": af,
            "cattyp": cattyp,
            "poscat": possible_categories,
            "po": po,
        })

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
    rc = RecordChoices()
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
        return HttpResponse(
            template.render({'computer': computer,
                             'bat_list': batteries,
                             "ram_list": rams,
                             "hdd_list": hdds,
                             "rc": rc}, request))

@csrf_exempt
def delete(request, int_index):
    print("DELETE")
    if request.method == 'POST':
        print("This was POST request")
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
        if not Computers.objects.filter(f_manufacturer=manufacturer.id_manufacturer).exists():
            manufacturer.delete()


@csrf_exempt
def mass_delete(request):
    print("Mass delete")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    for record_index in data:
        recordDeleteByIndex(record_index)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def mass_excel(request):
    print("Mass excel")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    excel_file = createExcelFile(data)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(excel_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.xlsx"
    excel_file.close()
    return response


@csrf_exempt
def cat_change(request):
    print("Mass cat_change")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    changeCategoriesUsingDict(data)
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def ord_assign(request):
    print("Mass ord_change")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    print(data)
    assignComputersToOrderUsingDict(data)
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def categories(request):
    print("Categories")
    if request.method == 'POST':
        print("This was POST request")
        save_category(request.POST.get("item_name"))
        print("Finished")
    if request.method == 'GET':
        print("This was GET request")
    categories = get_categories_list()
    print(categories)
    template = loader.get_template('items.html')
    return HttpResponse(template.render({'items': categories}, request))


@csrf_exempt
def delCat(request, int_index):
    print("Delete category")
    if request.method == 'POST':
        print("This was POST request")
        deleteCategory(int_index)
    if request.method == 'GET':
        print("This was GET request")


@csrf_exempt
def cat_edit(request):
    print("cat_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_category(data)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def types(request):
    print("types")
    if request.method == 'POST':
        print("This was POST request")
        save_type(request.POST.get("item_name"))
    if request.method == 'GET':
        print("This was GET request")
    types = get_types_list()
    template = loader.get_template('items.html')
    return HttpResponse(template.render({'items': types}, request))


@csrf_exempt
def delTyp(request, int_index):
    print("Delete type")
    if request.method == 'POST':
        print("This was POST request")
        deleteType(int_index)
    if request.method == 'GET':
        print("This was GET request")


@csrf_exempt
def typ_edit(request):
    print("typ_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_type(data)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def testers(request):
    print("testers")
    if request.method == 'POST':
        print("This was POST request")
        save_tester(request.POST.get("item_name"))
    if request.method == 'GET':
        print("This was GET request")
    testers = get_testers_list()
    template = loader.get_template('items.html')
    return HttpResponse(template.render({'items': testers}, request))


@csrf_exempt
def delTes(request, int_index):
    print("Delete tester")
    message = ""
    if request.method == 'POST':
        print("This was POST request")
        deleteTester(int_index)
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('items.html')
    return HttpResponse(template.render({'items': testers}, request))


@csrf_exempt
def tes_edit(request):
    print("tes_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_tester(data)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def new_record(request):
    print("new_record")
    rc = RecordChoices()
    if request.method == 'POST':
        print("This was POST request")
        rta = record_to_add(request.POST.copy())
        rta.save()
        if rta.isSaved():
            return HttpResponse("Success", request)
        else:
            template = loader.get_template('new_record.html')
            return HttpResponse(template.render({"rtac": rc, "error_message": rta.get_error_message()}, request))
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('new_record.html')
    return HttpResponse(template.render({"rc": rc}), request)


@csrf_exempt
def cat_to_sold(request):
    print("cat_to_sold")
    if request.method == 'POST':
        print("This was POST request")
        executor = ExecutorOfCatToSold(request.POST.copy())
        if executor.validated:
            executor.write_to_database()
            return HttpResponse("Success", request)
        else:
            computers = computersForCatToSold(request.GET.copy())
            template = loader.get_template('catToSold.html')
            return HttpResponse(template.render({'computers': computers, "error_message": executor.get_error_message()}), request)
    if request.method == 'GET':
        print("This was GET request")
        computers = computersForCatToSold(request.GET.copy())
        template = loader.get_template('catToSold.html')
        return HttpResponse(template.render({'computers': computers}), request)


@csrf_exempt
def new_order(request):
    print("tes_edit")
    noc = NewOrderChoices()
    if request.method == 'POST':
        print("This was POST request")
        no = NewOrder(request.POST.copy())
        no.save()
        if no.isSaved():
            return HttpResponse("Success", request)
        else:
            template = loader.get_template('new_order.html')
            return HttpResponse(template.render({"noc": noc, "error_message": no.get_error_message()}), request)
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('new_order.html')
    return HttpResponse(template.render({"noc": noc}), request)


@csrf_exempt
def edit_order(request, int_index):
    print("EDIT order")
    ote = OrderToEdit(int_index)
    if request.method == 'POST':
        print("This was POST request")
        ote.set_new_data(request.POST.copy())
        if ote.isSaved():
            return HttpResponse("Success", request)
        else:
            template = loader.get_template('order_edit.html')
            return HttpResponse(template.render({"ote": ote, "error_message": ote.get_error_message()}), request)
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('order_edit.html')
    return HttpResponse(template.render({"ote": ote}), request)