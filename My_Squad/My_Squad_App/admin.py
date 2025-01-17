from datetime import date
from django.contrib import admin

from .models import Osoba, Stanowisko, Zawodnik, Druzyna, Trener, Mecz, StatystykiZawodnika, Trening

admin.site.register(Osoba)
admin.site.register(Stanowisko)
#usunąłem stąd zawodnika
admin.site.register(Druzyna)
admin.site.register(Trener)
admin.site.register(Mecz)
admin.site.register(StatystykiZawodnika)
admin.site.register(Trening)

@admin.register(Zawodnik)
class ZawodnikAdmin(admin.ModelAdmin):
    list_display = ('nazwisko', 'pozycja')  
    list_filter = ('pozycja',)  
    search_fields = ('nazwisko',)  
    ordering = ['pozycja', 'nazwisko']  
    





class OsobaAdmin(admin.ModelAdmin):
    @admin.display(description=" Stanowisko (ID)")
    def stanowisko_with_id(self, obj):
        if obj.stanowisko :
            return f'{obj.stanowisko} ({obj.stanowisko})'
        return 'Brak stanowiska'
    list_display = ["imie", "nazwisko", "plec", "stanowisko_with_id", "data_dodania"]

