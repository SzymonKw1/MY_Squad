from django.shortcuts import render
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
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


#paginacja paparapapap - działa już :))))
class ZawodnikPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'  #- Można sobie zmienić wyświetlanie ilości rekordów (defaultowo będzie 6, maksymalnie 20)
    max_page_size = 20
@api_view(['GET', 'POST'])  
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
def trening_list(request):
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


