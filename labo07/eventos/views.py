from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento, Usuario, RegistroEvento
from .forms import EventoForm, RegistroEventoForm
#ORM
from django.db.models import Count
from django.utils import timezone

# Create your views here.

# Vista para crear un nuevo evento
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

# Vista para ver detalles de un evento
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuarios_registrados = evento.registroevento_set.all()  # Obtiene los usuarios registrados en este evento
    return render(request, 'eventos/detalle_evento.html', {'evento': evento, 'usuarios_registrados': usuarios_registrados})

# Vista para actualizar información de un evento
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})

# Vista para eliminar un evento
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('lista_eventos')
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})


#Listar eventos
def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})


#Consutla ORM tarea
def estadisticas(request):
    # Consulta 1: ¿Cuántos usuarios están registrados en un evento específico?
    evento_id = 1  # evento Halloween Horror Nights
    usuarios_registrados_count = Evento.objects.get(pk=evento_id).registroevento_set.count()

    # Consulta 2: ¿Cuántos eventos se están llevando a cabo este mes?
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = start_of_month.replace(month=start_of_month.month + 1)
    eventos_estem_mes = Evento.objects.filter(fecha__gte=start_of_month, fecha__lt=end_of_month)
    eventos_estem_mes_count = eventos_estem_mes.count()

    # Consulta 3: ¿Quiénes son los usuarios más activos en términos de participación en eventos?
    usuarios_activos = Usuario.objects.annotate(eventos_registrados_count=Count('registroevento'))
    usuarios_activos = usuarios_activos.order_by('-eventos_registrados_count')

    # Consulta 4: ¿Cuántos eventos ha organizado un usuario en particular?
    usuario_id = 2  # Frank Ranzek
    eventos_organizados_count = Usuario.objects.get(pk=usuario_id).evento_set.count()

    return render(request, 'eventos/estadisticas.html', {
        'usuarios_registrados_count': usuarios_registrados_count,
        'eventos_estem_mes_count': eventos_estem_mes_count,
        'usuarios_activos': usuarios_activos,
        'eventos_organizados_count': eventos_organizados_count,
    })