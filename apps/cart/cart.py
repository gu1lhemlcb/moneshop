from django.conf import settings

from apps.store.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session # !!!!  + ne pas oublier, l'attribut session est un dictionnnaire
        cart = self.session.get(settings.CART_SESSION_ID) #  dans la doc django on utilise normalement request.session.get(...), voir : https://docs.djangoproject.com/fr/1.10/topics/http/sessions/

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()

        product_clean_ids = []

        for p in product_ids:
            product_clean_ids.append(p)

            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.price

        print('Product_id:', product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,'price': price, 'id': product_id} # !

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] + 1 #Si mon produit est bien dans self.cart alors j'ajoute une unité en quantité puis je sauvegarde
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    #ci dessous une fonction donnnant la quantité totale de produits, tous confondus
    def get_total_length(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_cost(self):
        if "total_price" in self.cart.values():
            return sum(float(item['total_price']) for item in self)
        else:
            return 0
    