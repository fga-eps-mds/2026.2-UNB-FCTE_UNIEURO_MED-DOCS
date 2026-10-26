import json
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import FAIXAS_RISCO, RAW_DATA_DIR  # noqa: E402
from src.metrics import (  # noqa: E402
    classificar_risco,
    process_risks_summary,
    revisoes_realizadas,
    tabela_historico_riscos,
)

PLANO = os.path.join(os.path.dirname(RAW_DATA_DIR), "docs", "processo", "riscos.md")


def risco(id_, p, i):
    return {"id": id_, "titulo": "t", "categoria": "Técnico", "probabilidade": p, "impacto": i}


class EscalaUnicaTest(unittest.TestCase):
    def test_faixas_do_plano(self):
        self.assertEqual(classificar_risco(1), "Baixo")
        self.assertEqual(classificar_risco(5), "Baixo")
        self.assertEqual(classificar_risco(6), "Médio")
        self.assertEqual(classificar_risco(12), "Médio")
        self.assertEqual(classificar_risco(15), "Elevado")
        self.assertEqual(classificar_risco(25), "Elevado")

    def test_todo_produto_possivel_tem_grau(self):
        graus = {classificar_risco(p * i) for p in range(1, 6) for i in range(1, 6)}
        self.assertEqual(graus, {"Baixo", "Médio", "Elevado"})

    def test_plano_de_riscos_usa_as_mesmas_faixas(self):
        with open(PLANO, encoding="utf-8") as f:
            texto = f.read()
        for minimo, maximo, grau in FAIXAS_RISCO:
            self.assertIn(f"| {minimo} - {maximo} | {grau} |", texto)


class ResumoTest(unittest.TestCase):
    def test_marca_risco_concretizado(self):
        df = process_risks_summary([risco("R01", 3, 4), risco("R02", 4, 3)], [{"risco": "R02"}])
        self.assertEqual(df["Grau"].tolist(), ["Médio", "Médio"])
        self.assertEqual(df["Situação"].tolist(), ["Monitorado", "Concretizado"])


class HistoricoTest(unittest.TestCase):
    def test_descarta_sprint_futura_e_sem_data(self):
        revisoes = [
            {"sprint": "Sprint 2", "data": "2026-10-11", "riscos": {}},
            {"sprint": "Sprint 1", "data": "2026-09-27", "riscos": {}},
            {"sprint": "Sprint 8", "data": "2026-12-20", "riscos": {}},
            {"sprint": "Sprint X", "riscos": {}},
        ]
        nomes = [r["sprint"] for r in revisoes_realizadas(revisoes, hoje=date(2026, 10, 25))]
        self.assertEqual(nomes, ["Sprint 1", "Sprint 2"])

    def test_tabela_por_sprint(self):
        revisoes = [
            {"sprint": "Sprint 1", "data": "2026-09-27", "riscos": {"R02": {"probabilidade": 4, "impacto": 3}}},
            {"sprint": "Sprint 2", "data": "2026-10-11", "riscos": {"R02": {"probabilidade": 3, "impacto": 3}}},
        ]
        tabela = tabela_historico_riscos(revisoes)
        self.assertEqual(tabela.loc[0, "Sprint 1"], "4×3 = 12 (Médio)")
        self.assertEqual(tabela.loc[0, "Sprint 2"], "3×3 = 9 (Médio)")

    def test_arquivo_real_nao_tem_sprint_futura(self):
        with open(os.path.join(RAW_DATA_DIR, "riscos_historico.json"), encoding="utf-8") as f:
            dados = json.load(f)
        hoje = date.today()
        for rev in dados["revisoes"]:
            self.assertLessEqual(date.fromisoformat(rev["data"]), hoje, rev["sprint"])
        r02 = [o for o in dados["ocorrencias"] if o["risco"] == "R02"]
        self.assertEqual(len(r02), 1)
        for campo in ("data", "impacto", "resposta"):
            self.assertTrue(r02[0].get(campo), campo)


if __name__ == "__main__":
    unittest.main()
