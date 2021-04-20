from . import views as primer_views
from django.urls import path
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('primerinput/', login_required(primer_views.PrimerFormView.as_view()), name='primerinput'),
    path('primer/', primer_views.PrimerFilteredTableView.as_view(), name='primer'),
    path('primer/<int:pk>/', primer_views.PrimerDetailView.as_view(), name='primerinfo'),
    path('primer/<int:pk>/update', primer_views.PrimerUpdateView.as_view(), name='primerupdate'),
    path('primer/<int:pk>/delete/', primer_views.PrimerDeleteView.as_view(), name='primerdelete'),

    path('vector/', primer_views.vector_index, name='vector_index'),
    path('vector/new/', primer_views.VectorCreateView.as_view(), name='vector_create'),
    path('vector/<int:pk>/', primer_views.VectorDetailView.as_view(), name='vector_detail'),
    path('vector/<int:pk>/delete/', primer_views.VectorDeleteView.as_view(), name='vector_delete'),
    path('vector/<int:pk>/update', primer_views.VectorUpdateView.as_view(), name='vector_update'),

    path('seq/', primer_views.calpcr, name='seq'),
    path('seq/vector/', primer_views.SelectVector, name='seqvector'),
    path('seq_setL/', primer_views.calpcr_setL, name='seq_setL'),
    path('seq/showPCR', primer_views.show_pcr, name='showpcr'),



]