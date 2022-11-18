from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    return HttpResponse(content='<h1>Lolkek</h1>')


def docs(request):
    list = ['еблан?']
    data = {"header":'Документы',
            "list":list}
    return render(request, 'base.html', context=data)


def temp(request):
    list = []
    data = {"header": 'Шаблоны',
            "list":list}
    return render(request, 'base.html', context=data)


def reports(request):
    list = []
    data = {"header": "Отчеты",
            "list":list}
    return render(request, 'base.html', context=data)


def data(request):
    list = []
    data = {"header": 'Источники данных',
            "list":list}
    return render(request, 'base.html', context=data)


def groups(request):
    list = []
    data = {"header": 'Группы',
            "list":list}
    return render(request, 'base.html', context=data)


def users(request):
    list = []
    data = {"header": 'Пользователи',
            "list":list}
    return render(request, 'base.html', context=data)


def api_keys(request):
    list = []
    data = {"header": 'API-ключи',
            "list":list}
    return render(request, 'base.html', context=data)

def download_file(request):
    ...

def export_file(request):
    ...

def delete_file(request):
    ...

def create_file(request):
    ...