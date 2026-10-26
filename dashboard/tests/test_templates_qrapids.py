"""
Testes dos utilitários de apresentação da aba Q-Rapids (src/templates.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import unittest
from datetime import datetime

from src import qualidade, templates
from src.qualidade import BRASILIA


def metrica(valor, conformes=0, total=0, fora=()):
    return {"valor": valor, "conformes": conformes, "total": total, "fora_do_limiar": list(fora)}


def avaliacao(versao, valores, momento=datetime(2026, 10, 1, tzinfo=BRASILIA)):
    """Avaliação de uma versão com as métricas dadas; as que faltam ficam não medidas."""
    metricas = {chave: metrica(valores.get(chave)) for chave in qualidade.METRICAS}
    return {"versao": versao, "momento": momento, "metricas": metricas, "agregacao": qualidade.agregar(metricas)}


COMPLETA = {chave: 0.9 for chave in qualidade.METRICAS}


class FormatarIndiceTest(unittest.TestCase):
    def test_duas_casas_decimais(self):
        self.assertEqual(templates.formatar_indice(0.9136), "0.91")

    def test_valor_sem_dado_e_nao_medido_e_nao_zero(self):
        self.assertEqual(templates.formatar_indice(None), "n/m")
        self.assertEqual(templates.formatar_indice(0.0), "0.00")

    def test_valor_parcial_ganha_asterisco(self):
        self.assertEqual(templates.formatar_indice(0.91, parcial=True), "0.91*")

    def test_sem_dado_ignora_o_asterisco(self):
        self.assertEqual(templates.formatar_indice(None, parcial=True), "n/m")


class CorDaFaixaTest(unittest.TestCase):
    def test_cada_faixa_tem_uma_cor_propria(self):
        cores = {templates.cor_da_faixa(v) for v in (0.95, 0.7, 0.3, None)}
        self.assertEqual(len(cores), 4)

    def test_limites_da_tabela_3_do_plano(self):
        self.assertEqual(templates.cor_da_faixa(0.80), templates.cor_da_faixa(1.0))
        self.assertEqual(templates.cor_da_faixa(0.79), templates.cor_da_faixa(0.60))
        self.assertEqual(templates.cor_da_faixa(0.59), templates.cor_da_faixa(0.0))


class TabelaQrapidsTest(unittest.TestCase):
    def test_uma_coluna_por_marco_medido_e_marco_sem_versao_fica_de_fora(self):
        marcos = {"R1": avaliacao("v1.0.0", COMPLETA), "RM1": None, "R2": avaliacao("v1.2.3", COMPLETA)}

        tabela = templates.tabela_qrapids(marcos)

        self.assertEqual(list(tabela.columns), ["Indicador", "R1 (v1.0.0)", "R2 (v1.2.3)"])

    def test_tem_as_oito_metricas_e_os_oito_indices_agregados(self):
        tabela = templates.tabela_qrapids({"R1": avaliacao("v1.0.0", COMPLETA)})

        self.assertEqual(len(tabela), 8 + 8)
        self.assertTrue(tabela["Indicador"].iloc[0].startswith("m1 "))
        self.assertTrue(tabela["Indicador"].iloc[-1].startswith("Q "))

    def test_indice_agregado_mostra_a_faixa(self):
        tabela = templates.tabela_qrapids({"R1": avaliacao("v1.0.0", COMPLETA)})

        self.assertEqual(tabela["R1 (v1.0.0)"].iloc[-1], "0.90 Adequado")

    def test_metrica_sem_dado_aparece_como_nao_medida_e_deixa_o_indice_parcial(self):
        valores = {**COMPLETA, "m4": None}

        tabela = templates.tabela_qrapids({"R1": avaliacao("v1.0.0", valores)})
        linhas = dict(zip(tabela["Indicador"], tabela["R1 (v1.0.0)"]))

        self.assertEqual(linhas["m4 Taxa de sucesso dos testes"], "n/m")
        self.assertEqual(linhas["ST Sucesso dos testes"], "n/m")
        self.assertTrue(linhas["C Confiabilidade"].startswith("0.90*"))

    def test_sem_marco_medido_a_tabela_so_tem_os_indicadores(self):
        tabela = templates.tabela_qrapids({"R1": None})

        self.assertEqual(list(tabela.columns), ["Indicador"])


    def test_nome_das_densidades_perde_o_prefixo_para_caber_na_tabela(self):
        tabela = templates.tabela_qrapids({"R1": avaliacao("v1.0.0", COMPLETA)})

        self.assertEqual(tabela["Indicador"].iloc[6], "m7 Arquivos sem problema grave de manutenibilidade")


class SerieEDetalheTest(unittest.TestCase):
    def test_versao_nao_medida_fica_com_valor_vazio_e_nao_zero(self):
        serie = templates.serie_do_indice([avaliacao("v1", COMPLETA), avaliacao("v2", {})])

        self.assertEqual(serie["versao"].tolist(), ["v1", "v2"])
        self.assertAlmostEqual(serie["valor"].iloc[0], 0.9)
        self.assertTrue(serie["valor"].isna().iloc[1])

    def test_detalhe_traz_os_arquivos_fora_do_limiar(self):
        item = avaliacao("v1", COMPLETA)
        item["metricas"]["m2"] = metrica(0.25, conformes=11, total=44, fora=["a.ts", "b.ts"])

        detalhe = templates.arquivos_fora_do_limiar(item, "m2")

        self.assertEqual((detalhe["conformes"], detalhe["total"]), (11, 44))
        self.assertEqual(detalhe["arquivos"], ["a.ts", "b.ts"])

    def test_detalhe_de_metrica_nao_medida_traz_o_motivo(self):
        item = avaliacao("v1", {})
        item["metricas"]["m4"]["motivo"] = "Sem resultado dos testes"

        detalhe = templates.arquivos_fora_do_limiar(item, "m4")

        self.assertIsNone(detalhe["valor"])
        self.assertEqual(detalhe["motivo"], "Sem resultado dos testes")


class MarcosSemMedidaTest(unittest.TestCase):
    def marcos(self, **medidos):
        return {nome: (avaliacao("v1", COMPLETA) if tem else None) for nome, tem in medidos.items()}

    def test_marco_passado_ou_em_curso_sem_versao_e_apontado(self):
        marcos = self.marcos(R1=True, RM1=False, R2=False, R3=False)
        agora = datetime(2026, 10, 23, tzinfo=BRASILIA)

        self.assertEqual(templates.marcos_sem_medida(marcos, agora), ["RM1", "R2"])

    def test_marco_futuro_sem_versao_nao_e_falta_de_dado(self):
        marcos = self.marcos(R1=True, RM1=True, R2=True, R3=False)
        agora = datetime(2026, 10, 23, tzinfo=BRASILIA)

        self.assertEqual(templates.marcos_sem_medida(marcos, agora), [])

    def test_depois_do_ultimo_marco_todos_sao_esperados(self):
        marcos = self.marcos(R1=True, RM1=True, R2=True, R3=False)
        agora = datetime(2026, 12, 15, tzinfo=BRASILIA)

        self.assertEqual(templates.marcos_sem_medida(marcos, agora), ["R3"])


class TabelasDeProcessoTest(unittest.TestCase):
    def test_tabela_de_processo_marca_release_em_andamento_e_indice_sem_dado(self):
        dados = {
            "R2": {"indicadores": {"P1": 0.97, "P2": 0.0, "P3": None}, "P": 0.49, "parcial": True,
                   "sprints": ["Sprint 2", "Sprint 3"], "em_andamento": True, "execucoes": None},
            "R3": {"indicadores": {"P1": None, "P2": None, "P3": None}, "P": None, "parcial": True,
                   "sprints": [], "em_andamento": False, "execucoes": None},
        }

        tabela = templates.tabela_processo(dados)

        self.assertEqual(tabela["Release"].tolist(), ["R2 (em andamento)", "R3"])
        self.assertEqual(list(tabela.columns), ["Release", "Sprints", "P1", "P2", "P3", "P"])
        self.assertEqual(tabela["P2"].tolist(), ["0.00", "n/m"])
        self.assertEqual(tabela["P"].tolist(), ["0.49* Crítico", "n/m"])
        self.assertEqual(tabela["Sprints"].tolist(), ["Sprint 2, Sprint 3", "n/m"])

    def test_comparativo_so_tem_texto_nas_celulas_para_nao_quebrar_a_tabela(self):
        dados = {"R1": {"versao": None, "velocidade": None, "planejados_por_sprint": 21.0, "cobertura": None,
                        "bugs_abertos_na_release": 0, "arquivos_com_defeito_provavel": None}}

        tabela = templates.tabela_comparativo(dados)

        self.assertEqual(tabela.iloc[0].tolist(), ["R1", "n/m", "n/m", "21.0", "n/m", "0", "n/m"])
        self.assertTrue(all(isinstance(celula, str) for celula in tabela.to_numpy().ravel()))


class AvisoModoEntreguesTest(unittest.TestCase):
    def test_diz_os_pontos_em_aceitacao_e_os_ja_aceitos(self):
        texto = templates.aviso_modo_entregues("Aceitas + em Aceitação PO", 8.0, 45.0, 5)

        self.assertIn("**45 SP** de 5 história(s) em Aceitação PO", texto)
        self.assertIn("Já aceitos: 8 SP", texto)

    def test_explica_que_a_historia_conta_na_ultima_sprint(self):
        texto = templates.aviso_modo_entregues("Aceitas + em Aceitação PO", 0.0, 45.0, 5)

        self.assertIn("última sprint em que aparece", texto)
        self.assertIn("velocity daquela sprint anterior fica mais baixa", texto)


if __name__ == "__main__":
    unittest.main()
