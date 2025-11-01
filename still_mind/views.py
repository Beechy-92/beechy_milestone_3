from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

from django.http import HttpResponse
def index(request):
    return HttpResponse("StillMind is alive ✨")

class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    paginate_by = 5
    template_name = "still_mind/post_list.html"

class PostDetailView(DetailView):
    model = Post
    template_name = "still_mind/post_detail.html"

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

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "still_mind/post_confirm_delete.html"

# newline at end of file
