from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from .models import Primer, UploadPrimer, Vector
from .forms import PrimerForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import datetime
from .filters import PrimerFilter

from pydna.dseq import Dseq

from django.contrib.auth.decorators import login_required
import django_excel as excel
import numpy as np



def index(request):
    primers = Primer.objects.all().order_by('-created_at')
    primerFilter = PrimerFilter(queryset=primers)

    if request.method == 'POST':
        primerFilter = PrimerFilter(request.POST, queryset=primers)

    context = {
        'primerFilter':primerFilter
    }
    return render(request, 'primer/primer_index.html', context)


class PrimerListView(ListView):
    model = Primer
    template_name = 'primer/primer_list.html'
    context_object_name = 'primers'
    ordering = ['-created_at']


class PrimerFormView(FormView):
    template_name = 'primer/primer_form.html'
    form_class = PrimerForm
    # model = Primer
    success_url = reverse_lazy('primerlist')  # back to url name: fileupload (in urls)

    # context = {'form': }
    def form_valid(self, form): # FormView does not save, you need to add
        form.instance.created_by = self.request.user
        form.save()
        return super(PrimerFormView, self).form_valid(form)

class PrimerUploadView(CreateView):
    model = UploadPrimer
    template_name = 'primer/primerupload_form.html'
    fields = ['excel_file', ]
    success_url = reverse_lazy('homepage')  # back to url name: fileupload (in urls)



class PrimerDetailView(DetailView):
    model = Primer
    template_name = 'primer/primer_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PrimerDetailView, self).get_context_data(**kwargs)
        context['primers'] = Primer.objects.all()
        context['all_fields'] = Primer._meta.fields
        context['form'] = PrimerForm
        return context


class PrimerUpdateView(LoginRequiredMixin, UpdateView):
    model = Primer
    fields = ['name', 'sequence', 'modification', 'who_ordered', 'purpose', 'price', 'volumn', 'brand']
    def get_success_url(self):
        return reverse('primerinfo', kwargs={'pk': self.object.id})
    def form_valid(self, form): # make authen to the user, over-write this function.
        form.instance.created_at = datetime.datetime.now()
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PrimerDeleteView(LoginRequiredMixin, DeleteView):
    model = Primer
    template_name = 'primer/primer_confirm_delete.html'
    success_url = '/'


def delblank(request):
    pbr = Vector.objects.get(name='pbr322')
    primers = Primer.objects.all()
    seq = pbr.sequence
    seq = Dseq(seq.replace(' ', ''))
    L = len(str(seq))
    rseq = seq.reverse_complement()
    poss = []
    for primer in primers:
        p_seq = Dseq(primer.sequence.replace(' ', ''))
        p_seq_s = str(p_seq)
        Lp = len(p_seq_s)
        if seq.find(str.lower(p_seq_s)) != -1: # match it
            position = seq.find(str.lower(p_seq_s)) + 1
            dir = 'forward'
            in_vector = True
        elif rseq.find(str.lower(p_seq_s)) != -1:
            position = rseq.find(str.lower(p_seq_s)) - L - 1
            dir = 'reverse'
            in_vector = True
        else:
            position = -1
            dir = 'none'
            in_vector = False
        primer.position = position
        primer.dir = dir
        primer.in_vector = in_vector
        primer.length = Lp
        primer.save()

    primers = primers.filter(in_vector=True).order_by('position')
    # primers = Primer.objects.all().order_by('-created_at')
    primerFilter = PrimerFilter(queryset=primers)

    if request.method == 'POST' and 'Search' in request.POST:
        primerFilter = PrimerFilter(request.POST, queryset=primers)

    L = len(str(seq))

    # if request.method == 'POST' and 'cal' in request.POST:
    check_box_list = request.POST.getlist("check_box")
    if len(check_box_list) == 2:
        primer_1 = Primer.objects.get(id=check_box_list[0])
        primer_2 = Primer.objects.get(id=check_box_list[1])
        if primer_1.dir == 'reverse':
            pr = primer_1.position
            pf = primer_2.position
        else:
            pr = primer_2.position
            pf = primer_1.position
        if abs(pr) > abs(pf):
            L_pcr = -pr - pf
        else:
            L_pcr = L - pr - pf
    else:
        L_pcr = 0


    return render(request, template_name='primer/seq.html', context={'seq': seq, 'L': L, 'primers': primers,
                                                                     'primerFilter': primerFilter,
                                                                     'check_box_list': check_box_list,
                                                                     'L_pcr': L_pcr})

class VectorCreateView(LoginRequiredMixin, CreateView):
    model = Vector
    template_name = 'primer/vector_form.html'
    fields = ['name', 'sequence']
    success_url = '/'
    def form_valid(self, form): # make authen to the user, over-write this fun.
        return super().form_valid(form)