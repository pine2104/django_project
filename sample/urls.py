"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from uploader import views as uploader_views
from primer import views as primer_views
from posts import views as posts_views
from users import views as user_views
from index import views as index_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', posts_views.index, name='homepage'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('post/<int:pk>/', posts_views.PostDetailView.as_view(), name='postdetail'),
    path('post/new/', posts_views.PostCreateView.as_view(), name='postcreate'),
    path('category/', posts_views.show_category, name='category'),
    path('category/new/', posts_views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/delete/', posts_views.CateDeleteView.as_view(), name='category_delete'),
    path('category/<int:pk>/', posts_views.CateDetailView.as_view(), name='category_detail'),

    path('post/<int:pk>/update/', posts_views.PostUpdateView.as_view(), name='postupdate'),
    path('post/<int:pk>/delete/', posts_views.PostDeleteView.as_view(), name='postdelete'),

    # path('fileupload/', uploader_views.UploadView.as_view(), name='fileupload'), #its name is 'fileupload'
    path('fileupload/', uploader_views.upload_file, name='fileupload'),

    path('delete/<int:pk>/', uploader_views.FileDeleteView.as_view(), name='delete'),
    path('primerinput/', login_required(primer_views.PrimerFormView.as_view()), name='primerinput'),
    # path('primer/', primer_views.index, name='primer'),
    # path('primerlist/', primer_views.PrimerListView.as_view(), name='primerlist'),
    # path('primerupload/', primer_views.PrimerUploadView.as_view(), name='primerupload'),
    path('primer/<int:pk>/', primer_views.PrimerDetailView.as_view(), name='primerinfo'),
    path('primer/<int:pk>/update', primer_views.PrimerUpdateView.as_view(), name='primerupdate'),
    path('primer/<int:pk>/delete/', primer_views.PrimerDeleteView.as_view(), name='primerdelete'),
    path('seq/vector/', primer_views.SelectVector, name='seqvector'),
    path('primer/', primer_views.PrimerFilteredTableView.as_view(), name='primer'),

    # path('seq/vector/', primer_views.PrimerVectorUpdateView.as_view(), name='seqvector'),
    path('seq/', primer_views.calpcr, name='seq'),
    path('vector/new/', primer_views.VectorCreateView.as_view(), name='vector_create'),
    path('vector/', primer_views.vector_index, name='vector_index'),

    path('mypost/', posts_views.userprofile, name='myposts'),
    path('protocols/TPM/', posts_views.protocols_TPM, name='protocols_TPM'),
    path('protocols/FRET/', posts_views.protocols_FRET, name='protocols_FRET'),
    path('protocols/CoSMoS/', posts_views.protocols_CoSMoS, name='protocols_CoSMoS'),
    path('protocols/OT/', posts_views.protocols_OT, name='protocols_OT'),

    path('JC/new/', login_required(posts_views.JCForm.as_view()), name='JCcreate'),
    path('JC/<int:pk>/', posts_views.JCDetailView.as_view(), name='JCdetail'),
    path('JC/<int:pk>/update/', posts_views.JCUpdateView.as_view(), name='JCupdate'),
    path('JC/<int:pk>/delete/', posts_views.JCDeleteView.as_view(), name='JCdelete'),
    path('JC/', posts_views.index_JC, name='JC'),

    path('form/', include('index.urls')),

    path('form/', index_views.index, name="index"),
    # path('login', views.login_view, name="login"),
    # path('register', views.register, name="register"),
    # path('logout', views.logout_view, name="logout"),
    path('form/create', index_views.create_form, name="create_form"),
    path('form/create/contact', index_views.contact_form_template, name="contact_form_template"),
    path('form/create/feedback', index_views.customer_feedback_template, name="customer_feedback_template"),
    path('form/create/event', index_views.event_registration_template, name="event_registration_template"),
    path('form/<str:code>/edit', index_views.edit_form, name="edit_form"),
    path('form/<str:code>/edit_title', index_views.edit_title, name="edit_title"),
    path('form/<str:code>/edit_description', index_views.edit_description, name="edit_description"),
    path('form/<str:code>/edit_background_color', index_views.edit_bg_color, name="edit_background_color"),
    path('form/<str:code>/edit_text_color', index_views.edit_text_color, name="edit_text_color"),
    path('form/<str:code>/edit_setting', index_views.edit_setting, name="edit_setting"),
    path('form/<str:code>/delete', index_views.delete_form, name="delete_form"),
    path('form/<str:code>/edit_question', index_views.edit_question, name="edit_question"),
    path('form/<str:code>/edit_choice', index_views.edit_choice, name="edit_choice"),
    path('form/<str:code>/add_choice', index_views.add_choice, name="add_choice"),
    path('form/<str:code>/remove_choice', index_views.remove_choice, name="remove_choice"),
    path('form/<str:code>/get_choice/<str:question>', index_views.get_choice, name="get_choice"),
    path('form/<str:code>/add_question', index_views.add_question, name="add_question"),
    path('form/<str:code>/delete_question/<str:question>', index_views.delete_question, name="delete_question"),
    path('form/<str:code>/score', index_views.score, name="score"),
    path('form/<str:code>/edit_score', index_views.edit_score, name="edit_score"),
    path('form/<str:code>/answer_key', index_views.answer_key, name="answer_key"),
    path('form/<str:code>/feedback', index_views.feedback, name="feedback"),
    path('form/<str:code>/viewform', index_views.view_form, name="view_form"),
    path('form/<str:code>/submit', index_views.submit_form, name="submit_form"),
    path('form/<str:code>/responses', index_views.responses, name='responses'),
    path('form/<str:code>/response/<str:response_code>', index_views.response, name="response"),
    path('form/<str:code>/response/<str:response_code>/edit', index_views.edit_response, name="edit_response"),
    path('form/<str:code>/responses/delete', index_views.delete_responses, name="delete_responses"),
    path('403', index_views.FourZeroThree, name="403"),
    path('404', index_views.FourZeroFour, name="404"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)