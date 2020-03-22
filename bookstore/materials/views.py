from django.shortcuts import render

def articles(request):
    return render(request, 'materials/material_article.html')

def podcasts(request):
    return render(request, 'materials/material_podcast.html')
