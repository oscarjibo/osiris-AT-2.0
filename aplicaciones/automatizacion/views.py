from django.shortcuts import render, redirect
from django.contrib import messages
from .models import data, SensorData, ControlData, Support
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.http import HttpResponse
from datetime import datetime
import json 

def actualizar_control_data(request):
    if request.method == 'POST':
        estado_bomba1 = request.POST.get('estadoBomba1', '0')  # Obtiene el estado de la bomba1
        estado_bomba2 = request.POST.get('estadoBomba2', '0')  # Obtiene el estado de la bomba1
        print("ESTADO BOMBA 1: ", estado_bomba1)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_insert = {"bomba1_state": estado_bomba1,
                       "bombas2_state": estado_bomba2,}
        # Aquí insertas una nueva fila en tu tabla ControlData
        control_data_insert = ControlData.objects.create(
            cliente= 'Juan Ochoa',  # Aquí debes poner el valor que corresponda
            fecha= f'{fecha}',  # Aquí se inserta la fecha y hora actual
            control_data= f'{data_insert}' # Aquí se inserta el objeto JSON
        )
        messages.success(request, 'Control actualizado correctamente')  # Aquí creas el mensaje
        return JsonResponse({'status': 'success'})
    
def home(request):
    users = data.objects.all()
    return render(request, "home.html", {"users": users})

def enviar_mail(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        cliente = request.POST.get('cliente')
        descripcion = request.POST.get('descripcion')

        fecha = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Persistir registro de soporte
        Support.objects.create(
            estado=(tipo or 'Solicitud'),
            cliente=(cliente or 'N/D'),
            support_information=str(descripcion or ''),
            fecha=fecha,
        )

        msg = 'Tu solicitud fue registrada correctamente.'
        return render(request, "support.html", {'messages': msg})
    # GET: mostrar formulario vacío
    return render(request, "support.html")

def get_data_sensor(request):
    if request.method == 'POST':
        print("POST request received")
        db_informations = SensorData.objects.values('DB_information')
        print("DB_information: ", db_informations)
        db_informations = [{"Luz_ultravioleta" : "20", "Presion_barometrica" : "30", "Luminosidad" : "40", "Lluvia" : "NO", "temperatura_aire" : "60", "Humedad_aire" : "70"}]
        print("DB_information: ", db_informations)
        return render(request, 's2.html', {"data": list(db_informations)})

def login(request):
    print("Función login_validate llamada")
    if request.method == 'POST':
        print("Método POST detectado")
        user_id = request.POST.get('user_id').strip()  # Elimina espacios en blanco
        password = request.POST.get('clave').strip()  # Elimina espacios en blanco
        print(f"user_id recibido: {user_id}, password recibida: {password}")
        try:
            print("=============")
            user = data.objects.get(id=user_id)
            # Convierte la clave a str antes de comparar, si es necesario
            if str(user.clave) == password:
                print("La contraseña es correcta, redirigiendo...")
                return render(request, "grid.html")
            else:
                print("La contraseña no coincide, mostrando mensaje de error")
                messages.error(request, 'Contraseña incorrecta')
        except data.DoesNotExist:
            print("El usuario no existe, mostrando mensaje de error")
            messages.error(request, 'El usuario no existe')
    
    print("Re-renderizando el formulario con la lista de usuarios")
    users = data.objects.all()
    return render(request, "home.html", {'users': users})


def s1(request):
    return render(request, "s1.html")

def s2(request):
    return render(request, "s2.html")

def s3(request):
    return render(request, "s3.html")

def inicio(request):
    return render(request, "grid.html")

def support(request):
    return render(request, "support.html")

def yolov5(request):
    return render(request, "yolov5.html")
def ia(request):
    return render(request, "ia.html")
def detector(request):
    return render(request, "detector.html")

def reported(request):
    # Dashboard demo de cultivo y animales
    return render(request, "reported.html")

def nvid(request):
    # Vista para análisis NVID/NDVI con imágenes de drones
    return render(request, "nvid.html")

def drones(request):
    # Módulo de planificación y supervisión de drones y tareas
    return render(request, "drones.html")


#import google.generativeai as genai
#
## Create your views here.
## add here to your generated API key
#genai.configure(api_key="AIzaSyDDURhIdmkTmkxvPKTnya0kg63hGStcSkk")
#from django.views.decorators.csrf import csrf_exempt


def _demo_response(user_text: str) -> str:
    """Genera una respuesta de demostración sobre cultivo y animales."""
    if not user_text:
        return (
            "Hola, soy tu asistente agro. Puedo hablar sobre tu cultivo, "
            "riego, clima, plagas y también sobre manejo de animales. ¿Qué te gustaría saber?"
        )

    text = user_text.lower()
    # Reglas básicas por palabras clave
    if any(k in text for k in ["riego", "regar", "humedad suelo", "goteo"]):
        return (
            "Para el riego: si la humedad del suelo está por debajo de 40%, "
            "recomiendo activar 15–20 min de goteo y reevaluar. Evita regar en horas de alta evaporación (12–15 h)."
        )
    if any(k in text for k in ["temperatura", "calor", "frío", "frio"]):
        return (
            "La temperatura óptima depende del cultivo; en general, 22–26 °C para hortalizas. "
            "Si supera 30 °C, mejora la ventilación y valora sombreo 30–40%."
        )
    if any(k in text for k in ["plaga", "plagas", "enfermedad", "trips", "pulgón", "pulgon"]):
        return (
            "Monitorea hojas jóvenes y envés 2–3 veces por semana. "
            "Implementa control integrado: trampas cromáticas, liberación de benéficos y, si es necesario, biocontrol selectivo."
        )
    if any(k in text for k in ["fertiliz", "nutriente", "nitrógeno", "nitrogeno", "npk", "abon"]):
        return (
            "Ajusta NPK según etapa: crecimiento vegetativo (más N), floración/engorde (más K). "
            "Mantén pH suelo 6.0–6.8 para disponibilidad de nutrientes."
        )
    if any(k in text for k in ["ganado", "vaca", "vacas", "bovino", "pollo", "pollos", "aves", "cerdo", "cerdos"]):
        return (
            "Para animales: revisa agua limpia y sombra. En bovinos, oferta 8–10% de MS del peso vivo en pastoreo; "
            "en aves, vigila densidad y ventilación para evitar estrés por calor."
        )
    if any(k in text for k in ["lluvia", "clima", "pronóstico", "pronostico", "uv", "radiación", "radiacion"]):
        return (
            "Considera el clima: si se esperan lluvias, reduce riego previo. "
            "Con radiación UV alta, usa sombreo parcial para evitar estrés lumínico."
        )
    if any(k in text for k in ["hola", "buenos", "buenas", "saludo"]):
        return "¡Hola! ¿En qué te ayudo con tu cultivo o animales hoy?"

    # Respuesta genérica
    return (
        "Puedo ayudarte con riego, clima, plagas, fertilización y manejo de animales. "
        "Dime el tema y doy una recomendación práctica."
    )


def chat(request):
    # GET: renderiza la página del chat (UI). POST: responde JSON para el chat.
    if request.method == 'POST':
        # Admite tanto formulario como JSON
        user_text = request.POST.get('user_text')
        body = None
        if not user_text:
            try:
                body = json.loads(request.body.decode('utf-8') or '{}')
            except Exception:
                body = None
        message = user_text or (body.get('message') if isinstance(body, dict) else None)

        # Si no hay mensaje (por ejemplo, POST desde el grid), renderiza la página
        if not message:
            return render(request, 'chat.html')

        reply = _demo_response(message)
        return JsonResponse({'ok': True, 'reply': reply})

    return render(request, 'chat.html')

def cercas(request):
    lote = request.GET.get('lote', 'A').upper()
    if lote not in ("A", "B"):
        lote = "A"
    return render(request, "fences.html", {"lote": lote})
