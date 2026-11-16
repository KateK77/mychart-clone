"""Serve browser routes from the compiled React app in a single-origin deployment."""
from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe


@require_safe
@never_cache
def frontend(request):
    index = settings.BASE_DIR.parent / "frontend" / "dist" / "index.html"
    if not index.is_file():
        raise Http404("Build the frontend before starting the hosted service.")
    return FileResponse(index.open("rb"), content_type="text/html; charset=utf-8")
