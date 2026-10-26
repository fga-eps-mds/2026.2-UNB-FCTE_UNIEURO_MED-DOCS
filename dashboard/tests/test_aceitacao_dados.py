"""
Testes de como a leitura dos dados e os indicadores de processo tratam as histórias em
Aceitação PO (src/data_layer.py e src/processo.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import json
import os
import tempfile
import unittest
from unittest import mock

from src import data_layer, processo
from src.config import MODO_ACEITAS, MODO_ENTREGUES


def issue(id_, numero, estimativa, coluna=None):
    resultado = {"id": id_, "numero": numero, "estimativa": estimativa}
    if coluna is not None:
        resultado["coluna"] = coluna
    return resultado


def sprint(planejados, aceitos, issues, fim="2026-10-12T02:59:00Z", inicio="2026-09-28T03:59:00Z"):
    return {
        "total_points": planejados, "delivered_story_points": aceitos, "points_added": 0,
        "state": "CLOSED", "start_at": inicio, "end_at": fim,
        "issues": issues, "issues_total": len(issues),
    }


class PastaDeDados:
    """Pasta temporária com os arquivos de analytics-raw-data/ que o teste precisa."""

    def __init__(self, sprints, manual=None):
        self.pasta = tempfile.TemporaryDirectory()
        self.caminho = self.pasta.name
        self.gravar("zenhub_analytics.json", {"sprints_velocity": sprints})
        if manual is not None:
            self.gravar("aceitacao_po_manual.json", manual)

    def gravar(self, nome, conteudo):
        with open(os.path.join(self.caminho, nome), "w", encoding="utf-8") as arquivo:
            json.dump(conteudo, arquivo)

    def __enter__(self):
        return self

    def __exit__(self, *erro):
        self.pasta.cleanup()


SPRINTS_COM_COLUNA = {
    "Sprint 2": sprint(21, 0, [issue("A", 5, 13, "Aceitação PO"), issue("B", 6, 8, "Em andamento")]),
    "Sprint 3": sprint(21, 0, [issue("A", 5, 13, "Aceitação PO"), issue("C", 7, 8, "Aceitação PO")],
                       fim="2026-10-26T02:59:00Z", inicio="2026-10-12T03:59:00Z"),
}


class ProcessoPorModoTest(unittest.TestCase):
    def test_modo_aceitas_deixa_p2_em_zero_enquanto_nada_foi_aceito(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            r2 = processo.indicadores_por_release(dados.caminho, MODO_ACEITAS)["R2"]

        self.assertEqual(r2["indicadores"]["P2"], 0.0)
        self.assertEqual(r2["pontos_aceitos"], 0.0)
        self.assertEqual(r2["pontos_em_aceitacao"], 21.0)

    def test_modo_entregues_conta_as_historias_em_aceitacao_em_p2(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            r2 = processo.indicadores_por_release(dados.caminho, MODO_ENTREGUES)["R2"]

        # Sprint 2: 0 (a #5 conta na Sprint 3). Sprint 3: 13 + 8 = 21 de 21. Média por sprint: 0,5.
        self.assertEqual(r2["indicadores"]["P2"], 0.5)

    def test_o_padrao_continua_sendo_so_as_aceitas(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            padrao = processo.indicadores_por_release(dados.caminho)["R2"]
            aceitas = processo.indicadores_por_release(dados.caminho, MODO_ACEITAS)["R2"]

        self.assertEqual(padrao["indicadores"], aceitas["indicadores"])

    def test_a_estabilidade_do_escopo_nao_depende_do_modo(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            aceitas = processo.indicadores_por_release(dados.caminho, MODO_ACEITAS)["R2"]
            entregues = processo.indicadores_por_release(dados.caminho, MODO_ENTREGUES)["R2"]

        self.assertEqual(aceitas["indicadores"]["P3"], entregues["indicadores"]["P3"])

    def test_velocidade_da_comparacao_segue_o_modo(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            aceitas = processo.comparativo(dados.caminho, MODO_ACEITAS)["R2"]
            entregues = processo.comparativo(dados.caminho, MODO_ENTREGUES)["R2"]

        self.assertEqual(aceitas["velocidade"], 0.0)
        self.assertEqual(entregues["velocidade"], 10.5)
        self.assertEqual(entregues["pontos_em_aceitacao"], 21.0)

    def test_aceitos_somam_com_os_em_aceitacao_no_modo_entregues(self):
        sprints = {"Sprint 3": sprint(21, 8, [issue("A", 5, 8, "Closed"), issue("B", 6, 13, "Aceitação PO")],
                                      fim="2026-10-26T02:59:00Z")}
        with PastaDeDados(sprints) as dados:
            r2 = processo.indicadores_por_release(dados.caminho, MODO_ENTREGUES)["R2"]

        self.assertEqual(r2["indicadores"]["P2"], 1.0)

    def test_sem_a_coluna_coletada_os_dois_modos_dao_o_mesmo_p2(self):
        sprints = {"Sprint 3": sprint(21, 8, [issue("A", 5, 8), issue("B", 6, 13)], fim="2026-10-26T02:59:00Z")}
        with PastaDeDados(sprints) as dados:
            aceitas = processo.indicadores_por_release(dados.caminho, MODO_ACEITAS)["R2"]
            entregues = processo.indicadores_por_release(dados.caminho, MODO_ENTREGUES)["R2"]

        self.assertEqual(aceitas["indicadores"]["P2"], entregues["indicadores"]["P2"])

    def test_lista_manual_so_vale_sem_a_coluna(self):
        sprints = {"Sprint 3": sprint(21, 0, [issue("A", 5, 13), issue("B", 6, 8)], fim="2026-10-26T02:59:00Z")}
        with PastaDeDados(sprints, manual={"issues": [5]}) as dados:
            r2 = processo.indicadores_por_release(dados.caminho, MODO_ENTREGUES)["R2"]

        self.assertEqual(r2["pontos_em_aceitacao"], 13.0)
        self.assertAlmostEqual(r2["indicadores"]["P2"], 13 / 21)


class SprintsDoDashboardTest(unittest.TestCase):
    def carregar(self, dados):
        with mock.patch.object(data_layer, "RAW_DATA_DIR", dados.caminho):
            return data_layer.get_zenhub_sprints_data()

    def test_cada_sprint_traz_os_pontos_em_aceitacao_sem_dupla_contagem(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            lista, mock_ = self.carregar(dados)

        self.assertFalse(mock_)
        self.assertEqual([s["aguardando_pontos"] for s in lista], [0.0, 21.0])
        self.assertEqual([i["numero"] for i in lista[1]["aguardando_issues"]], [5, 7])
        self.assertEqual({s["aceitacao_fonte"] for s in lista}, {"zenhub"})

    def test_os_pontos_aceitos_continuam_separados(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            lista, _ = self.carregar(dados)

        self.assertEqual([s["delivered_sp"] for s in lista], [0.0, 0.0])

    def test_sem_a_coluna_a_fonte_fica_vazia(self):
        sprints = {"Sprint 3": sprint(21, 0, [issue("A", 5, 13)])}
        with PastaDeDados(sprints) as dados:
            lista, _ = self.carregar(dados)

        self.assertIsNone(lista[0]["aceitacao_fonte"])
        self.assertEqual(lista[0]["aguardando_pontos"], 0.0)

    def test_coluna_lida_e_vazia_nao_vira_aviso_de_nao_coletada(self):
        sprints = {"Sprint 3": sprint(21, 0, [issue("A", 5, 13, "Em andamento")])}
        with PastaDeDados(sprints) as dados:
            dados.gravar("zenhub_analytics.json", {"colunas_coletadas": True, "sprints_velocity": sprints})
            lista, _ = self.carregar(dados)
            do_processo = processo.sprints(dados.caminho, MODO_ENTREGUES)

        self.assertEqual(lista[0]["aceitacao_fonte"], "zenhub")
        self.assertEqual(lista[0]["aguardando_pontos"], 0.0)
        self.assertEqual(do_processo[0]["aceitacao_fonte"], "zenhub")

    def test_o_sinal_de_nao_coletada_do_json_chega_ao_painel_e_ao_processo(self):
        sprints = {"Sprint 3": sprint(21, 0, [issue("A", 5, 13, "Aceitação PO")])}
        with PastaDeDados(sprints) as dados:
            dados.gravar("zenhub_analytics.json", {"colunas_coletadas": False, "sprints_velocity": sprints})
            lista, _ = self.carregar(dados)
            do_processo = processo.sprints(dados.caminho, MODO_ENTREGUES)

        self.assertIsNone(lista[0]["aceitacao_fonte"])
        self.assertIsNone(do_processo[0]["aceitacao_fonte"])

    def test_lista_manual_marca_as_historias_quando_a_coleta_nao_trouxe_a_coluna(self):
        sprints = {"Sprint 3": sprint(21, 0, [issue("A", 5, 13), issue("B", 6, 8)])}
        with PastaDeDados(sprints, manual={"issues": [6]}) as dados:
            lista, _ = self.carregar(dados)

        self.assertEqual(lista[0]["aguardando_pontos"], 8.0)
        self.assertEqual(lista[0]["aceitacao_fonte"], "manual")

    def test_dados_de_exemplo_nao_inventam_historias_em_aceitacao(self):
        with tempfile.TemporaryDirectory() as vazia:
            with mock.patch.object(data_layer, "RAW_DATA_DIR", vazia):
                lista, mock_ = data_layer.get_zenhub_sprints_data()

        self.assertTrue(mock_)
        self.assertTrue(all(s["aguardando_pontos"] == 0.0 and s["aceitacao_fonte"] is None for s in lista))

    def test_o_modo_chega_aos_indicadores_de_processo_da_aba(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            aceitas = data_layer.get_qrapids_data(dados.caminho, MODO_ACEITAS)
            entregues = data_layer.get_qrapids_data(dados.caminho, MODO_ENTREGUES)

        self.assertEqual(aceitas["processo"]["R2"]["indicadores"]["P2"], 0.0)
        self.assertEqual(entregues["processo"]["R2"]["indicadores"]["P2"], 0.5)


if __name__ == "__main__":
    unittest.main()
