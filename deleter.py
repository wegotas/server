from ULCDTinterface.modelers import *

v4_ids = []

for computer in Computers.objects.all():
    if not computer.is5th_version():
        v4_ids.append(computer.id_computer)
        # print("Serial: {0}, isSold: {1}, category: {2}".format(
        #     computer.computer_serial, computer.f_sale, computer.f_category.category_name))
# print(v4_ids)


print('Deleting 4v battocomps and batteries')
battocomps = BatToComp.objects.filter(f_id_computer_bat_to_com__in=v4_ids)
print(battocomps.count())
battery_ids = list(battocomps.values_list('f_bat_bat_to_com', flat=True))
battocomps.delete()
batteries = Batteries.objects.filter(id_battery__in=battery_ids)
print(batteries.count())
batteries.delete()
print("Batteries.objects.all() count: {0}".format(Batteries.objects.all().count()))
print("BatToComp.objects.all() count: {0}".format(BatToComp.objects.all().count()))


print('Deleting 4v ramtocomps and rams')
ramtocomps = RamToComp.objects.filter(f_id_computer_ram_to_com__in=v4_ids)
print(ramtocomps.count())
ram_ids = list(ramtocomps.values_list('f_id_ram_ram_to_com', flat=True))
ramtocomps.delete()
rams = Rams.objects.filter(id_ram__in=ram_ids)
print(rams.count())
rams.delete()
print("RamToComp.objects.all() count: {0}".format(RamToComp.objects.all().count()))
print("Rams.objects.all() count: {0}".format(Rams.objects.all().count()))

HddToComp.objects.all().delete()

print('Deleting 4v computers')
print("Computers.objects.all() count: {0}".format(Computers.objects.all().count()))
v4_computers = Computers.objects.filter(id_computer__in=v4_ids)
print("v4_computers count: {0}".format(v4_computers.count()))
v4_computers.delete()
print("Computers.objects.all() count: {0}".format(Computers.objects.all().count()))
