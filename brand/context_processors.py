from .models import Brand


def brand_links(request):
    links = Brand.objects.all()
    return dict(links=links)
