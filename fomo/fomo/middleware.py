
def LastFiveMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('>>>>>> Middleware called at beginning')

        last5_list = request.session.get('last5')
        if last5_list is None:
            last5_list = []
        request.last5 = last5_list

        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        request.session['last5'] = request.last5[:5]
        return response

    return middleware
