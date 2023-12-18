from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import *

from .forms import *
from .models import *


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'monolith/index.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Post.objects.filter(date_created__gte=timezone.now() - datetime.timedelta(days=1)).order_by(
            '-date_created')


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

    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user.filter()
    #
    #
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        votes = Vote.objects.filter(post=post)
        context['votes'] = votes
        context['post'] = post
        return context

    def post(self, request):
        question = request.POST['vote']
        stub = Vote.objects.get(choise=question)
        stub.votes += 1
        return redirect(reverse_lazy('voted', kwargs={'pk': stub.post}))


    # def post(self, request, **kwargs):
    #     post = Post.objects.get(id=kwargs['pk'])
    #
    #     if request.POST.get('choice'):
    #         vote = Vote.objects.get(choice=request.POST.get('choice'), post=post)
    #         vote.votes += 1
    #         vote.save()
    #         return redirect(reverse('voted', kwargs={'pk': post.pk}))
    #
    #     return redirect('/')


def create_post(request):
    if request.method == 'POST':
        form = VoteForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            post_obj = Post.objects.create(
                name=cd['name'],
                content=cd['content'],
                photo=cd['photo']
            )

            Vote.objects.create(choice=cd['choice1'], post=post_obj, )
            Vote.objects.create(choice=cd['choice2'], post=post_obj, )
            Vote.objects.create(choice=cd['choice3'], post=post_obj, )
            return redirect('/')
    else:
        form = VoteForm()
        return render(request, 'polls/create.html', context={'form': form})


class VotedView(generic.DetailView):
    model = Post
    template_name = 'polls/voted.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        votes = Vote.objects.filter(post=post)
        context['votes'] = votes
        context['post'] = post
        return context
