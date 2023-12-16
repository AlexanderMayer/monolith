from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import *

from .forms import *
from .models import *


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'monolith/index.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Post.objects.order_by('-date_created')


class Login(LoginView):
    template_name = 'registration/login.html'


class Profile(DetailView):
    template_name = 'monolith/profile.html'
    model = User
    context_object_name = 'profile'


def delete(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect(reverse('home'))


class UserView(UpdateView):
    template_name = 'monolith/update.html'
    model = User
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        update_session_auth_hash(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])


class DetailView(generic.DetailView):
    model = Post
    template_name = 'polls/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        votes = Vote.objects.filter(post=post)
        context['votes'] = votes
        return context


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        formset = VoteFormSet(request.POST, prefix='votes')
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.save()
            formset.instance = post
            formset.save()
            return redirect('home')
    else:
        form = PostForm()
        formset = VoteFormSet()

    return render(request, 'polls/create.html', {'form': form, 'formset': formset})
