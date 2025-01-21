from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CustomAuthToken

urlpatterns = [
    path('zawodnicy/', views.zawodnik_list),
    path('zawodnicy/<int:pk>/', views.zawodnik_detail),
    path('druzyny/', views.druzyna_list),
    path('druzyny/<int:pk>/', views.druzyna_detail),
    path('trenerzy/', views.trener_list),
    path('trenerzy/<int:pk>/', views.trener_detail),
    path('treningi/', views.trening_list),
    path('treningi/<int:pk>/', views.trening_detail),
    path('statystyki_zawodnikow/', views.statystyki_zawodnika_list),
    path('statystyki_zawodnikow/<int:pk>/', views.statystyki_zawodnika_detail),
    path('mecze/', views.mecz_list),
    path('mecze/<int:pk>/', views.mecz_detail),
    path('zawodnicy/starts-with/<str:letter>/', views.Zawodnik_na_litere),
    path('zawodnicy/narodowosc/<str:narodowosc>/', views.zawodnik_po_narodowosci),
    path('zawodnicy/pozycja/<str:pozycja>/', views.zawodnik_po_pozycji),
    path('rejestracja/', views.Rejestracja_uzytkownika),
    path('mecze/<int:mecz_id>/strzelcy-bramek/', views.strzelcy_bramek, name='strzelcy_bramek'),
    path('api/login/', CustomAuthToken.as_view()),
    path('sprawdz-uprawnienia/', views.sprawdz_uprawnienia),
    path('zawodnik/<int:pk>/delete/', views.zawodnik_detail_or_delete)

]