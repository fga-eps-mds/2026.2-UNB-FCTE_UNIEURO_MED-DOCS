"""
Testes da comparação lado a lado dos dois modos de pontos entregues (aceitas e entregues).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover -s tests -t .
"""

import unittest
from datetime import date

from src import templates
from src.metrics import comparar_modos

RELEASES = [
    {"id": "R1", "nome": "Release 1", "inicio": "2026-08-10", "fim": "2026-09-28", "bac_brl": 1000.0},
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26", "bac_brl": 1000.0},
]
HOJE = date(2026, 10, 12)


def sprint(nome, planejados, aceitos, aguardando=0.0, fim="2026-10-12T02:59:00Z", fonte="zenhub"):
    return {
        "name": nome, "total_points": planejados, "delivered_sp": aceitos, "points_added": 0.0,
        "status": "CLOSED", "start_at": "2026-09-29T03:59:00Z", "end_at": fim,
        "aguardando_pontos": aguardando, "aguardando_issues": [], "aceitacao_fonte": fonte,
    }


def linha_de(**mudancas):
    base = {
        "id": "R2", "status": "Em andamento", "bac": 1000.0, "prp": 20.0, "ppc": 0.5, "fonte": "zenhub",
        "aceitas": {"rpc": 4.0, "apc": 0.2, "ev": 200.0, "spi": 0.4, "cpi": 0.4},
        "entregues": {"rpc": 14.0, "apc": 0.7, "ev": 700.0, "spi": 1.4, "cpi": 1.4},
        "aguardando_pontos": 10.0,
    }
    base.update(mudancas)
    return base


class CompararModosTest(unittest.TestCase):
    def setUp(self):
        self.linhas = comparar_modos([sprint("Sprint 2", 20, 4, 10)], RELEASES, HOJE)
        self.r2 = next(r for r in self.linhas if r["id"] == "R2")

    def test_calcula_cada_modo_com_a_mesma_regra_do_evm(self):
        self.assertEqual(self.r2["aceitas"]["rpc"], 4.0)
        self.assertEqual(self.r2["entregues"]["rpc"], 14.0)
        self.assertAlmostEqual(self.r2["aceitas"]["apc"], 0.2)
        self.assertAlmostEqual(self.r2["entregues"]["apc"], 0.7)

    def test_prp_e_prazo_nao_dependem_do_modo(self):
        self.assertEqual(self.r2["prp"], 20.0)
        self.assertGreater(self.r2["ppc"], 0)

    def test_a_diferenca_entre_os_modos_e_o_que_aguarda_o_aceite(self):
        self.assertEqual(self.r2["aguardando_pontos"], 10.0)

    def test_sem_a_coluna_coletada_os_modos_coincidem(self):
        linhas = comparar_modos([sprint("Sprint 2", 20, 4, fonte=None)], RELEASES, HOJE)
        r2 = next(r for r in linhas if r["id"] == "R2")

        self.assertIsNone(r2["fonte"])
        self.assertEqual(r2["aguardando_pontos"], 0.0)
        self.assertEqual(r2["aceitas"], r2["entregues"])

    def test_release_futura_fica_de_fora_como_no_evm(self):
        linhas = comparar_modos([sprint("Sprint 2", 20, 4)], RELEASES, date(2026, 8, 1))

        self.assertEqual([r["id"] for r in linhas], ["R1"])


class LeituraTest(unittest.TestCase):
    def test_diz_que_a_espera_do_aceite_e_o_que_atrasa_quando_so_o_entregue_acompanha_o_prazo(self):
        texto = templates.leitura_escopo_e_tempo(linha_de())

        self.assertIn("50% do prazo", texto)
        self.assertIn("entregue é 70%", texto)
        self.assertIn("aceito é 20%", texto)
        self.assertIn("10 SP", texto)
        self.assertIn("espera do aceite", texto)

    def test_avisa_quando_nem_o_entregue_acompanha_o_prazo(self):
        texto = templates.leitura_escopo_e_tempo(linha_de(
            ppc=0.9, entregues={"rpc": 14.0, "apc": 0.7, "ev": 700.0, "spi": 0.78, "cpi": 0.78}))

        self.assertIn("abaixo do prazo", texto)

    def test_sem_historia_aguardando_nao_atribui_atraso_ao_aceite(self):
        texto = templates.leitura_escopo_e_tempo(linha_de(aguardando_pontos=0.0))

        self.assertIn("Nenhuma história aguarda", texto)
        self.assertNotIn("espera do aceite", texto)

    def test_sem_a_coluna_coletada_diz_que_nao_da_para_separar(self):
        self.assertIn("não foi coletada", templates.leitura_escopo_e_tempo(linha_de(fonte=None)))

    def test_sem_pontos_estimados_nao_ha_escopo_para_comparar(self):
        self.assertIn("Sem pontos estimados", templates.leitura_escopo_e_tempo(linha_de(prp=0.0)))


class TabelaEGraficoTest(unittest.TestCase):
    def test_tabela_traz_os_dois_modos_e_a_faixa_do_spi(self):
        tabela = templates.tabela_lado_a_lado(linha_de())
        spi = tabela[tabela["Indicador"] == "SPI"].iloc[0]
        faixa = tabela[tabela["Indicador"] == "Faixa do SPI"].iloc[0]

        self.assertEqual((spi["Somente aceitas"], spi["Aceitas + em Aceitação PO"]), ("0.40", "1.40"))
        self.assertEqual((faixa["Somente aceitas"], faixa["Aceitas + em Aceitação PO"]), ("Crítico", "Adequado"))

    def test_indice_sem_valor_aparece_como_na_e_nao_como_zero(self):
        vazio = {"rpc": 0.0, "apc": None, "ev": None, "spi": None, "cpi": None}
        tabela = templates.tabela_lado_a_lado(linha_de(aceitas=vazio, entregues=vazio))

        self.assertEqual(tabela[tabela["Indicador"] == "SPI"].iloc[0]["Somente aceitas"], "N/A")

    def test_serie_do_grafico_em_porcentagem_so_das_releases_com_escopo(self):
        dados = templates.dados_escopo_e_tempo([linha_de(id="R1", prp=0.0), linha_de()])

        self.assertEqual(dados["releases"], ["R2"])
        self.assertEqual((dados["prazo"], dados["aceitas"], dados["entregues"]), ([50.0], [20.0], [70.0]))


if __name__ == "__main__":
    unittest.main()
