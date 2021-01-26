from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from .models import Primer, UploadPrimer, Vector
from .forms import PrimerForm
from .tables import SimpleTable
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import datetime
from .filters import PrimerFilter

from pydna.dseq import Dseq
import django_tables2 as tables
from django.contrib.auth.decorators import login_required
from .pcr import hamming_distance, match_primer, plotpcr



class PrimerFormView(FormView):
    template_name = 'primer/primer_form.html'
    form_class = PrimerForm
    # model = Primer
    success_url = reverse_lazy('primerlist')  # back to url name: fileupload (in urls)

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
    fields = ['name', 'sequence', 'project', 'modification_5', 'modification_3', 'modification_internal', 'who_ordered', 'purpose', 'price', 'volumn', 'brand']
    def get_success_url(self):
        return reverse('primerinfo', kwargs={'pk': self.object.id})
    def form_valid(self, form): # make authen to the user, over-write this function.
        form.instance.edit_at = datetime.datetime.now()
        form.instance.edit_by = self.request.user
        return super().form_valid(form)


class PrimerDeleteView(LoginRequiredMixin, DeleteView):
    model = Primer
    template_name = 'primer/primer_confirm_delete.html'
    success_url = '/'


class PrimerVectorUpdateView(LoginRequiredMixin, UpdateView):
    model = Primer
    fields = ['vector']
    template_name = 'primer/primervector_update.html'


@login_required
def SelectVector(request):
    vectors = Vector.objects.all()
    primers = Primer.objects.all()
    template_name = 'primer/vector_choose.html'
    context = {
        'vectors': vectors,
    }
    if request.method == 'POST':
        id = request.POST["vector_choice"]
        vector = Vector.objects.get(id=id)
        for primer in primers:
            primer.vector = vector
            primer.save() # update choose vector and redirect to result
        # return render(request, template_name, context={'vector': vector})
        return redirect('seq')

    return render(request, template_name, context)


def calpcr(request):
    # pbr = Vector.objects.get(name='pbr322')
    primers = Primer.objects.all()
    vector = primers[0].vector
    vector_name = vector.name
    seq = str.lower(vector.sequence)
    seq = Dseq(seq.replace(' ', ''))
    L = len(str(seq))
    rseq = seq.reverse_complement()
    poss = []
    for primer in primers:
        p_seq = Dseq(primer.sequence.replace(' ', ''))
        p_seq_s = str.lower(str(p_seq)) # all lower case
        nt='atcgn'
        idt_codes_subtract1 = ['icy5', 'icy3', '5biosg', '(am)']
        idt_codes_subtract2 = ['dspacer']
        idt_codes_subtract3 = ['dbcoteg']
        idt_codes_subtract4 = ['biotinteg']
        idt_codes_plus1 = ['ds', 'idsp']

        Lp_subtract = 0
        for s1 in idt_codes_subtract1:
            if p_seq_s.find(s1) >= 0:
                Lp_subtract += 1
        for s2 in idt_codes_subtract2:
            if p_seq_s.find(s2) >= 0:
                Lp_subtract += 2
        for s3 in idt_codes_subtract3:
            if p_seq_s.find(s3) >= 0:
                Lp_subtract += 3
        for s4 in idt_codes_subtract4:
            if p_seq_s.find(s4) >= 0:
                Lp_subtract += 4
        for p1 in idt_codes_plus1:
            if p_seq_s.find(p1) >= 0:
                Lp_subtract -= 1

        Lp = 0
        for i in nt:
            Lp += p_seq_s.count(i)
        Lp = Lp - Lp_subtract
        # Lp = len(p_seq_s)
        if seq.find(p_seq_s) != -1: # match it
            position = seq.find(p_seq_s) + 1
            dir = 'forward'
            in_vector = True
        elif rseq.find(p_seq_s) != -1:
            position = rseq.find(p_seq_s) - L - 1
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
        p1_name = primer_1.name
        primer_2 = Primer.objects.get(id=check_box_list[1])
        p2_name = primer_2.name


        if primer_1.dir == 'reverse' and primer_2.dir == 'forward':
            pr = primer_1.position
            pr_name = primer_1.name
            pr_seq = primer_1.sequence
            pf = primer_2.position
            pf_name = primer_2.name
            pf_seq = primer_2.sequence
        elif primer_2.dir == 'reverse' and primer_1.dir == 'forward':
            pr = primer_2.position
            pr_name = primer_2.name
            pr_seq = primer_2.sequence
            pf = primer_1.position
            pf_name = primer_1.name
            pf_seq = primer_1.sequence

        else:
            pr = 0
            pf = 0
        if abs(pr) >= abs(pf):
            L_pcr = -pr - pf
        else:
            L_pcr = L - pr - pf
        show_seq = plotpcr(str(seq), pf_seq, pr_seq)
        primer_name = [pf_name] + [pr_name]
        primer_position = [pf, pr]
    else:
        L_pcr = 'You can only select two primers!!'
        primer_name = ['','']
        show_seq = "can't pcr"
        primer_name = [''] + ['']
        primer_position = ['x', 'x']

    return render(request, template_name='primer/seq.html',
                  context={'seq': seq, 'L': L, 'primers': primers, 'show_seq': show_seq,
                           'primerFilter': primerFilter, 'primer_name': primer_name,
                           'L_pcr': L_pcr, 'vector_name': vector_name, 'primer_position': primer_position,
                           })

tables.SingleTableView.table_pagination = False
class TableView(tables.SingleTableView):
    filter_class = None
    # table_class = SimpleTable
    # primers = Primer.objects.all()
    # queryset = primers
    # template_name = "primer/primer_list.html"
    def get_table_data(self):
        queryset_data = super(TableView, self).get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=queryset_data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class PrimerFilteredTableView(TableView):
    model = Primer
    table_class = SimpleTable
    template_name = "primer/primer_list.html"
    filter_class = PrimerFilter


class VectorCreateView(LoginRequiredMixin, CreateView):
    model = Vector
    template_name = 'primer/vector_form.html'
    fields = ['name', 'sequence']
    success_url = '/'
    def form_valid(self, form): # make authen to the user, over-write this fun.
        return super().form_valid(form)


def vector_index(request):
    vectors = Vector.objects.all()
    template_name = 'primer/vector_index.html'
    context = {
        'vectors': vectors,
    }
    return render(request, template_name, context)
