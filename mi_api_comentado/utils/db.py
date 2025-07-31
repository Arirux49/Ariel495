# Importa el cliente de MongoDB para conectarse a la base de datos
from pymongo import MongoClient

# Crea una instancia del cliente de MongoDB usando una URI de conexión a MongoDB Atlas
# Esta URI incluye nombre de usuario, contraseña, nombre del cluster y configuración de reintentos
client = MongoClient(
    "mongodb+srv://Arirux:ariel123@cluster0.vcs8lnn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Se conecta a la base de datos principal del proyecto, llamada 'social_music'
db = client["social_music"]

# A continuación, se definen las colecciones de la base de datos, que equivalen a "tablas" en SQL

# Colección que almacena información de los usuarios
users_collection = db["users"]

# Colección que almacena los instrumentos musicales registrados
instruments_collection = db["instruments"]

# Colección que almacena los samples (fragmentos de audio subidos por los usuarios)
samples_collection = db["samples"]

# Colección que almacena las grabaciones musicales que combinan varios samples
recordings_collection = db["recordings"]

# Colección que almacena los comentarios realizados sobre samples o grabaciones
comments_collection = db["comments"]

# Tabla intermedia que representa la relación muchos-a-muchos entre usuarios e instrumentos
user_instruments = db["user_instruments"]

# Tabla intermedia que vincula samples con los instrumentos que se usaron en ellos
sample_instruments = db["sample_instruments"]

# Tabla intermedia que vincula grabaciones con los samples utilizados en ellas
recording_samples = db["recording_samples"]

# Función auxiliar que permite verificar si la conexión a la base de datos está activa
def ping_db():
    try:
        # Ejecuta un comando 'ping' a la base de datos para comprobar conectividad
        client.admin.command('ping')
        return True  # Si tiene éxito, devuelve True
    except Exception as e:
        # Si hay un error, lo imprime en consola y devuelve False
        print(f"Error de conexión a MongoDB: {e}")
        return False
