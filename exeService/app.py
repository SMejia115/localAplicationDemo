import fastapi
import os
import sys
import threading
import webbrowser
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pystray import Icon, Menu, MenuItem
from PIL import Image
from plyer import notification
from winotify import Notification, audio
import uvicorn
import time


# --- Función para acceder a recursos dentro del .exe ---
def resource_path(relative_path):
    """Obtiene la ruta absoluta incluso dentro del ejecutable .exe"""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal creada por PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- Inicializar FastAPI ---
app = FastAPI()

# --- Permitir CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia a ["http://127.0.0.1:5500"] si usas Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dirección del servidor
SERVER_URL = "http://127.0.0.1:5000"


# ---- API ROUTES ----
@app.get("/status")
async def get_status():
    return {"status": ".exe corriendo correctamente"}


@app.post("/message")
async def post_message(request: Request):
    data = await request.json()
    message = data.get("message", "")

    # Usar winotify para notificaciones nativas de Windows
    toast = Notification(
        app_id="DemoApp",
        title="Nuevo mensaje recibido",
        msg=message,
        duration="short",
        icon=resource_path("icon.png")
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()

    return {"response": f"Servidor recibió: {message}"}


@app.get("/fibonacci/{n}")
async def get_fibonacci(n: int):
    """Devuelve los primeros n números de Fibonacci"""
    if n <= 0:
        return JSONResponse(status_code=400, content={"error": "n debe ser mayor a 0"})

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    fib = fib[:n]

    # Usar winotify para notificaciones nativas de Windows
    toast = Notification(
        app_id="DemoApp",
        title="Serie Fibonacci generada",
        msg=f"Se generaron {n} números",
        duration="short",
        icon=resource_path("icon.png")
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()

    return {"fibonacci": fib}


# ---- TRAY ICON ----
def run_api():
    """Lanza el servidor FastAPI"""
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


def open_front():
    """Abre la interfaz frontend"""
    webbrowser.open("http://127.0.0.1:5500/app/index.html")


def show_server_url(icon, item):
    """Muestra la URL del backend"""
    toast = Notification(
        app_id="DemoApp",
        title="Servidor en ejecución",
        msg=f"Backend activo en {SERVER_URL}",
        duration="short",
        icon=resource_path("icon.png")
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()


def on_exit(icon, item):
    """Cierra el programa completamente"""
    icon.stop()
    os._exit(0)


def setup_tray():
    """Crea el ícono en la bandeja del sistema"""
    try:
        icon_path = resource_path("icon.png")
        if not os.path.exists(icon_path):
            toast = Notification(
                app_id="DemoApp",
                title="Error",
                msg="No se encontró el icono de bandeja (icon.png)",
                duration="short"
            )
            toast.show()
            return

        icon_image = Image.open(icon_path)
        menu = Menu(
            MenuItem("Abrir interfaz", lambda: open_front()),
            MenuItem("Mostrar URL", lambda: (lambda: (
                toast := Notification(
                    app_id="DemoApp",
                    title="Servidor local",
                    msg="http://127.0.0.1:5000",
                    duration="short",
                    icon=resource_path("icon.png")
                ),
                toast.show()
            ))()),
            MenuItem("Salir", on_exit)
        )
        icon = Icon("DemoApp", icon_image, "DemoApp", menu)
        icon.run()
    except Exception as e:
        toast = Notification(
            app_id="DemoApp",
            title="Error en bandeja",
            msg=str(e),
            duration="long"
        )
        toast.show()

if __name__ == "__main__":
    # Inicia el servidor en segundo plano
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # Espera un poco antes de crear la bandeja (asegura que todo cargó)
    time.sleep(2)

    # Ejecuta la bandeja en el hilo principal
    setup_tray()