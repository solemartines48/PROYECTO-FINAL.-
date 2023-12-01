from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Passenger, Trip, Sale, Itinerary, Payment, Contact
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PassengerForm, TripForm, SaleForm, ItineraryForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Case, Value, When
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "travel/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("index")

        else:
            return render(request, "travel/login.html", {
                "message": "Nombre de usuario o contraseña inválida."
            })
    else:
        return render(request, "travel/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travel/register.html", {
                "message": "Las contraseñas no coinciden."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travel/register.html", {
                "message": "Nombre de usuario ya existe."
            })
        return HttpResponseRedirect(reverse("login"))

    else:
        return render(request, "travel/register.html")
    

@login_required
def list_passengers(request):
    # Obtener todos los pasajeros
    #Sale.objects.all().delete()

    all_passengers = Passenger.objects.all()
   # Filtrar por nombre si se proporciona un término de búsqueda
    search_query = request.GET.get('search_query')
    if search_query:
        all_passengers = all_passengers.filter(
                Q(name__icontains=search_query) | Q(lastname__icontains=search_query) | Q(dni__icontains=search_query))

    # Número de pasajeros por página
    items_per_page = 5
    paginator = Paginator(all_passengers, items_per_page)

    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        passengers = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        passengers = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        passengers = paginator.page(paginator.num_pages)

    return render(request, 'travel/list_passengers.html', {'passengers': passengers, 'search_query': search_query})



@login_required
def delete_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.delete()
    messages.success(request, 'El pasajero se ha eliminado exitosamente.')
    return redirect('list_passengers')

@login_required
def edit_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)

    if request.method == 'POST':
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información del pasajero actualizada exitosamente.')
            return redirect('list_passengers')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = PassengerForm(instance=passenger)
    return render(request, 'travel/edit_passenger.html', {'form': form, 'passenger': passenger})

@login_required
def create_passenger(request):
    form_passenger = PassengerForm()
    form_payer = PassengerForm()
    form_passenger_invited = PassengerForm()

    form = PassengerForm()
    context = {
        'form_passenger': form_passenger,
        'form_payer': form_payer,
        'form_passenger_invited': form_passenger_invited,
        'form': form,
    }

    # Agregar los valores de 'role' a los contextos de cada formulario
    context['form_passenger'].fields['role'].widget.attrs['readonly'] = True
    context['form_passenger'].fields['role'].initial = 'PASSENGER'

    context['form_payer'].fields['role'].widget.attrs['readonly'] = True
    context['form_payer'].fields['role'].initial = 'PAYER'

    context['form_passenger_invited'].fields['role'].widget.attrs['readonly'] = True
    context['form_passenger_invited'].fields['role'].initial = 'BOTH'

    return render(request, 'travel/create_passenger.html', context)


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje creado exitosamente.')
            return redirect('create_trip')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = TripForm()
    return render(request, 'travel/create_trip.html', {'form': form})

@login_required
def list_trips(request):
    # Obtener todos los pasajeros
    all_trips = Trip.objects.all()

   # Filtrar por nombre si se proporciona un término de búsqueda
    search_query = request.GET.get('search_query')
    if search_query:
        all_trips = all_trips.filter( Q(origin__icontains=search_query) | Q(destination__icontains=search_query))

    # Número de pasajeros por página
    items_per_page = 5
    paginator = Paginator(all_trips, items_per_page)

    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        trips = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        trips = paginator.page(paginator.num_pages)
    return render(request, 'travel/list_trips.html', {'trips': trips})

@login_required
def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    trip.delete()
    messages.success(request, 'El viaje se ha eliminado exitosamente.')
    return redirect('list_trips')



@login_required
def edit_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información del viaje actualizada exitosamente.')
            return redirect('list_trips')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = TripForm(instance=trip)
    return render(request, 'travel/edit_trip.html', {'form': form, 'trip': trip})

@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)        
   
        if form.is_valid():
            passenger_id = request.POST.get('passenger')
            trip_id = request.POST.get('trip')
            passenger = Passenger.objects.get(pk=passenger_id)
            trip = Trip.objects.get(pk=trip_id)

            form.fields['passenger'].initial = passenger
            form.fields['trip'].initial = trip
            form.save()
            messages.success(request, 'Venta creada exitosamente.')
            return redirect('create_sale')
        else:
            print("Errores de validación:")
            print(form.errors)
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = SaleForm()
    return render(request, 'travel/create_sale.html', {'form': form})



def get_trip_price(request, trip_id):
    try:
        trip = Trip.objects.get(pk=trip_id)
        return JsonResponse({'price': trip.price_per_day})  # Devuelve el precio del viaje en formato JSON
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'El viaje no existe'}, status=404)
    
def get_trips_by_date(request, selected_date):
    if selected_date:
        trips = Trip.objects.filter(departure_date=selected_date)
        trips_data = [{'id': trip.id, 'origin': trip.origin, 'destination': trip.destination, 'price': trip.price_per_day, 'arrival_date':trip.arrival_date, 'departure_date':trip.departure_date } for trip in trips]
        return JsonResponse({'trips': trips_data})
    return JsonResponse({'error': 'No se proporcionó una fecha válida'})

def passenger_sales(request, passenger_id):
    passenger = Passenger.objects.get(pk=passenger_id)
    sales = Sale.objects.filter(passenger=passenger)
    sales = sales.annotate(
        custom_order=Case(
            When(sale_status='PENDING', then=Value(1)),
            default=Value(2)
        )
    ).order_by('custom_order', '-sale_status')
    has_pending_sales = sales.filter(sale_status='PENDING').exists()
    total_debt = sales.aggregate(total=Sum('total_debt'))['total'] or 0
    total_installments = sum([sale.installments for sale in sales])
    for sale in sales:
        print(sale.id, sale.installments)  #

    # Número de pasajeros por página
    items_per_page = 2
    paginator = Paginator(sales, items_per_page)
    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        sales = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        sales = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        sales = paginator.page(paginator.num_pages)

    for sale in sales:
        if(sale.installments > 0):
            sale.installment_value = sale.total_debt / sale.installments
    sale_status_display = 'Pendiente' if has_pending_sales else 'No tienes pagos pendientes'
    context = {
        'passenger': passenger,
        'sales': sales,
        'total_debt': total_debt,
        'installments_left': total_installments,
        'total_installments': total_installments,
        'sale_status': 'pending', 
        'sale_status_display': sale_status_display 
    }
    

    return render(request, 'travel/passenger_sales.html', context)


@login_required
def list_trips(request):
    # Obtener todos los pasajeros
    all_trips = Trip.objects.all()

   # Filtrar por nombre si se proporciona un término de búsqueda
    search_query = request.GET.get('search_query')
    if search_query:
        all_trips = all_trips.filter( Q(origin__icontains=search_query) | Q(destination__icontains=search_query))

    # Número de pasajeros por página
    items_per_page = 5
    paginator = Paginator(all_trips, items_per_page)

    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        trips = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        trips = paginator.page(paginator.num_pages)
    return render(request, 'travel/list_trips.html', {'trips': trips})

@login_required
def create_itinerary(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Itinerario creado exitosamente.')
            return redirect('create_itinerary')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = ItineraryForm()
    return render(request, 'travel/create_itinerary.html', {'form': form})

@login_required
def list_itineraries(request):
    all_itineraries = Itinerary.objects.all()

    search_query = request.GET.get('search_query')
    if search_query:
            all_itineraries = all_itineraries.filter(trip_id=search_query)

    items_per_page = 5
    paginator = Paginator(all_itineraries, items_per_page)

    page = request.GET.get('page')
    try:
        itineraries = paginator.page(page)
    except PageNotAnInteger:
        itineraries = paginator.page(1)
    except EmptyPage:
        itineraries = paginator.page(paginator.num_pages)
    return render(request, 'travel/list_itineraries.html', {'itineraries': itineraries, 'trips': Trip.objects.all()})

@login_required
def list_trips(request):
    # Obtener todos los pasajeros
    all_trips = Trip.objects.all()

   # Filtrar por nombre si se proporciona un término de búsqueda
    search_query = request.GET.get('search_query')
    if search_query:
        all_trips = all_trips.filter( Q(origin__icontains=search_query) | Q(destination__icontains=search_query))

    # Número de pasajeros por página
    items_per_page = 5
    paginator = Paginator(all_trips, items_per_page)

    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        trips = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        trips = paginator.page(paginator.num_pages)
    return render(request, 'travel/list_trips.html', {'trips': trips})

@login_required
def delete_itinerary(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    itinerary.delete()
    messages.success(request, 'El itinerario se ha eliminado exitosamente.')
    return redirect('list_itineraries')

@login_required
def edit_itinerary(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)

    if request.method == 'POST':
        form = ItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información del itinerario actualizada exitosamente.')
            return redirect('list_itineraries')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = ItineraryForm(instance=itinerary)
    return render(request, 'travel/edit_itinerary.html', {'form': form, 'itinerary': itinerary})


def save_passenger(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST) 
        if form.is_valid():
            role = form.cleaned_data['role']  
            dni = form.cleaned_data['dni']  
            existing_passenger = Passenger.objects.filter(dni=dni).exists()
            if existing_passenger:
                data = {
                    'error': 'Ya existe un usuario con este DNI.'
                }
                return JsonResponse(data, status=400)

            if role == 'PAYER':
                message = 'Usuario pagador guardado, ahora puedes guardar el pasajero invitado.'
            elif role == 'BOTH':
                message = 'Usuario pagador guardado, ahora puedes guardar el pasajero invitado.'
            else:
                message = 'Pasajero guardado exitosamente'
            
            passenger = form.save(commit=False)
            passenger.user = request.user
            passenger.save()
            data = {
                'message': message
            }
            return JsonResponse(data)
        else:
            data = {
                'error': 'Error en los datos del formulario.'
            }
            return JsonResponse(data, status=400)  # Código de error 400 (Bad Request)
    else:
        data = {
            'error': 'Método no permitido.'
        }
        return JsonResponse(data, status=405)



@require_POST
def create_payment(request, sale_id, passenger_id):
    sale = get_object_or_404(Sale, id=sale_id)
    num_installments = int(request.POST.get('cuotas'))
    total_payment = Decimal(request.POST.get('totalPagar'))
    sale.total_debt -= total_payment
    sale.installments -= num_installments
    sale.save()
    payment = Payment(sale=sale, amount_paid=total_payment, payment_method=sale.payment_method)
    payment.save()
    if sale.installments == 0:
        sale.sale_status = 'COMPLETED'
        sale.save()
    messages.success(request, 'Pago registrado exitosamente!')
    return redirect('passenger_sales', passenger_id=passenger_id)

def get_itineraries_by_trip(request, trip_id):
    # Obtener el parámetro 'page' de la solicitud GET para la paginación
    page_number = request.GET.get('page')
    items_per_page = request.GET.get('items_per_page')  # Número de elementos por página, si es proporcionado
    # Obtener los itinerarios para el ID de viaje dado
    itineraries = Itinerary.objects.filter(trip_id=trip_id).values('id', 'description', 'dates_and_times', 'hotels')
    # Paginar los itinerarios
    paginator = Paginator(itineraries, items_per_page if items_per_page else 10)  # 10 elementos por página por defecto
    try:
        paginated_itineraries = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el parámetro 'page' no es un número, mostrar la primera página
        paginated_itineraries = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página disponible
        paginated_itineraries = paginator.page(paginator.num_pages)

    # Formatear los itinerarios paginados como lista de diccionarios
    itineraries_list = list(paginated_itineraries)

    # Devolver los itinerarios paginados como una respuesta JSON
    return JsonResponse({'itineraries': itineraries_list})

def view_notifications(request):
    notification_contact = Contact.objects.order_by('-timestamp')[:5]
    return render(request, 'travel/notifications.html', {'notifications': notification_contact})

@csrf_exempt
def create_contact_form(request):
    if request.method == 'POST':
        contact = Contact.objects.create(
            name=request.POST.get('nombre'),
            email=request.POST.get('email'),
            message=request.POST.get('mensaje')
        )
        print(contact)
        contact.save()
        return JsonResponse({'message': "Hemos guardado tu registro, pronto nos pondremos en contacto!"}, status=201)
    return JsonResponse({'error': 'Método no permitido'}, status=405)