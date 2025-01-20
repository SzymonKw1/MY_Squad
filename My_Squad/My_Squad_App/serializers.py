from datetime import date
from rest_framework import serializers
from .models import  Zawodnik, Druzyna, Trener, Mecz, StatystykiZawodnika, Trening
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

#Rejestracja użytkownika
class RejestracjaSerializer(serializers.ModelSerializer):
    haslo = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'haslo', 'email']
        extra_kwargs = {
            'haslo': {
                'write_only': True,
                'style': {'input_type': 'password'}
                }
            }
    def validate_haslo(self, value):
        # Sprawdzanie, czy hasło zawiera co najmniej jedną dużą literę
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Hasło musi zawierac co najmniej jedna wielką literę.")
        # Sprawdzanie, czy hasło zawiera co najmniej jeden znak specjalny
        specjalne_znaki = ['!', '@', '#', '$', '%', '^', '&', '*', ',', '.', '?', ':', '"', '{', '}', '<', '>', '-', '_', '=', '+', ';', '~', '`']
        if not any(char in specjalne_znaki for char in value):
            raise serializers.ValidationError("Hasło musi zawierać co najmniej jeden znak specjalny.")
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Użytkownik z takim emialem już istnieje.")
        return value
    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['haslo'])
        user.save()
        token, created = Token.objects.get_or_create(user = user)
        return user
    #Działa w Api view, trzeba wpisywac JSON-em




# serializery z Mysquad
class ZawodnikSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    imie = serializers.CharField(max_length=50, required=True)
    nazwisko = serializers.CharField(max_length=80, required=True)
    data_urodzenia = serializers.DateField(required=True)
    pozycja = serializers.ChoiceField(choices='pozycje_wybor' , required=True)
    numer_koszulki = serializers.IntegerField(required=True)
    narodowosc = serializers.CharField(max_length=50, required=True)
    druzyna = serializers.PrimaryKeyRelatedField(queryset=Druzyna.objects.all(), required=False)


    def create(self, validated_data):
        return Zawodnik.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.imie = validated_data.get('imie', instance.imie)
        instance.nazwisko = validated_data.get('nazwisko', instance.nazwisko)
        instance.data_urodzenia = validated_data.get('data_urodzenia', instance.data_urodzenia)
        instance.pozycja = validated_data.get('pozycja', instance.pozycja)
        instance.numer_koszulki = validated_data.get('numer_koszulki', instance.numer_koszulki)
        instance.narodowosc = validated_data.get('narodowosc', instance.narodowosc)
        instance.druzyna = validated_data.get('druzyna', instance.druzyna)
        instance.save()
        return instance
   
class DruzynaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Druzyna
        fields = [
            'id', 'nazwa', 'miasto', 'stadion', 
            'trener', 'rok_zalozenia'
        ]
        read_only_fields = ['id']

class TrenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trener
        fields = [
            'id', 'imie', 'nazwisko', 'data_urodzenia',
            'narodowosc', 'lata_doswiadczenia'
        ]
        read_only_fields = ['id']

class MeczSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecz
        fields = [
            'id', 'druzyna_gospodarz', 'druzyna_gosc', 
            'data', 'stadion', 'wynik_gospodarz', 'wynik_gosc'
        ]
        read_only_fields = ['id']

class StatystykiZawodnikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatystykiZawodnika
        fields = [
            'id', 'mecz', 'zawodnik', 'bramki', 
            'asysty', 'zolte_kartki', 'czerwone_kartki', 'minuty_na_boisku'
        ]
        read_only_fields = ['id']

class TreningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trening
        fields = [
            'id', 'druzyna', 'data', 'czas_trwania_minuty', 'obszar_skupienia'
        ]
        read_only_fields = ['id']




    
