import tempfile
import unittest
from pathlib import Path

import organizador as org


class PruebasOrganizador(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def crear(self, *nombres):
        for nombre in nombres:
            (self.carpeta / nombre).write_text(nombre, encoding="utf-8")

    def test_categoria_ignora_mayusculas(self):
        self.assertEqual(org.categoria_de(Path("FOTO.JPG")), "Imágenes")
        self.assertEqual(org.categoria_de(Path("raro.xyz")), "Otros")

    def test_simulacion_no_mueve(self):
        self.crear("a.pdf", "b.png")
        org.main([str(self.carpeta)])
        self.assertTrue((self.carpeta / "a.pdf").exists())

    def test_aplicar_mueve_por_tipo(self):
        self.crear("a.pdf", "b.png", "c.xyz")
        org.main([str(self.carpeta), "--aplicar"])
        self.assertTrue((self.carpeta / "Documentos" / "a.pdf").exists())
        self.assertTrue((self.carpeta / "Imágenes" / "b.png").exists())
        self.assertTrue((self.carpeta / "Otros" / "c.xyz").exists())

    def test_no_sobrescribe_archivos_existentes(self):
        (self.carpeta / "Documentos").mkdir()
        (self.carpeta / "Documentos" / "a.pdf").write_text("viejo")
        self.crear("a.pdf")
        org.main([str(self.carpeta), "--aplicar"])
        self.assertEqual((self.carpeta / "Documentos" / "a.pdf").read_text(), "viejo")
        self.assertTrue((self.carpeta / "Documentos" / "a (1).pdf").exists())

    def test_deshacer_restaura(self):
        self.crear("a.pdf", "b.png")
        org.main([str(self.carpeta), "--aplicar"])
        org.main([str(self.carpeta), "--deshacer"])
        self.assertTrue((self.carpeta / "a.pdf").exists())
        self.assertTrue((self.carpeta / "b.png").exists())
        self.assertFalse((self.carpeta / "Documentos").exists())

    def test_carpeta_inexistente(self):
        self.assertEqual(org.main([str(self.carpeta / "nada")]), 1)


if __name__ == "__main__":
    unittest.main()
