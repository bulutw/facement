from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Card, CardHolder, PayHolder, CustomUser, Item
from .forms import CreateCard, CardCheck, PaymentForm, LoginForm, RegisterForm

from rest_framework import viewsets
from .serializers import CardHolderSerializer, PayHolderSerializer

from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib import messages

import requests as rqs, random, time

from .facement import add_a_card, check_card

delay = time.sleep

def LoginView(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)

        login(request, user)
        return redirect('/marketplace')
    return render(request, 'registiration/login.html', {'form': form})

def RegisterView(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit = False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        CustomUser.objects.create(user = user)

        login(request, user)
        return redirect('/marketplace')

    return render(request, 'registiration/register.html', {'form': form})

def AddToCart(request, pk):
    item = Item.objects.filter(id = pk)[0]
    target = CustomUser.objects.filter(user = request.user)[0]

    if (str(pk) in target.cart) == True:
        messages.info(request, 'Eklemeye çalıştığınız ürün zaten sepetinizde bulunuyor!')
    else:
        if target.cart == "":
            target.cart = pk
        else:
            target.cart = target.cart + "," + pk
        messages.info(request, 'Başarıyla sepetinize eklendi!')
    target.save()
    
    return redirect('/marketplace')
    
def MarketPlace(request):
    items = Item.objects.all()
    return render(request, 'marketplace.html', {'items': items})

def AddCard(request):
    form = CreateCard(request.POST or None)
    if request.method == 'POST':
        form = CreateCard(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = CreateCard()
    return render(request, 'land.html', {'form': form})

class CardHolderViewSet(viewsets.ModelViewSet):
    serializer_class = CardHolderSerializer
    queryset = CardHolder.objects.all()

class PayHolderViewSet(viewsets.ModelViewSet):
    serializer_class = PayHolderSerializer
    queryset = PayHolder.objects.all()

def Facement(request):
    form = CardCheck(request.POST or None)
    if request.method == 'POST':
        form = CardCheck(request.POST)
        if form.is_valid():
            cc_number = form.cleaned_data.get('card_num')
            client = form.cleaned_data.get('client_id')
            
            add_card = add_a_card(cc_number, client)
            if add_card:
                return HttpResponse(f''' Facement System Responses Success: {add_a_card.response_for_text}''')
            else:
                if add_a_card.err:
                    return HttpResponse(f''' Facement System Responses Error: {add_a_card.err_text}''')
                else:
                    return HttpResponse(f''' Facement System Responses Failure: {add_a_card.response_for_text}''')

    else:
        form = CardCheck()
    return render(request, 'facement.html', {'form': form})
    
def Pay(request):
    if request.user.is_authenticated:
        form = PaymentForm(request.POST or None)
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                cc_num = form.cleaned_data.get('cc_number')
                check = check_card(cc_num)
                if not check_card.failure:
                    if check_card.exists:
                        messages.success(request, 'Görünüşe göre kartınız Facement sistemine dahil. Onay bekleniyor...')
                    else:
                        messages.success(request, 'Ödemeniz başarıyla tamamlandı.')
                else:
                    messages.success(request, 'Bir hata ile karşılaşıldı.')

        else:
            form = PaymentForm()

        items = Item.objects.all()
        price = 90
        return render(request, 'pay.html', {'form': form, 'items': items, 'price': price})
    else:
        return redirect('/login')