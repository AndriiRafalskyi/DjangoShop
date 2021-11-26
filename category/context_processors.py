from .models import Category

def category_options(request):
    return dict(category_options=Category.objects.all())