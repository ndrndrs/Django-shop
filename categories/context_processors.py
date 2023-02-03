from .models import Category


def links_menu(request):
    links = Category.objects.all()
    all_links = {
        'links': links
    }
    return all_links