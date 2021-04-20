from . import views as posts_views
from django.urls import path
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('', posts_views.index, name='homepage'),

    path('category/', posts_views.show_category, name='category'),
    path('category/new/', posts_views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/delete/', posts_views.CateDeleteView.as_view(), name='category_delete'),
    path('category/<int:pk>/', posts_views.CateDetailView.as_view(), name='category_detail'),

    path('post/<int:pk>/', posts_views.PostDetailView.as_view(), name='postdetail'),
    path('post/new/', posts_views.PostCreateView.as_view(), name='postcreate'),
    path('post/<int:pk>/update/', posts_views.PostUpdateView.as_view(), name='postupdate'),
    path('post/<int:pk>/delete/', posts_views.PostDeleteView.as_view(), name='postdelete'),
    path('mypost/', posts_views.userprofile, name='myposts'),

    path('protocols/TPM/', posts_views.protocols_TPM, name='protocols_TPM'),
    path('protocols/FRET/', posts_views.protocols_FRET, name='protocols_FRET'),
    path('protocols/CoSMoS/', posts_views.protocols_CoSMoS, name='protocols_CoSMoS'),
    path('protocols/OT/', posts_views.protocols_OT, name='protocols_OT'),

    path('JC/', posts_views.index_JC, name='JC'),
    path('JC/new/', login_required(posts_views.JCForm.as_view()), name='JCcreate'),
    path('JC/<int:pk>/', posts_views.JCDetailView.as_view(), name='JCdetail'),
    path('JC/<int:pk>/update/', posts_views.JCUpdateView.as_view(), name='JCupdate'),
    path('JC/<int:pk>/delete/', posts_views.JCDeleteView.as_view(), name='JCdelete'),
]