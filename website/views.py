from django.http import HttpResponse
from ULCDTinterface.modelers import Computers, BatToComp
from django.template import loader
from website.logic import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from website.forms import *
import json


def index(request):
    print('index')
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data_dict = request.GET.copy()
    qty = get_qty(data_dict)
    page = get_page(data_dict)
    keyword = get_keyword(data_dict)
    autoFilters = AutoFilter(data_dict)
    typcat = TypCat()
    so = SearchOptions()

    if 'lots' in request.GET:
        lh = LotsHolder()
        lh.filter(request.GET.copy())
        return render(
            request,
            'main.html',
            {
                "typcat": typcat,
                'lh': lh,
                'so': so
            }
        )

    elif 'hdds' in request.GET:
        hh = HddHolder()
        hh.filter(request.GET.copy())
        return render(
            request,
            'main.html',
            {
                "typcat": typcat,
                'hh': hh,
                'so': so
            }
        )

    elif 'hdd_orders' in request.GET:
        oh = HddOrdersHolder()
        oh.filter(request.GET.copy())
        return render(
            request,
            'main.html',
            {
                "typcat": typcat,
                'oh': oh,
                'so': so
            }
        )

    if request.GET.get('chargers') == "True":
        #TODO: PRIDETI FILTRAVIMA
        cch = ChargerCategoriesHolder()
        cch.filter(request.GET.copy())
        return render(
            request,
            'main.html',
            {
                'cch': cch,
                "typcat": typcat,
                'so': so
            }
        )

    if keyword:
        computers = Computers.objects.all()
        computers = search(keyword, computers)
        for option in so.options:
            computers = option.search(computers, data_dict.pop(option.tagname, ""))
        computers = autoFilters.filter(computers)
        counter = Counter()
        qtySelect = QtySelect()
        af = AutoFiltersFromComputers(computers)
        category_queryset = Categories.objects.values_list('category_name')
        possible_categories = []
        for query_member in category_queryset:
            possible_categories.append(query_member[0])
        po = PossibleOrders()
        return render(
            request,
            'main.html',
            {
                'computers': computers,
                "counter": counter,
                "qtySelect": qtySelect,
                "autoFilters": af,
                "typcat": typcat,
                "poscat": possible_categories,
                "po": po,
                'so': so,
                "global": True
            }
        )

    elif request.GET.get('sold') == "True":
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
        return render(
            request,
            'main.html',
            {
                'computers': computers,
                "counter": counter,
                "qtySelect": qtySelect,
                "autoFilters": af,
                "typcat": typcat,
                "poscat": possible_categories,
                'so': so
            }
        )

    elif request.GET.get('orders') == "True":
        counter = Counter()
        orders = OrdersClass()
        orders.filter(data_dict)
        return render(
            request,
            'main.html',
            {
                "counter": counter,
                "typcat": typcat,
                "orders": orders,
                'so': so
            }
        )

    else:
        typ = data_dict.get('type')
        cat = data_dict.get('cat')
        data_dict.pop("sold", None)
        possible_categories = None
        if cat or typ:
            qtySelect = QtySelect()
            qtySelect.setDefaultSelect(qty)
            typeRecord = Types.objects.filter(type_name=typ)[:1].get()
            catRecord = Categories.objects.filter(category_name=cat)[:1].get()
            computers = Computers.objects.filter(
                f_type=typeRecord.id_type,
                f_category=catRecord.id_category,
                f_sale=None
            ).exclude(f_id_comp_ord__isnull=False)\
                .exclude(f_sale__isnull=False)
            computers = autoFilters.filter(computers)
            if keyword is not None:
                computers = search(keyword, computers)
            af = AutoFiltersFromComputers(computers)
            paginator = Paginator(computers, qty)
            computers = paginator.get_page(page)
            counter = Counter()
            counter.count = qty * (page - 1)
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
        return render(
            request,
            'main.html',
            {
                'computers': computers,
                "counter": counter,
                "qtySelect": qtySelect,
                "autoFilters": af,
                "typcat": typcat,
                "poscat": possible_categories,
                "po": po,
                'so': so
            }
        )


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
            template.render(
                {
                    'computer': computer,
                    'bat_list': batteries,
                    "ram_list": rams,
                    "hdd_list": hdds
                },
                request
            )
        )


@csrf_exempt
def edit(request, int_index):
    print("EDIT ")
    rc = RecordChoices()
    if request.method == 'POST':
        print("This was POST request")
        ecr = EditComputerRecord(request.POST.copy())
        return render(request, 'success.html')

    if request.method == 'GET':
        print("This was GET request")
        template = loader.get_template('computer_edit2.html')
        computer = Computers.objects.get(id_computer=int_index)
        batteries = get_batteries(int_index)
        rams = get_rams(int_index)
        hdds = get_hdds(int_index)
        return HttpResponse(
            template.render(
                {
                    'computer': computer,
                    'bat_list': batteries,
                    "ram_list": rams,
                    "hdd_list": hdds,
                    "rc": rc
                 },
                request
            )
        )


@csrf_exempt
def edit2(request, int_index):
    print("EDIT ")
    cte = ComputerToEdit(int_index=int_index)
    if request.method == 'POST':
        print("This was POST request")
        cte.process_post(request.POST.copy())
        if cte.record.version == 4:
            if cte.success():
                return render(request, 'success.html')
            else:
                return render(
                    request,
                    'failure.html',
                    {'message': cte.message},
                    status=404
                )
        elif cte.record.version == 5:
            if cte.success():
                return render(request, 'success.html')
            else:
                return render(
                    request,
                    'failure.html',
                    {'message': cte.message},
                    status=404
                )
    if request.method == 'GET':
        print("This was GET request")
        cte.process_get()
        if cte.record.version == 4:
            return render(request, 'computer_edit_v4.html', {'record': cte.record})
        elif cte.record.version == 5:
            return render(request, 'computer_edit_v5.html', {'record': cte.record})


@csrf_exempt
def edit_by_serial(request, serial):
    print("EDIT ")
    print(serial)
    cte = ComputerToEdit(serial=serial)
    if request.method == 'POST':
        print("This was POST request")
        cte.process_post(request.POST.copy())
        if cte.record.version == 4:
            if cte.success():
                return render(request, 'success.html')
            else:
                return render(
                    request,
                    'failure.html',
                    {'message': cte.message},
                    status=404
                )
        elif cte.record.version == 5:
            if cte.success():
                return render(request, 'success.html')
            else:
                return render(
                    request,
                    'failure.html',
                    {'message': cte.message},
                    status=404
                )
    if request.method == 'GET':
        print("This was GET request")
        cte.process_get()
        if cte.record.version == 4:
            return render(request, 'computer_edit_v4.html', {'record': cte.record})
        elif cte.record.version == 5:
            return render(request, 'computer_edit_v5.html', {'record': cte.record})


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
def get_observation(request, observation_id):
    observation = Observations.objects.get(id_observation=observation_id)
    return render(request, 'observation_template.html', {'observation': observation})


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
    print("get_gpu")
    print(gpu_id)
    return render(request, 'gpu_template.html', {'gpu': Gpus.objects.get(id_gpu=gpu_id)})


@csrf_exempt
def mass_delete(request):
    print("Mass delete")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    for record_index in data:
        cte = ComputerToEdit(int_index=record_index)
        cte.delete_record()
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
    generator = ExcelGenerator()
    # excel_file = createExcelFile(data)
    excel_file = generator.generate_file(indexes=data)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(excel_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.xlsx"
    excel_file.close()
    return response


@csrf_exempt
def mass_csv(request):
    print("Mass csv")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    # csv_file = createCsvFile(data)
    generator = CsvGenerator()
    csv_file = generator.generate_file(indexes=data)
    response = HttpResponse(content_type="application/ms-excel")
    response.write(csv_file.getvalue())
    response["Content-Disposition"] = "attachment; filename=computers.csv"
    csv_file.close()
    return response


@csrf_exempt
def mass_qr_print(request):
    # print(JSONParser().parse(request))
    print("Mass qr print")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    cmsp = ComputerMultipleSerialPrinter(JSONParser().parse(request))
    cmsp.print()


@csrf_exempt
def mass_qr_print_with_printer(request, printer):
    # print(JSONParser().parse(request))
    print("Mass qr print")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    cmsp = ComputerMultipleSerialPrinter(JSONParser().parse(request), printer)
    cmsp.print()


@csrf_exempt
def cat_change(request):
    print("Mass cat_change")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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
    print("Mass ord_change")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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

    print("Computer form factors")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != '':
            ComputerFormFactors.objects.get_or_create(form_factor_name=name)
    if request.method == 'GET':
        print("This was GET request")
    return render(request, 'items.html', {'items': get_computer_form_factors()})


@csrf_exempt
def del_computer_form_factor(request, int_index):
    print("Delete computer_form_factor")
    if request.method == 'POST':
        print("This was POST request")
        ComputerFormFactors.objects.get(id_computer_form_factor=int_index).delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def computer_form_factor_edit(request):
    print("computer_form_factor_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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

    print("Batches")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != "":
            Receivedbatches.objects.get_or_create(received_batch_name=name)
    if request.method == 'GET':
        print("This was GET request")
    return render(request, 'items.html', {'items': get_received_batches_list()})


@csrf_exempt
def delreceivedBatch(request, int_index):
    print("Delete batch")
    if request.method == 'POST':
        print("This was POST request")
        Receivedbatches.objects.get(id_received_batch=int_index).delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def recieved_batch_edit(request):
    print("recieved batch_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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

    print("Categories")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != "":
            Categories.objects.get_or_create(category_name=name)
        print("Finished")
    if request.method == 'GET':
        print("This was GET request")
    return render(request, 'items.html', {'items': get_categories_list()})


@csrf_exempt
def delCat(request, int_index):
    print("Delete category")
    if request.method == 'POST':
        print("This was POST request")
        cat = Categories.objects.get(id_category=int_index)
        if cat.permanent != 1:
            cat.delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def cat_edit(request):
    print("cat_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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

    print("types")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != "":
            Types.objects.get_or_create(type_name=name)
    if request.method == 'GET':
        print("This was GET request")
    return render(request, 'items.html', {'items': get_types_list()})


@csrf_exempt
def delTyp(request, int_index):
    print("Delete type")
    if request.method == 'POST':
        print("This was POST request")
        Types.objects.get(id_type=int_index).delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def typ_edit(request):
    print("typ_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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

    print("testers")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != "":
            Testers.objects.get_or_create(tester_name=name)
    if request.method == 'GET':
        print("This was GET request")
    return render(request, 'items.html', {'items': get_testers_list()})


@csrf_exempt
def delTes(request, int_index):
    print("Delete tester")
    if request.method == 'POST':
        print("This was POST request")
        Testers.objects.get(id_tester=int_index).delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def tes_edit(request):
    print("tes_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    tes = Testers.objects.get(id_tester=data["ItemId"])
    tes.tester_name = data["ItemName"]
    tes.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observations(request):
    print("observations")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
        return render(request, "observations.html")


@csrf_exempt
def observation_category(request):
    def get_observation_category_list():
        lst = []
        for member in Observationcategory.objects.all():
            lst.append(Item(item_id=member.id_observation_category, item_name=member.category_name))
        return lst

    print("observation_category")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != "":
            Observationcategory.objects.get_or_create(category_name=name)
    if request.method == 'GET':
        print("This was GET request")
    return render(request, "observationsCategorySubtemplate.html", {'items': get_observation_category_list()})


@csrf_exempt
def del_observation_category(request, int_index):
    print("Delete observation_category")
    if request.method == 'POST':
        print("This was POST request")
        Observationcategory.objects.get(id_observation_category=int_index).delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after changes post update on JS side page reload has failed")


@csrf_exempt
def observation_category_edit(request):
    print("observation_category edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
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

    print("observation_subcategory")
    if request.method == 'POST':
        print("This was POST request")
        name = request.POST.get("item_name")
        if name != "":
            Observationsubcategory.objects.get_or_create(subcategory_name=name)
    if request.method == 'GET':
        print("This was GET request")
    return render(request, "observationsSubcategorySubtemplate.html", {'items': get_observation_subcategory_list()})


@csrf_exempt
def del_observation_subcategory(request, int_index):
    print("Delete observation_subcategory")
    if request.method == 'POST':
        print("This was POST request")
        Observationsubcategory.objects.get(id_observation_subcategory=int_index).delete()
    if request.method == 'GET':
        print("This was GET request")
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observation_subcategory_edit(request):
    print("observation_subcategory edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    item = Observationsubcategory.objects.get(id_observation_subcategory=data["ItemId"])
    item.subcategory_name = data["ItemName"]
    item.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observations_details(request):
    print("observations_details")
    if request.method == 'POST':
        print("This was POST request")
        ota = ObservationToAdd(request.POST)
        if ota.validated():
            ota.process()
    if request.method == 'GET':
        print("This was GET request")
    return render(
        request,
        "observationsDetailsSubtemplate.html",
        {
            "categories": Observationcategory.objects.values_list('category_name', flat=True),
            "subcategories": Observationsubcategory.objects.values_list('subcategory_name', flat=True),
            'observations': ObservationsCollection()
        }
    )


@csrf_exempt
def delete_observations_details(request, int_index):
    print('delete_observations_details')
    Observations.objects.get(id_observation=int_index).delete()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def edit_observations_details(request):
    print('edit_observations_details')
    print(request.POST)
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

    print("new_record")
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
        print("This was POST request")
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
        print("This was GET request")
        return render(request, 'new_record.html', {"rc": rc, "many_to_many_unique_values_dict": many_to_many_unique_values_dict})


@csrf_exempt
def cat_to_sold(request):
    print("cat_to_sold")
    computers = Computers.objects.filter(id_computer__in=request.GET.copy().pop('id'))
    if request.method == 'POST':
        print("This was POST request")
        executor = ExecutorOfCatToSold(request.POST.copy())
        if executor.validated:
            executor.write_to_database()
            return render(request, 'success.html')
        else:
            template = loader.get_template('catToSold.html')
            return HttpResponse(
                template.render(
                    {
                        'computers': computers,
                        "error_message": executor.get_error_message()
                    }
                ),
                request
            )
    if request.method == 'GET':
        print("This was GET request")
        template = loader.get_template('catToSold.html')
        return HttpResponse(
            template.render(
                {'computers': computers}
            ),
            request
        )


@csrf_exempt
def new_order(request):
    print("tes_edit")
    noc = NewOrderChoices()
    if request.method == 'POST':
        print("This was POST request")
        no = NewOrder(request.POST.copy())
        no.save()
        if no.is_saved():
            return render(request, 'success.html')
        else:
            template = loader.get_template('new_order.html')
            return HttpResponse(
                template.render(
                    {
                        "noc": noc,
                        "error_message": no.get_error_message()
                    }
                ),
                request
            )
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('new_order.html')
    return HttpResponse(
        template.render(
            {"noc": noc}
        ),
        request
    )


@csrf_exempt
def edit_order(request, int_index):
    print("EDIT order")
    ote = OrderToEdit(int_index)
    print(int_index)
    if request.method == 'POST':
        print("This was POST request")
        # ote.process_uploaded_file(request.FILES["csv_excel"])
        ote.set_new_data(request.POST.copy())
        if ote.hasErrors():
            return render(request, 'success.html')
        else:
            template = loader.get_template('order_edit.html')
            return HttpResponse(
                template.render(
                    {
                        "ote": ote,
                        "error_message": ote.get_error_message()
                    }
                ),
                request
            )
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('order_edit.html')
    return HttpResponse(
        template.render({"ote": ote}),
        request
    )

@csrf_exempt
def delete_order(request, int_index):
    if request.method == 'POST':
        print("This was POST request")
        try:
            order = Orders.objects.get(id_order=int_index)
            OrdTes.objects.filter(f_order=order).delete()
            order.delete()
            return render(request, 'success.html')
        except Exception as e:
            return HttpResponse(e, status=404)
    if request.method == 'GET':
        print("This was GET request")
        return HttpResponse("You shouldn't be here", status=404)


@csrf_exempt
def strip_order(request, int_index):
    def _strip_order_of_computer():
        computer = Computers.objects.get(id_computer=int_index)
        compord = CompOrd.objects.get(id_comp_ord=computer.f_id_comp_ord.id_comp_ord)
        computer.f_id_comp_ord = None
        computer.save()
        compord.delete()

    print("Strip computer from order")
    if request.method == 'POST':
        print("This was POST request")
        _strip_order_of_computer()
        return HttpResponse(status=200)
    if request.method == 'GET':
        print("This was GET request")
        return HttpResponse('This should not be returned', status=404)


@csrf_exempt
def computer_search_table_from_order(request):
    print("Computer search table from order")
    if request.method == 'POST':
        print("This was POST request")
        return HttpResponse("Disallowed action", status=404)
    if request.method == 'GET':
        print("This was GET request")
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
        print("This was POST request")
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
        print("This was GET request")
        return HttpResponse('Get request not Implemented', status=404)


@csrf_exempt
def hdd_edit(request, int_index):
    print('hdd_edit')
    hte = HddToEdit(int_index)
    if request.method == 'POST':
        print('POST method')
        hte.process_edit(request.POST.copy())
        return render(request, 'success.html')
    if request.method == 'GET':
        print('GET method')
        return render(request, 'hdd_edit.html', {'hte': hte})


@csrf_exempt
def hdd_delete(request, int_index):
    print('hdd_delete')
    htd = HddToDelete(pk=int_index)
    if request.method == 'POST':
        print('POST method')
        htd.delete()
        if htd.success:
            print('success')
            return render(request, 'success.html')
        else:
            print('Failed deletion')
            print(htd.message)
            return HttpResponse(htd.message, status=404)
    if request.method == 'GET':
        print('GET method')
        return HttpResponse('<p>You should not be here.</p><p>What are you doing over here?</p>', status=404)


def view_pdf(request, int_index):
    print('Index is: ' + str(int_index))
    print('view_pdf')

    if request.method == 'POST':
        print('POST request')
    elif request.method == 'GET':
        print('GET request')
        try:
            hdd = Drives.objects.get(hdd_id=int_index)
            tf = tarfile.open(os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), hdd.f_lot.lot_name + '.tar'))
            pdf_content = tf.extractfile(tf.getmember(hdd.tar_member_name)).read()
            return HttpResponse(pdf_content, content_type='application/pdf')
        except:
            return render(
                request,
                'failure.html',
                {'message': "Failed to fetch pdf.\r\nMost likely cause is that pdf is nonexistant."},
                status=404
            )

@csrf_exempt
def hdd_order_content(request, int_index):
    print(int_index)
    print('hdd_order_edit')
    hoch = HddOrderContentHolder(int_index)
    if request.method == 'POST':
        print('POST method')
        try:
            hoch.edit(request.POST.copy())
            return render(request, 'success.html')
        except Exception as e:
            return render(
                request,
                'failure.html',
                {'message': str(e)},
                status=404
            )
    if request.method == 'GET':
        print('GET method')
        hoch.filter(request.GET.copy())
        print(hoch.hdd_order.f_order_status.is_shown)
        return render(
            request,
            'hdd_order_content.html',
            {'hoch': hoch}
        )


@csrf_exempt
def hdd_order_content_csv(request, int_index):
    print('hdd_order_content_csv')
    if request.method == 'POST':
        print('POST method')
    if request.method == 'GET':
        print('GET method')
        hocc = HddOrderContentCsv(int_index)
        csv_file = hocc.createCsvFile()
        response = HttpResponse(content_type="application/ms-excel")
        response.write(csv_file.getvalue())
        response["Content-Disposition"] = "attachment; filename=computers.csv"
        csv_file.close()
        return response


@csrf_exempt
def hdd_delete_order(request, int_index):
    print(int_index)
    if request.method == 'POST':
        print('POST method')
    if request.method == 'GET':
        print('GET method')
        hod = HddOrderToDelete(int_index)
        hod.delete()
        if hod.success:
            return render(request, 'success.html')
        return render(
            request,
            'failure.html',
            {'message': hod.message},
            status=404
        )


@csrf_exempt
def hdd_order(request):
    print("order upload")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            hop = HddOrderProcessor(request.FILES['document'])
            if hop.message != '':
                return render(request, 'failure.html', {'message': hop.message})
            else:
                return render(request, 'success.html')
        else:
            print("Invalid")
            return render(
                request,
                'uploader.html',
                {'form': form}
            )
    else:
        form = DocumentForm()
        return render(
            request,
            'uploader.html',
            {'form': form}
        )


@csrf_exempt
def hdd_orderAlt(request):
    print("Alternative order upload")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            ahop = AlternativeHddOrderProcessor(request.FILES['document'])
            ahop.process_data()
            if ahop.message != '':
                return render(
                    request,
                    'failure.html',
                    {'message': ahop.message}
                )
            else:
                return render(
                    request,
                    'success.html'
                )
        else:
            print("Invalid")
            return render(
                request,
                'uploader.html',
                {'form': form}
            )
    else:
        form = DocumentForm()
        return render(
            request,
            'uploader.html',
            {'form': form}
        )


@csrf_exempt
def tar(request):
    print("tar upload")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            tp = TarProcessor(request.FILES['document'])
            tp.process_data()
            return render(
                request,
                'success.html'
            )
        else:
            return render(
                request,
                'uploader.html',
                {'form': form}
            )
    else:
        form = DocumentForm()
        return render(
            request,
            'uploader.html',
            {'form': form}
        )


@csrf_exempt
def tarAlt(request):
    print("tar upload")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            atp = AlternativeTarProcessor(request.FILES['document'])
            atp.process_data()
            return render(
                request,
                'success.html'
            )
        else:
            return render(
                request,
                'uploader.html',
                {'form': form}
            )
    else:
        form = DocumentForm()
        return render(
            request,
            'uploader.html',
            {'form': form}
        )


@csrf_exempt
def lot_content(request, int_index):
    if request.method == 'POST':
        print('POST method')
    if request.method == 'GET':
        print('GET method')
        lch = LotContentHolder(int_index)
        lch.filter(request.GET.copy())
        return render(
            request,
            'lot_content.html',
            {'lch': lch}
        )


@csrf_exempt
def success(request):
    if request.method == 'POST':
        print('POST method')
    if request.method == 'GET':
        print('GET method')
        return render(
            request,
            'success.html'
        )


@csrf_exempt
def serial_processing(request, serial):
    csp = ChargerSerialProcessor(serial)
    if request.method == 'POST':
        print('POST method')
        csp.process()
        if csp.message == '':
            return render(request, 'success.html')
        else:
            return render(
                request,
                'failure.html',
                {'message': csp.message}
            )
    if request.method == 'GET':
        print('GET method')
        # csp.proccess()
        if csp.serial_exists():
            print('Such serial exists')
            ch = ChargerHolder(serial=serial)
            return render(
                request,
                'charger_view.html',
                {'ch': ch}
            )
        else:
            print('Such serial is non-existant')
            return render(
                request,
                'charger_nonexistant.html'
            )


@csrf_exempt
def delete_charger_from_scan(request, serial):
    if request.method == 'POST':
        print('POST method')
        '''
        charger = Chargers.objects.get(charger_id=JSONParser().parse(request)['charger_id'])
        charger.delete()
        '''
        # Chargers.objects.get(charger_serial=serial.split('_'[2])).delete()
        # print(serial.split('_')[2])
        Chargers.objects.get(charger_serial=serial.split('_')[2]).delete()
        return HttpResponse('POST request finished', status=200)
    if request.method == 'GET':
        print('GET method')
        return HttpResponse('Get request not Implemented', status=404)


@csrf_exempt
def edit_charger(request, int_index):
    ccte = ChargerCategoryToEdit(int_index)
    if request.method == 'POST':
        print('POST method')
        # ccte = ChargerCategoryToEdit(int_index)
        ccte.process(request.POST.copy())
        if ccte.isValidData:
            return render(
                request,
                'success.html'
            )
        else:
             return render(
                 request,
                 'failure.html',
                 {'message': ccte.message}
             )
    if request.method == 'GET':
        print('GET method')
        # ccte = ChargerCategoryToEdit(int_index)
        return render(
            request,
            'charger_edit.html',
            {'ccte': ccte}
        )


@csrf_exempt
def edit_charger_serial(request, int_index):
    print('edit_charger_serial')
    if request.method == 'POST':
        print('POST method')
        cse = ChargerSerialEditor(JSONParser().parse(request))
        cse.process()
    if request.method == 'GET':
        print('GET method')


@csrf_exempt
def print_charger_serial(request, int_index):
    print('print_charger_serial')
    if request.method == 'POST':
        print('POST method')
        csp = ChargerSingleSerialPrinter(JSONParser().parse(request))
        csp.print()
    if request.method == 'GET':
        print('GET method')


@csrf_exempt
def print_chargers_serials(request, int_index):
    print('print_chargers_serials')
    if request.method == 'POST':
        print('POST method')
        # print(JSONParser().parse(request))
        cdsp = ChargerDualSerialPrinter(JSONParser().parse(request))
        cdsp.print()
    if request.method == 'GET':
        print('GET method')


@csrf_exempt
def delete_charger(request, int_index):
    print('delete_charger')
    if request.method == 'POST':
        print('POST method')
        ctd = ChargerToDelete(JSONParser().parse(request))
        ctd.delete()
    if request.method == 'GET':
        print('GET method')


@csrf_exempt
def delete_charger_category(request, int_index):
    print('print_charger_serial')
    if request.method == 'POST':
        print('POST method')
        cctd = ChargerCategoryToDelete(int_index)
        cctd.delete()
        if cctd.success:
            return render(
                request,
                'success.html'
            )
        else:
            return HttpResponse(cctd.message, status=404)
    if request.method == 'GET':
        print('GET method')


@csrf_exempt
def print_computer_qr(request, int_index):
    print('print_computer_qr')
    if request.method == 'POST':
        print('POST method')
        # variable = JSONParser().parse(request)
        # variable = json.loads(request.bod y)
        # cssp = ComputerSingleSerialPrinter(variable)
        # cssp = ComputerSingleSerialPrinter(JSONParser().parse(request))

        cssp = ComputerSingleSerialPrinter(int_index)
        cssp.print()
        return HttpResponse("Not implemented return", status=200)
    if request.method == 'GET':
        print('GET method')

@csrf_exempt
def print_computer_qr_with_printer(request, int_index, printer):
    print('print_computer_qr')
    if request.method == 'POST':
        print('POST method')
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
        print('GET method')