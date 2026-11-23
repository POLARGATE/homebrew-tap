"""Sube Casks/polarbat.rb a la última versión del canal de Sparkle.

Sin dependencias: lee el appcast, compara con el cask y, si hay versión
nueva, descarga el DMG, calcula su sha256 y reescribe version y sha256.
"""
import hashlib
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

APPCAST = "https://polargate.ai/polarbat/appcast.xml"
CASK = pathlib.Path(__file__).resolve().parent.parent / "Casks" / "polarbat.rb"
SP = "{http://www.andymatuschak.org/xml-namespaces/sparkle}"


def main() -> int:
    with urllib.request.urlopen(APPCAST, timeout=30) as r:
        canal = ET.fromstring(r.read())
    items = canal.findall("./channel/item")
    ultimo = max(items, key=lambda i: int(i.findtext(f"{SP}version")))
    corta = ultimo.findtext(f"{SP}shortVersionString")
    build = ultimo.findtext(f"{SP}version")
    url = ultimo.find("enclosure").attrib["url"]
    nueva = f"{corta},{build}"

    texto = CASK.read_text()
    actual = re.search(r'version "([^"]+)"', texto).group(1)
    if actual == nueva:
        print(f"polarbat ya está en {actual}")
        return 0

    esperada = f"PolarBat-{corta}-{build}.dmg"
    if not url.endswith(esperada):
        print(f"El DMG no sigue el patrón del cask: {url}", file=sys.stderr)
        return 1

    sha = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=300) as r:
        for trozo in iter(lambda: r.read(1 << 20), b""):
            sha.update(trozo)

    texto = re.sub(r'version "[^"]+"', f'version "{nueva}"', texto, count=1)
    texto = re.sub(r'sha256 "[0-9a-f]+"', f'sha256 "{sha.hexdigest()}"', texto, count=1)
    CASK.write_text(texto)
    print(f"polarbat {actual} -> {nueva}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
