from ULCDTinterface.modelers import *


variables = {}

for drive in Drives.objects.all():
    if not drive.f_speed.speed_name.isdigit():
        variables[drive.hdd_serial] = drive.f_speed.speed_name

print(variables)