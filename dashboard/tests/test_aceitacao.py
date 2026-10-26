"""
Testes das histórias que aguardam o aceite do PO (src/aceitacao.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import unittest

from src import aceitacao
from src.config import MODO_ACEITAS, MODO_ENTREGUES


def issue(id_, numero, estimativa, coluna=None):
    resultado = {"id": id_, "numero": numero, "estimativa": estimativa}
    if coluna is not None:
        resultado["coluna"] = coluna
    return resultado


def sprint(nome, *issues):
    return {"name": nome, "issues": list(issues)}


class MarcarAguardandoTest(unittest.TestCase):
    def test_soma_so_as_historias_da_coluna_aceitacao_po(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5, "Aceitação PO"), issue("B", 8, 8, "Em andamento"),
                          issue("C", 9, 3, "Closed"))]

        fonte = aceitacao.marcar_aguardando(sprints)

        self.assertEqual(fonte, aceitacao.FONTE_ZENHUB)
        self.assertEqual(sprints[0]["aguardando_pontos"], 5.0)
        self.assertEqual([i["numero"] for i in sprints[0]["aguardando_issues"]], [7])

    def test_reconhece_a_coluna_sem_depender_de_acento_caixa_ou_espaco(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5, "aceitacao po"), issue("B", 8, 2, "  ACEITAÇÃO   PO "))]

        aceitacao.marcar_aguardando(sprints)

        self.assertEqual(sprints[0]["aguardando_pontos"], 7.0)

    def test_historia_que_passa_de_sprint_conta_uma_vez_na_ultima_sprint(self):
        sprints = [
            sprint("Sprint 2", issue("A", 7, 5, "Aceitação PO"), issue("B", 8, 8, "Aceitação PO")),
            sprint("Sprint 3", issue("A", 7, 5, "Aceitação PO")),
        ]

        aceitacao.marcar_aguardando(sprints)

        self.assertEqual(sprints[0]["aguardando_pontos"], 8.0)
        self.assertEqual(sprints[1]["aguardando_pontos"], 5.0)
        self.assertEqual(sum(s["aguardando_pontos"] for s in sprints), 13.0)

    def test_usa_a_estimativa_da_ultima_sprint(self):
        sprints = [sprint("Sprint 2", issue("A", 7, 3, "Aceitação PO")),
                   sprint("Sprint 3", issue("A", 7, 8, "Aceitação PO"))]

        aceitacao.marcar_aguardando(sprints)

        self.assertEqual(sum(s["aguardando_pontos"] for s in sprints), 8.0)

    def test_item_sem_estimativa_nao_conta_como_historia(self):
        sprints = [sprint("Sprint 3", issue("A", 7, None, "Aceitação PO"), issue("B", 8, 0, "Aceitação PO"),
                          issue("C", 9, 5, "Aceitação PO"))]

        fonte = aceitacao.marcar_aguardando(sprints)

        self.assertEqual(fonte, aceitacao.FONTE_ZENHUB)
        self.assertEqual([i["numero"] for i in sprints[0]["aguardando_issues"]], [9])
        self.assertEqual(sprints[0]["aguardando_pontos"], 5.0)

    def test_pull_requests_na_coluna_nao_entram_na_contagem(self):
        sprints = [sprint("Sprint 3", issue("A", 5, 13, "Aceitação PO"), issue("P1", 69, None, "Aceitação PO"),
                          issue("P2", 70, None, "Aceitação PO"))]

        aceitacao.marcar_aguardando(sprints)

        self.assertEqual(len(sprints[0]["aguardando_issues"]), 1)
        self.assertEqual(sprints[0]["aguardando_pontos"], 13.0)

    def test_lista_manual_tambem_ignora_o_que_nao_tem_estimativa(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5), issue("B", 7, None))]

        aceitacao.marcar_aguardando(sprints, manual={7})

        self.assertEqual([i["id"] for i in sprints[0]["aguardando_issues"]], ["A"])

    def test_sem_coluna_coletada_nada_e_marcado_e_a_fonte_fica_vazia(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5), issue("B", 8, 8))]

        fonte = aceitacao.marcar_aguardando(sprints)

        self.assertIsNone(fonte)
        self.assertEqual(sprints[0]["aguardando_pontos"], 0.0)
        self.assertIsNone(sprints[0]["aceitacao_fonte"])

    def test_sprint_sem_detalhe_de_issues_fica_com_zero(self):
        sprints = [{"name": "Sprint 1"}, {"name": "Sprint 2", "issues": None}]

        aceitacao.marcar_aguardando(sprints)

        self.assertTrue(all(s["aguardando_pontos"] == 0.0 and s["aguardando_issues"] == [] for s in sprints))

    def test_lista_manual_vale_so_quando_a_coleta_nao_trouxe_a_coluna(self):
        sem_coluna = [sprint("Sprint 3", issue("A", 7, 5), issue("B", 8, 8))]
        com_coluna = [sprint("Sprint 3", issue("A", 7, 5, "Em andamento"), issue("B", 8, 8, "Aceitação PO"))]

        fonte_manual = aceitacao.marcar_aguardando(sem_coluna, manual={7})
        fonte_zenhub = aceitacao.marcar_aguardando(com_coluna, manual={7})

        self.assertEqual(fonte_manual, aceitacao.FONTE_MANUAL)
        self.assertEqual(sem_coluna[0]["aguardando_pontos"], 5.0)
        self.assertEqual(fonte_zenhub, aceitacao.FONTE_ZENHUB)
        self.assertEqual(com_coluna[0]["aguardando_pontos"], 8.0)

    def test_usa_o_numero_quando_a_issue_nao_tem_id(self):
        sprints = [sprint("Sprint 2", issue(None, 7, 5, "Aceitação PO")),
                   sprint("Sprint 3", issue(None, 7, 5, "Aceitação PO"))]

        aceitacao.marcar_aguardando(sprints)

        self.assertEqual(sum(s["aguardando_pontos"] for s in sprints), 5.0)

    def test_registra_em_que_sprint_cada_historia_conta(self):
        sprints = [sprint("Sprint 2", issue("A", 7, 5, "Aceitação PO")), sprint("Sprint 3")]

        aceitacao.marcar_aguardando(sprints)

        self.assertEqual(sprints[0]["aguardando_issues"][0]["sprint"], "Sprint 2")

    def test_aceita_outras_colunas_configuradas(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5, "Revisão"), issue("B", 8, 8, "Aceitação PO"))]

        aceitacao.marcar_aguardando(sprints, colunas=("Revisão",))

        self.assertEqual(sprints[0]["aguardando_pontos"], 5.0)


class SinalDeColetaTest(unittest.TestCase):
    def test_coluna_lida_e_vazia_e_zero_medido_e_nao_dado_ausente(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5, "Em andamento"), issue("B", 8, 8, "Em andamento"))]

        fonte = aceitacao.marcar_aguardando(sprints, coletada=True)

        self.assertEqual(fonte, aceitacao.FONTE_ZENHUB)
        self.assertEqual(sprints[0]["aguardando_pontos"], 0.0)

    def test_coluna_lida_mas_sem_nenhuma_issue_com_coluna_tambem_e_zero_medido(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5), issue("B", 8, 8))]

        fonte = aceitacao.marcar_aguardando(sprints, coletada=True)

        self.assertEqual(fonte, aceitacao.FONTE_ZENHUB)

    def test_o_sinal_de_nao_coletada_vale_mais_que_a_inferencia(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5, "Aceitação PO"))]

        fonte = aceitacao.marcar_aguardando(sprints, coletada=False)

        self.assertIsNone(fonte)
        self.assertEqual(sprints[0]["aguardando_pontos"], 0.0)

    def test_nao_coletada_com_lista_manual_usa_a_lista(self):
        sprints = [sprint("Sprint 3", issue("A", 7, 5), issue("B", 8, 8))]

        fonte = aceitacao.marcar_aguardando(sprints, manual={8}, coletada=False)

        self.assertEqual(fonte, aceitacao.FONTE_MANUAL)
        self.assertEqual(sprints[0]["aguardando_pontos"], 8.0)

    def test_sem_o_sinal_a_coluna_e_inferida_pelas_issues(self):
        com = [sprint("Sprint 3", issue("A", 7, 5, "Aceitação PO"))]
        sem = [sprint("Sprint 3", issue("A", 7, 5))]

        self.assertEqual(aceitacao.marcar_aguardando(com), aceitacao.FONTE_ZENHUB)
        self.assertIsNone(aceitacao.marcar_aguardando(sem))


class PontosEntreguesTest(unittest.TestCase):
    def test_modo_aceitas_ignora_os_pontos_em_aceitacao(self):
        self.assertEqual(aceitacao.pontos_entregues(10, 5, MODO_ACEITAS), 10.0)

    def test_modo_entregues_soma_os_pontos_em_aceitacao(self):
        self.assertEqual(aceitacao.pontos_entregues(10, 5, MODO_ENTREGUES), 15.0)

    def test_sem_nada_aceito_o_modo_entregues_mostra_so_o_que_aguarda(self):
        self.assertEqual(aceitacao.pontos_entregues(0, 13, MODO_ENTREGUES), 13.0)
        self.assertEqual(aceitacao.pontos_entregues(0, 13, MODO_ACEITAS), 0.0)


class NumerosManuaisTest(unittest.TestCase):
    def test_le_a_lista_de_numeros(self):
        self.assertEqual(aceitacao.numeros_manuais({"issues": [7, 8]}), {7, 8})

    def test_ignora_o_que_nao_e_numero_de_issue(self):
        self.assertEqual(aceitacao.numeros_manuais({"issues": [7, "8", True, None, 9.5]}), {7})

    def test_formato_invalido_ou_lista_vazia_vira_none(self):
        for dados in (None, [], {"issues": "7"}, {"outra": [7]}, {"issues": []}):
            self.assertIsNone(aceitacao.numeros_manuais(dados))


if __name__ == "__main__":
    unittest.main()
