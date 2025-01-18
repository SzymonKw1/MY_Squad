from django.db import models
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

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
    def clean(self):
        if Zawodnik.objects.filter(druzyna=self.druzyna, numer_koszulki=self.numer_koszulki).exclude(id=self.id).exists():
            raise ValidationError(f"Numer koszulki {self.numer_koszulki} już istnieje w tej drużynie.")
    
    
    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.pozycja})"
    
    class Meta:
        verbose_name = "Zawodnik"
        verbose_name_plural = "Zawodnicy"
        ordering = ['pozycja', 'nazwisko' ]
    

class Druzyna(models.Model):
    nazwa = models.CharField(max_length=100)
    miasto = models.CharField(max_length=100)
    stadion = models.CharField(max_length=100)
    trener = models.OneToOneField('Trener', on_delete=models.SET_NULL, null=True, blank=True)
    rok_zalozenia = models.IntegerField(
        validators=[
            MinValueValidator(1800),  
            MaxValueValidator(date.today().year)  
        ]
    )

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
    def clean(self):
        if self.druzyna_gospodarz == self.druzyna_gosc:
            raise ValidationError("Drużyna gospodarzy i drużyna gości nie mogą być takie same.")
    
    class Meta:
        verbose_name = "Mecz"
        verbose_name_plural = "Mecze"

class StatystykiZawodnika(models.Model):
    mecz = models.ForeignKey('Mecz', on_delete=models.CASCADE, related_name='statystyki_zawodnikow')
    zawodnik = models.ForeignKey('Zawodnik', on_delete=models.CASCADE, related_name='statystyki')
    bramki = models.PositiveIntegerField(default=0)
    asysty = models.PositiveIntegerField(default=0)
    zolte_kartki = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(2)])
    czerwone_kartki = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)])
    minuty_na_boisku = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(120)])
    def clean(self):
        wynik_meczu = self.mecz.wynik_gospodarz + self.mecz.wynik_gosc
        if self.bramki > wynik_meczu:
            raise ValidationError(f"Zawodnik nie może strzelić więcej bramek ({self.bramki}) niż wynosi suma bramek meczu ({wynik_meczu}).")
        if self.zawodnik.druzyna == self.mecz.druzyna_gospodarz:
            druzyna_bramki = self.mecz.wynik_gospodarz
        elif self.zawodnik.druzyna == self.mecz.druzyna_gosc:
            druzyna_bramki = self.mecz.wynik_gosc
        else:
            raise ValidationError("Zawodnik nie należy do żadnej z drużyn w tym meczu.")

        if self.bramki > druzyna_bramki:
            raise ValidationError(f"Zawodnik nie może strzelić więcej bramek ({self.bramki}) niż jego drużyna ({druzyna_bramki}).")

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
