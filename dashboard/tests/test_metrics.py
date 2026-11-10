import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import MODO_ENTREGUES  # noqa: E402
from src.metrics import classificar_indice, compute_release_evm, pontos_distintos  # noqa: E402

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


DUAS_RELEASES = [
    {"id": "R1", "nome": "Release 1", "inicio": "2026-08-10", "fim": "2026-09-28", "bac_brl": 20000.0},
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26", "bac_brl": 10000.0},
]


def sprint_aguardando(nome, fim, aguardando, total):
    s = sprint(nome, fim, total=total)
    s["aguardando_pontos"] = aguardando
    return s


class ClassificarIndiceTest(unittest.TestCase):
    def test_usa_os_limites_do_plano_de_custos(self):
        # Adequado a partir de 0,90, Atenção de 0,80 a 0,89 e Crítico abaixo de 0,80.
        self.assertEqual(classificar_indice(1.2), "Adequado")
        self.assertEqual(classificar_indice(0.90), "Adequado")
        self.assertEqual(classificar_indice(0.89), "Atenção")
        self.assertEqual(classificar_indice(0.80), "Atenção")
        self.assertEqual(classificar_indice(0.79), "Crítico")
        self.assertEqual(classificar_indice(0.0), "Crítico")

    def test_sem_valor_nao_tem_estado(self):
        self.assertIsNone(classificar_indice(None))


class CurvaDeCustoTest(unittest.TestCase):
    def setUp(self):
        self.sprints = [
            sprint("Sprint 1", "2026-09-13T02:59:00Z", entregues=10, total=10),
            sprint("Sprint 2", "2026-09-27T02:59:00Z", entregues=10, total=10),
            sprint("Sprint 3", "2026-10-11T02:59:00Z", entregues=5, total=10),
        ]

    def curva(self, hoje, sprints=None, modo=None):
        argumentos = {} if modo is None else {"modo": modo}
        return compute_release_evm(
            self.sprints if sprints is None else sprints, DUAS_RELEASES, hoje=hoje, **argumentos)["curva"]

    def test_comeca_no_inicio_do_projeto_e_termina_hoje(self):
        curva = self.curva(date(2026, 10, 20))

        self.assertEqual(curva[0]["data"], date(2026, 8, 10))
        self.assertEqual(curva[-1]["data"], date(2026, 10, 20))
        self.assertEqual([p["data"] for p in curva], sorted({p["data"] for p in curva}))

    def test_inclui_os_marcos_das_releases(self):
        datas = {p["data"] for p in self.curva(date(2026, 10, 20))}

        self.assertIn(date(2026, 9, 28), datas)
        self.assertIn(date(2026, 9, 29), datas)

    def test_pv_nunca_diminui_e_o_ac_estimado_e_igual_ao_pv(self):
        curva = self.curva(date(2026, 10, 20))

        pvs = [p["pv"] for p in curva]
        self.assertEqual(pvs, sorted(pvs))
        for ponto in curva:
            self.assertEqual(ponto["ac"], ponto["pv"])

    def test_no_fim_de_uma_release_o_pv_acumulado_e_o_bac_dela(self):
        curva = {p["data"]: p for p in self.curva(date(2026, 10, 20))}

        self.assertEqual(curva[date(2026, 9, 28)]["pv"], 20000.0)

    def test_no_dia_de_hoje_bate_com_a_soma_dos_pv_das_releases(self):
        hoje = date(2026, 10, 20)
        resultado = compute_release_evm(self.sprints, DUAS_RELEASES, hoje=hoje)

        ultimo = resultado["curva"][-1]

        self.assertAlmostEqual(ultimo["pv"], sum(r["pv"] for r in resultado["releases"]), places=2)
        self.assertAlmostEqual(ultimo["ev"], sum(r["ev"] for r in resultado["releases"]), places=2)

    def test_o_ev_so_sobe_quando_a_sprint_termina(self):
        curva = {p["data"]: p for p in self.curva(date(2026, 10, 20))}

        # R1 tem PRP 20 e entregou 10 na Sprint 1 (fim em 12/09) e mais 10 na Sprint 2 (fim em 26/09).
        self.assertEqual(curva[date(2026, 9, 7)]["ev"], 0.0)
        self.assertEqual(curva[date(2026, 9, 28)]["ev"], 20000.0)

    def test_sem_historia_aceita_o_ev_fica_em_zero_o_tempo_todo(self):
        sem_aceite = [sprint("Sprint 1", "2026-09-13T02:59:00Z", total=10)]

        curva = self.curva(date(2026, 10, 20), sprints=sem_aceite)

        self.assertTrue(all(p["ev"] == 0.0 for p in curva))
        self.assertGreater(curva[-1]["pv"], 0)

    def test_modo_entregues_soma_o_que_esta_em_aceitacao(self):
        em_aceitacao = [sprint_aguardando("Sprint 1", "2026-09-13T02:59:00Z", aguardando=10, total=20)]

        so_aceitas = self.curva(date(2026, 10, 20), sprints=em_aceitacao)
        com_aguardando = self.curva(date(2026, 10, 20), sprints=em_aceitacao, modo=MODO_ENTREGUES)

        self.assertEqual(so_aceitas[-1]["ev"], 0.0)
        self.assertEqual(com_aguardando[-1]["ev"], 10000.0)

    def test_sprint_em_andamento_com_pontos_conta_no_dia_de_hoje(self):
        # A Sprint 4 só termina em 25/10 (Brasília), mas os cartões já contam o que ela entregou.
        em_andamento = [sprint("Sprint 4", "2026-10-26T02:59:00Z", entregues=5, total=10)]
        hoje = date(2026, 10, 20)
        resultado = compute_release_evm(em_andamento, DUAS_RELEASES, hoje=hoje)

        curva = resultado["curva"]

        self.assertEqual(curva[-1]["data"], hoje)
        self.assertEqual(curva[-1]["ev"], 5000.0)
        self.assertAlmostEqual(curva[-1]["ev"], sum(r["ev"] or 0.0 for r in resultado["releases"]), places=2)

    def test_sprint_em_andamento_nao_adianta_o_ev_dos_dias_anteriores(self):
        em_andamento = [sprint("Sprint 4", "2026-10-26T02:59:00Z", entregues=5, total=10)]

        curva = self.curva(date(2026, 10, 20), sprints=em_andamento)

        self.assertTrue(all(p["ev"] == 0.0 for p in curva[:-1]))

    def test_modo_entregues_soma_na_curva_a_aceitacao_de_uma_sprint_em_andamento(self):
        # O caso da R3: pontos em Aceitação PO numa sprint que ainda não terminou.
        em_aceitacao = [sprint_aguardando("Sprint 4", "2026-10-26T02:59:00Z", aguardando=10, total=10)]
        hoje = date(2026, 10, 20)

        resultado = compute_release_evm(em_aceitacao, DUAS_RELEASES, hoje=hoje, modo=MODO_ENTREGUES)

        self.assertEqual(resultado["curva"][-1]["ev"], 10000.0)
        self.assertAlmostEqual(
            resultado["curva"][-1]["ev"], sum(r["ev"] or 0.0 for r in resultado["releases"]), places=2)

    def test_sprint_encerrada_continua_contando_na_data_em_que_terminou(self):
        curva = {p["data"]: p for p in self.curva(date(2026, 10, 20))}

        # A Sprint 1 termina em 12/09; antes disso o EV continua em zero, e depois dela sobe.
        self.assertEqual(curva[date(2026, 9, 7)]["ev"], 0.0)
        self.assertGreater(curva[date(2026, 9, 14)]["ev"], 0.0)

    def test_antes_do_inicio_do_projeto_nao_ha_curva(self):
        self.assertEqual(self.curva(date(2026, 8, 1)), [])

    def test_release_futura_nao_entra_no_valor_planejado(self):
        curva = {p["data"]: p for p in self.curva(date(2026, 9, 20))}

        self.assertLess(curva[date(2026, 9, 20)]["pv"], 20000.0)

    def test_o_orcamento_acumulado_soma_os_bac_ate_a_release(self):
        resultado = compute_release_evm(self.sprints, DUAS_RELEASES, hoje=date(2026, 10, 20))

        acumulado = {r["id"]: r["orcamento_acumulado"] for r in resultado["releases"]}

        self.assertEqual(acumulado, {"R1": 20000.0, "R2": 30000.0})


if __name__ == "__main__":
    unittest.main()
