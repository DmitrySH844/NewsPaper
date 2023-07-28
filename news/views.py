from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from .filters import PostFilter, CategoryFilter, WeeklyPostFilter
from django.urls import reverse_lazy
from .forms import PostForm, SubscribeForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

class HomePageView(RedirectView):
    url = 'posts/'
    permanent = True

class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post'
    pk_url_kwarg = "pk"

class PostSearch(ListView):
    model = Post
    template_name = 'searching.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('posts_lst')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'creation.html'
    success_url = reverse_lazy('posts_lst')

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'creation.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_lst')
    pk_url_kwarg = "pk"

class SubscribeView(TemplateView):
    model = Category
    form_class = SubscribeForm
    template_name = 'subscribe.html'
    context_object_name = 'subscribe'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategoryFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = CategoryFilter(self.request.GET, queryset=Category.objects.all())
        context['filterset'] = filterset
        return context

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return redirect('../')
        return render(request, self.template_name, {'form': form})

class WeeklyPostsView(ListView):
    model = Post
    template_name = 'weekly_digest_mail.html'
    context_object_name = 'posts'

    # success_url = reverse_lazy('posts_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = WeeklyPostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список постов
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
