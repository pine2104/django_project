import django_tables2 as tables
from .models import Primer
from django_tables2.utils import A

class SimpleTable(tables.Table):
    name = tables.LinkColumn('primerinfo', args=[A('pk')])
    class Meta:
        model = Primer
        fields = ['name', 'project', 'length', 'modification_5', 'modification_3', 'modification_internal', 'sequence']
        attrs = {"class": "paleblue"}