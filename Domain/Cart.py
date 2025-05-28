from itertools import product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            self.session["cart"] = {}
            self.cart = self.session["cart"]
        else:
            self.cart = cart

    def add(self, product):
        id = str(product.id)
        if id not in self.cart.keys():
            self.cart[id] = {
                "product_id": product.id,
                "name": product.name,
                "quantity": 1,
                "price": product.price,
                "image": product.image.url,
                "subtotal": product.price,
            }
        else:
            self.cart[id]["quantity"] += 1
            self.cart[id]["subtotal"] += product.price
        self.save_cart()
    
    def save_cart(self):
        self.session["cart"] = self.cart
        self.session.modified = True
    
    def remove(self, product):
        id = str(product.id)
        if id in self.cart:
            del self.cart[id]
            self.save_cart()
        
    def subtract(self, product):
        id = str(product.id)
        if id in self.cart.keys():
            self.cart[id]["quantity"] -= 1
            self.cart[id]["subtotal"] -= product.price
            if self.cart[id]["quantity"] <= 0:
                self.remove(product)
            self.save_cart()
    
    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

