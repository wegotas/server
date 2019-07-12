from ULCDTinterface.modelers import *
from django.db.models import Count

duplicate_processors = Processors.objects.values('f_manufacturer', 'model_name', 'stock_clock', 'max_clock', 'cores', 'threads').annotate(cnt=Count('id_processor')).filter(cnt__gt=1)

for dp in duplicate_processors:
    processors = Processors.objects.filter(f_manufacturer=dp['f_manufacturer'], model_name=dp['model_name'], stock_clock=dp['stock_clock'], max_clock=dp['max_clock'], cores=dp['cores'], threads=dp['threads'])
    Computerprocessors.objects.filter(f_id_processor=processors[0]).update(f_id_processor=processors[1])
    processors[0].delete()
