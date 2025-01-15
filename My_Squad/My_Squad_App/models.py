from django.db import models
from datetime import date

MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')
PLCIE = models.IntegerChoices('PLEC', 'Kobieta Mężczyzna Inna')

class Team(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Klub"
        verbose_name_plural = "Kluby"

class Osoba(models.Model):
    PLEC_CHOICES = (
        ("K", "Kobieta"),
        ("M", "Mężczyzna"),
        ("I", "Inna"),
    )
    
    imie = models.CharField(max_length=40, blank = False, null = False)
    nazwisko = models.CharField(max_length=60, blank = False, null = False)
    plec = models.IntegerField(choices=PLCIE.choices, default=PLCIE.choices[2][0])
    stanowisko = models.ForeignKey('Stanowisko', on_delete = models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=3, blank = False, default='', null = False)
    data_dodania = models.DateField(default = date.today, blank=False, null=False)
    
    def __str__(self):
        return f'{self.imie} {self.nazwisko}' 
    
    class Meta:
        ordering = ["nazwisko"]
        verbose_name = "Osoba"
        verbose_name_plural = "Osoby"

class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=80, blank = False, null = False)
    opis = models.TextField(blank = False, null = False)
    
    def __str__(self):
        return self.nazwa
    
    class Meta:
        verbose_name = "Stanowisko"
        verbose_name_plural = "Stanowiska"


# Modele związane z funkcjonalnością MY_SQUAD
class Zawodnik(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    pozycje_wybor = [
        ('BR', 'Bramkarz'),
        ('OB', 'Obrońca'),
        ('PP', 'Pomocnik'),
        ('NA', 'Napastnik'),
    ]
    pozycja = models.CharField(max_length=2, choices=pozycje_wybor)
    druzyna = models.ForeignKey('Druzyna', on_delete=models.SET_NULL, null=True, blank=True, related_name='zawodnicy')
    numer_koszulki = models.PositiveIntegerField()
    narodowosc = models.CharField(max_length=50)
    
    
    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.pozycja})"
    
    class Meta:
        verbose_name = "Zawodnik"
        verbose_name_plural = "Zawodnicy"
    

class Druzyna(models.Model):
    nazwa = models.CharField(max_length=100)
    miasto = models.CharField(max_length=100)
    stadion = models.CharField(max_length=100)
    trener = models.OneToOneField('Trener', on_delete=models.SET_NULL, null=True, blank=True)
    data_zalozenia = models.DateField()

    def __str__(self):
        return self.nazwa
    
    class Meta:
        verbose_name = "Drużyna"
        verbose_name_plural = "Drużyny"


class Trener(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    narodowosc = models.CharField(max_length=50)
    lata_doswiadczenia = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"
    
    class Meta:
        verbose_name = "Trener"
        verbose_name_plural = "Trenerzy"

class Mecz(models.Model):
    druzyna_gospodarz = models.ForeignKey('Druzyna', on_delete=models.CASCADE, related_name='mecze_gospodarz')
    druzyna_gosc = models.ForeignKey('Druzyna', on_delete=models.CASCADE, related_name='mecze_gosc')
    data = models.DateTimeField()
    stadion = models.CharField(max_length=100)
    wynik_gospodarz = models.PositiveIntegerField(default=0)
    wynik_gosc = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.druzyna_gospodarz} vs {self.druzyna_gosc} ({self.data})"
    
    class Meta:
        verbose_name = "Mecz"
        verbose_name_plural = "Mecze"

class StatystykiZawodnika(models.Model):
    mecz = models.ForeignKey('Mecz', on_delete=models.CASCADE, related_name='statystyki_zawodnikow')
    zawodnik = models.ForeignKey('Zawodnik', on_delete=models.CASCADE, related_name='statystyki')
    bramki = models.PositiveIntegerField(default=0)
    asysty = models.PositiveIntegerField(default=0)
    zolte_kartki = models.PositiveIntegerField(default=0)
    czerwone_kartki = models.PositiveIntegerField(default=0)
    minuty_na_boisku = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Statystyki {self.zawodnik} w meczu {self.mecz}"
    
    class Meta:
        verbose_name_plural = "Statystyki"

class Trening(models.Model):
    druzyna = models.ForeignKey('Druzyna', on_delete=models.CASCADE, related_name='treningi')
    data = models.DateField()
    czas_trwania_minuty = models.PositiveIntegerField()
    obszar_skupienia = models.CharField(max_length=100)

    def __str__(self):
        return f"Trening drużyny {self.druzyna} w dniu {self.data}"
    
    class Meta:
        verbose_name = "Trening"
        verbose_name_plural = "Treningi"
