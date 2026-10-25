"""
Testes da leitura resiliente dos dados da aba Q-Rapids (src/data_layer.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import json
import os
import tempfile
import unittest
from unittest import mock

from src import data_layer, qualidade


class DadosDaAbaTest(unittest.TestCase):
    def gravar(self, pasta, nome, conteudo):
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo if isinstance(conteudo, str) else json.dumps(conteudo))

    def test_pasta_vazia_nao_e_disponivel_e_nao_inventa_dado(self):
        with tempfile.TemporaryDirectory() as pasta:
            dados = data_layer.get_qrapids_data(pasta)

        self.assertFalse(dados["disponivel"])
        self.assertEqual(dados["processo"], {})
        self.assertEqual(dados["comparativo"], {})
        for repo in ("APP", "IA"):
            self.assertEqual(dados["produto"][repo]["avaliacoes"], [])
            self.assertEqual(dados["produto"][repo]["quedas"], [])
            self.assertFalse(any(dados["produto"][repo]["marcos"].values()))

    def test_json_malformado_nao_derruba_a_aba(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.gravar(pasta, "zenhub_analytics.json", "{ isto nao e json")

            with mock.patch("builtins.print"):
                dados = data_layer.get_qrapids_data(pasta)

        self.assertFalse(dados["disponivel"])

    def test_com_so_as_sprints_a_aba_mostra_o_processo(self):
        sprints = {"sprints_velocity": {"Sprint 1": {
            "total_points": 21, "delivered_story_points": 0, "points_added": 0, "state": "CLOSED",
            "start_at": "2026-09-14T03:59:00Z", "end_at": "2026-09-28T02:59:00Z"}}}
        with tempfile.TemporaryDirectory() as pasta:
            self.gravar(pasta, "zenhub_analytics.json", sprints)

            dados = data_layer.get_qrapids_data(pasta)

        self.assertTrue(dados["disponivel"])
        self.assertEqual(list(dados["processo"]), ["R1"])
        self.assertEqual(dados["processo"]["R1"]["indicadores"]["P2"], 0.0)

    def test_falha_no_q_rapids_nao_apaga_o_processo(self):
        sprints = {"sprints_velocity": {"Sprint 1": {
            "total_points": 21, "delivered_story_points": 21, "points_added": 0, "state": "CLOSED",
            "start_at": "2026-09-14T03:59:00Z", "end_at": "2026-09-28T02:59:00Z"}}}
        with tempfile.TemporaryDirectory() as pasta:
            self.gravar(pasta, "zenhub_analytics.json", sprints)
            with mock.patch.object(qualidade, "avaliar_repositorio", side_effect=ValueError("quebrou")):
                with mock.patch("builtins.print") as log:
                    dados = data_layer.get_qrapids_data(pasta)

        self.assertEqual(dados["produto"]["APP"]["avaliacoes"], [])
        self.assertIn("R1", dados["processo"])
        self.assertTrue(any("Q-Rapids APP" in str(chamada) for chamada in log.call_args_list))


if __name__ == "__main__":
    unittest.main()
