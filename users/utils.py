def is_superuser(request):
    import ipdb
    ipdb.set_trace()
    print(request)
    return request.user.is_superuser