from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Primer, UploadPrimer, Project, Vector

# Register your models here.

@admin.register(Primer)
class PrimerAdmin(ImportExportModelAdmin):
 list_display = ('name', 'sequence', 'modification_5', 'who_ordered', 'purpose', 'price', 'volumn', 'vendor', 'created_at')

# admin.site.register(Primer)
admin.site.register(UploadPrimer)
admin.site.register(Project)
admin.site.register(Vector)
