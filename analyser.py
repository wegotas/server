from ULCDTinterface.modelers import *
from django.db.models import Count

# '''
version4_qty = 0
v4_dict = {}
version5_qty = 0
v5_dict = {}
lst = []

for computer in Computers.objects.all():
    status = computer.get_status()
    if computer.is5th_version():
        version5_qty += 1
        if status in v4_dict:
            v4_dict[status] += 1
        else:
            v4_dict[status] = 1
    else:
        if status == 'No status':
            lst.append(computer.id_computer)
        version4_qty += 1
        if status in v5_dict:
            v5_dict[status] += 1
        else:
            v5_dict[status] = 1

print("Version 4 qty: {0},\n Version 5 qty: {1}".format(version4_qty, version5_qty))
print(v4_dict)
print('____________________________________________')
print(v5_dict)
print('____________________________________________')
print(lst)
# '''
'''
# for computer_drives
computer_drives = Computerdrives.objects.values('f_id_computer').annotate(Count('id_computer_drive'))\
    .order_by()\
    .filter(id_computer_drive__count__gt=1)

# print(computer_drives)
for member in computer_drives:
    print(member)
'''
'''
computer_batteries = BatToComp.objects.values('f_id_computer_bat_to_com').annotate(Count('id_bat_to_comp'))\
    .order_by()\
    .filter(id_bat_to_comp__count__gt=1)

for member in computer_batteries:
    print(member)
'''
'''
computer_processors = Computerprocessors.objects.values('f_id_computer').annotate(Count('f_id_processor'))\
    .order_by()\
    # .filter(f_id_processor__count__gt=1)

for member in computer_processors:
    print(member)
'''
'''
computer_gpus = Computergpus.objects.values('f_id_computer').annotate(Count('id_computergpus'))\
    .order_by()\
    .filter(id_computergpus__count__gt=1)

for member in computer_gpus:
    print(member)
'''
'''
computer_observations = Computerobservations.objects.values('f_id_computer').annotate(Count('id_computer_observations'))\
    .order_by()\
    .filter(id_computer_observations__count__gt=8)

for member in computer_observations:
    print(member)
'''