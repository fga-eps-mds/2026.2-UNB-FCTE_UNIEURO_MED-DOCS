"""
Testes dos indicadores de processo e da comparação R1 × R2 (src/processo.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import json
import os
import tempfile
import unittest
from datetime import datetime

from src import processo
from src.qualidade import BRASILIA


def sprint(planejados, entregues=0, adicionados=0, fim="2026-09-28T02:59:00Z", estado="CLOSED"):
    return {"total_points": planejados, "delivered_story_points": entregues, "points_added": adicionados,
            "start_at": "2026-09-14T03:59:00Z", "end_at": fim, "state": estado}


def execucao(conclusao, quando):
    return {"conclusion": conclusao, "created_at": quando}


class PastaDeDados:
    """Pasta temporária com os arquivos de analytics-raw-data/ que o teste precisa."""

    def __init__(self, **arquivos):
        self.arquivos = arquivos

    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        for nome, conteudo in self.arquivos.items():
            with open(os.path.join(self.temp.name, nome.replace("__", "-") + ".json"), "w", encoding="utf-8") as f:
                json.dump(conteudo, f)
        return self.temp.name

    def __exit__(self, *erro):
        self.temp.cleanup()


class ReleaseTest(unittest.TestCase):
    def test_cada_momento_pertence_a_release_em_que_cai(self):
        self.assertEqual(processo.release_de(datetime(2026, 9, 28, 23, 0, tzinfo=BRASILIA)), "R1")
        self.assertEqual(processo.release_de(datetime(2026, 9, 29, 0, 1, tzinfo=BRASILIA)), "R2")
        self.assertEqual(processo.release_de(datetime(2026, 12, 1, tzinfo=BRASILIA)), None)


class SprintsTest(unittest.TestCase):
    def test_ignora_sprint_sem_pontos_e_associa_pela_data_de_fim(self):
        zenhub = {"sprints_velocity": {
            "Preparação": sprint(0),
            "Sprint 1": sprint(21),
            # Termina em 11/10, 23:59 em Brasília: R2.
            "Sprint 2": sprint(40, fim="2026-10-12T02:59:00Z"),
        }}
        with PastaDeDados(zenhub_analytics=zenhub) as pasta:
            lista = processo.sprints(pasta)
        self.assertEqual([(s["nome"], s["release"]) for s in lista], [("Sprint 1", "R1"), ("Sprint 2", "R2")])


class IndicadoresTest(unittest.TestCase):
    def test_calcula_p1_p2_p3_e_o_indice_por_release(self):
        zenhub = {"sprints_velocity": {
            "Sprint 1": sprint(20, entregues=10),
            "Sprint 2": sprint(40, entregues=40, adicionados=10, fim="2026-10-12T02:59:00Z"),
            "Sprint 3": sprint(50, entregues=0, adicionados=25, fim="2026-10-26T02:59:00Z", estado="OPEN"),
        }}
        runs_app = {"workflow_runs": [execucao("success", "2026-09-20T10:00:00Z"),
                                      execucao("failure", "2026-09-21T10:00:00Z"),
                                      execucao("skipped", "2026-09-22T10:00:00Z"),
                                      execucao("success", "2026-10-05T10:00:00Z")]}
        with PastaDeDados(zenhub_analytics=zenhub, GitHub_API__Runs__APP=runs_app,
                          GitHub_API__Runs__IA={"workflow_runs": []}) as pasta:
            resultado = processo.indicadores_por_release(pasta)

        r1 = resultado["R1"]
        self.assertAlmostEqual(r1["indicadores"]["P1"], 0.5)   # a execução pulada não conta
        self.assertAlmostEqual(r1["indicadores"]["P2"], 0.5)
        self.assertAlmostEqual(r1["indicadores"]["P3"], 1.0)
        self.assertAlmostEqual(r1["P"], (0.5 + 0.5 + 1.0) / 3)
        self.assertFalse(r1["em_andamento"])

        r2 = resultado["R2"]
        self.assertAlmostEqual(r2["indicadores"]["P1"], 1.0)
        # Média por sprint, e não soma de pontos.
        self.assertAlmostEqual(r2["indicadores"]["P2"], (1.0 + 0.0) / 2)
        self.assertAlmostEqual(r2["indicadores"]["P3"], (30 / 40 + 25 / 50) / 2)
        self.assertTrue(r2["em_andamento"])

    def test_release_sem_execucao_de_ci_fica_parcial(self):
        with PastaDeDados(zenhub_analytics={"sprints_velocity": {"Sprint 1": sprint(10, entregues=10)}}) as pasta:
            r1 = processo.indicadores_por_release(pasta)["R1"]
        self.assertIsNone(r1["indicadores"]["P1"])
        self.assertAlmostEqual(r1["P"], 1.0)
        self.assertTrue(r1["parcial"])

    def test_entrega_acima_do_planejado_fica_em_1(self):
        with PastaDeDados(zenhub_analytics={"sprints_velocity": {"Sprint 1": sprint(10, entregues=15)}}) as pasta:
            self.assertEqual(processo.indicadores_por_release(pasta)["R1"]["indicadores"]["P2"], 1.0)


class BugsTest(unittest.TestCase):
    def test_sem_o_arquivo_de_bugs_a_contagem_e_nao_medida(self):
        with PastaDeDados(GitHub_API__Bugs__APP={"bugs": []}) as pasta:
            self.assertIsNone(processo.bugs(pasta))

    def test_le_os_bugs_dos_dois_repositorios(self):
        app = {"bugs": [{"numero": 52, "aberta_em": "2026-10-05T12:00:00Z", "fechada_em": None}]}
        with PastaDeDados(GitHub_API__Bugs__APP=app, GitHub_API__Bugs__IA={"bugs": []}) as pasta:
            lista = processo.bugs(pasta)
        self.assertEqual([(b["repositorio"], b["numero"]) for b in lista], [("APP", 52)])
        self.assertEqual(processo.release_de(lista[0]["aberta_em"]), "R2")


if __name__ == "__main__":
    unittest.main()
