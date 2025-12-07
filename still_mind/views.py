from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post
from .forms import PostForm


def index(request):
    return HttpResponse("StillMind is app for mindful blogging.")


class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the logged-in user is the author of the object.
    Used on detail / edit / delete views.
    """
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    template_name = "still_mind/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Only published posts for THIS user
        return (
            Post.objects
            .filter(author=self.request.user, status=1)
            .order_by("-created_at")
        )


class PostDetailView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    model = Post
    template_name = "still_mind/post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


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


class HomeView(TemplateView):
    template_name = "still_mind/home.html"