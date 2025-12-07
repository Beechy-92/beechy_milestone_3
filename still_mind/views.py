from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q

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
        qs = Post.objects.filter(author=self.request.user).order_by("-created_at")

        # Status filter (all / published / draft)
        status = self.request.GET.get("status")
        if status == "published":
            qs = qs.filter(status=1)
        elif status == "draft":
            qs = qs.filter(status=0)

        # Search filter
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(content__icontains=query)
                | Q(mood__icontains=query)
            )

        return qs


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            posts = Post.objects.filter(author=user).order_by("-created_at")

            context["recent_posts"] = posts[:5]
            context["published_count"] = posts.filter(status=1).count()
            context["draft_count"] = posts.filter(status=0).count()

            mood_stats = (
                posts.filter(status=1)
                .values("mood")
                .annotate(count=Count("mood"))
                .order_by("-count")
            )
            context["mood_stats"] = mood_stats

        return context
    