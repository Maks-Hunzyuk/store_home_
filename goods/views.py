from django.shortcuts import render

from goods.models import Categories


def catalog(request):
    categories = Categories.objects.all()
    context = {
        "title": "Home - Каталог",
        "categories": categories
    }
    return render(request, "goods/catalog.html", context)


def product(request):
    return render(request, "goods/product.html")
