from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# DLa my_Squad
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Zawodnik, Druzyna, Trener, Trening, StatystykiZawodnika, Mecz
from .serializers import RejestracjaSerializer, ZawodnikSerializer, DruzynaSerializer, TrenerSerializer, TreningSerializer, StatystykiZawodnikaSerializer, MeczSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes

from .permissions import IsSuperuser, IsAuthenticated


#paginacja paparapapap - działa już :))))
class ZawodnikPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'  #- Można sobie zmienić wyświetlanie ilości rekordów (defaultowo będzie 6, maksymalnie 20)
    max_page_size = 20
@api_view(['GET', 'POST'])  
@permission_classes([IsAuthenticated])
def zawodnik_list(request):
    if request.method == 'GET':
        zawodnicy = Zawodnik.objects.all()
        paginator = ZawodnikPagination()
        result_page = paginator.paginate_queryset(zawodnicy, request)  
        serializer = ZawodnikSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ZawodnikSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('is_staff', raise_exception=True)
# def admin_view(request):
def zawodnik_detail(request, pk):
    try:
        zawodnik = Zawodnik.objects.get(pk=pk)
    except Zawodnik.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ZawodnikSerializer(zawodnik)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ZawodnikSerializer(zawodnik, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        zawodnik.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def druzyna_list(request):
    if request.method == 'GET':
        druzyny = Druzyna.objects.all()
        serializer = DruzynaSerializer(druzyny, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DruzynaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def druzyna_detail(request, pk):
    try:
        druzyna = Druzyna.objects.get(pk=pk)
    except Druzyna.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DruzynaSerializer(druzyna)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DruzynaSerializer(druzyna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        druzyna.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def trener_list(request):
    if request.method == 'GET':
        trenerzy = Trener.objects.all()
        serializer = TrenerSerializer(trenerzy, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TrenerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def trener_detail(request, pk):
    try:
        trener = Trener.objects.get(pk=pk)
    except Trener.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrenerSerializer(trener)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TrenerSerializer(trener, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trener.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsSuperuser])
def trening_list(request):
    print(f"Użytkownik: {request.user}")  # Wyświetli zalogowanego użytkownika
    print(f"Czy superuser: {request.user.is_superuser}")
    print(f"Nagłówki: {request.headers}")
    if request.method == 'GET':
        treningi = Trening.objects.all()
        serializer = TreningSerializer(treningi, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TreningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsSuperuser])
def trening_detail(request, pk):
    try:
        trening = Trening.objects.get(pk=pk)
    except Trening.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TreningSerializer(trening)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TreningSerializer(trening, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trening.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def statystyki_zawodnika_list(request):
    if request.method == 'GET':
        statystyki = StatystykiZawodnika.objects.all()
        serializer = StatystykiZawodnikaSerializer(statystyki, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = StatystykiZawodnikaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def statystyki_zawodnika_detail(request, pk):
    try:
        statystyki = StatystykiZawodnika.objects.get(pk=pk)
    except StatystykiZawodnika.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StatystykiZawodnikaSerializer(statystyki)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StatystykiZawodnikaSerializer(statystyki, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        statystyki.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def mecz_list(request):
    if request.method == 'GET':
        mecze = Mecz.objects.all()
        serializer = MeczSerializer(mecze, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MeczSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def mecz_detail(request, pk):
    try:
        mecz = Mecz.objects.get(pk=pk)
    except Mecz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeczSerializer(mecz)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeczSerializer(mecz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mecz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Nowy endpointy, wychodzący poza schemat CRUD- Wszystkie działają (pozycja musi być wpisywana skrótem tj. BR, OB, PP, NA)
@api_view(['GET'])
def Zawodnik_na_litere(request, letter):
    zawodnicy = Zawodnik.objects.filter(imie__istartswith= letter)
    if not zawodnicy.exists():
        return Response( "Nie istnieją zawodnicy, których imię zaczyna się na podaną literę. Spróbuj innej :D")  
    serializer = ZawodnikSerializer(zawodnicy, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def zawodnik_po_narodowosci(request, narodowosc):
    zawodnicy = Zawodnik.objects.filter(narodowosc__iexact= narodowosc)
    if not zawodnicy.exists():
         return Response("Nie ma zawodników o podanej narodowości, spróbuj innej :D")
    serializer = ZawodnikSerializer(zawodnicy, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def zawodnik_po_pozycji(request, pozycja):
    zawodnicy = Zawodnik.objects.filter(pozycja__iexact=pozycja)
    serializer = ZawodnikSerializer(zawodnicy, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def Rejestracja_uzytkownika(request):
    serializer = RejestracjaSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response(
            {
                "message": "Użytkownik został pomyślnie zarejestrowany!",
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#endpoint z bramkami 
@api_view(['GET'])
def strzelcy_bramek(request, mecz_id):
    try:
        mecz = Mecz.objects.get(pk=mecz_id)
    except Mecz.DoesNotExist:
        return Response({"error": "Mecz nie istnieje"}, status=404)

    statystyki = StatystykiZawodnika.objects.filter(mecz=mecz, bramki__gt=0)
    response_data = [
        {
            "zawodnik": f"{stat.zawodnik.imie} {stat.zawodnik.nazwisko}",
            "druzyna": stat.zawodnik.druzyna.nazwa if stat.zawodnik.druzyna else "Brak drużyny",
            "liczba_bramek": stat.bramki
        }
        for stat in statystyki
    ]
    return Response(response_data)


from rest_framework.authtoken.views import ObtainAuthToken
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sprawdz_uprawnienia(request):
    return Response({
        "username": request.user.username,
        "is_superuser": request.user.is_superuser,
        "is_staff": request.user.is_staff,
        "permissions": list(request.user.get_all_permissions()),  # Wszystkie uprawnienia użytkownika
    })


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def zawodnik_detail_or_delete(request, pk):

    zawodnik = get_object_or_404(Zawodnik, pk=pk)

    if request.method == 'GET':
        serializer = ZawodnikSerializer(zawodnik)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        zawodnik.delete()
        return Response({"detail": "Zawodnik został pomyślnie usunięty."}, status=status.HTTP_204_NO_CONTENT)