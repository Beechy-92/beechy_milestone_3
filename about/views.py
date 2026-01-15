from django.shortcuts import render


def about(request):
    """
    Render the About page with the main site layout.
    """
    return render(request, "about/about.html")
