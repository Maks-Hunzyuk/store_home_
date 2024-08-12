from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from carts.utils import get_user_carts

from goods.models import Products
from carts.models import Cart


def cart_add(request, product_slug):
    """Добавление товара в карзину"""
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    return redirect(request.META["HTTP_REFERER"])


def cart_change(request, product_slug):
    ...


def cart_remove(request, cart_id):
    """Удаление карты товара из карзины"""
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META["HTTP_REFERER"])