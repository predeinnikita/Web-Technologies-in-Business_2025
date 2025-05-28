def total_cart(request):
    total = 0
    total_items = 0
    if request.user.is_authenticated:
        if "cart" in request.session.keys():
            for key, value in request.session["cart"].items():
                total += float(value.get("subtotal", 0))
                total_items += 1
    return {"total_cart": total, "total_items": total_items}
