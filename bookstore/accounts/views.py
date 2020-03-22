from django.shortcuts import render

def selections(request):
    return render(request, 'accounts/selections.html')

def wish_list(request):
    return render(request, 'accounts/wish_list.html')

def cart(request):
    return render(request, 'accounts/cart.html')