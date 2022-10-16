from category.models import Category


def menu_links(request):
    links = Category.objects.all()
    return dict(categories_list=links)
