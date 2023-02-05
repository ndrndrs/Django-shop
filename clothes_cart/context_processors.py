from .models import Cart, Item
from .views import _cart_session_id


def items_counter(request):
    count = 0
    if 'admin' in request.path:
        return ()
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_session_id(request))
            cart_items = Item.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                count += item.quantity

        except Cart.DoesNotExist:
            count = 0

    return dict(count=count)
