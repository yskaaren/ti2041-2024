from django.shortcuts import render

# Create your views here.

def product(request):
    print("Productos")

    return render(request, 'index.html')