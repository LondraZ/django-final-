from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from chatbot.models import Conversacion
from chatbot.serializers import ConversacionSerializer
from chatbot.rag import generar_respuesta
from cuentas.models import Cliente


class ChatbotView(APIView):
    serializer_class = ConversacionSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        engine = request.query_params.get('engine', "groq").lower()
        pregunta = serializer.validated_data["pregunta"].lower()

        Cliente = Cliente.objects.all()
        if not Cliente:
            return Response({"message": "No puedo generar la respuesta"}, status=status.HTTP_404_NOT_FOUND)
        contexto = "\n".join(
            [f"cliente: {p.nombre.lower()} | Apellido: {p.segundo_apellido.lower()} | " for p in Cliente])
        
        SYSTEM_PROMPT = (
            "Eres el asistente del sistema de clientes de seguro Durango. "
            "Usa solo la información provista en el 'CONTEXT' para responder "
            "consultas sobre clientes, doctores y necesidades medicas segun la locacion. "
            "Si no puedes responder con la información disponible, indica que no puedes responder."
        )
        historial_usuario = Conversacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')[:3]
        historial_plano = "".join([
            f"\nPregunta: {h.pregunta.lower()}\nUsuario: {h.respuesta.lower()}" for h in historial_usuario]
        )
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"=== CONTEXT ===\n{contexto}\n\n"
            f"=== HISTORIAL RELEVANTE ===\n"
            f"{historial_plano}" if historial_plano else "Sin historial previo relevante.\n"
            f"\n=== INSTRUCCIÓN ===\n"
            "\nResponde solo con información del contexto. Sé claro, conciso y emite la respuesta en texto plano.\n"
        )
        temperatura = serializer.validated_data.get("temperatura", 0.7)
        modelo = serializer.validated_data.get("modelo", "modelo_base")
        try:
            print("Prompt:", prompt)
            print("Haciendo petición con el modelo:", modelo)
            #print("Engine:", engine)
            respuesta = generar_respuesta(
                prompt, pregunta, temperatura=temperatura, engine=engine)
            print("Respuesta:", respuesta)
            LISTA_ERROR = ["No puedo responder a esa pregunta.",
                           "No puedo responder a tu pregunta.", "No puedo responder a tu pregunta", ""]
            if respuesta or respuesta not in LISTA_ERROR:
                print("Guardando conversacion")
                Conversacion.objects.create(
                    pregunta=pregunta, respuesta=respuesta, usuario=request.user, temperatura=temperatura)
                return Response({"pregunta": pregunta, "respuesta": respuesta})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"pregunta": pregunta, "respuesta": respuesta})

    def get(self, request):
        if request.user.is_authenticated:
            conversacion = Conversacion.objects.filter(
                usuario=request.user)
        else:
            conversacion = Conversacion.objects.all()[:10]
        serializer = ConversacionSerializer(conversacion, many=True)
        return Response(serializer.data)