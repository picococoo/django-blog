from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.views import generic

from .forms import PostForm
from .models import BlogPost


class IndexView(generic.ListView):
    model = BlogPost
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.order_by('-timestamp')


class DetailView(generic.DetailView):
    model = BlogPost
    template_name = 'post/detail.html'
    context_object_name = 'post'
    slug_field = 'title'
    slug_url_kwarg = 'title'

    # def get_object(self, **kwargs):
        # title = self.kwargs.get('title')
        # try:
            # article = BlogPost.objects.get(title=title)
        # except BlogPost.DoesNotExist:
            # raise Http404('Article does not exist')
        # return article


class MyLoginMixin(LoginRequiredMixin):
    login_url = '/login'
    # redirect_field_name = 'redirect_to'


# class NewArticle(MyLoginMixin, FormView):
    # template_name = 'post/new.html'
    # form_class = PostForm
    # success_url = '/'


class NewArticle(MyLoginMixin, CreateView):
    model = BlogPost
    # fields = ['title', 'body']
    form_class = PostForm
    template_name = 'post/new.html'


class UpdateArticle(MyLoginMixin, UpdateView):
    model = BlogPost
    # fields = ['title', 'body']
    form_class = PostForm
    template_name = 'post/edit.html'

    def get_object(self):
        return BlogPost.objects.get(title=self.kwargs.get('title'))


# @login_required
# def new_article(request):
    # if request.method == 'POST':
        # form = PostForm(request.POST)
        # if form.is_valid():
            # form.save()
            # return redirect('/')
        # print(form)
        # return redirect(reverse('blog:new_post'))
    # else:
        # form = PostForm()
        # return render(request, 'post/new.html', {'form': form})


# @login_required
# def edit_article(request, title):
    # pass


class DeleteArticle(MyLoginMixin, View):
    def get(self, request, title):
        post = BlogPost.objects.filter(title=title)
        post.delete()
        return redirect('/')


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            return HttpResponseRedirect(request.session.get('login_from', '/'))
        return redirect(reverse('blog:index'))  # Need to be corrected


class Register(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login_user(request)
        return redirect(reverse('blog:index'))


class Logout(View):
    def get(self, request):
        logout_user(request)
        return redirect('/')


class LatestEntriesFeed(Feed):
    title = 'Feeds'
    link = '/feed/'
    description = 'Show lastest posts'

    def items(self):
        return BlogPost.objects.order_by('-timestamp')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('blog:detail_post', args=[item.title])
