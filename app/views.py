import sentry_sdk
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from app.forms import CarrosForm
from app.models import Carros
from app.CloudWatch import put_log_event
import os

sentry_sdk.init(
    dsn=os.environ['DSN_SENTRY'],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    environment='views',
    traces_sample_rate=1.0
)

# Create your views here.
def home(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Carros.objects.filter(modelo__icontains=search)
    else:
        data['db'] = Carros.objects.all()
    all = Carros.objects.all()
    paginator = Paginator(all, 2)
    pages = request.GET.get('page')
    data['db'] = paginator.get_page(pages)
    return render(request, 'index.html', data)


def form(request):
    data = {}
    data['form'] = CarrosForm()
    return render(request, 'form.html', data)


def create(request):
    form = CarrosForm(request.POST or None)
    if form.is_valid():
        carros_instance = form.save(commit=False)
        carros_instance.save()

        # Chame a função para enviar os dados para o CloudWatch
        data = {
            # 'timestamp': carros_instance.timestamp,
            'acao': 'CREATE',
            'modelo': carros_instance.modelo,
            'ano': carros_instance.ano,
            'marca': carros_instance.marca,
        }
        put_log_event(data)

    return redirect('home')

def view(request, pk):
    data = {}
    data['db'] = Carros.objects.get(pk=pk)
    return render(request, 'view.html', data)


def edit(request, pk):
    data = {}
    data['db'] = Carros.objects.get(pk=pk)
    data['form'] = CarrosForm(instance=data['db'])
    return render(request, 'form.html', data)


def update(request, pk):
    data = {}
    data['db'] = Carros.objects.get(pk=pk)
    form = CarrosForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        # form.save()
        carros_instance = form.save(commit=False)
        carros_instance.save()

        # Chame a função para enviar os dados para o CloudWatch
        data = {
            # 'timestamp': carros_instance.timestamp,
            'acao': 'UPDATE',
            'modelo': carros_instance.modelo,
            'ano': carros_instance.ano,
            'marca': carros_instance.marca,
        }
        put_log_event(data)


    return redirect('home')


def delete(request, pk):
    db = Carros.objects.get(pk=pk)
    db.delete()
    return redirect('home')

