from django.shortcuts import render, redirect
from .forms import OrderForm


def order_medicine(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, '', {'form': form})


def order_success(request):
    return render(request, '')

