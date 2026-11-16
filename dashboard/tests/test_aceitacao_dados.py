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
from datetime import date
from unittest import mock

from src import data_layer, metrics, processo
from src.config import MODO_ACEITAS, MODO_ENTREGUES, RELEASES


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

        # APC da release, como na aba de EVM: a #5 passa pelas duas sprints e entra uma vez no PRP
        # (13 + 8 + 8 = 29). Em aceitação, a #5 e a #7 somam 13 + 8 = 21 pontos entregues.
        self.assertAlmostEqual(r2["indicadores"]["P2"], 21 / 29)

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


def historia_fechada(id_, numero, estimativa, quando="2026-11-11T01:39:20Z"):
    return {"id": id_, "numero": numero, "estimativa": estimativa, "coluna": "Aceitação PO",
            "fechada": True, "fechada_em": quando}


# Sprint 4 entregou a #5 ao PO, que a aceitou já na Sprint 5; a #8 ainda espera o aceite.
SPRINTS_COM_ACEITE_TARDIO = {
    "Sprint 4": sprint(21, 0, [historia_fechada("A", 5, 13), issue("B", 8, 8, "Aceitação PO")],
                       inicio="2026-10-26T03:59:00Z", fim="2026-11-09T02:59:00Z"),
    "Sprint 5": sprint(21, 13, [historia_fechada("A", 5, 13), issue("B", 8, 8, "Aceitação PO")],
                       inicio="2026-11-09T03:59:00Z", fim="2026-11-23T02:59:00Z"),
}


class AceiteTardioNosDadosTest(unittest.TestCase):
    def test_o_painel_atribui_o_aceite_a_sprint_de_origem_e_nao_conta_a_historia_fechada_como_aguardando(self):
        with PastaDeDados(SPRINTS_COM_ACEITE_TARDIO) as dados:
            with mock.patch.object(data_layer, "RAW_DATA_DIR", dados.caminho):
                lista, _ = data_layer.get_zenhub_sprints_data()

        self.assertEqual([s["delivered_sp"] for s in lista], [13.0, 0.0])
        self.assertEqual([s["aguardando_pontos"] for s in lista], [8.0, 0.0])
        self.assertEqual([i["numero"] for i in lista[0]["aceitos_depois_issues"]], [5])

    def test_o_processo_atribui_o_aceite_a_sprint_de_origem(self):
        with PastaDeDados(SPRINTS_COM_ACEITE_TARDIO) as dados:
            lista = processo.sprints(dados.caminho, MODO_ENTREGUES)

        self.assertEqual([s["aceitos"] for s in lista], [13.0, 0.0])
        self.assertEqual([s["entregues"] for s in lista], [21.0, 0.0])
        self.assertEqual(lista[0]["aceitos_depois_pontos"], 13.0)

    def test_a_release_soma_o_mesmo_total_que_antes_da_atribuicao(self):
        with PastaDeDados(SPRINTS_COM_ACEITE_TARDIO) as dados:
            lista = processo.sprints(dados.caminho, MODO_ACEITAS)

        self.assertEqual(sum(s["aceitos"] for s in lista), 13.0)


class AceiteTardioPorReleaseTest(unittest.TestCase):
    """O caso real do projeto: o PO aceitou na Sprint 5 histórias que a equipe entregou em sprints anteriores."""

    DATAS = {
        "Sprint 1": ("2026-09-14T03:59:00Z", "2026-09-28T02:59:00Z"),
        "Sprint 2": ("2026-09-28T03:59:00Z", "2026-10-12T02:59:00Z"),
        "Sprint 3": ("2026-10-12T03:59:00Z", "2026-10-26T02:59:00Z"),
        "Sprint 4": ("2026-10-26T03:59:00Z", "2026-11-09T02:59:00Z"),
        "Sprint 5": ("2026-11-09T03:59:00Z", "2026-11-23T02:59:00Z"),
    }
    # (número, pontos, sprint em que foi cotada, aceita?)
    HISTORIAS = [
        (5, 13, 1, True), (6, 8, 1, True),
        (7, 8, 2, True), (21, 3, 2, True), (46, 8, 2, False),
        (8, 8, 3, True), (9, 8, 3, True), (11, 5, 3, True),
        (23, 8, 4, True),
    ]

    def sprints(self, tardias=()):
        """`tardias`: números das histórias aceitas em 16/11, que o ZenHub tirou da lista da Sprint 5."""
        resultado = {}
        for indice, (nome, (inicio, fim)) in enumerate(self.DATAS.items(), start=1):
            issues = []
            for numero, pontos, cotada, aceita in self.HISTORIAS:
                if indice < cotada or (nome == "Sprint 5" and numero in tardias):
                    continue
                historia = issue(f"US{numero}", numero, pontos, "Aceitação PO")
                fechada_em = "2026-11-16T03:07:00Z" if numero in tardias else "2026-11-11T01:39:20Z"
                issues.append({**historia, "fechada": aceita or numero in tardias,
                               "fechada_em": fechada_em if aceita or numero in tardias else None})
            # O ZenHub conta os pontos fechados na lista da Sprint 5, em que o PO aceitou, e o total
            # planejado de cada sprint é o acumulado de tudo que já foi cotado.
            aceitos = sum(p for n, p, _, ok in self.HISTORIAS if ok and n not in tardias) if nome == "Sprint 5" else 0
            planejados = sum(pontos for _, pontos, cotada, _ in self.HISTORIAS if cotada <= indice)
            resultado[nome] = sprint(planejados, aceitos, issues, inicio=inicio, fim=fim)
        return resultado

    def release(self, modo, tardias=()):
        with PastaDeDados(self.sprints(tardias)) as dados:
            with mock.patch.object(data_layer, "RAW_DATA_DIR", dados.caminho):
                lista, _ = data_layer.get_zenhub_sprints_data()
        evm = metrics.compute_release_evm(lista, RELEASES, date(2026, 11, 16), modo)
        return lista, {r["id"]: r for r in evm["releases"]}

    def test_cada_sprint_ganha_os_pontos_que_cotou(self):
        lista, _ = self.release(MODO_ACEITAS)

        pontos = {s["name"]: s["delivered_sp"] for s in lista}
        self.assertEqual([pontos[f"Sprint {n}"] for n in range(1, 6)], [21.0, 11.0, 21.0, 8.0, 0.0])
        self.assertEqual(sum(pontos.values()), 61.0)

    def test_cada_release_fica_com_os_pontos_das_historias_que_entregou(self):
        _, releases = self.release(MODO_ACEITAS)

        self.assertEqual(releases["R1"]["rpc"], 21.0)
        self.assertEqual(releases["R2"]["rpc"], 32.0)
        self.assertEqual(releases["R3"]["rpc"], 8.0)

    def test_historia_aceita_depois_de_sair_da_sprint_aberta_ainda_conta_na_release_de_origem(self):
        # A #8 e a #46 foram aceitas em 16/11 e o ZenHub as tirou da Sprint 5: ele não conta esses 16 pontos.
        lista, releases = self.release(MODO_ACEITAS, tardias=(8, 46))

        # 53 pontos que o ZenHub contou na Sprint 5, mais os 16 da #8 e da #46 que ele deixou de contar.
        self.assertEqual(sum(s["delivered_sp"] for s in lista), 69.0)
        self.assertEqual(releases["R2"]["rpc"], 40.0)
        self.assertEqual(releases["R2"]["apc"], 1.0)
        self.assertEqual(releases["R2"]["rpc_aguardando"], 0.0)

    def test_o_planejado_de_cada_release_conta_so_as_historias_cotadas_nela(self):
        _, releases = self.release(MODO_ACEITAS)

        # R1: #5 e #6. R2: #7, #21, #46, #8, #9 e #11, sem as duas da R1 que passam por ela. R3: #23.
        self.assertEqual([releases[r]["prp"] for r in ("R1", "R2", "R3")], [21.0, 40.0, 8.0])
        self.assertEqual(sum(r["prp"] for r in releases.values()), 69.0)

    def test_o_avanco_de_cada_release_usa_o_planejado_dela(self):
        _, aceitas = self.release(MODO_ACEITAS)
        _, entregues = self.release(MODO_ENTREGUES)

        self.assertEqual(aceitas["R1"]["apc"], 1.0)
        self.assertAlmostEqual(aceitas["R2"]["apc"], 32 / 40)
        self.assertEqual(entregues["R2"]["apc"], 1.0)

    def test_a_historia_que_ainda_espera_o_aceite_conta_na_release_em_que_foi_cotada(self):
        _, releases = self.release(MODO_ENTREGUES)

        self.assertEqual(releases["R2"]["rpc_aguardando"], 8.0)
        self.assertEqual(releases["R2"]["rpc"], 40.0)
        self.assertEqual(releases["R3"]["rpc_aguardando"], 0.0)
        self.assertEqual({i["numero"] for i in releases["R2"]["em_aceitacao"]}, {46})


class SprintsDoDashboardTest(unittest.TestCase):
    def carregar(self, dados):
        with mock.patch.object(data_layer, "RAW_DATA_DIR", dados.caminho):
            return data_layer.get_zenhub_sprints_data()

    def test_a_release_diz_se_a_coleta_trouxe_o_estado_das_issues(self):
        for fechada, esperado in ((None, False), (False, True)):
            issues = [issue("US8", 8, 8, "Aceitação PO")]
            if fechada is not None:
                issues = [{**i, "fechada": fechada} for i in issues]
            sprints = {"Sprint 5": sprint(8, 0, issues, fim="2026-11-23T02:59:00Z", inicio="2026-11-09T03:00:00Z")}
            with PastaDeDados(sprints) as dados:
                lista, _ = self.carregar(dados)
                evm = metrics.compute_release_evm(lista, RELEASES, date(2026, 11, 12), MODO_ENTREGUES)
            r3 = next(r for r in evm["releases"] if r["id"] == "R3")

            self.assertIs(r3["estado_coletado"], esperado)

    def test_json_com_fechadas_em_aceitacao_nao_duplica_o_rpc(self):
        aceitas = [(5, 13), (6, 8), (7, 8), (9, 8), (11, 5), (21, 3), (23, 8)]
        issues = [
            {**issue(f"US{numero}", numero, pontos, "Aceitação PO"), "fechada": True}
            for numero, pontos in aceitas
        ]
        issues += [
            {**issue(f"T{numero}", numero, pontos, "Closed"), "fechada": True}
            for numero, pontos in [(102, 3), (104, 13)]
        ]
        issues += [
            {**issue(f"US{numero}", numero, 8, "Aceitação PO"), "fechada": False}
            for numero in [8, 46]
        ]
        sprints = {"Sprint 5": sprint(85, 69, issues, fim="2026-11-23T02:59:00Z",
                                      inicio="2026-11-09T03:00:00Z")}
        with PastaDeDados(sprints) as dados:
            lista, exemplo = self.carregar(dados)
            evm = metrics.compute_release_evm(lista, RELEASES, date(2026, 11, 12), MODO_ENTREGUES)
        r3 = next(r for r in evm["releases"] if r["id"] == "R3")

        self.assertFalse(exemplo)
        self.assertEqual(r3["rpc_aceito"], 69.0)
        self.assertEqual(r3["rpc_aguardando"], 16.0)
        self.assertEqual(r3["rpc"], 85.0)
        self.assertEqual({i["numero"] for i in r3["em_aceitacao"]}, {8, 46})

    def test_cada_sprint_traz_os_pontos_em_aceitacao_sem_dupla_contagem(self):
        with PastaDeDados(SPRINTS_COM_COLUNA) as dados:
            lista, mock_ = self.carregar(dados)

        self.assertFalse(mock_)
        # A #5 passa pelas duas sprints e conta na Sprint 2, em que foi cotada; a #7 foi cotada na Sprint 3.
        self.assertEqual([s["aguardando_pontos"] for s in lista], [13.0, 8.0])
        self.assertEqual([i["numero"] for i in lista[0]["aguardando_issues"]], [5])
        self.assertEqual([i["numero"] for i in lista[1]["aguardando_issues"]], [7])
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

    def test_o_sinal_de_estado_coletado_chega_ao_painel_e_ao_processo(self):
        sem_estado = {"Sprint 3": sprint(21, 0, [issue("A", 5, 13, "Aceitação PO")])}
        com_estado = {"Sprint 3": sprint(21, 0, [{**issue("A", 5, 13, "Aceitação PO"), "fechada": False}])}

        for sprints, esperado in ((sem_estado, False), (com_estado, True)):
            with PastaDeDados(sprints) as dados:
                lista, _ = self.carregar(dados)
                do_processo = processo.sprints(dados.caminho, MODO_ENTREGUES)

            self.assertIs(lista[0]["estado_coletado"], esperado)
            self.assertIs(do_processo[0]["estado_coletado"], esperado)

    def test_dados_de_exemplo_nao_afirmam_estado_coletado(self):
        with tempfile.TemporaryDirectory() as vazia:
            with mock.patch.object(data_layer, "RAW_DATA_DIR", vazia):
                lista, _ = data_layer.get_zenhub_sprints_data()

        self.assertTrue(all(s["estado_coletado"] is False for s in lista))

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
        self.assertAlmostEqual(entregues["processo"]["R2"]["indicadores"]["P2"], 21 / 29)


if __name__ == "__main__":
    unittest.main()
