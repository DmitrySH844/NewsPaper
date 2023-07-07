from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm

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
<<<<<<< HEAD
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

class PostCreate(CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'creation.html'
    success_url = reverse_lazy('posts_lst')

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'creation.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_lst')
=======
    pk_url_kwarg = "id"
>>>>>>> 38b278149551e42a18b4f44b3dcd7ac5364e08b9
