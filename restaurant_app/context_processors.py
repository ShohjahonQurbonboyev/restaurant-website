def cart_count(request):
    cart = request.session.get("cart", {})  # {"1": 2, "2": 1}
    return {"cart_count": sum(cart.values())}
