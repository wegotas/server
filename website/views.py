from django.http import HttpResponse
from website.logic import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from website.forms import *
import re
from decimal import Decimal


@csrf_exempt
def index(request):
    return render(request, 'main.html', {
        "typcat": TypCat(),
        'so': SearchOptions()
    })


@csrf_exempt
def drives_view(request):
    hh = HddHolder(request.GET.copy())
    return render(request, 'main.html', {
        "typcat": TypCat(),
        'hh': hh,
        'so': SearchOptions()
    })


@csrf_exempt
def lots_view(request):
    lh = LotsHolder(request.GET.copy())
    return render(request, 'main.html', {
        "typcat": TypCat(),
        'lh': lh,
        'so': SearchOptions()
    })


@csrf_exempt
def drive_orders_view(request):
    oh = DriveOrdersHolder(request.GET.copy())
    return render(request, 'main.html', {
        "typcat": TypCat(),
        'oh': oh,
        'so': SearchOptions()
    })


@csrf_exempt
def chargers_view(request):
    cch = ChargerCategoriesHolder(request.GET.copy())
    return render(request, 'main.html', {
        'cch': cch,
        "typcat": TypCat(),
        'so': SearchOptions()
    })


@csrf_exempt
def orders_view(request):
    counter = Counter()
    orders = OrdersClass(request.GET.copy())
    return render(request, 'main.html', {
        "counter": counter,
        "typcat": TypCat(),
        "orders": orders,
        'so': SearchOptions()
    })


@csrf_exempt
def sold_view(request):
    qty = int(request.GET.get('qty', 10))
    page = int(request.GET.get('page', 1))
    autoFilters = AutoFilter(request.GET.copy())
    qtySelect = QtySelect(qty)
    computers = Computers.objects.exclude(f_sale__isnull=True)
    computers = autoFilters.filter(computers)
    af = AutoFiltersFromSoldComputers(computers)
    paginator = Paginator(computers, qty)
    computers = paginator.get_page(page)
    counter = Counter()
    counter.count = qty * (page - 1)
    return render(request, 'main.html', {
        'computers': computers,
        "counter": counter,
        "qtySelect": qtySelect,
        "autoFilters": af,
        "typcat": TypCat(),
        "poscat": Categories.objects.values_list('category_name', flat=True),
        'so': SearchOptions()
    })


@csrf_exempt
def typcat_view(request):
    data_dict = request.GET.copy()
    qty = int(data_dict.get('qty', 10))
    page = int(data_dict.get('page', 1))
    autoFilters = AutoFilter(data_dict)
    computers = Computers.objects.filter(
        f_type=Types.objects.get(type_name=data_dict.get('type')),
        f_category=Categories.objects.get(category_name=data_dict.get('cat')),
        f_sale=None
    ).exclude(f_id_comp_ord__isnull=False) \
        .exclude(f_sale__isnull=False)
    computers = autoFilters.filter(computers)
    qtySelect = QtySelect(qty)
    af = AutoFiltersFromComputers(computers)
    paginator = Paginator(computers, qty)
    computers = paginator.get_page(page)
    counter = Counter()
    counter.count = qty * (page - 1)
    return render(request, 'main.html', {
        'computers': computers,
        "counter": counter,
        "qtySelect": qtySelect,
        "autoFilters": af,
        "typcat": TypCat(),
        "poscat": Categories.objects.values_list('category_name', flat=True),
        "po": PossibleOrders(),
        'so': SearchOptions()
    })


@csrf_exempt
def search_view(request):

    data_dict = request.GET.copy()
    qty = int(request.GET.get('qty', 10))
    page = int(request.GET.get('page', 1))
    computers = Computers.objects.all()
    computers = search(data_dict.get('keyword', None), computers)
    so = SearchOptions()
    for option in so.options:
        computers = option.search(computers, data_dict.pop(option.tagname, ""))
    autoFilters = AutoFilter(data_dict)
    computers = autoFilters.filter(computers)
    qtySelect = QtySelect(qty)
    af = AutoFiltersFromComputers(computers)
    paginator = Paginator(computers, qty)
    computers = paginator.get_page(page)
    counter = Counter()
    counter.count = qty * (page - 1)
    '''

    scl = SearchComputersLogic(request.GET.copy())

    print('STARTING')

    for computer in scl.iterate():
        print(scl.index)
        print(computer)

    print('ENDING')

    '''
    return render(request, 'main.html', {
        'computers': computers,
        "counter": counter,
        "qtySelect": qtySelect,
        "autoFilters": af,
        "typcat": TypCat(),
        "poscat": Categories.objects.values_list('category_name', flat=True),
        'so': so,
        "global": True
    })
    '''
    return render(request, 'main.html', {
        'computers': None,
        "counter": None,
        "qtySelect": None,
        "autoFilters": None,
        "typcat": TypCat(),
        "poscat": Categories.objects.values_list('category_name', flat=True),
        'so': None,
        "global": True
    })
    '''


@csrf_exempt
def export_view(request):
    if request.method == 'POST':
        form = ExportComputersForm(request.POST)
        if form.is_valid():

            query = None
            if form.cleaned_data['ordered']:
                query = Q(f_sale__isnull=True, f_id_comp_ord__isnull=False)
            if form.cleaned_data['sold']:
                if not query:
                    query = Q(f_sale__isnull=False)
                else:
                    query = query | Q(f_sale__isnull=False)
            if form.cleaned_data['no_status']:
                if not query:
                    query = Q(f_id_comp_ord__isnull=True, f_sale__isnull=True)
                else:
                    query = query | Q(f_id_comp_ord__isnull=True, f_sale__isnull=True)

            serials = Computers.objects.filter(query).values_list('id_computer', flat=True)

            generator = None

            response = HttpResponse(content_type="application/ms-excel")
            if form.cleaned_data['file_type'] == 'EXCEL':
                generator = ExcelGenerator()
                response["Content-Disposition"] = "attachment; filename=computers.xlsx"
            if form.cleaned_data['file_type'] == 'CSV':
                generator = CsvGenerator()
                response["Content-Disposition"] = "attachment; filename=computers.csv"

            file = generator.generate_file(indexes=serials)
            response.write(file.getvalue())
            file.close()
            return response

    if request.method == 'GET':
        form = ExportComputersForm()
    return render(request, 'exports.html', {
        "typcat": TypCat(),
        "form": form,
        'so': SearchOptions()
    })


@csrf_exempt
def edit(request, int_index):
    cte = ComputerToEdit(int_index=int_index)
    if request.method == 'POST':
        cte.process_post(request.POST.copy())
        if cte.success():
            return render(request, 'success.html')
        else:
            return render(request, 'failure.html', {'message': cte.message}, status=404)
    if request.method == 'GET':
        cte.process_get()
        return render(request, 'computer_edit.html', {'record': cte.record})


@csrf_exempt
def edit_by_serial(request, serial):
    cte = ComputerToEdit(serial=serial)
    if request.method == 'POST':
        cte.process_post(request.POST.copy())
        if cte.success():
            return render(request, 'success.html')
        else:
            return render(request, 'failure.html', {'message': cte.message}, status=404)
    if request.method == 'GET':
        cte.process_get()
        return render(request, 'computer_edit.html', {'record': cte.record})


@csrf_exempt
def remove_ramstick_from_computer(request, ramstick_id, computer_id):
    def get_number(value):
        try:
            return Decimal(re.findall("\d*[,.]?\d*", value)[0])
        except TypeError:
            return 0

    def get_total_ram():
        rams_sizes = Rams.objects.filter(
            ramtocomp__f_id_computer_ram_to_com=Computers.objects.get(id_computer=computer_id)
        ).values_list('capacity', flat=True)
        if not rams_sizes:
            return '0 GB'
        summary = 0
        for ram_size in rams_sizes:
            summary += get_number(ram_size)
        return str(summary) + ' GB'

    ramstick = Rams.objects.get(id_ram=ramstick_id)
    ramstick_type = ramstick.type
    RamToComp.objects.filter(
        f_id_computer_ram_to_com=Computers.objects.get(id_computer=computer_id),
        f_id_ram_ram_to_com=ramstick
    ).delete()
    try:
        ramstick.delete()
    except:
        pass
    computer = Computers.objects.get(id_computer=computer_id)
    ramsize = RamSizes.objects.get_or_create(ram_size_text=get_total_ram())[0]
    computer.f_ram_size = ramsize
    computer.save()
    if RamToComp.objects.filter(f_id_computer_ram_to_com=Computers.objects.get(id_computer=computer_id)).count() > 0:
        return HttpResponse("")

    ram = Rams.objects.get_or_create(
        ram_serial='Nonexistant',
        capacity='0',
        clock='0',
        type=ramstick_type,
    )[0]
    RamToComp.objects.get_or_create(
        f_id_computer_ram_to_com=Computers.objects.get(id_computer=computer_id),
        f_id_ram_ram_to_com=ram
    )
    return render(request, 'nonexistant_ramstick_template.html', {'id_computer': computer_id, 'ramstick': ram})


@csrf_exempt
def remove_drive_from_computer(request, drive_id, computer_id):
    Computerdrives.objects.filter(
        f_id_computer=Computers.objects.get(id_computer=computer_id),
        f_drive=Drives.objects.get(hdd_id=drive_id)
    ).delete()
    return HttpResponse("Succesfully removed drive from computer")


@csrf_exempt
def observations_to_add(request, int_index, keyword):
    searchfields = (
        'full_name',
        'shortcode',
        'f_id_observation_category__category_name',
        'f_id_observation_subcategory__subcategory_name'
    )
    observations = Observations.objects.exclude(
        id_observation__in=Computerobservations.objects.filter(
            f_id_computer=int_index
        ).values_list('f_id_observation', flat=True)
    ).filter(get_query_for_item_search_from_computer_edit(keyword, searchfields))
    return render(request, 'observations_to_add.html', {'observations': observations})


@csrf_exempt
def assign_observation_to_computer(request, observation_id, computer_id):
    observation = Observations.objects.get(id_observation=observation_id)
    Computerobservations.objects.create(
        f_id_computer=Computers.objects.get(id_computer=computer_id),
        f_id_observation=observation
    )
    return render(request, 'observation_template.html', {'observation': observation, 'computer_id': computer_id})


@csrf_exempt
def remove_observation_from_computer(request, observation_id, computer_id):
    Computerobservations.objects.filter(
        f_id_computer=Computers.objects.get(id_computer=computer_id),
        f_id_observation=Observations.objects.get(id_observation=observation_id)
    ).delete()
    return HttpResponse("Succesfully removed observation from computer")

@csrf_exempt
def remove_battery_from_computer(request, battery_id, computer_id):
    BatToComp.objects.filter(
        f_id_computer_bat_to_com=Computers.objects.get(id_computer=computer_id),
        f_bat_bat_to_com=Batteries.objects.get(id_battery=battery_id)
    ).delete()
    return HttpResponse("Succesfully removed battery from computer")


@csrf_exempt
def get_observation(request, observation_id):
    return render(request, 'observation_template.html', {
        'observation': Observations.objects.get(id_observation=observation_id)})


@csrf_exempt
def ramsticks_to_add(request, int_index, keyword):
    searchfields = (
        'ram_serial',
        'capacity',
        'clock',
        'type'
    )
    rams = Rams.objects.exclude(
        id_ram__in=RamToComp.objects.filter(
            f_id_computer_ram_to_com=int_index
        ).values_list('f_id_ram_ram_to_com', flat=True)
    ).filter(get_query_for_item_search_from_computer_edit(keyword, searchfields))
    return render(request, 'rams_to_add.html', {'rams': rams})


@csrf_exempt
def get_ramstick(request, ramstick_id):
    return render(request, 'ramstick_template.html', {'ramstick': Rams.objects.get(id_ram=ramstick_id)})


@csrf_exempt
def add_nonexistant_ramstick(request, computer_id):
    ram = Rams.objects.get_or_create(
        ram_serial='Nonexistant',
        capacity='0',
        clock='0',
        type='N/A',
    )[0]
    RamToComp.objects.get_or_create(
        f_id_computer_ram_to_com=Computers.objects.get(id_computer=computer_id),
        f_id_ram_ram_to_com=ram
    )
    return render(request, 'nonexistant_ramstick_template.html', {'id_computer': computer_id, 'ramstick': ram})


@csrf_exempt
def processors_to_add(request, int_index, keyword):
    searchfields = (
        'f_manufacturer__manufacturer_name',
        'model_name',
        'stock_clock',
        'max_clock',
        'cores',
        'threads'
    )
    processors = Processors.objects.exclude(
        id_processor__in=Computerprocessors.objects.filter(
            f_id_computer=int_index
        ).values_list('f_id_processor', flat=True)
    ).filter(get_query_for_item_search_from_computer_edit(keyword, searchfields))
    return render(request, 'processors_to_add.html', {'processors': processors})


@csrf_exempt
def get_processor(request, processor_id):
    return render(request, 'processor_template.html', {'processor': Processors.objects.get(id_processor=processor_id)})


@csrf_exempt
def gpus_to_add(request, int_index, keyword):
    searchfields = ('f_id_manufacturer__manufacturer_name', 'gpu_name')
    gpus = Gpus.objects.exclude(
        id_gpu__in=Computergpus.objects.filter(
            f_id_computer=int_index
        ).values_list('f_id_gpu', flat=True)
    ).filter(get_query_for_item_search_from_computer_edit(keyword, searchfields))
    return render(request, 'gpus_to_add.html', {'gpus': gpus})


@csrf_exempt
def get_gpu(request, gpu_id):
    return render(request, 'gpu_template.html', {'gpu': Gpus.objects.get(id_gpu=gpu_id)})


@csrf_exempt
def mass_delete(request):
    data = JSONParser().parse(request)
    for record_index in data:
        cte = ComputerToEdit(int_index=record_index)
        cte.delete_record()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def mass_excel(request):
    data = JSONParser().parse(request)
    generator = ExcelGenerator()
    excel_file = generator.generate_file(indexes=data)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(excel_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.xlsx"
    excel_file.close()
    return response


@csrf_exempt
def mass_csv(request):
    data = JSONParser().parse(request)
    generator = CsvGenerator()
    csv_file = generator.generate_file(indexes=data)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(csv_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.csv"
    csv_file.close()
    return response


@csrf_exempt
def mass_qr_print(request):
    cmsp = ComputerMultipleSerialPrinter(JSONParser().parse(request))
    cmsp.print()
    return HttpResponse('Print job is sent')


@csrf_exempt
def mass_qr_print_with_printer(request, printer):
    cmsp = ComputerMultipleSerialPrinter(JSONParser().parse(request), printer)
    cmsp.print()
    return HttpResponse('Print job is sent')


@csrf_exempt
def cat_change(request):
    data = JSONParser().parse(request)
    category_name = next(iter(data))
    indexes = data[category_name]
    category = Categories.objects.get(category_name=category_name)
    for ind in indexes:
        computer = Computers.objects.get(id_computer=ind)
        computer.f_category = category
        computer.save()
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def ord_assign(request):
    """
    This method is responsible for assigning computer_ids to a certain order.
    :param request: request initiated by javascript client side.
    :return: Nonsensical http response. Since this response should not be processed and only status code is reacted to.
    """
    data = JSONParser().parse(request)
    order_name = next(iter(data))
    order = Orders.objects.get(order_name=order_name)
    for indx in data[order_name]:
        compord = CompOrd.objects.create(is_ready=0, f_order_id_to_order=order)
        Computers.objects.select_for_update().filter(id_computer=indx).update(f_id_comp_ord=compord)
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def computer_form_factors(request):
    def get_computer_form_factors():
        computer_form_factor_list = []
        for computer_form_factor in ComputerFormFactors.objects.all():
            item = Item(computer_form_factor.id_computer_form_factor, computer_form_factor.form_factor_name)
            computer_form_factor_list.append(item)
        return computer_form_factor_list

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != '':
            ComputerFormFactors.objects.get_or_create(form_factor_name=name)
    if request.method == 'GET':
        pass
    return render(request, 'items.html', {'items': get_computer_form_factors()})


@csrf_exempt
def del_computer_form_factor(request, int_index):
    if request.method == 'POST':
        ComputerFormFactors.objects.get(id_computer_form_factor=int_index).delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def computer_form_factor_edit(request):
    data = JSONParser().parse(request)
    computer_form_factor = ComputerFormFactors.objects.get(id_computer_form_factor=data["ItemId"])
    computer_form_factor.form_factor_name = data["ItemName"]
    computer_form_factor.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def receivedbatches(request):
    def get_received_batches_list():
        received_batchlist = []
        for batch in Receivedbatches.objects.all():
            new_item = Item(batch.id_received_batch, batch.received_batch_name)
            received_batchlist.append(new_item)
        return received_batchlist

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != "":
            Receivedbatches.objects.get_or_create(received_batch_name=name)
    if request.method == 'GET':
        pass
    return render(request, 'items.html', {'items': get_received_batches_list()})


@csrf_exempt
def delreceivedBatch(request, int_index):
    if request.method == 'POST':
        Receivedbatches.objects.get(id_received_batch=int_index).delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def recieved_batch_edit(request):
    data = JSONParser().parse(request)
    received_batch = Receivedbatches.objects.get(id_received_batch=data["ItemId"])
    received_batch.received_batch_name = data["ItemName"]
    received_batch.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def categories(request):
    def get_categories_list():
        catlist = []
        for cat in Categories.objects.all():
            newItem = Item(cat.id_category, cat.category_name, cat.permanent)
            catlist.append(newItem)
        return catlist

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != "":
            Categories.objects.get_or_create(category_name=name)
    if request.method == 'GET':
        pass
    return render(request, 'items.html', {'items': get_categories_list()})


@csrf_exempt
def delCat(request, int_index):
    if request.method == 'POST':
        cat = Categories.objects.get(id_category=int_index)
        if cat.permanent != 1:
            cat.delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def cat_edit(request):
    data = JSONParser().parse(request)
    cat = Categories.objects.get(id_category=data["ItemId"])
    if cat.permanent != 1:
        cat.category_name = data["ItemName"]
        cat.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def types(request):
    def get_types_list():
        typeslist = []
        for typie in Types.objects.all():
            newItem = Item(typie.id_type, typie.type_name)
            typeslist.append(newItem)
        return typeslist

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != "":
            Types.objects.get_or_create(type_name=name)
    if request.method == 'GET':
        pass
    return render(request, 'items.html', {'items': get_types_list()})


@csrf_exempt
def delTyp(request, int_index):
    if request.method == 'POST':
        Types.objects.get(id_type=int_index).delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def typ_edit(request):
    data = JSONParser().parse(request)
    typ = Types.objects.get(id_type=data["ItemId"])
    typ.type_name = data["ItemName"]
    typ.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def testers(request):
    def get_testers_list():
        testerslist = []
        for tester in Testers.objects.all():
            newItem = Item(tester.id_tester, tester.tester_name)
            testerslist.append(newItem)
        return testerslist

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != "":
            Testers.objects.get_or_create(tester_name=name)
    if request.method == 'GET':
        pass
    return render(request, 'items.html', {'items': get_testers_list()})


@csrf_exempt
def delTes(request, int_index):
    if request.method == 'POST':
        Testers.objects.get(id_tester=int_index).delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def tes_edit(request):
    data = JSONParser().parse(request)
    tes = Testers.objects.get(id_tester=data["ItemId"])
    tes.tester_name = data["ItemName"]
    tes.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observations(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return render(request, "observations.html")


@csrf_exempt
def observation_category(request):
    def get_observation_category_list():
        lst = []
        for member in Observationcategory.objects.all():
            lst.append(Item(item_id=member.id_observation_category, item_name=member.category_name))
        return lst

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != "":
            Observationcategory.objects.get_or_create(category_name=name)
    if request.method == 'GET':
        pass
    return render(request, "observationsCategorySubtemplate.html", {'items': get_observation_category_list()})


@csrf_exempt
def del_observation_category(request, int_index):
    if request.method == 'POST':
        Observationcategory.objects.get(id_observation_category=int_index).delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def observation_category_edit(request):
    data = JSONParser().parse(request)
    item = Observationcategory.objects.get(id_observation_category=data["ItemId"])
    item.category_name = data["ItemName"]
    item.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observation_subcategory(request):
    def get_observation_subcategory_list():
        lst = []
        for member in Observationsubcategory.objects.all():
            lst.append(Item(item_id=member.id_observation_subcategory, item_name=member.subcategory_name))
        return lst

    if request.method == 'POST':
        name = request.POST.get("item_name")
        if name != "":
            Observationsubcategory.objects.get_or_create(subcategory_name=name)
    if request.method == 'GET':
        pass
    return render(request, "observationsSubcategorySubtemplate.html", {'items': get_observation_subcategory_list()})


@csrf_exempt
def del_observation_subcategory(request, int_index):
    if request.method == 'POST':
        Observationsubcategory.objects.get(id_observation_subcategory=int_index).delete()
    if request.method == 'GET':
        pass
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observation_subcategory_edit(request):
    data = JSONParser().parse(request)
    item = Observationsubcategory.objects.get(id_observation_subcategory=data["ItemId"])
    item.subcategory_name = data["ItemName"]
    item.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observations_details(request):
    if request.method == 'POST':
        ota = ObservationToAdd(request.POST)
        if ota.validated():
            ota.process()
    if request.method == 'GET':
        pass
    return render(request, "observationsDetailsSubtemplate.html",
        {
            "categories": Observationcategory.objects.values_list('category_name', flat=True),
            "subcategories": Observationsubcategory.objects.values_list('subcategory_name', flat=True),
            'observations': ObservationsCollection()
        }
    )


@csrf_exempt
def delete_observations_details(request, int_index):
    Observations.objects.get(id_observation=int_index).delete()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def edit_observations_details(request):
    data = JSONParser().parse(request)
    observation = Observations.objects.get(id_observation=data['observation_id'])
    observation.shortcode = data['shortcode']
    observation.full_name = data['fullname']
    observation.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def new_record(request):
    def remove_none_if_exists(query):
        lst = list(query)
        try:
            lst.remove(None)
        except ValueError:
            pass
        return lst

    def get_unique_models_field_values(model, field):
        return remove_none_if_exists(model.objects.order_by(field).values_list(field, flat=True).distinct())

    rc = RecordChoices()
    many_to_many_unique_values_dict = {
        "RAMs": {
            "capacities": get_unique_models_field_values(Rams, "capacity"),
            "clocks": get_unique_models_field_values(Rams, "clock"),
            "types": get_unique_models_field_values(Rams, "type")
        },
        "Processors": {
            "manufacturer_names": get_unique_models_field_values(Processors, "f_manufacturer__manufacturer_name"),
            "model_names": get_unique_models_field_values(Processors, "model_name"),
            "stock_clocks": get_unique_models_field_values(Processors, "stock_clock"),
            "max_clocks": get_unique_models_field_values(Processors, "max_clock"),
            "cores": get_unique_models_field_values(Processors, "cores"),
            "threads": get_unique_models_field_values(Processors, "threads"),
        },
        "GPUs": {
            "gpu_names": get_unique_models_field_values(Gpus, "gpu_name"),
            "manufacturer_names": get_unique_models_field_values(Gpus, "f_id_manufacturer__manufacturer_name"),
        }
    }

    if request.method == 'POST':
        rta = RecordToAdd(request.POST.copy())
        if rta.validate():
            rta.save()
            return render(request, 'success.html')
        return render(request, 'new_record.html', {
            "rc": rc,
            "error_message": rta.get_error_message(),
            "many_to_many_unique_values_dict": many_to_many_unique_values_dict
        })
    if request.method == 'GET':
        return render(request, 'new_record.html', {"rc": rc, "many_to_many_unique_values_dict": many_to_many_unique_values_dict})


@csrf_exempt
def cat_to_sold(request):
    computers = Computers.objects.filter(id_computer__in=request.GET.copy().pop('id'))
    if request.method == 'POST':
        executor = ExecutorOfCatToSold(request.POST.copy())
        if executor.validated:
            executor.write_to_database()
            return render(request, 'success.html')
        else:
            return render(request, 'catToSold.html', {
                'computers': computers,
                "error_message": executor.get_error_message()
            })
    if request.method == 'GET':
        return render(request, 'catToSold.html', {'computers': computers})


@csrf_exempt
def new_order(request):
    noc = NewOrderChoices()
    if request.method == 'POST':
        no = NewOrder(request.POST.copy())
        no.save()
        if no.is_saved():
            return render(request, 'success.html')
        else:
            return render(request, 'new_order.html', {
                "noc": noc,
                "error_message": no.get_error_message()
            })
    if request.method == 'GET':
        pass
    return render(request, 'new_order.html', {"noc": noc})


@csrf_exempt
def edit_order(request, int_index):
    ote = OrderToEdit(int_index)
    if request.method == 'POST':
        ote.set_new_data(request.POST.copy())
        if ote.hasErrors():
            return render(request, 'success.html')
        else:
            return render(request, 'order_edit.html', {
                "ote": ote,
                "error_message": ote.get_error_message()
            })
    if request.method == 'GET':
        pass
    return render(request, 'order_edit.html', {"ote": ote, })


@csrf_exempt
def delete_order(request, int_index):
    if request.method == 'POST':
        try:
            order = Orders.objects.get(id_order=int_index)
            OrdTes.objects.filter(f_order=order).delete()
            order.delete()
            return render(request, 'success.html')
        except Exception as e:
            return HttpResponse(str(e), status=404)
    if request.method == 'GET':
        return HttpResponse("You shouldn't be here", status=404)


@csrf_exempt
def strip_order(request, int_index):
    def _strip_order_of_computer():
        computer = Computers.objects.get(id_computer=int_index)
        compord = CompOrd.objects.get(id_comp_ord=computer.f_id_comp_ord.id_comp_ord)
        computer.f_id_comp_ord = None
        computer.save()
        compord.delete()

    if request.method == 'POST':
        _strip_order_of_computer()
        return HttpResponse(status=200)
    if request.method == 'GET':
        return HttpResponse('This should not be returned', status=404)


@csrf_exempt
def computer_search_table_from_order(request):
    if request.method == 'POST':
        return HttpResponse("Disallowed action", status=404)
    if request.method == 'GET':
        keyword = request.GET['keyword']
        searchfields = (
            'computer_serial',
            'f_model__model_name',
            'f_manufacturer__manufacturer_name'
        )
        query = get_query_for_item_search_from_computer_edit(keyword, searchfields)
        computers = Computers.objects.filter(query)
        computers = computers.filter(f_id_comp_ord__isnull=True, f_sale__isnull=True)
        return render(request, 'computer_search_from_order_table.html', {'computers': computers})


@csrf_exempt
def add_computer_to_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Orders.objects.get(id_order=order_id)
            comp_ord = CompOrd.objects.create(is_ready=0, f_order_id_to_order=order)
            computer = Computers.objects.get(id_computer=JSONParser().parse(request)['computer_id'])
            computer.f_id_comp_ord = comp_ord
            computer.save()
            counter = Computers.objects.filter(f_id_comp_ord__f_order_id_to_order=order).count()
            return render(request, 'computer_search_from_order_row.html', {'counter': counter, 'computer': computer})
        except Exception as e:
            return HttpResponse(e, status=404)
    if request.method == 'GET':
        return HttpResponse('Get request not Implemented', status=404)


@csrf_exempt
def order_excel(request, int_index):
    indexes = Computers.objects.filter(
        f_id_comp_ord__f_order_id_to_order=int_index).values_list('id_computer', flat=True)
    generator = ExcelGenerator()
    excel_file = generator.generate_file(indexes=indexes)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(excel_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.xlsx"
    excel_file.close()
    return response


@csrf_exempt
def order_csv(request, int_index):
    indexes = Computers.objects.filter(
        f_id_comp_ord__f_order_id_to_order=int_index).values_list('id_computer', flat=True)
    generator = CsvGenerator()
    csv_file = generator.generate_file(indexes=indexes)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(csv_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.csv"
    csv_file.close()
    return response


@csrf_exempt
def hdd_edit(request, int_index):
    hte = HddToEdit(int_index)
    if request.method == 'POST':
        hte.process_edit(request.POST.copy())
        return render(request, 'success.html')
    if request.method == 'GET':
        return render(request, 'hdd_edit.html', {'hte': hte})


@csrf_exempt
def hdd_delete(request, int_index):
    message = try_drive_delete_and_get_message(pk=int_index)
    if message:
        return HttpResponse(message, status=404)
    else:
        return render(request, 'success.html')


def view_pdf(request, int_index):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            hdd = Drives.objects.get(hdd_id=int_index)
            tf = tarfile.open(os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), hdd.f_lot.lot_name + '.tar'))
            pdf_content = tf.extractfile(tf.getmember(hdd.tar_member_name)).read()
            return HttpResponse(pdf_content, content_type='application/pdf')
        except:
            return render(request, 'failure.html',
                          {'message': "Failed to fetch pdf.\r\nMost likely cause is that pdf is nonexistant."},
                          status=404)


@csrf_exempt
def drive_order_content(request, int_index):
    hoch = HddOrderContentHolder(int_index)
    if request.method == 'POST':
        try:
            hoch.edit(request.POST.copy())
            return render(request, 'success.html')
        except Exception as e:
            return render(request, 'failure.html', {'message': str(e)}, status=404)
    if request.method == 'GET':
        hoch.filter(request.GET.copy())
        return render(request, 'hdd_order_content.html', {'hoch': hoch})


@csrf_exempt
def drive_order_content_csv(request, int_index):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        hocc = HddOrderContentCsv(int_index)
        csv_file = hocc.createCsvFile()
        response = HttpResponse(content_type="application/ms-excel")
        response.write(csv_file.getvalue())
        response["Content-Disposition"] = "attachment; filename=computers.csv"
        csv_file.close()
        return response


@csrf_exempt
def drive_delete_order(request, int_index):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        hod = HddOrderToDelete(int_index)
        hod.delete()
        if hod.success:
            return render(request, 'success.html')
        return render(request, 'failure.html', {'message': hod.message}, status=404)


@csrf_exempt
def drive_order_view(request):
    if request.method == 'POST':
        form = DriveOrderDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dop = DriveOrderProcessor(request.FILES['document'])
                dop.process_data()
                if dop.message != '':
                    return render(request, 'partial_success.html', {'message': dop.message})
                return render(request, 'success.html')
            except Warning as warning:
                return render(request, 'failure.html', {'message': f'{warning})'})
        else:
            return render(request, 'uploader.html', {'form': form})
    else:
        form = DriveOrderDocumentForm()
        return render(request, 'uploader.html', {'form': form})


@csrf_exempt
def process_tar_view(request):
    if request.method == 'POST':
        form = TarDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                tp = TarProcessor(request.FILES['document'])
                tp.process_data()
                if tp.message:
                    return render(request, 'partial_success.html', {'message': tp.message})
                return render(request, 'success.html')
            except Warning as warning:
                return render(request, 'failure.html', {'message': f'{warning})'})
        else:
            return render(request, 'uploader.html', {'form': form})
    else:
        form = TarDocumentForm()
        return render(request, 'uploader.html', {'form': form})


@csrf_exempt
def lot_content(request, int_index):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        lch = LotContentHolder(int_index)
        lch.filter(request.GET.copy())
        return render(request, 'lot_content.html', {'lch': lch})


@csrf_exempt
def success(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return render(request, 'success.html')


@csrf_exempt
def serial_processing(request, serial):
    csp = ChargerSerialProcessor(serial)
    if request.method == 'POST':
        csp.process()
        if csp.message == '':
            return render(request, 'success.html')
        else:
            return render(request, 'failure.html', {'message': csp.message})
    if request.method == 'GET':
        # csp.proccess()
        if csp.serial_exists():
            ch = ChargerHolder(serial=serial)
            return render(request, 'charger_view.html', {'ch': ch})
        else:
            return render(request, 'charger_nonexistant.html')


@csrf_exempt
def delete_charger_from_scan(request, serial):
    if request.method == 'POST':
        Chargers.objects.get(charger_serial=serial.split('_')[2]).delete()
        return HttpResponse('POST request finished', status=200)
    if request.method == 'GET':
        return HttpResponse('Get request not Implemented', status=404)


@csrf_exempt
def edit_charger(request, int_index):
    ccte = ChargerCategoryToEdit(int_index)
    if request.method == 'POST':
        ccte.process(request.POST.copy())
        if ccte.isValidData:
            return render(request, 'success.html')
        else:
             return render(request, 'failure.html', {'message': ccte.message})
    if request.method == 'GET':
        return render(request, 'charger_edit.html', {'ccte': ccte})


@csrf_exempt
def edit_charger_serial(request, int_index):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        charger = Chargers.objects.get(charger_id=data['Index'])
        charger.charger_serial = data['Serial']
        charger.save()
        return render(request, 'success.html')
    if request.method == 'GET':
        pass


@csrf_exempt
def print_charger_serial(request, int_index):
    if request.method == 'POST':
        csp = ChargerSingleSerialPrinter(JSONParser().parse(request))
        csp.print()
        return HttpResponse('Print job is sent')
    if request.method == 'GET':
        pass


@csrf_exempt
def print_chargers_serials(request, int_index):
    if request.method == 'POST':
        cdsp = ChargerDualSerialPrinter(JSONParser().parse(request))
        cdsp.print()
        return HttpResponse('Print job is sent')
    if request.method == 'GET':
        pass


@csrf_exempt
def delete_charger(request, int_index):
    if request.method == 'POST':
        Chargers.objects.get(charger_id=JSONParser().parse(request)['Index']).delete()
        return HttpResponse('Charger deleted')
    if request.method == 'GET':
        pass


@csrf_exempt
def delete_charger_category(request, int_index):
    if request.method == 'POST':
        try:
            ChargerCategories.objects.get(charger_category_id=int_index).delete()
        except Exception as e:
            return HttpResponse(str(e), status=404)
    if request.method == 'GET':
        pass


@csrf_exempt
def print_computer_qr(request, int_index):
    if request.method == 'POST':
        # Keep this comment
        # cssp = ComputerSingleSerialPrinter(JSONParser().parse(request))
        cssp = ComputerSingleSerialPrinter(int_index)
        cssp.print()
        return HttpResponse("Not implemented return", status=200)
    if request.method == 'GET':
        pass

@csrf_exempt
def print_computer_qr_with_printer(request, int_index, printer):
    if request.method == 'POST':
        # todo: Figure tout what to do with printing.
        # Keep this comment
        """
        if printer == "Godex_DT4x":
            cssp = ComputerSingleSerialPrinter(int_index, printer)
            cssp.print()
        elif printer == "Godex_g500":
            cmsp = ComputerMultipleSerialPrinter([int_index], printer)
            cmsp.print()
        """
        cssp = ComputerSingleSerialPrinter(int_index, printer)
        cssp.print()
        return HttpResponse("Not implemented return", status=200)
    if request.method == 'GET':
        pass
