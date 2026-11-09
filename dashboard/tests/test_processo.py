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
from src.config import MODO_ENTREGUES
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
        # APC da release: RPC ÷ PRP. Sem a lista de issues, o PRP é a soma das sprints (aproximado).
        self.assertAlmostEqual(r2["indicadores"]["P2"], 40 / 90)
        self.assertTrue(r2["prp_aproximado"])
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


def historia(id_, pontos, coluna="Done"):
    return {"id": id_, "numero": id_, "estimativa": pontos, "coluna": coluna}


class ApcDaReleaseTest(unittest.TestCase):
    def test_p2_conta_uma_vez_a_historia_que_passa_de_uma_sprint_para_a_outra(self):
        # A história 2 começa na Sprint 2 e só fecha na Sprint 3: entra uma vez no PRP da R2.
        s2 = sprint(13, entregues=0, fim="2026-10-12T02:59:00Z")
        s2.update(issues=[historia(1, 8, "In Progress"), historia(2, 5, "In Progress")], issues_total=2)
        s3 = sprint(13, entregues=13, fim="2026-10-26T02:59:00Z")
        s3.update(issues=[historia(2, 5), historia(3, 8)], issues_total=2)
        with PastaDeDados(zenhub_analytics={"sprints_velocity": {"Sprint 2": s2, "Sprint 3": s3}}) as pasta:
            r2 = processo.indicadores_por_release(pasta)["R2"]
        self.assertEqual((r2["prp"], r2["rpc"]), (21, 13))
        self.assertFalse(r2["prp_aproximado"])
        self.assertAlmostEqual(r2["indicadores"]["P2"], 13 / 21)

    def test_p2_e_o_mesmo_apc_da_aba_de_evm(self):
        from src.metrics import pontos_distintos
        s2 = sprint(13, fim="2026-10-12T02:59:00Z")
        s2.update(issues=[historia(1, 8), historia(2, 5)], issues_total=2)
        s3 = sprint(13, entregues=5, fim="2026-10-26T02:59:00Z")
        s3.update(issues=[historia(2, 5), historia(3, 8)], issues_total=2)
        with PastaDeDados(zenhub_analytics={"sprints_velocity": {"Sprint 2": s2, "Sprint 3": s3}}) as pasta:
            r2 = processo.indicadores_por_release(pasta)["R2"]
        prp_evm, _ = pontos_distintos([s2, s3])
        self.assertAlmostEqual(r2["indicadores"]["P2"], min(1.0, 5 / prp_evm))


class VariacaoDoPrpTest(unittest.TestCase):
    def test_mostra_o_prp_do_inicio_e_do_fim_o_rpc_e_o_apc_de_cada_sprint(self):
        zenhub = {"sprints_velocity": {
            "Sprint 3": sprint(74, entregues=0, adicionados=37, fim="2026-10-26T02:59:00Z"),
        }}
        with PastaDeDados(zenhub_analytics=zenhub) as pasta:
            linha = processo.variacao_do_prp(pasta)[0]
        self.assertEqual((linha["prp_inicio"], linha["adicionados"], linha["prp_fim"]), (37, 37, 74))
        self.assertEqual(linha["rpc"], 0)
        self.assertEqual(linha["apc"], 0)
        self.assertEqual(linha["release"], "R2")

    def test_prp_do_inicio_nunca_fica_negativo(self):
        # Uma história tirada da sprint pode fazer os adicionados passarem do total.
        zenhub = {"sprints_velocity": {"Sprint 1": sprint(10, adicionados=13)}}
        with PastaDeDados(zenhub_analytics=zenhub) as pasta:
            linha = processo.variacao_do_prp(pasta)[0]
        self.assertEqual(linha["prp_inicio"], 0)

    def test_sprint_em_andamento_fica_marcada(self):
        zenhub = {"sprints_velocity": {
            "Sprint 3": sprint(74, fim="2026-10-26T02:59:00Z"),
            "Sprint 4": sprint(74, fim="2026-11-09T02:59:00Z", estado="OPEN"),
        }}
        zenhub["sprints_velocity"]["Sprint 4"]["start_at"] = "2026-10-26T03:00:00Z"
        with PastaDeDados(zenhub_analytics=zenhub) as pasta:
            linhas = processo.variacao_do_prp(pasta)
        self.assertEqual([(l["sprint"], l["em_andamento"]) for l in linhas],
                         [("Sprint 3", False), ("Sprint 4", True)])
        self.assertEqual(linhas[1]["release"], "R3")

    def test_modo_entregues_soma_os_pontos_em_aceitacao_no_rpc_e_no_apc(self):
        s1 = sprint(20, entregues=5)
        s1.update(issues=[historia(1, 5), historia(2, 8, "Aceitação PO"), historia(3, 7, "In Progress")],
                  issues_total=3)
        zenhub = {"colunas_coletadas": True, "sprints_velocity": {"Sprint 1": s1}}
        with PastaDeDados(zenhub_analytics=zenhub) as pasta:
            aceitas = processo.variacao_do_prp(pasta)[0]
            entregues = processo.variacao_do_prp(pasta, MODO_ENTREGUES)[0]
            p2_entregues = processo.indicadores_por_release(pasta, MODO_ENTREGUES)["R1"]["indicadores"]["P2"]
        self.assertEqual((aceitas["rpc"], aceitas["em_aceitacao"]), (5, 8))
        self.assertAlmostEqual(aceitas["apc"], 5 / 20)
        self.assertEqual(entregues["rpc"], 13)
        self.assertAlmostEqual(entregues["apc"], 13 / 20)
        self.assertAlmostEqual(p2_entregues, 13 / 20)


if __name__ == "__main__":
    unittest.main()
