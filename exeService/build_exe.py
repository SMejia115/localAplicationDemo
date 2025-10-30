"""
Script para compilar app.py en un ejecutable usando PyInstaller
Este script automatiza el proceso de creación del ejecutable con todas las dependencias necesarias
"""

import subprocess
import sys
import os

def build_executable():
    """
    Construye el ejecutable de app.py usando PyInstaller con todas las configuraciones necesarias
    """
    print("=" * 60)
    print("Iniciando proceso de compilación de app.py a ejecutable")
    print("=" * 60)
    
    # Definir los argumentos para PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--onefile",                          # Crear un solo archivo ejecutable
        "--windowed",                         # Sin ventana de consola
        "--name=DemoApp",                     # Nombre del ejecutable
        "--icon=icon.ico",                    # Ícono del ejecutable
        "--add-data=icon.png;.",              # Incluir el ícono PNG en el ejecutable
        "--hidden-import=fastapi",            # Importaciones ocultas necesarias
        "--hidden-import=uvicorn",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=plyer",
        "--hidden-import=winotify",           # Añadir winotify como importación oculta
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--additional-hooks-dir=.",           # Directorio con hooks personalizados
        "--collect-all=fastapi",              # Recolectar todos los módulos de FastAPI
        "--collect-all=winotify",             # Recolectar todos los módulos de winotify
        "--noconfirm",                        # Sobrescribir sin preguntar
        "app.py"                              # Archivo principal a compilar
    ]
    
    print("\nComando PyInstaller:")
    print(" ".join(pyinstaller_args))
    print("\n" + "=" * 60)
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(
            pyinstaller_args,
            check=True,
            capture_output=True,
            text=True
        )
        
        print("\n✓ Compilación exitosa!")
        print("\nSalida:")
        print(result.stdout)
        
        # Verificar que el ejecutable se creó
        exe_path = os.path.join("dist", "DemoApp.exe")
        if os.path.exists(exe_path):
            exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # Tamaño en MB
            print(f"\n✓ Ejecutable creado: {exe_path}")
            print(f"✓ Tamaño: {exe_size:.2f} MB")
        else:
            print(f"\n⚠ Advertencia: No se encontró el ejecutable en {exe_path}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n✗ Error durante la compilación:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("\n✗ Error: PyInstaller no está instalado.")
        print("Instálalo con: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"\n✗ Error inesperado: {str(e)}")
        return False

def check_requirements():
    """
    Verifica que todos los requisitos estén instalados
    """
    print("\nVerificando dependencias...")
    
    try:
        import pyinstaller
        print("✓ PyInstaller está instalado")
    except ImportError:
        print("✗ PyInstaller no está instalado")
        print("  Ejecuta: pip install pyinstaller")
        return False
    
    # Verificar archivos necesarios
    required_files = ["app.py", "icon.ico", "icon.png"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} encontrado")
        else:
            print(f"✗ {file} no encontrado")
            return False
    
    return True

def main():
    """
    Función principal del script
    """
    print("\n" + "=" * 60)
    print("  COMPILADOR DE APP.PY A EJECUTABLE")
    print("=" * 60)
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"\nDirectorio de trabajo: {script_dir}")
    
    # Verificar requisitos
    if not check_requirements():
        print("\n✗ No se cumplen todos los requisitos.")
        print("Por favor, instala las dependencias necesarias.")
        sys.exit(1)
    
    # Construir el ejecutable
    print("\n" + "=" * 60)
    if build_executable():
        print("\n" + "=" * 60)
        print("  ✓ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\nEl ejecutable se encuentra en: dist/DemoApp.exe")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("  ✗ PROCESO FALLIDO")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
