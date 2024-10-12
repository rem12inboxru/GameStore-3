from django.shortcuts import render
from django.http import HttpResponse, request, HttpRequest

from .forms import UserRegister
from .models import Buyer, Game

def render_start(request):
    return render(request, 'start.html')


'''def render_games(request):
    return render(request, 'games.html')'''


def index_basket(request):
    title = 'КОРЗИНА'
    message1 = 'В вашей корзине пока ничего нет'
    message2 = 'Сумма ваших покупок :'
    message3 = 'Благодарим за покупку'
    summ = ' 0.00 '
    glav = 'На главную страницу'
    context = {'title': title, 'message1': message1, 'message2': message2,
               'message3': message3, 'summ': summ, 'glav': glav}
    return render(request, 'basket.html', context)


def index_games(request):
    title = 'МАГАЗИН'
    games = []
    gam = Game.objects.all()
    for i in gam:
        games.append(f' {i.title} | {i.description}. Стоимость {i.cost}')
    buy = 'КУПИТЬ'
    glav = 'На главную страницу'
    context = {'title': title, 'games': [i for i in games], 'buy': buy, 'glav': glav}
    return render(request, 'games.html', context)


# Create your views here.
def sign_up_by_django(request):
    users = []
    buyer = Buyer.objects.all()
    for i in buyer:
        users.append(i.name)
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            repeat_password = request.POST.get("repeat_password")
            age = request.POST.get('age')

            if password == repeat_password and int(age) >= 18 and username not in users:
                username = Buyer.objects.create(name=username, balance=0.00, age=age)
                return HttpResponse(f'Приветствуем, {username} !!!')

            elif password != repeat_password:
                info['error'] = f"Пароли не совпадают"

            elif int(age) < 18:
                info['error'] = f'Вы должны быть старше 18 лет'

            elif username in users:
                info['error'] = f'Пользователь уже существует'

    else:
        form = UserRegister()
    return render(request, 'registration_page.html', {'form': form, 'info': info})
