from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import MenuItem, Category, Recipe, Order, OrderItem
from .models import Feedback
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def menu(request):
    categories = Category.objects.all()
    items = MenuItem.objects.select_related("category").all().order_by("-id")
    recipes = Recipe.objects.all().order_by("-id")  # ✅ template ishlatyapti

    return render(request, "restaurant_app/menu.html", {
        "categories": categories,
        "items": items,
        "recipes": recipes,  # ✅
    })


from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import MenuItem

@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    cart = request.session.get("cart", {})
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    total_qty = sum(cart.values())

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "ok": True,
            "item_id": item_id,
            "item_name": item.name,
            "qty": cart[key],
            "cart_total_qty": total_qty,
            "message": "Savatchaga qo‘shildi!"
        })

    return redirect(request.META.get("HTTP_REFERER", "/"))



def remove_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    key = str(item_id)

    if key in cart:
        del cart[key]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    ids = [int(i) for i in cart.keys()]
    items = MenuItem.objects.filter(id__in=ids)

    cart_items = []
    total = 0

    for item in items:
        qty = cart.get(str(item.id), 0)
        subtotal = item.price * qty
        total += subtotal
        cart_items.append({
            "item": item,
            "qty": qty,
            "subtotal": subtotal,
        })

    return render(request, "restaurant_app/cart.html", {
        "cart_items": cart_items,
        "total": total
    })


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("menu")

    items = []
    total = 0

    for item_id, qty in cart.items():
        menu_item = get_object_or_404(MenuItem, id=int(item_id))
        subtotal = menu_item.price * int(qty)
        total += subtotal
        items.append({
            "item": menu_item,
            "qty": int(qty),
            "subtotal": subtotal
        })

    if request.method == "GET":
        return render(request, "restaurant_app/checkout.html", {
            "items": items,
            "total": total
        })

    phone = request.POST.get("phone", "").strip()
    location = request.POST.get("location", "").strip()
    payment_method = request.POST.get("payment_method", "").strip()

    if not (phone and location and payment_method):
        return render(request, "restaurant_app/checkout.html", {
            "items": items,
            "total": total,
            "error": "Iltimos hamma maydonlarni to‘ldiring."
        })

    order = Order.objects.create(
        phone=phone,
        location=location,
        payment_method=payment_method,
        total=int(total),  # ✅ Decimal bo'lsa int/float moslang
    )

    for row in items:
        OrderItem.objects.create(
            order=order,
            menu_item=row["item"],
            quantity=row["qty"]
        )

    request.session["cart"] = {}
    request.session.modified = True
    request.session["last_order_id"] = order.id

    return redirect("order_complete")


def order_complete(request):
    order_id = request.session.get("last_order_id")
    if not order_id:
        return redirect("menu")

    order = get_object_or_404(Order, id=order_id)
    return render(request, "restaurant_app/order_complete.html", {"order": order})


def clear_cart(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("menu")



@require_POST
def set_cart_qty(request, item_id):
    qty = request.POST.get("qty")

    try:
        qty = int(qty)
    except (TypeError, ValueError):
        qty = 1

    if qty < 0:
        qty = 0

    # item mavjudligini tekshiramiz (xato item_id bo'lmasin)
    _ = get_object_or_404(MenuItem, id=item_id)

    cart = request.session.get("cart", {})
    key = str(item_id)

    if qty == 0:
        cart.pop(key, None)
    else:
        cart[key] = qty

    request.session["cart"] = cart
    request.session.modified = True

    total_qty = sum(cart.values())

    return JsonResponse({
        "ok": True,
        "item_id": item_id,
        "qty": cart.get(key, 0),
        "cart_total_qty": total_qty
    })


def send_feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Feedback.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False})