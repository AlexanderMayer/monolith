from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.db.models import *
from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
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
        return Post.objects.filter(date_created__gte=timezone.now() - datetime.timedelta(hours=1)).order_by(
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

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if UserVote.objects.filter(user=request.user, post=post.pk).exists():
            var = int(kwargs['pk'])
            return redirect(reverse('voted', args=(var,)))

        stub = Post.objects.get(pk=kwargs['pk'])
        if stub.was_published_recently():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('voted', args=(kwargs['pk'],)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        votes = Vote.objects.filter(post=post)
        context['votes'] = votes
        context['post'] = post
        return context

    def post(self, request, pk):
        post = self.get_object()
        choice_id = request.POST.get('vote')
        if choice_id:
            vote = Vote.objects.get(id=choice_id, post=post)
            vote.votes += 1
            vote.save()
            UserVote.objects.create(user=request.user, post=post)
        return redirect('voted', pk=post.id)


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
        total_votes = sum(vote.votes for vote in votes)
        vote_data = []
        for vote in votes:
            percent = (vote.votes / total_votes) * 100 if total_votes > 0 else 0
            vote_data.append({'choice': vote.choice, 'percent': percent})
        context['vote_data'] = vote_data
        context['post'] = post
        return context


class PollsList(generic.ListView):
    template_name = 'polls/polls_list.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Post.objects.all()
