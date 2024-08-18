from typing import Any
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart
from orders.models import Order, OrderItem


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    
    def get_success_url(self) -> str:
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")
    
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"{user.username} вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_success_url())
            
    def get_context_data(self, **kwargs ) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Авторизация"


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Регистрация"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(self.get_success_url())
        

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, f"Профиль успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Кабинет"
        context["orders"] = Order.objects.filter(user=self.request.user).prefetch_related(
        Prefetch(
            "orederitem_set",
            queryset=OrderItem.objects.select_related("product")
        )
    ).order_by("-id")
        return context


class UserCartView(TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Корзина"

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли")
    auth.logout(request)
    return redirect(reverse("main:index"))
