from . models import Category

#pass request in argument and return in dictinory
def category_links(request):
    links = Category.objects.all()
    return dict(links=links)