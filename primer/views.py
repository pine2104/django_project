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


class PrimerForm(FormView):
    template_name = 'primer/primer_form.html'
    form_class = PrimerForm
    # model = Primer
    success_url = reverse_lazy('primerlist')  # back to url name: fileupload (in urls)
    # context = {'form': }
    def form_valid(self, form): # FormView does not save, you need to add
        form.instance.created_by = self.request.user
        form.save()
        return super(PrimerForm, self).form_valid(form)



class PrimerUploadView(CreateView):
    model = UploadPrimer
    template_name = 'primer/primerupload_form.html'
    fields = ['excel_file', ]
    success_url = reverse_lazy('homepage')  # back to url name: fileupload (in urls)



class PrimerDetailView(DetailView):
    model = Primer
    template_name = 'primer/primer_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['primers'] = Primer.objects.all()
        context['all_fields'] = Primer._meta.fields
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
    rseq = seq.reverse_complement()
    poss = []
    for primer in primers:
        p_seq = Dseq(primer.sequence.replace(' ', ''))
        p_seq_s = str(p_seq)
        if seq.find(str.lower(p_seq_s)) != -1: # match it
            pos = seq.find(str.lower(p_seq_s))
        elif rseq.find(str.lower(p_seq_s)) != -1:
            pos = rseq.find(str.lower(p_seq_s)) * (-1)
        else:
            pos = 'none'
        primer.pos = str(pos)

    #
    # seq2 = seq[0:100] + '\n' +seq[101:200] + '\n'
    # + '\n' + seq[101:200] + '\n'
    # seq3 = Dseq(seq[0:100] ,circular = True)
    # rev_3 = seq3.reverse_complement()
    # rev_3s = str(rev_3)[::-1]
    # match_3 = seq3.find('atgtttgacagctta')

    # L = len(seq)
    L=1
    seq2=1
    seq3=1
    rev_3s=1
    match_3=1

    return render(request, template_name='primer/seq.html', context={'seq': seq, 'L': L, 'seq2': seq2, 'seq3': seq3,
                                                                     'rev_3': rev_3s, 'match_3': match_3, 'poss': poss,
                                                                     'primers': primers})
