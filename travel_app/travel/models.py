from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from enum import Enum

class User(AbstractUser):
    pass

class PassengerRole(Enum):
    TRAVELER = 'VIAJERO'  # Representa al pasajero que va a viajar
    PAYER = 'PAGADOR'        # Representa al pasajero que paga por otro
    BOTH = 'AMBOS'          # Representa al pasajero que es tanto viajero como pagador

class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    passenger_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dni = models.CharField(max_length=20)
    
    role = models.CharField(
        max_length=10,
        choices=[(role.name, role.value) for role in PassengerRole],
        default=PassengerRole.TRAVELER.value
    )

    def __str__(self):
        return f"{self.name} {self.lastname} - DNI: {self.dni}"
    


class TripStatus(Enum):
    ACTIVE = 'Activo'
    CANCELLED = 'Cancelado'
    COMPLETED = 'Completado'



class TransportationType(Enum):
    BUS = 'Colectivo'
    TRAIN = 'Trafi'
    PLANE = 'Avión'
    CAR = 'Auto'    

class Trip(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    capacity = models.IntegerField()
    TRANSPORT_CHOICES = [
        (tag.name, tag.value) for tag in TransportationType
    ]
    transportation_type = models.CharField(max_length=50, choices=TRANSPORT_CHOICES)
    trip_status = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in TripStatus], default=TripStatus.ACTIVE.value)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    arrival_date = models.DateField()
    departure_date = models.DateField()

    def __str__(self):
        return f"Viaje desde {self.origin} hacia {self.destination}"
    
class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    itinerary_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(blank=False, null=False)
    destination = models.CharField(max_length=100)
    excursion_names = models.TextField()
    dates_and_times = models.DateTimeField()
    hotels = models.TextField()
    def __str__(self):
        return f"Itinerario para Viaje: {self.trip}, Destino: {self.destination}, Código: {self.itinerary_code}"
    def get_itineraries(self):
        return Itinerary.objects.filter(trip=self)
        
class SaleStatus(Enum):
    PENDING = 'Pendiente'
    CANCELLED = 'Cancelado'
    COMPLETED = 'Terminado'


class PaymentMethod(Enum):
    CASH = 'Efectivo'
    CARD = 'Tarjeta'
    PAYPAL = 'Transferencia'

class Sale(models.Model):
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in PaymentMethod])
    installments = models.IntegerField(default=1) 
    total_debt = models.DecimalField(max_digits=10, decimal_places=2)
    sale_status = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in SaleStatus], default=SaleStatus.PENDING.value)
    def __str__(self):
        return f"Venta por {self.passenger} para {self.trip} en {self.sale_date}"
    
class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Pago de ${self.amount_paid} para la venta {self.sale.id}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name