from catalog import models as cmod

def LastFiveMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):

        last5_list = request.session.get('last5')
        if last5_list is None:
            last5_list = []

        last_5_products = []
        for id in last5_list[:5]:
            last_5_products.append(cmod.Product.objects.get(id=id))

        request.last5 = last5_list[:5]
        request.last5products = last_5_products

        response = get_response(request)

        request.session['last5'] = request.last5[:5]
        return response

    return middleware
