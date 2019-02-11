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
    # isSold = getIsSold(request)
    isSold = is_get_key_true(request, key='sold')
    # isOrder = getIsOrder(request)
    isOrder = is_get_key_true(request, key='orders')
    # isChargers = getIsChargers(request)
    isChargers = is_get_key_true(request, key='chargers')
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

    if isChargers:
        # PRIDETI FILTRAVIMA
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

    elif isSold:
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

    elif isOrder:
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
        # removeKeyword(request)
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
        ecr = Edit_computer_record(request.POST.copy())
        # return HttpResponse("Success", request)
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
def cat_change(request):
    print("Mass cat_change")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    # data = JSONParser().parse(request)
    change_category_for_computers(JSONParser().parse(request))
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
def receivedbatches(request):
    print("Batches")
    if request.method == 'POST':
        print("This was POST request")
        save_received_batch(request.POST.get("item_name"))
    if request.method == 'GET':
        print("This was GET request")
    received_batches = get_received_batches_list()
    template = loader.get_template('items.html')
    return HttpResponse(
        template.render(
            {'items': received_batches},
            request
        )
    )


@csrf_exempt
def delreceivedBatch(request, int_index):
    print("Delete batch")
    if request.method == 'POST':
        print("This was POST request")
        delete_batch(int_index)
    if request.method == 'GET':
        print("This was GET request")


@csrf_exempt
def recieved_batch_edit(request):
    print("recieved batch_edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_received_batch(data)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


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
    template = loader.get_template('items.html')
    return HttpResponse(
        template.render(
            {'items': categories},
            request
        )
    )


@csrf_exempt
def delCat(request, int_index):
    print("Delete category")
    if request.method == 'POST':
        print("This was POST request")
        delete_category(int_index)
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
    return HttpResponse(
        template.render(
            {'items': types},
            request
        )
    )


@csrf_exempt
def delTyp(request, int_index):
    print("Delete type")
    if request.method == 'POST':
        print("This was POST request")
        delete_type(int_index)
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
    return HttpResponse(
        template.render(
            {'items': testers},
            request
        )
    )


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
    print("observation_category")
    if request.method == 'POST':
        print("This was POST request")
        save_observation_category(request.POST.get("item_name"))
    if request.method == 'GET':
        print("This was GET request")
    return render(request, "observationsCategorySubtemplate.html", {'items': get_observation_category_list()})


@csrf_exempt
def del_observation_category(request, int_index):
    print("Delete observation_category")
    if request.method == 'POST':
        print("This was POST request")
        delete_observation_category(int_index)
    if request.method == 'GET':
        print("This was GET request")


@csrf_exempt
def observation_subcategory_edit(request):
    print("observation_category edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_observation_category(data)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observation_category_edit(request):
    print("observation_category edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_observation_category(data)
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def observation_subcategory(request):
    print("observation_subcategory")
    if request.method == 'POST':
        print("This was POST request")
        save_observation_subcategory(request.POST.get("item_name"))
    if request.method == 'GET':
        print("This was GET request")
    return render(request, "observationsSubcategorySubtemplate.html", {'items': get_observation_subcategory_list()})


@csrf_exempt
def del_observation_subcategory(request, int_index):
    print("Delete observation_subcategory")
    if request.method == 'POST':
        print("This was POST request")
        delete_observation_subcategory(int_index)
    if request.method == 'GET':
        print("This was GET request")


@csrf_exempt
def observation_subcategory_edit(request):
    print("observation_subcategory edit")
    if request.method == 'POST':
        print("This was POST request")
    if request.method == 'GET':
        print("This was GET request")
    data = JSONParser().parse(request)
    edit_observation_subcategory(data)
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
            return render(
                request,
                "observationsDetailsSubtemplate.html",
                {
                    "categories": Observationcategory.objects.all().values_list('category_name', flat=True),
                    "subcategories": Observationsubcategory.objects.all().values_list('subcategory_name', flat=True),
                    'observations': ObservationsCollection()
                }
            )
        return render(
            request,
            "observationsDetailsSubtemplate.html",
            {
                'message':ota.message,
                "categories": Observationcategory.objects.all().values_list('category_name', flat=True),
                "subcategories": Observationsubcategory.objects.all().values_list('subcategory_name', flat=True),
                'observations': ObservationsCollection()
            }
        )
    if request.method == 'GET':
        print("This was GET request")
    return render(
        request,
        "observationsDetailsSubtemplate.html",
        {
            "categories": Observationcategory.objects.all().values_list('category_name', flat=True),
            "subcategories": Observationsubcategory.objects.all().values_list('subcategory_name', flat=True),
            'observations': ObservationsCollection()
        }
    )


@csrf_exempt
def delete_observations_details(request, int_index):
    print('delete_observations_details')
    observation = Observations.objects.get(id_observation=int_index)
    observation.delete()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def edit_observations_details(request):
    print('edit_observations_details')
    print(request.POST)
    data = JSONParser().parse(request)
    # ote = ObservationToEdit(data)
    # edit_observation(data)
    observation = Observations.objects.get(id_observation=data['observation_id'])
    observation.shortcode = data['shortcode']
    observation.full_name = data['fullname']
    observation.save()
    return HttpResponse(
        "If you see this message that means after deletion post update on JS side page reload has failed")


@csrf_exempt
def delTes(request, int_index):
    print("Delete tester")
    message = ""
    if request.method == 'POST':
        print("This was POST request")
        delete_tester(int_index)
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('items.html')
    return HttpResponse(
        template.render(
            {'items': testers},
            request
        )
    )


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
        rta = RecordToAdd(request.POST.copy())
        rta.save()
        if rta.isSaved():
            return render(request, 'success.html')
        else:
            template = loader.get_template('new_record.html')
            return HttpResponse(
                template.render(
                    {
                        "rc": rc,
                        "error_message": rta.get_error_message()
                    },
                    request
                )
            )
    if request.method == 'GET':
        print("This was GET request")
    template = loader.get_template('new_record.html')
    return HttpResponse(
        template.render(
            {"rc": rc}
        ),
        request
    )


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
            # return HttpResponse("Success", request)
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
        query = get_query_for_computer_search_from_order_edit(keyword)
        computers = Computers.objects.filter(query)
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
        return render(
            request,
            'hdd_edit.html',
            {'hte': hte}
        )


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
            # return render('message': htd.message, status=404)
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
        # variable = json.loads(request.body)
        # cssp = ComputerSingleSerialPrinter(variable)
        # cssp = ComputerSingleSerialPrinter(JSONParser().parse(request))

        cssp = ComputerSingleSerialPrinter(int_index)
        cssp.print()
    if request.method == 'GET':
        print('GET method')