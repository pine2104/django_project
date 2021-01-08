# from django.shortcuts import render
# from .models import User, Choices, Questions, Answer, Form, Responses
# from django.contrib.auth.decorators import login_required
# from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.urls import reverse_lazy, reverse
#
# import json
# import random
# import string
# from django.views.generic.edit import FormView
#
# from .forms import QuestionsForm

# Create your views here.

# class ChoiceCreateView(LoginRequiredMixin, CreateView):
#     model = Choices
#     fields = [ 'choice']
#     #success_url = '/poll/'
#     success_url = reverse_lazy('create_poll')
#     def form_valid(self, form): # make authen to the user, over-write this fun.
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['choices'] = Choices.objects.all()
#         return context
#
# class ChoiceListView(ListView):
#     model = Choices
#     template_name = 'pollform/choices_form.html'
#     context_object_name = 'choices'






#
# class QuestionsForm(FormView):
#     template_name = 'pollform/poll_list.html'
#     form_class = QuestionsForm
#     # model = Primer
#     # success_url = reverse_lazy('primerlist')  # back to url name: fileupload (in urls)
#     # context = {'form': }
#     def form_valid(self, form): # FormView does not save, you need to add
#         form.instance.created_by = self.request.user
#         form.save()
#         return super(QuestionsForm, self).form_valid(form)
#
#
# @login_required(login_url='/users/login/')
# def create_form(request):
#     # Create a blank form API
#     # if request.method == "POST":
#         # data = json.loads(request.body)
#         # title = data["title"]
#     title = 'poll1'
#     code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
#     choices = Choices(choice = "Option 1")
#     choices.save()
#     question = Questions(question_type = "multiple choice", question= "Untitled Question", required= False)
#     question.save()
#     question.choices.add(choices)
#     question.save()
#     # form = Form(code = code, title = title, creator=request.user)
#     # form.save()
#     # form.questions.add(question)
#     # form.save()
#     context = {
#
#         'code': code,
#         'choices': choices,
#         'question': question,
#         # 'form': form,
#
#     }
#     return render(request, 'pollform/poll_list.html', context)
