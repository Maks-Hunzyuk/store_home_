from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_list_or_404
from django.views.generic import ListView, DetailView

from goods.models import Products, Categories
from goods.utils import q_search


class CatalogView(ListView):
    model = Products
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("query")

        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = get_list_or_404(super().get_queryset().filter(category__slug=category_slug))
            if not goods.exist():
                return Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
        
        return goods

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get("category_slug")
        context["categpries"] = Categories.objects.all()
        return context


class ProductView(DetailView):
    slug_url_kwarg = "product_slug"
    template_name = "goods/product.html"
    context_object_name = "product"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.context_object_name
        return context