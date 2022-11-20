import random
import string

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from webapp.data import DataSources
from webapp.forms import Export
from webapp.groups import get_user_groups
from webapp.users import get_my_profile
from webapp.api_keys import get_api_keys, create_api_key, delete_api_key
from webapp.shablon import Templates
from webapp.export import Exports, USER_NAME, TOKEN, PROS
from webapp.reports import Reports, USER_NAME, TOKEN, PROS


def home(request):
    return HttpResponse(content='<h1>Lolkek</h1>')


def temp(request):
    form = Export()
    tem = Templates(USER_NAME, TOKEN, PROS, 'https://fastreport.cloud')
    a = tem._get_list_files_folder()
    data = {"header": 'Шаблоны',
            "list": a,
            'form': form}
    return render(request, 'shablon.html', context=data)


def reports(request):
    form = Export()
    rep = Reports(USER_NAME, TOKEN, PROS)
    a = rep.get_all_file_and_folder()
    data = {"header": "Отчеты",
            "list": a,
            "form":form}
    return render(request, 'reports.html', context=data)


def data(request):
    form = Export()
    dt = DataSources('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
    a = dt.get_all_data_sources()['dataSources']
    data = {"header": 'Источники данных',
            "list": a,
            "form":form}
    return render(request, 'data.html', context=data)


def groups(request):
    gr = get_user_groups()
    data = {"header": 'Группы',
            "list": gr}
    return render(request, 'groups.html', context=data)


def users(request):
    sp = get_my_profile()
    a = [sp.to_dict()]
    data = {"header": 'Пользователи',
            "list": a}
    return render(request, 'users.html', context=data)


def exports(request):
    ex = Exports('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
    a = ex._get_list_files_folder()
    data = {"header": 'Экспорты',
            "list": a}
    return render(request, 'exports.html', context=data)


def _api_keys(request):
    keys = [i.to_dict() for i in get_api_keys()]
    data = {"header": 'API-ключи',
            "list": keys}
    return render(request, 'api_keys.html', context=data)


def _download_file(request, down, id, name):
    if down == 'shablon_down':
        return redirect('temp')
    if down == 'doc_down':
        return redirect('docs')
    if down == 'reports_down':
        rep = Reports(USER_NAME, TOKEN, PROS)
        rep.download_file(id)
        return redirect('reports')
    if down == 'api_down':
        return redirect('api_keys')
    if down == 'export_down':
        return redirect('exports')
    if down == 'data_down':
        return redirect('data')


def _export_file(request, down, id, name):
    print('dsfdgffgdfggfh')
    if down == 'shablon_exp':
        if request.method == 'POST':
            form = Export(request.POST)
            if form.is_valid():
                name = name.split('.frx')[0]
                print(name)
                tem = Templates(USER_NAME, TOKEN, PROS, 'https://fastreport.cloud')
                tem.prepare_file(file_name=name, file_prepare_name=name)
                tem.export_file(file_name=name, format='pdf')
            else:
                print('Че ты ввел?')
        return redirect('temp')
    if down == 'doc_exp':
        return redirect('docs')
    if down == 'reports_exp':
        return redirect('reports')
    if down == 'api_exp':
        return redirect('api_keys')
    if down == 'export_exp':
        return redirect('exports')


def _delete_file(request, down, id, name):
    if down == 'shablon_del':
        name = name.split('.')[0]
        tem = Templates('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        tem.delete_file(name)
        return redirect('temp')
    if down == 'doc_del':
        return redirect('docs')
    if down == 'reports_del':
        rep = Reports(USER_NAME, TOKEN, PROS)
        rep.delite_file(id)
        return redirect('reports')
    if down == 'api_del':
        delete_api_key(name)
        return redirect('api-keys')
    if down == 'export_del':
        ex = Exports('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        ex.delete_file(name)
        return redirect('exports')
    if down == 'data_del':
        dt = DataSources('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        dt.delete_ds(name)
        return redirect('data')


def _delete_package(request, down, id, name):
    if down == 'reports_del':
        rep = Reports(USER_NAME, TOKEN, PROS)
        rep.delite_package(id)
        return redirect('reports')
    if down == 'shablon_del':
        tem = Templates('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        tem.delete_folder(name)
        return redirect('temp')
    if down == 'export_del':
        ex = Exports('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        ex.delete_folder(name)
        return redirect('exports')
    if down == 'data_del':
        return redirect('data')


def _create_file(request, down):
    if down == 'shablon_cr':
        tem = Templates('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        tem.create_file()
        return redirect('temp')
    if down == 'doc_cr':
        return redirect('docs')
    if down == 'reports_cr':
        rep = Reports('apikey', TOKEN, PROS)
        rep.create_file('new')
        return redirect('reports')
    if down == 'api_cr':
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(100))
        create_api_key(description=rand_string)
        print(create_api_key(description=rand_string))
        return redirect('api-keys')
    if down == 'export_cr':
        ex = Exports('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        ex.create_folder()
        return redirect('exports')
    if down == 'data_cr':
        dt = DataSources('apikey', 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy', '6379fb4b5f620ebfce9a63e4', 'https://fastreport.cloud')
        dt.create_data_source()
        return redirect('data')
