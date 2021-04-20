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
from .pcr import hamming_distance, match_primer, plotpcr, setL_pcr, get_prop_primers



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
    fields = ['name', 'sequence', 'project', 'modification_5', 'modification_3', 'modification_internal', 'who_ordered', 'purpose', 'price', 'volumn', 'vendor']
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
        if 'Select_Pairs' in request.POST:
            return redirect('seq')
        elif 'Set_PCR_Length' in request.POST:
            return redirect('seq_setL')

    return render(request, template_name, context)



def show_pcr(request):
    check_box_list = request.session['selected_primer_id']
    vector_name = request.session['vector_name']
    L = request.session['L']
    primer_name = request.session['primer_name']
    primer_position = request.session['primer_position']
    L_pcr = request.session['L_pcr']
    show_seq = request.session['show_seq']

    return render(request, template_name='primer/show_pcr_seq.html',
                  context={'vector_name': vector_name, 'L': L, 'primer_name': primer_name,
                           'primer_position': primer_position, 'L_pcr': L_pcr,
                           'show_seq': show_seq, 'check_box_list': check_box_list
                           })

def calpcr_setL(request):
    primers = Primer.objects.all()
    vector = primers[0].vector
    vector_name, seq, L, position, dir, in_vector = get_prop_primers(primers, vector)
    primers = primers.filter(in_vector=True).order_by('position')
    if request.method == 'POST':

        check_box_list = request.POST.getlist("check_box")
        request.session['selected_primer_id'] = check_box_list

        # L_set = int(request.POST.get('L_set'))
        # tol = int(request.POST.get('tol'))
        if len(check_box_list) >= 1 and (request.POST.get('L_set') != None) and (request.POST.get('tol') != None):
            L_set = int(request.POST.get('L_set'))
            tol = int(request.POST.get('tol'))
            # L_pcr = []
            for check_box in check_box_list:
                p1 = Primer.objects.get(id=check_box)
                p1_pos = p1.position
                name_collect = [p1.name]
                for primer in primers:
                    L_pcr = setL_pcr(L, p1_pos, primer.position)
                    primer.L_pcr = L_pcr
                    primer.save()
                    if (L_pcr > L_set-tol) and (L_pcr < L_set+tol): ## reverse
                        name_collect += [primer.name]
                primers_collect = primers.filter(name__in=name_collect).order_by('position')
                primerFilter = PrimerFilter(request.POST, queryset=primers_collect)

        else:
            primerFilter = PrimerFilter(request.POST, queryset=primers)

    else:
        L_pcr = 'You can only select two primers!!'
        primer_name = ['','']
        primer_position = ['x', 'x']
        primerFilter = PrimerFilter(request.POST, queryset=primers)

    return render(request, template_name='primer/set_pcr_length.html',
                  context={ 'primers': primers,
                           'primerFilter': primerFilter,'L_pcr': L_pcr,

                           })


def calpcr(request):
    primers = Primer.objects.all()
    vector = primers[0].vector
    vector_name, seq, L, position, dir, in_vector = get_prop_primers(primers, vector)
    primers = primers.filter(in_vector=True).order_by('position')
    primerFilter = PrimerFilter(queryset=primers)

    if request.method == 'POST' or 'cal' in request.POST:

        check_box_list = request.POST.getlist("check_box")
        primerFilter = PrimerFilter(request.POST, queryset=primers)
        request.session['selected_primer_id'] = check_box_list

        # if request.method == 'POST' and 'cal' in request.POST:
        # check_box_list = request.POST.getlist("check_box")
        if len(check_box_list) == 2:
            primer_1 = Primer.objects.get(id=check_box_list[0])
            primer_2 = Primer.objects.get(id=check_box_list[1])

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

            else: ## not to pcr mode
                pr = 0
                pf = 0
                pf_seq = ''
                pr_seq = ''
                pf_name = ''
                pr_name = ''
            if abs(pr) >= abs(pf):
                L_pcr = -pr - pf
            else:
                L_pcr = L - pr - pf

            show_seq = plotpcr(str(seq), pf_seq, pr_seq)
            primer_name = [pf_name] + [pr_name]
            primer_position = [pf, pr]

            request.session['show_seq'] = show_seq
            request.session['vector_name'] = vector_name
            request.session['L'] = L
            request.session['primer_position'] = primer_position
            request.session['L_pcr'] = L_pcr
            request.session['primer_name'] = primer_name
            return redirect('showpcr')

    return render(request, template_name='primer/seq.html',
                  context={'vector_name': vector_name, 'seq': seq, 'L': L, 'primers': primers,
                           'primerFilter': primerFilter,
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

class VectorDetailView(DetailView):
    model = Vector
    template_name = 'primer/vector_detail.html'

class VectorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vector
    template_name = 'primer/vector_confirm_delete.html'
    success_url = '/'

class VectorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vector
    template_name = 'primer/vector_form.html'
    fields = ['name', 'sequence']

def vector_index(request):
    vectors = Vector.objects.all()
    template_name = 'primer/vector_index.html'
    context = {
        'vectors': vectors,
    }
    return render(request, template_name, context)
