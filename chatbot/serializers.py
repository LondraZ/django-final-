from rest_framework import serializers
from chatbot.models import Conversacion

groq_model_list= ["openai/gpt-oss-120b", "llama-3.1-8b-instant", "openai/gpt-oss-20b", "llama-3.3-70b-versatile", "meta-llama/llama-4-scout-17b-16e-instruct", "qwen/qwen3-32b"]

class ConversacionSerializer(serializers.ModelSerializer):
    engine = serializers.CharField(default="groq", write_only=True)

    def validate(self, data):
        if data["pregunta"] == "":
            raise serializers.ValidationError("La pregunta no puede estar vacia")
        if data["temperatura"] <= 0 or data["temperatura"] > 1:
            raise serializers.ValidationError("La temperatura debe estar entre 0 y 1")
        if data["engine"] not in ["groq", "llamacpp"]:
            raise serializers.ValidationError("Engine no valido")
        if data["engine"]=="groq" and data.get("modelo") not in groq_model_list:
            raise serializers.ValidationError("Modelo no valido")      
        return data
    
    class Meta:
        model = Conversacion
        fields = '__all__'
        extra_kwargs = {
            "fecha_creacion": {"read_only": True},
            "fecha_actualizacion": {"read_only": True},
            "usuario": {"read_only": True},
            "respuesta": {"read_only": True},
        }