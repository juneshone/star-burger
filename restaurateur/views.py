import requests
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from geopy import distance

from foodcartapp.models import Product, Restaurant, OrderItem, OrderDetail, RestaurantMenuItem
from places.models import Place
from star_burger.settings import YANDEX_MAP_API


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    menu = RestaurantMenuItem.objects.filter(availability=True) \
        .prefetch_related('restaurant', 'product')
    orders = OrderDetail.objects.exclude(status='DELIVERED').prefetch_related(
        'order_items').annotate(
        order_cost=OrderItem.objects.calculate_order_cost())
    for order in orders:
        restaurants = []
        products_in_order = [order_item.product.id for order_item in order.order_items.select_related('product')]
        for product_in_order in products_in_order:
            product_in_restaurant = menu.filter(product=product_in_order)
            availability_restaurants = set(product_in_restaurant.values_list('restaurant', flat=True))
            if not restaurants:
                restaurants = availability_restaurants
            else:
                restaurants.intersection_update(availability_restaurants)

        distance_to_restaurants = []
        for restaurant in restaurants:
            restaurant_details = get_object_or_404(Restaurant, id=restaurant)
            restaurant_coords = fetch_coordinates(YANDEX_MAP_API, restaurant_details.address)
            places = set(Place.objects.values_list('address', flat=True))
            if order.address in places:
                place = get_object_or_404(Place, address=order.address)
                distance_to_restaurant = round(distance.distance(restaurant_coords, (place.lon, place.lat)).km, 3)
            else:
                lon, lat = fetch_coordinates(YANDEX_MAP_API, order.address)
                Place.objects.create(
                    address=order.address,
                    lat=lat,
                    lon=lon
                )
                distance_to_restaurant = round(distance.distance(restaurant_coords, (lon, lat)).km, 3)

            distance_to_restaurants.append(
                {'name': restaurant_details.name, 'distance_to_restaurant': distance_to_restaurant}
            )
        order.restaurants = sorted(distance_to_restaurants, key=lambda restaurant: restaurant['distance_to_restaurant'])

    return render(request, template_name='order_items.html', context={
        'order_items': orders
    })
