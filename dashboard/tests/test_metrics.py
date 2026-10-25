import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metrics import compute_release_evm, pontos_distintos  # noqa: E402

RELEASES = [
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26", "bac_brl": 10000.0},
]


def issue(id_, estimativa):
    return {"id": id_, "numero": 1, "estimativa": estimativa}


def sprint(nome, fim, entregues=0.0, total=0.0, issues=None, issues_total=None):
    s = {
        "name": nome,
        "delivered_sp": entregues,
        "total_points": total,
        "start_at": "2026-09-28T03:59:00Z",
        "end_at": fim,
    }
    if issues is not None:
        s["issues"] = issues
        s["issues_total"] = len(issues) if issues_total is None else issues_total
    return s


class PontosDistintosTest(unittest.TestCase):
    def test_historia_repetida_entre_sprints_conta_uma_vez(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21, issues=[issue("A", 13), issue("B", 8)]),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21, issues=[issue("A", 13), issue("C", 8)]),
        ]

        pontos, aproximado = pontos_distintos(sprints)

        self.assertEqual(pontos, 29)
        self.assertFalse(aproximado)

    def test_usa_a_estimativa_da_ultima_sprint_em_que_a_historia_aparece(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", issues=[issue("A", 5)]),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", issues=[issue("A", 8)]),
        ]

        self.assertEqual(pontos_distintos(sprints), (8, False))

    def test_issue_sem_estimativa_vale_zero(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", issues=[issue("A", None), issue("B", 3)]),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", issues=[issue("C", 2)]),
        ]

        self.assertEqual(pontos_distintos(sprints), (5, False))

    def test_sem_detalhe_soma_o_total_e_marca_como_aproximado(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21),
        ]

        self.assertEqual(pontos_distintos(sprints), (42, True))

    def test_detalhe_em_so_uma_das_sprints_e_aproximado(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21, issues=[issue("A", 13)]),
        ]

        self.assertEqual(pontos_distintos(sprints), (42, True))

    def test_lista_truncada_pela_api_e_aproximada(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21, issues=[issue("A", 13)], issues_total=150),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21, issues=[issue("B", 8)]),
        ]

        self.assertEqual(pontos_distintos(sprints), (42, True))

    def test_issue_sem_id_e_aproximado(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21, issues=[issue(None, 13)]),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21, issues=[issue("B", 8)]),
        ]

        self.assertEqual(pontos_distintos(sprints), (42, True))

    def test_uma_sprint_so_usa_o_total_e_e_exata(self):
        sprints = [sprint("Sprint 3", "2026-10-26T02:59:00Z", total=69)]

        self.assertEqual(pontos_distintos(sprints), (69, False))

    def test_sem_sprints_o_prp_e_zero(self):
        self.assertEqual(pontos_distintos([]), (0.0, False))


class ReleaseEvmTest(unittest.TestCase):
    def test_prp_da_release_nao_dobra_as_historias_que_atravessam_sprints(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21, issues=[issue("A", 13), issue("B", 8)]),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", entregues=8, total=21,
                   issues=[issue("A", 13), issue("B", 8)]),
        ]

        r = compute_release_evm(sprints, RELEASES, hoje=date(2026, 10, 20))["releases"][0]

        self.assertEqual(r["prp"], 21)
        self.assertFalse(r["prp_aproximado"])
        self.assertAlmostEqual(r["apc"], 8 / 21)

    def test_rpc_continua_a_soma_dos_pontos_entregues(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", entregues=5, issues=[issue("A", 13)]),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", entregues=8, issues=[issue("A", 13)]),
        ]

        r = compute_release_evm(sprints, RELEASES, hoje=date(2026, 10, 20))["releases"][0]

        self.assertEqual(r["rpc"], 13)

    def test_sem_detalhe_o_resultado_marca_prp_aproximado(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21),
        ]

        r = compute_release_evm(sprints, RELEASES, hoje=date(2026, 10, 20))["releases"][0]

        self.assertEqual(r["prp"], 42)
        self.assertTrue(r["prp_aproximado"])

    def test_tabela_de_auditoria_indica_prp_aproximado(self):
        sprints = [
            sprint("Sprint 2", "2026-10-12T02:59:00Z", total=21),
            sprint("Sprint 3", "2026-10-26T02:59:00Z", total=21),
        ]

        tabela = compute_release_evm(sprints, RELEASES, hoje=date(2026, 10, 20))["audit_df"]

        self.assertEqual(tabela.loc[0, "PRP (SP)"], "42.0 (aprox.)")

    def test_historias_sem_aceite_deixam_rpc_e_ev_em_zero(self):
        sprints = [sprint("Sprint 3", "2026-10-26T02:59:00Z", total=69)]

        r = compute_release_evm(sprints, RELEASES, hoje=date(2026, 10, 20))["releases"][0]

        self.assertEqual(r["rpc"], 0)
        self.assertEqual(r["ev"], 0)
        self.assertEqual(r["spi"], 0)


if __name__ == "__main__":
    unittest.main()
