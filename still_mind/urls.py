from django.urls import path
from . import views


app_name = "still_mind"

urlpatterns = [
    # Home and post list
    path("", views.HomeView.as_view(), name="home"),
    path("posts/", views.PostListView.as_view(), name="post_list"),

    # --- Specific routes FIRST ---
    path(
        "post/create/",
        views.PostCreateView.as_view(),
        name="post_create",
    ),
    path(
        "post/<slug:slug>/edit/",
        views.PostUpdateView.as_view(),
        name="post_edit",
    ),
    path(
        "post/<slug:slug>/delete/",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),

    # --- Catch-all slug LAST ---
    path(
        "post/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
]
