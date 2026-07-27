import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Product, Wishlist, Order


# ---------------- HOME ----------------

def home(request):

    query = request.GET.get("q")
    category = request.GET.get("category")

    products = Product.objects.all()

    # Search
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Category Filter
    if category:
        products = products.filter(category__name__iexact=category)

    return render(request, "home.html", {
        "products": products
    })
def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    return render(request, "product_detail.html", {
        "product": product
    })


# ---------------- CART ----------------

def add_to_cart(request, id):

    cart = request.session.get("cart", {})

    # Old cart -> convert to dictionary
    if isinstance(cart, list):
        new_cart = {}

        for pid in cart:
            pid = str(pid)

            if pid in new_cart:
                new_cart[pid] += 1
            else:
                new_cart[pid] = 1

        cart = new_cart

    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    return redirect("cart")


def remove_from_cart(request, id):

    cart = request.session.get("cart", {})

    if isinstance(cart, list):
        cart = {}

    product_id = str(id)

    if product_id in cart:

        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


def cart(request):

    cart = request.session.get("cart", {})

    if isinstance(cart, list):

        new_cart = {}

        for pid in cart:
            pid = str(pid)

            if pid in new_cart:
                new_cart[pid] += 1
            else:
                new_cart[pid] = 1

        cart = new_cart

        request.session["cart"] = cart

    items = []

    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

        total += subtotal

    return render(request, "cart.html", {
        "items": items,
        "total": total,
    })


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(request, "register.html", {
        "form": form
    })


# ---------------- WISHLIST ----------------

@login_required
def wishlist(request):

    items = Wishlist.objects.filter(user=request.user)

    return render(request, "wishlist.html", {
        "items": items
    })


@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("wishlist")


# ---------------- CHECKOUT ----------------

@login_required
def checkout(request):

    cart = request.session.get("cart", {})

    if isinstance(cart, list):
        new_cart = {}

        for pid in cart:
            pid = str(pid)

            if pid in new_cart:
                new_cart[pid] += 1
            else:
                new_cart[pid] = 1

        cart = new_cart
        request.session["cart"] = cart

    items = []
    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

        total += subtotal

    if request.method == "POST":

        Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            total_amount=total,
        )

        request.session["cart"] = {}

        return redirect("order_success")

    return render(request, "checkout.html", {
        "items": items,
        "total": total,
    })

@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "my_orders.html", {
        "orders": orders
    })

@login_required
def order_success(request):
    return render(request, "order_success.html")

@login_required
def profile(request):

    total_orders = Order.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, "profile.html", {
        "total_orders": total_orders,
        "wishlist_count": wishlist_count,
    })

def contact(request):
    return render(request, "contact.html")

from django.http import JsonResponse
import requests

def ai_recommend(request):

    skin = request.GET.get("skin", "normal")

    response = requests.get(
        f"https://glowcart-ai-backend-1301.onrender.com/recommend?skin={skin}"
    )

    return JsonResponse(response.json())

def ai_page(request):
    return render(request, "ai_recommend.html")