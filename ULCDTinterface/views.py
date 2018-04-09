from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ULCDTinterface.modelers import Categories, Types, Testers

# Create your views here.
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
            print(type.id_type)
            print(type.type_name)
            typ_dict[type.id_types] = type.type_name
        print(typ_dict)
        print("___________________________")
        testers = Testers.objects.all()
        tes_dict = dict()
        for tester in testers:
            print(tester.id_tester)
            print(tester.tester_name)
            tes_dict[tester.id_category] = tester.category_name
        print(tes_dict)
        print("___________________________")
        dict_dict = dict()
        dict_dict["cat_dict"] = cat_dict
        dict_dict["typ_dict"] = typ_dict
        dict_dict["tes_dict"] = tes_dict
        print(dict_dict)
        return JsonResponse(dict_dict)
