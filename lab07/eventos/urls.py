from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('evento/<int:evento_id>/editar/', views.editar_evento, name='editar_evento'),
    path('evento/<int:evento_id>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
]
