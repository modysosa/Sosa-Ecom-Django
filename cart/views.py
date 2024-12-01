from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products" :cart_products, "quantities" : quantities, "totals":totals})




def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        # responce = JsonResponse({'Product Name : ': product.name})
        responce = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added Successfully To your Cart..."))
        return responce
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product ID
        product_id = int(request.POST.get('product_id'))
        # Call delete method in Cart
        cart.delete(product=product_id)  # Corrected parameter name
        # Return response
        response = JsonResponse({'product': product_id})
        messages.success(request, ("the product was deleted successfully..."))
        return response
    return HttpResponseBadRequest('Invalid request')


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Your cart has been updated..."))
        return response
        # return redirect('cart_summary')
