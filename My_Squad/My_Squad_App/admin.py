from datetime import date
from django.contrib import admin

from .models import Osoba, Stanowisko, Zawodnik, Druzyna, Trener, Mecz, StatystykiZawodnika, Trening

admin.site.register(Osoba)
admin.site.register(Stanowisko)
#usunąłem stąd zawodnika
#usunałem drużyna
#usunalem trenera
#usunalem mecz
#usnąłem stąd statystykizawodnika
#usunalem trening

@admin.register(Zawodnik)
class ZawodnikAdmin(admin.ModelAdmin):
    list_display = ('nazwisko', 'pozycja', 'numer_koszulki', 'druzyna' )  
    list_filter = ('pozycja',)  
    search_fields = ('nazwisko',)  
    ordering = ['pozycja', 'nazwisko']  
    
@admin.register(StatystykiZawodnika)
class StatystykiZawodnikaAdmin(admin.ModelAdmin):
    # Wyświetlanie wszystkich pól w liście
    list_display = ('zawodnik', 'mecz', 'bramki', 'asysty', 'zolte_kartki', 'czerwone_kartki', 'minuty_na_boisku')

@admin.register(Druzyna)
class DruzynaAdmin(admin.ModelAdmin):
    list_display =('nazwa', 'miasto', 'stadion', 'trener')
    list_filter = ('miasto',)
    search_fields = ('nazwa',)

@admin.register(Trener)
class TrenerAdmin(admin.ModelAdmin):
    list_display =('nazwisko', 'data_urodzenia', 'lata_doswiadczenia', 'narodowosc' )
    ordering = ['lata_doswiadczenia']


@admin.register(Mecz)
class MeczAdmin(admin.ModelAdmin):
    list_display = ('druzyna_gospodarz', 'druzyna_gosc', 'data', 'wynik_gospodarz', 'wynik_gosc' )

@admin.register(Trening)
class TreningAdmin(admin.ModelAdmin):
    list_display = ('druzyna', 'data', 'czas_trwania_minuty','obszar_skupienia' )


class OsobaAdmin(admin.ModelAdmin):
    @admin.display(description=" Stanowisko (ID)")
    def stanowisko_with_id(self, obj):
        if obj.stanowisko :
            return f'{obj.stanowisko} ({obj.stanowisko})'
        return 'Brak stanowiska'
    list_display = ["imie", "nazwisko", "plec", "stanowisko_with_id", "data_dodania"]

