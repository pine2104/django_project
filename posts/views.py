from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views.generic.edit import FormView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Jcpaper
from django.contrib.auth.decorators import login_required
from .filters import PostFilter, JCFilter
from .forms import JCForm
from django.urls import reverse_lazy, reverse

from django.utils import timezone
from django.urls import reverse_lazy

# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-date_posted')
    postFilter = PostFilter(queryset=posts)

    if request.method == 'POST':
        postFilter = PostFilter(request.POST, queryset=posts)

    context = {
        'postFilter':postFilter
    }
    return render(request, 'posts/index.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'file', 'content', 'private']
    success_url = '/'
    template_name = 'posts/post_form.html'
    def form_valid(self, form): # make authen to the user, over-write this fun.
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    # template_name = 'posts/post_detail.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['now'] = timezone.now()
#        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    success_url = '/'
    def form_valid(self, form): # make authen to the user, over-write this fun.
        return super().form_valid(form)

class CateDetailView(DetailView):
    model = Category

class CateDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/'
    template_name = 'posts/category_confirm_delete.html'

    # def get_success_url(self):
    #     return reverse('category_detail')

def show_category(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'posts/category_index.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'file', 'content', 'private']

    def form_valid(self, form): # make authen to the user, over-write this function.
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_detail.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# user posts filter
@login_required(login_url='/users/login/')
def userprofile(request):
    user = request.user
    user_posts = Post.objects.filter(author=request.user)
    template = 'posts/own_post.html'
    context = {
        'user_posts': user_posts,
        'user': user
    }
    return render(request, template, context)

def protocols_TPM(request):
    TPMposts = Post.objects.filter(category__name="TPM")

    context = {
        'TPMposts':TPMposts
    }
    return render(request, 'posts/protocols_TPM.html', context)

def protocols_FRET(request):
    FRETposts = Post.objects.filter(category__name="FRET")

    context = {
        'FRETposts':FRETposts
    }
    return render(request, 'posts/protocols_FRET.html', context)

def protocols_CoSMoS(request):
    CoSMoSposts = Post.objects.filter(category__name="CoSMoS")

    context = {
        'CoSMoSposts':CoSMoSposts
    }
    return render(request, 'posts/protocols_CoSMoS.html', context)

def protocols_OT(request):
    OTposts = Post.objects.filter(category__name="Optical Tweezers")

    context = {
        'OTposts':OTposts
    }
    return render(request, 'posts/protocols_OT.html', context)

### for JCpaper
def index_JC(request):
    JC = Jcpaper.objects.all().order_by('-date_posted')
    jcFilter = JCFilter(queryset=JC)

    if request.method == 'POST':
        jcFilter = JCFilter(request.POST, queryset=JC)

    context = {
        'jcFilter':jcFilter
    }
    return render(request, 'posts/JC_index.html', context)

class JCForm(FormView):
    template_name = 'posts/jcpaper_form.html'
    form_class = JCForm
    success_url = reverse_lazy('JC')  # back to url name: fileupload (in urls)
    def form_valid(self, form):
        form.save()
        return super(JCForm, self).form_valid(form)

class JCDetailView(DetailView):
    model = Jcpaper
    template_name = 'posts/JC_detail.html'

class JCUpdateView(LoginRequiredMixin, UpdateView):
    model = Jcpaper
    fields = ['title', 'journal','hwl_recommend', 'presenter', 'file', 'location', 'time', 'link', 'content']
    template_name = 'posts/jcpaper_form.html'
    queryset = Jcpaper.objects.all()

class JCDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Jcpaper
    # template_name = 'posts/post_detail.html'
    def get_success_url(self):
        return reverse('JC')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.presenter:
            return True
        return False
