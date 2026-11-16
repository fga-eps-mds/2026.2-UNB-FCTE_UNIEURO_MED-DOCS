"""
Testes da leitura dos dados da aba de qualidade por característica (src/data_layer.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from unittest import mock

from src import data_layer

RELEASES = [
    {"id": "R1", "nome": "Release 1", "inicio": "2026-08-10", "fim": "2026-09-28"},
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-11-30"},
]
HOJE = datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc)

SONAR = {
    "repositorio": "APP",
    "coletado_em": "2026-11-12T09:12:25Z",
    "medidas": {"security_rating": "1.0", "coverage": "98.3"},
    "historico": [
        {"metric": "security_rating", "history": [{"date": "2026-09-17T20:50:27+0000", "value": "1.0"}]},
        {"metric": "coverage", "history": [{"date": "2026-09-17T20:50:27+0000", "value": "95.0"}]},
    ],
}


class CaracteristicasDadosTest(unittest.TestCase):
    def gravar(self, pasta, nome, conteudo):
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo if isinstance(conteudo, str) else json.dumps(conteudo))

    def test_calcula_as_caracteristicas_de_cada_repositorio(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.gravar(pasta, "Sonar_API-Measures-APP.json", SONAR)
            self.gravar(pasta, "Sonar_API-Measures-IA.json", {**SONAR, "repositorio": "IA"})

            dados = data_layer.get_caracteristicas_data(pasta, RELEASES, HOJE)

        self.assertEqual(sorted(dados), ["APP", "IA"])
        self.assertEqual([r["release"] for r in dados["APP"]], ["R1", "R2"])
        r2 = {c["chave"]: c for c in dados["APP"][1]["caracteristicas"]}
        self.assertEqual(r2["testabilidade"]["valor"], 98.3)  # a última coleta vale na release em curso
        self.assertEqual(r2["seguranca"]["nota"], "A")

    def test_pasta_vazia_nao_inventa_dado(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.assertEqual(data_layer.get_caracteristicas_data(pasta, RELEASES, HOJE), {})

    def test_json_malformado_ou_sem_medidas_e_ignorado(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.gravar(pasta, "Sonar_API-Measures-APP.json", "{ nao e json")
            self.gravar(pasta, "Sonar_API-Measures-IA.json", {"repositorio": "IA"})

            with mock.patch("builtins.print"):
                dados = data_layer.get_caracteristicas_data(pasta, RELEASES, HOJE)

        self.assertEqual(dados, {})

    def test_repositorio_sem_historico_fica_nao_medido_em_vez_de_zero(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.gravar(pasta, "Sonar_API-Measures-APP.json", {"repositorio": "APP", "medidas": {}})

            dados = data_layer.get_caracteristicas_data(pasta, RELEASES, HOJE)

        for release in dados["APP"]:
            self.assertTrue(all(c["valor"] is None for c in release["caracteristicas"]))


if __name__ == "__main__":
    unittest.main()
