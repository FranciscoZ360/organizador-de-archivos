# Organizador de archivos

Herramienta de línea de comandos en Python que ordena los archivos de una carpeta en subcarpetas según su tipo (imágenes, documentos, audio, video, etc.). Sin dependencias externas: solo la biblioteca estándar.

Nació de un problema real: carpetas de descargas con cientos de archivos mezclados.

## Características

- **Simulación por defecto:** muestra qué haría sin mover nada hasta que uses `--aplicar`.
- **No sobrescribe:** si el destino ya existe, renombra a `nombre (1).ext`.
- **Se puede deshacer:** guarda un registro y `--deshacer` devuelve los archivos a su lugar.
- **Fácil de ajustar:** las categorías y extensiones están en un diccionario al inicio de `organizador.py`.
- Solo toca los archivos del primer nivel; no entra en subcarpetas.

## Requisitos

Python 3.9 o superior.

## Uso

```bash
# 1. Ver qué se movería (no cambia nada)
python organizador.py "C:/Users/yo/Descargas"

# 2. Mover los archivos
python organizador.py "C:/Users/yo/Descargas" --aplicar

# 3. Revertir el último movimiento
python organizador.py "C:/Users/yo/Descargas" --deshacer
```

Ejemplo de salida:

```
foto.JPG     ->  Imágenes/foto.JPG
informe.pdf  ->  Documentos/informe.pdf
datos.zip    ->  Comprimidos/datos.zip

Simulación: 3 archivo(s). Usa --aplicar para moverlos.
```

## Tests

```bash
python -m unittest discover
```

Cubre la clasificación por extensión, la simulación, el movimiento, la protección contra sobrescritura y el deshacer.

## Estado y próximos pasos

Versión inicial, funcional y probada. Ideas pendientes:

- Opción para leer las categorías desde un archivo de configuración.
- Opción para incluir subcarpetas de forma recursiva.
- Empaquetarlo para instalarlo con `pip`.

## Qué aprendí construyéndolo

Manejo de rutas con `pathlib`, interfaces de línea de comandos con `argparse`, operaciones seguras sobre archivos (simular antes de aplicar, registrar para deshacer) y pruebas con `unittest`.
