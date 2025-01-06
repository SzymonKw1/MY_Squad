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