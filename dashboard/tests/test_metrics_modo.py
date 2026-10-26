"""
Testes do EVM por release nos dois modos de pontos entregues (src/metrics.py): só as
histórias aceitas ou também as que estão em Aceitação PO.

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import unittest
from datetime import date

from src import aceitacao
from src.config import MODO_ACEITAS, MODO_ENTREGUES, MODO_PADRAO
from src.metrics import compute_release_evm

RELEASES = [
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26", "bac_brl": 10000.0},
]
HOJE = date(2026, 10, 12)  # metade da release: 14 de 28 dias


def issue(id_, numero, estimativa, coluna):
    return {"id": id_, "numero": numero, "estimativa": estimativa, "coluna": coluna}


def sprint(nome, fim, aceitos, total, *issues):
    return {
        "name": nome,
        "delivered_sp": aceitos,
        "total_points": total,
        "start_at": "2026-09-28T03:59:00Z",
        "end_at": fim,
        "issues": list(issues),
        "issues_total": len(issues),
    }


def release(sprints, modo, hoje=HOJE):
    aceitacao.marcar_aguardando(sprints)
    return compute_release_evm(sprints, RELEASES, hoje=hoje, modo=modo)["releases"][0]


def duas_sprints():
    """Sprint 2: 8 aceitos e 13 em aceitação. Sprint 3: mais 5 em aceitação. PRP = 8 + 13 + 5 + 14 = 40."""
    return [
        sprint("Sprint 2", "2026-10-12T02:59:00Z", 8.0, 21.0,
               issue("A", 1, 8, "Closed"), issue("B", 2, 13, "Aceitação PO")),
        sprint("Sprint 3", "2026-10-26T02:59:00Z", 0.0, 19.0,
               issue("B", 2, 13, "Aceitação PO"), issue("C", 3, 5, "Aceitação PO"), issue("D", 4, 14, "Em andamento")),
    ]


class RpcPorModoTest(unittest.TestCase):
    def test_modo_aceitas_conta_so_os_pontos_aceitos(self):
        r = release(duas_sprints(), MODO_ACEITAS)

        self.assertEqual(r["rpc"], 8.0)
        self.assertEqual(r["rpc_aceito"], 8.0)
        self.assertEqual(r["rpc_aguardando"], 18.0)

    def test_modo_entregues_soma_os_pontos_em_aceitacao(self):
        r = release(duas_sprints(), MODO_ENTREGUES)

        self.assertEqual(r["rpc"], 26.0)
        self.assertEqual(r["rpc_aceito"], 8.0)
        self.assertEqual(r["rpc_aguardando"], 18.0)

    def test_historia_que_passa_de_sprint_nao_e_somada_duas_vezes(self):
        r = release(duas_sprints(), MODO_ENTREGUES)

        # A #2 (13 SP) está nas duas sprints e conta uma vez: 13 + 5 = 18, e não 31.
        self.assertEqual(r["rpc_aguardando"], 18.0)

    def test_o_prp_nao_muda_com_o_modo(self):
        aceitas = release(duas_sprints(), MODO_ACEITAS)
        entregues = release(duas_sprints(), MODO_ENTREGUES)

        self.assertEqual(aceitas["prp"], entregues["prp"])

    def test_o_modo_fica_registrado_no_resultado(self):
        self.assertEqual(release(duas_sprints(), MODO_ACEITAS)["modo"], MODO_ACEITAS)
        self.assertEqual(release(duas_sprints(), MODO_ENTREGUES)["modo"], MODO_ENTREGUES)


class IndicadoresPorModoTest(unittest.TestCase):
    def test_com_nada_aceito_o_modo_entregues_tira_o_ev_e_o_spi_de_zero(self):
        sprints = [sprint("Sprint 3", "2026-10-26T02:59:00Z", 0.0, 40.0,
                          issue("A", 1, 20, "Aceitação PO"), issue("B", 2, 20, "Em andamento"))]

        aceitas = release([dict(s) for s in sprints], MODO_ACEITAS)
        entregues = release([dict(s) for s in sprints], MODO_ENTREGUES)

        self.assertEqual((aceitas["ev"], aceitas["spi"]), (0.0, 0.0))
        self.assertAlmostEqual(entregues["apc"], 0.5)
        self.assertEqual(entregues["ev"], 5000.0)
        self.assertEqual(entregues["spi"], 1.0)

    def test_apc_nao_passa_de_100_por_cento(self):
        sprints = [sprint("Sprint 3", "2026-10-26T02:59:00Z", 30.0, 30.0, issue("A", 1, 20, "Aceitação PO"))]

        r = release(sprints, MODO_ENTREGUES)

        self.assertEqual(r["apc"], 1.0)

    def test_sem_a_coluna_coletada_os_dois_modos_dao_o_mesmo_resultado(self):
        def sem_coluna():
            return [sprint("Sprint 3", "2026-10-26T02:59:00Z", 8.0, 40.0,
                           {"id": "A", "numero": 1, "estimativa": 8}, {"id": "B", "numero": 2, "estimativa": 13})]

        aceitas = release(sem_coluna(), MODO_ACEITAS)
        entregues = release(sem_coluna(), MODO_ENTREGUES)

        self.assertIsNone(entregues["aceitacao_fonte"])
        self.assertEqual((aceitas["rpc"], aceitas["ev"]), (entregues["rpc"], entregues["ev"]))


class SerieEListaPorModoTest(unittest.TestCase):
    def test_a_serie_acumula_os_aceitos_e_os_entregues_por_sprint(self):
        serie = release(duas_sprints(), MODO_ENTREGUES)["serie"]

        self.assertEqual([p["aceito_acum"] for p in serie], [8.0, 8.0])
        self.assertEqual([p["entregue_acum"] for p in serie], [8.0, 26.0])

    def test_no_modo_aceitas_a_serie_entregue_acompanha_os_aceitos(self):
        serie = release(duas_sprints(), MODO_ACEITAS)["serie"]

        self.assertEqual([p["entregue_acum"] for p in serie], [8.0, 8.0])

    def test_o_burndown_restante_segue_o_modo(self):
        serie = release(duas_sprints(), MODO_ENTREGUES)["serie"]

        self.assertEqual(serie[-1]["restante"], max(40.0 - 26.0, 0.0))

    def test_lista_as_historias_em_aceitacao_da_release_uma_vez_cada(self):
        r = release(duas_sprints(), MODO_ACEITAS)

        self.assertEqual(sorted(h["numero"] for h in r["em_aceitacao"]), [2, 3])
        self.assertEqual(r["aceitacao_fonte"], aceitacao.FONTE_ZENHUB)

    def test_tabela_de_auditoria_separa_aceitos_de_em_aceitacao(self):
        sprints = duas_sprints()
        aceitacao.marcar_aguardando(sprints)
        auditoria = compute_release_evm(sprints, RELEASES, hoje=HOJE, modo=MODO_ENTREGUES)["audit_df"]

        linha = auditoria.iloc[0]
        self.assertEqual(linha["RPC aceito (SP)"], "8.0")
        self.assertEqual(linha["Em aceitação (SP)"], "18.0")
        self.assertEqual(linha["RPC considerado (SP)"], "26.0")


class ModoPadraoTest(unittest.TestCase):
    def test_o_padrao_conta_so_as_historias_aceitas(self):
        self.assertEqual(MODO_PADRAO, MODO_ACEITAS)

    def test_sem_escolher_o_modo_os_pontos_em_aceitacao_ficam_fora(self):
        sprints = duas_sprints()
        aceitacao.marcar_aguardando(sprints)

        r = compute_release_evm(sprints, RELEASES, hoje=HOJE)["releases"][0]

        self.assertEqual(r["rpc"], 8.0)
        self.assertEqual(r["rpc_aguardando"], 18.0)


if __name__ == "__main__":
    unittest.main()
