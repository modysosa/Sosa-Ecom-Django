from .cart import Cart

# Creat context processor so our cart can work on all page of the site
def cart(request):
    # return the default data from our Cart
    return {'cart': Cart(request)}
