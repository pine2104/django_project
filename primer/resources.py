from import_export import resources
from .models import Primer

class PrimerResource(resources.ModelResource):
    class Meta:
        model = Primer