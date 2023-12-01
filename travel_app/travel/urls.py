from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register", views.register, name="register"),
    path('create_passenger', views.create_passenger, name='create_passenger'),
    path('list_passengers', views.list_passengers, name='list_passengers'),
    path('edit/<int:pk>', views.edit_passenger, name='edit_passenger'),
    path('delete/<int:pk>', views.delete_passenger, name='delete_passenger'),
    path('sales', views.create_sale, name='create_sale'),
    path('trips', views.create_trip, name='create_trip'),
    path('list_trips', views.list_trips, name='list_trips'),
    path('trip/edit/<int:pk>', views.edit_trip, name='edit_trip'),
    path('trip/delete/<int:pk>', views.delete_trip, name='delete_trip'),
    path('get_trip_price/<int:trip_id>/', views.get_trip_price, name='get_trip_price'),
    path('get_trips_by_date/<str:selected_date>/', views.get_trips_by_date, name='get_trips_by_date'),
    path('passenger_sales/<int:passenger_id>/', views.passenger_sales, name='passenger_sales'),
    path('create_itinerary', views.create_itinerary, name='create_itinerary'),
    path('list_itineraries', views.list_itineraries, name='list_itineraries'),
    path('edit_itinerary/<int:pk>', views.edit_itinerary, name='edit_itinerary'),
    path('delete_itinerary/<int:pk>', views.delete_itinerary, name='delete_itinerary'),
    path('get_itineraries_by_trip/<int:trip_id>/', views.get_itineraries_by_trip, name='get_itineraries_by_trip'),
    path('create_payment/<int:sale_id>/<int:passenger_id>/', views.create_payment, name='create_payment'),
    path('save_passenger', views.save_passenger, name='save_passenger'),
    path('save_contact', views.create_contact_form, name='save_contact'),
    path('get_notifications', views.view_notifications, name='get_notifications'),


] 


 