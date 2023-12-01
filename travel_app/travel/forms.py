from django import forms
from .models import Passenger, Trip
from .models import Trip, Sale, TripStatus, TransportationType, SaleStatus, PaymentMethod, Itinerary, Payment, PassengerRole

from django.core.exceptions import ValidationError

class PassengerForm(forms.ModelForm):


    role = forms.ChoiceField(
        label='Rol',
        choices=[(role.name, role.value) for role in PassengerRole],
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
        required=True
    )
    

    class Meta:
        model = Passenger
        fields = ['role', 'dni', 'name', 'lastname', 'age', 'email', 'phone_number']
        labels = {
            'dni': 'DNI',
            'name': 'Nombre',
            'lastname': 'Apellido',
            'age': 'Edad',
            'email': 'Correo Electrónico',
            'phone_number': 'Número de Teléfono',
        }

        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'required': True, 'placeholder': 'Ingrese DNI'}),
            'name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'required': True, 'placeholder': 'Ingrese Nombre'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'required': True, 'placeholder': 'Ingrese Apellido'}),
            'age': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'required': True, 'placeholder': 'Ingrese Edad'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill', 'required': True, 'placeholder': 'Ingrese Correo Electrónico'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'required': True, 'type': 'tel', 'pattern': '[0-9]+', 'placeholder': 'Ingrese Número de Teléfono'}),
        }



class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['origin', 'destination', 'departure_date','arrival_date', 'capacity', 'transportation_type', 'trip_status', 'price_per_day']
        widgets = {
            'origin': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese el origen'}),
            'destination': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese el destino'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese la capacidad'}),
            'transportation_type': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in TransportationType]),
            'trip_status': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in TripStatus]),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese el precio por día'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control rounded-pill', 'type': 'date'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control rounded-pill', 'type': 'date'}),
        }
        
        labels = {
            'origin': 'Origen',
            'destination': 'Destino',
            'departure_date': 'Fecha de Salida',
            'arrival_date': 'Fecha de Llegada',
            'capacity': 'Capacidad',
            'transportation_type': 'Tipo de Transporte',
            'trip_status': 'Estado del Viaje',
            'price_per_day': 'Precio por Día',
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['passenger', 'trip', 'price', 'payment_method', 'installments', 'total_debt', 'sale_status']
        widgets = {

            'price': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Precio', 'readonly': True}),
            'installments': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Número de cuotas'}),
            'total_debt': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Deuda total', 'readonly': True}),
            'payment_method': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in PaymentMethod]),
            'sale_status': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in SaleStatus]),
            'passenger': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'trip': forms.Select(attrs={'class': 'form-control rounded-pill d-none'}),
        }
        labels = {
            'passenger': 'Pasajero',
            'price': 'Precio',
            'payment_method': 'Método de Pago',
            'installments': 'Número de Cuotas',
            'total_debt': 'Deuda Total',
            'sale_status': 'Estado de Venta',
        }


    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['passenger'].queryset = Passenger.objects.filter(role__in=['PAYER', 'BOTH'])
        self.fields['price'].widget.attrs['readonly'] = True

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['trip', 'destination', 'excursion_names', 'dates_and_times', 'hotels', 'description']
        widgets = {
            'trip': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'destination': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Destino'}),
            'excursion_names': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Nombre excursión'}),
            'dates_and_times': forms.DateTimeInput(attrs={'class': 'form-control rounded-pill', 'type': 'datetime-local'}),
            'hotels': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Hotel'}),
        }
        labels = {
            'trip': 'Viaje',
            'description': 'Descripción',
            'destination': 'Destino',
            'excursion_names': 'Nombre de Excursión',
            'dates_and_times': 'Fecha y Hora',
            'hotels': 'Hoteles',
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['sale', 'payment_method', 'amount_paid']
        widgets = {
            'sale': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'payment_method': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Valor a Pagar'}),
        }
        labels = {
            'sale': 'Venta',
            'payment_method': 'Método de Pago',
            'amount_paid': 'Valor a Pagar',
        }        

class SaleSearchForm(forms.Form):
    sale_id = forms.IntegerField(label='Buscar por ID de Venta', widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'}))        