from django.shortcuts import render


def catalog(request):
    return render(request, 'catalogs/catalog.html')

def paper(request):
    return render(request, 'catalogs/catalog_paper.html')
