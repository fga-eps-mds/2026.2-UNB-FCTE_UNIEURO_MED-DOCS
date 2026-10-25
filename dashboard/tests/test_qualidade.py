"""
Testes do cálculo do Q-Rapids (src/qualidade.py) contra as fórmulas do Plano de Qualidade.

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta

from src import qualidade
from src.qualidade import BRASILIA


def arquivo(caminho, **medidas):
    return {"qualifier": "FIL", "path": caminho,
            "measures": [{"metric": k, "value": str(v)} for k, v in medidas.items()]}


def teste(caminho, **medidas):
    return {"qualifier": "UTS", "path": caminho,
            "measures": [{"metric": k, "value": str(v)} for k, v in medidas.items()]}


def problema(caminho, qualidade_, severidade, criado="2026-10-01T00:00:00+0000", fechado=None):
    return {"arquivo": caminho, "criado_em": criado, "fechado_em": fechado,
            "impactos": [{"qualidade": qualidade_, "severidade": severidade}]}


BOM = dict(ncloc=50, functions=5, complexity=10, comment_lines_density=15,
           duplicated_lines_density=0, coverage=90)


class MetricasTest(unittest.TestCase):
    def test_m1_conta_so_arquivos_com_funcao_e_complexidade_media_menor_que_10(self):
        componentes = [
            arquivo("a.ts", **BOM),                                        # 10 / 5 = 2
            arquivo("b.ts", **{**BOM, "complexity": 50}),                  # 50 / 5 = 10, no limite
            arquivo("c.ts", **{**BOM, "functions": 0, "complexity": 0}),   # sem função: fora de A_f
        ]
        m1 = qualidade.calcular_metricas(componentes, {}, [])["m1"]
        self.assertEqual((m1["conformes"], m1["total"]), (1, 2))
        self.assertEqual(m1["fora_do_limiar"], ["b.ts"])

    def test_arquivo_sem_linha_de_codigo_fica_fora_de_todas_as_metricas(self):
        componentes = [arquivo("a.ts", **BOM), arquivo("vazio.ts", **{**BOM, "ncloc": 0, "comment_lines_density": 0})]
        m = qualidade.calcular_metricas(componentes, {}, [])
        self.assertEqual(m["m2"]["total"], 1)
        self.assertEqual(m["m3"]["total"], 1)

    def test_m2_exige_comentarios_estritamente_entre_10_e_30_por_cento(self):
        componentes = [arquivo(f"{d}.ts", **{**BOM, "comment_lines_density": d}) for d in (10, 10.1, 29.9, 30)]
        m2 = qualidade.calcular_metricas(componentes, {}, [])["m2"]
        self.assertEqual(m2["fora_do_limiar"], ["10.ts", "30.ts"])

    def test_m3_aceita_menos_de_5_por_cento_de_duplicacao(self):
        componentes = [arquivo("a.ts", **BOM), arquivo("b.ts", **{**BOM, "duplicated_lines_density": 5})]
        self.assertEqual(qualidade.calcular_metricas(componentes, {}, [])["m3"]["valor"], 0.5)

    def test_m4_usa_o_total_do_projeto(self):
        m4 = qualidade.calcular_metricas([arquivo("a.ts", **BOM)],
                                         {"tests": 100, "test_errors": 1, "test_failures": 3}, [])["m4"]
        self.assertAlmostEqual(m4["valor"], 0.96)

    def test_m4_soma_os_arquivos_de_teste_quando_falta_o_total_do_projeto(self):
        componentes = [arquivo("a.ts", **BOM),
                       teste("a.test.ts", tests=8, test_errors=0, test_failures=1, test_execution_time=10),
                       teste("b.test.ts", tests=2, test_errors=1, test_failures=0, test_execution_time=10)]
        self.assertAlmostEqual(qualidade.calcular_metricas(componentes, {}, [])["m4"]["valor"], 0.8)

    def test_m4_e_m5_sem_resultado_dos_testes_sao_nao_medidas_e_nao_zero(self):
        componentes = [arquivo("a.ts", **BOM), {"qualifier": "UTS", "path": "a.test.ts", "measures": []}]
        m = qualidade.calcular_metricas(componentes, {}, [])
        self.assertIsNone(m["m4"]["valor"])
        self.assertIsNone(m["m5"]["valor"])
        self.assertIn("motivo", m["m4"])

    def test_m5_considera_rapido_o_arquivo_de_teste_com_menos_de_5_segundos(self):
        componentes = [arquivo("a.ts", **BOM),
                       teste("rapido.test.ts", tests=1, test_execution_time=4999),
                       teste("lento.test.ts", tests=1, test_execution_time=5000)]
        m5 = qualidade.calcular_metricas(componentes, {}, [])["m5"]
        self.assertEqual(m5["fora_do_limiar"], ["lento.test.ts"])

    def test_m6_usa_so_arquivos_com_cobertura_medida(self):
        sem_cobertura = {k: v for k, v in BOM.items() if k != "coverage"}
        componentes = [arquivo("a.ts", **BOM), arquivo("b.ts", **{**BOM, "coverage": 74.9}),
                       arquivo("rota.tsx", **sem_cobertura)]
        m6 = qualidade.calcular_metricas(componentes, {}, [])["m6"]
        self.assertEqual((m6["conformes"], m6["total"]), (1, 2))

    def test_m7_conta_so_problema_de_manutenibilidade_alto_ou_bloqueante(self):
        componentes = [arquivo(n, **BOM) for n in ("a.ts", "b.ts", "c.ts", "d.ts")]
        abertos = [problema("a.ts", "MAINTAINABILITY", "HIGH"), problema("b.ts", "MAINTAINABILITY", "BLOCKER"),
                   problema("c.ts", "MAINTAINABILITY", "MEDIUM")]
        m7 = qualidade.calcular_metricas(componentes, {}, abertos)["m7"]
        self.assertEqual(m7["fora_do_limiar"], ["a.ts", "b.ts"])

    def test_m8_conta_qualquer_problema_de_confiabilidade(self):
        componentes = [arquivo(n, **BOM) for n in ("a.ts", "b.ts")]
        abertos = [problema("a.ts", "RELIABILITY", "LOW"), problema("b.ts", "MAINTAINABILITY", "HIGH")]
        self.assertEqual(qualidade.calcular_metricas(componentes, {}, abertos)["m8"]["fora_do_limiar"], ["a.ts"])

    def test_sem_os_problemas_da_branch_m7_e_m8_sao_nao_medidas(self):
        m = qualidade.calcular_metricas([arquivo("a.ts", **BOM)], {}, None)
        self.assertIsNone(m["m7"]["valor"])
        self.assertIsNone(m["m8"]["valor"])

    def test_versao_sem_arquivos_deixa_todas_as_metricas_nao_medidas(self):
        m = qualidade.calcular_metricas([], {"coverage": 96}, [])
        self.assertTrue(all(v["valor"] is None for v in m.values()))


class ProblemasAbertosTest(unittest.TestCase):
    def test_considera_aberto_o_problema_criado_antes_e_fechado_depois_do_momento(self):
        momento = datetime(2026, 10, 10, 12, tzinfo=BRASILIA)
        problemas = [
            problema("antes.ts", "RELIABILITY", "LOW", criado="2026-10-01T00:00:00+0000"),
            problema("depois.ts", "RELIABILITY", "LOW", criado="2026-10-11T00:00:00+0000"),
            problema("fechado.ts", "RELIABILITY", "LOW", criado="2026-10-01T00:00:00+0000",
                     fechado="2026-10-05T00:00:00+0000"),
            problema("fechou_depois.ts", "RELIABILITY", "LOW", criado="2026-10-01T00:00:00+0000",
                     fechado="2026-10-12T00:00:00+0000"),
        ]
        abertos = [p["arquivo"] for p in qualidade.problemas_abertos_em(problemas, momento)]
        self.assertEqual(abertos, ["antes.ts", "fechou_depois.ts"])

    def test_compara_os_horarios_em_fusos_diferentes(self):
        # 10/10 12:00 em Brasília é 15:00 em UTC.
        momento = datetime(2026, 10, 10, 12, tzinfo=BRASILIA)
        problemas = [problema("a.ts", "RELIABILITY", "LOW", criado="2026-10-10T14:59:00+0000"),
                     problema("b.ts", "RELIABILITY", "LOW", criado="2026-10-10T15:01:00+0000")]
        self.assertEqual([p["arquivo"] for p in qualidade.problemas_abertos_em(problemas, momento)], ["a.ts"])


def metricas(**valores):
    return {k: {"valor": valores.get(k)} for k in qualidade.METRICAS}


class AgregacaoTest(unittest.TestCase):
    def test_segue_as_formulas_da_secao_3_3(self):
        g = qualidade.agregar(metricas(m1=0.9, m2=0.3, m3=0.6, m4=1.0, m5=0.6, m6=0.9, m7=0.8, m8=0.7))
        qc, cb, t = 0.6, 0.8, (0.6 + 2 * 0.9) / 3
        m, c = (qc + cb + t) / 3, 0.5 * 1.0 + 0.5 * 0.7
        self.assertAlmostEqual(g["QC"]["valor"], qc)
        self.assertAlmostEqual(g["T"]["valor"], t)
        self.assertAlmostEqual(g["M"]["valor"], m)
        self.assertAlmostEqual(g["C"]["valor"], c)
        self.assertAlmostEqual(g["Q"]["valor"], 0.5 * m + 0.5 * c)
        self.assertFalse(any(v["parcial"] for v in g.values()))

    def test_metrica_ausente_divide_o_peso_entre_as_outras_e_marca_parcial(self):
        g = qualidade.agregar(metricas(m1=1, m2=1, m3=1, m4=None, m5=None, m6=0.9, m7=1, m8=0.8))
        self.assertAlmostEqual(g["T"]["valor"], 0.9)
        self.assertTrue(g["T"]["parcial"])
        self.assertIsNone(g["ST"]["valor"])
        self.assertAlmostEqual(g["C"]["valor"], 0.8)
        self.assertTrue(g["C"]["parcial"])
        self.assertTrue(g["Q"]["parcial"])
        self.assertFalse(g["QC"]["parcial"])

    def test_sem_nenhuma_metrica_tudo_fica_nao_medido(self):
        g = qualidade.agregar(metricas())
        self.assertIsNone(g["Q"]["valor"])
        self.assertFalse(g["Q"]["parcial"])

    def test_faixas_da_tabela_3(self):
        self.assertEqual([qualidade.faixa(v) for v in (0.80, 0.7999, 0.60, 0.5999, None)],
                         ["Adequado", "Atenção", "Atenção", "Crítico", "Não medida"])


def avaliacao(versao, dia, **valores):
    m = metricas(**valores)
    return {"versao": versao, "momento": datetime(2026, 10, dia, 12, tzinfo=BRASILIA),
            "metricas": m, "agregacao": qualidade.agregar(m)}


COMPLETA = dict(m1=1, m2=1, m3=1, m4=1, m5=1, m6=1, m7=1, m8=1)


class EvolucaoTest(unittest.TestCase):
    def test_aponta_queda_de_0_05_entre_versoes_seguidas(self):
        serie = [avaliacao("v1", 1, **COMPLETA), avaliacao("v2", 2, **{**COMPLETA, "m2": 0.85})]
        indicadores = {q["indicador"] for q in qualidade.quedas(serie)}
        self.assertEqual(indicadores, {"QC"})

    def test_nao_compara_valor_parcial(self):
        serie = [avaliacao("v1", 1, **{**COMPLETA, "m5": None}), avaliacao("v2", 2, **{**COMPLETA, "m5": 0.5})]
        self.assertEqual(qualidade.quedas(serie), [])

    def test_cada_marco_usa_a_ultima_versao_desde_o_marco_anterior(self):
        marcos = {"A": datetime(2026, 10, 5, tzinfo=BRASILIA), "B": datetime(2026, 10, 15, tzinfo=BRASILIA),
                  "C": datetime(2026, 10, 25, tzinfo=BRASILIA)}
        serie = [avaliacao("v1", 1, **COMPLETA), avaliacao("v2", 3, **COMPLETA), avaliacao("v3", 10, **COMPLETA)]
        escolhidas = {k: (v["versao"] if v else None) for k, v in qualidade.por_marco(serie, marcos).items()}
        self.assertEqual(escolhidas, {"A": "v2", "B": "v3", "C": None})


class LeituraTest(unittest.TestCase):
    def test_le_a_versao_o_horario_de_brasilia_e_a_branch_da_release(self):
        with tempfile.TemporaryDirectory() as pasta:
            nome = "fga-eps-mds-2026.2-UNB-FCTE_UNIEURO_MED-APP-10-22-2026-21-04-55-v1.2.3.json"
            with open(os.path.join(pasta, nome), "w", encoding="utf-8") as f:
                json.dump({"baseComponent": {"measures": [{"metric": "tests", "value": "3"}]},
                           "components": [arquivo("a.ts", **BOM)]}, f)
            with open(os.path.join(pasta, "GitHub_API-Releases-APP.json"), "w", encoding="utf-8") as f:
                json.dump({"releases": [{"tag": "v1.2.3", "branch": "develop"}]}, f)

            [versao] = qualidade.carregar_versoes("APP", pasta)
            self.assertEqual(versao["versao"], "v1.2.3")
            self.assertEqual(versao["branch"], "develop")
            self.assertEqual(versao["momento"].utcoffset(), timedelta(hours=-3))
            self.assertEqual((versao["momento"].hour, versao["momento"].minute), (21, 4))
            self.assertEqual(qualidade.carregar_versoes("IA", pasta), [])


if __name__ == "__main__":
    unittest.main()
