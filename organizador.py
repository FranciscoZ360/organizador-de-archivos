"""Organizador de archivos: clasifica los archivos de una carpeta por tipo.

Uso:
    python organizador.py CARPETA            # simula, no mueve nada
    python organizador.py CARPETA --aplicar  # mueve los archivos
    python organizador.py CARPETA --deshacer # revierte el último movimiento
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

CATEGORIAS = {
    "Imágenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".md", ".rtf"},
    "Hojas de cálculo": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentaciones": {".ppt", ".pptx", ".odp"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Código": {".py", ".js", ".html", ".css", ".php", ".java", ".kt", ".json"},
    "Instaladores": {".exe", ".msi", ".apk", ".dmg"},
}
OTROS = "Otros"
REGISTRO = ".organizador-registro.json"


def categoria_de(archivo: Path) -> str:
    """Devuelve la categoría según la extensión (sin distinguir mayúsculas)."""
    extension = archivo.suffix.lower()
    for nombre, extensiones in CATEGORIAS.items():
        if extension in extensiones:
            return nombre
    return OTROS


def destino_libre(destino: Path) -> Path:
    """Si el destino existe, agrega ' (1)', ' (2)'... para no sobrescribir."""
    if not destino.exists():
        return destino
    contador = 1
    while True:
        candidato = destino.with_name(f"{destino.stem} ({contador}){destino.suffix}")
        if not candidato.exists():
            return candidato
        contador += 1


def planificar(carpeta: Path) -> list[tuple[Path, Path]]:
    """Lista (origen, destino) para los archivos de primer nivel de la carpeta."""
    movimientos = []
    reservados: set[Path] = set()
    for archivo in sorted(carpeta.iterdir()):
        if not archivo.is_file() or archivo.name == REGISTRO:
            continue
        destino = destino_libre(carpeta / categoria_de(archivo) / archivo.name)
        # Evita choques entre dos archivos del mismo plan con igual nombre.
        while destino in reservados:
            destino = destino_libre(
                destino.with_name(f"{destino.stem} (+){destino.suffix}")
            )
        reservados.add(destino)
        movimientos.append((archivo, destino))
    return movimientos


def aplicar(carpeta: Path, movimientos: list[tuple[Path, Path]]) -> None:
    """Mueve los archivos y guarda un registro para poder deshacerlo."""
    hechos = []
    for origen, destino in movimientos:
        destino.parent.mkdir(exist_ok=True)
        shutil.move(str(origen), str(destino))
        hechos.append([str(origen), str(destino)])
    (carpeta / REGISTRO).write_text(
        json.dumps(hechos, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def deshacer(carpeta: Path) -> int:
    """Revierte el último movimiento registrado. Devuelve cuántos archivos volvió."""
    registro = carpeta / REGISTRO
    if not registro.exists():
        return 0
    hechos = json.loads(registro.read_text(encoding="utf-8"))
    revertidos = 0
    for origen, destino in reversed(hechos):
        destino, origen = Path(destino), Path(origen)
        if destino.exists() and not origen.exists():
            shutil.move(str(destino), str(origen))
            revertidos += 1
    registro.unlink()
    for subcarpeta in carpeta.iterdir():
        if subcarpeta.is_dir() and not any(subcarpeta.iterdir()):
            subcarpeta.rmdir()
    return revertidos


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Organiza los archivos de una carpeta en subcarpetas por tipo."
    )
    parser.add_argument("carpeta", type=Path, help="carpeta a organizar")
    modo = parser.add_mutually_exclusive_group()
    modo.add_argument("--aplicar", action="store_true", help="mover los archivos")
    modo.add_argument("--deshacer", action="store_true", help="revertir el último movimiento")
    args = parser.parse_args(argv)

    if not args.carpeta.is_dir():
        print(f"Error: '{args.carpeta}' no es una carpeta.", file=sys.stderr)
        return 1

    if args.deshacer:
        print(f"Archivos devueltos a su lugar: {deshacer(args.carpeta)}")
        return 0

    movimientos = planificar(args.carpeta)
    if not movimientos:
        print("No hay archivos para organizar.")
        return 0

    for origen, destino in movimientos:
        print(f"{origen.name}  ->  {destino.parent.name}/{destino.name}")

    if args.aplicar:
        aplicar(args.carpeta, movimientos)
        print(f"\nListo: {len(movimientos)} archivo(s) movido(s).")
    else:
        print(f"\nSimulación: {len(movimientos)} archivo(s). Usa --aplicar para moverlos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
