from typing import Any
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Главная страница"
        context["content"] = "Магазин мебели - HOME"
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - О нас"
        context["content"] = "О нас"
        context["text_on_page"] = "Текст почему этот магазин такой классный"
