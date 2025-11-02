from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

from django.http import HttpResponse
def index(request):
    return HttpResponse("StillMind is app for mindful blogging.")

class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = "still_mind/post_list.html"

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by("-created_at")

class PostDetailView(DetailView):
    model = Post
    template_name = "still_mind/post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "still_mind/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "still_mind/post_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("still_mind:post_list")
    template_name = "still_mind/post_confirm_delete.html"

# newline at end of file
