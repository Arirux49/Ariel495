# Importamos HTTPException para lanzar errores HTTP desde controladores
# Importa la clase HTTPException de FastAPI, que se utiliza para lanzar errores HTTP personalizados
from fastapi import HTTPException

# Módulo personalizado que gestiona autenticación con Firebase
# Importa las funciones 'auth' y 'verify_firebase_token' desde el módulo utils.firebase
# - 'auth' permite interactuar con Firebase Authentication
# - 'verify_firebase_token' verifica la validez de los tokens de Firebase
from utils.firebase import auth, verify_firebase_token

# Función para crear tokens JWT de acceso
# Importa la función para crear tokens JWT que se usarán para autenticar sesiones
from utils.security import create_access_token

# Conexión a la colección de usuarios en MongoDB
# Importa la colección de usuarios desde la base de datos MongoDB (usuarios)
from utils.db import users_collection

# Para manejar fechas y horas
# Importa 'datetime' para capturar la fecha y hora actuales (registro del usuario)
from datetime import datetime

# BaseModel y EmailStr de Pydantic para validar entradas de datos
# Importa 'BaseModel' para definir esquemas de datos y 'EmailStr' para validar correos electrónicos
from pydantic import BaseModel, EmailStr

# Optional permite declarar atributos que pueden ser nulos u opcionales
# Importa 'Optional' para declarar campos que pueden ser opcionales en los modelos
from typing import Optional


# Modelo para registrar un usuario: requiere email, password y nombre
# Define el esquema de validación para el registro de usuario
# Se hereda de 'BaseModel' para validar automáticamente los datos recibidos
class UserRegister(BaseModel):
# Campo obligatorio: correo electrónico, validado como dirección válida
    email: EmailStr                          # Email con validación de formato
# Campo obligatorio: contraseña en formato de texto plano
    password: str                            # Contraseña del usuario
# Campo obligatorio: nombre del usuario
    nombre: str                              # Nombre del usuario
# Campo opcional: descripción del perfil artístico del usuario
    perfil_artista: Optional[str] = ""       # Perfil opcional del artista


# Modelo para login de usuario: requiere email y password
# Esquema que representa los datos necesarios para iniciar sesión
class UserLogin(BaseModel):
# Campo obligatorio: correo electrónico, validado como dirección válida
    email: EmailStr
# Campo obligatorio: contraseña en formato de texto plano
    password: str


# Controlador de autenticación con métodos estáticos para registrar e iniciar sesión
class AuthController:

    @staticmethod
# Método asincrónico que permite registrar un usuario nuevo en Firebase y MongoDB
    async def register_user(user_data: dict) -> dict:
        """
        Registra un nuevo usuario usando Firebase Auth y lo guarda en MongoDB.
        """
        try:
            # Crea el usuario en Firebase Auth
# Se crea el usuario en Firebase con email y contraseña
            firebase_user = auth.create_user_with_email_and_password(
                user_data["email"],
                user_data["password"]
            )

            # Prepara el objeto a guardar en MongoDB
# Se construye un diccionario con los datos que se guardarán en la base de datos
            user_db = {
                "firebase_uid": firebase_user["localId"],                # UID de Firebase
                "email": user_data["email"],
                "nombre": user_data["nombre"],
# Campo opcional: descripción del perfil artístico del usuario
                "perfil_artista": user_data.get("perfil_artista", ""),  # Por defecto vacío si no se especifica
                "fecha_registro": datetime.utcnow()                      # Fecha y hora actual en UTC
            }

            # Inserta el documento en la colección de usuarios
# Se inserta el nuevo documento en la colección de usuarios y se guarda el resultado
            result = users_collection.insert_one(user_db)

            # Retorna una respuesta con los datos guardados y el ID insertado como string
            return {
# Se retorna el ID del usuario insertado (convertido a string) junto con los demás datos
                "id": str(result.inserted_id),
                "firebase_uid": user_db["firebase_uid"],
                "email": user_db["email"],
                "nombre": user_db["nombre"],
# Campo opcional: descripción del perfil artístico del usuario
                "perfil_artista": user_db["perfil_artista"],
                "fecha_registro": user_db["fecha_registro"].isoformat()
            }

# Captura cualquier excepción ocurrida durante el registro del usuario
        except Exception as e:
# Si el correo ya estaba registrado en Firebase, se lanza un error 400 personalizado
            # Captura errores comunes como "EMAIL_EXISTS"
            error_message = str(e)
# Si el correo ya estaba registrado en Firebase, se lanza un error 400 personalizado
            if "EMAIL_EXISTS" in error_message:
                raise HTTPException(400, "El correo ya está registrado")
            raise HTTPException(400, f"Error en registro: {error_message}")

    @staticmethod
# Método asincrónico para iniciar sesión de usuario
    async def login_user(credentials: dict) -> dict:
        """
        Inicia sesión con Firebase y retorna un token JWT si las credenciales son correctas.
        """
        try:
            # Verifica usuario en Firebase con email y contraseña
# Se autentica al usuario con Firebase Auth usando email y contraseña
            firebase_user = auth.sign_in_with_email_and_password(
                credentials["email"],
                credentials["password"]
            )

            # Crea token JWT usando el UID de Firebase
# Se genera un token de acceso JWT usando el UID del usuario autenticado
            token = create_access_token(firebase_user["localId"])

            # Retorna el token JWT y tipo de token
            return {
                "access_token": token,
                "token_type": "bearer",
                "uid": firebase_user["localId"]
            }

# Captura cualquier excepción ocurrida durante el registro del usuario
        except Exception as e:
            # Captura errores de login como contraseña inválida o usuario no encontrado
            error_message = str(e)
            if "INVALID_PASSWORD" in error_message or "EMAIL_NOT_FOUND" in error_message:
                raise HTTPException(401, "Correo o contraseña incorrectos")
            raise HTTPException(401, f"Error en autenticación: {error_message}")
