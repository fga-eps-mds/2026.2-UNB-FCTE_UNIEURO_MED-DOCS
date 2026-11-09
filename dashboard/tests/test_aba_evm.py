import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.testing.v1 import AppTest  # noqa: E402

DASHBOARD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard.py")


class AbaEvmTest(unittest.TestCase):
    """Renderiza o painel de verdade, com os dados de analytics-raw-data, e olha a aba de EVM."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppTest.from_file(DASHBOARD, default_timeout=120)
        cls.app.run()
        cls.textos = [m.value for m in cls.app.markdown] + [c.value for c in cls.app.caption]

    def test_a_aba_abre_sem_erro(self):
        self.assertEqual([e.value for e in self.app.exception], [])

    def test_mostra_o_grafico_de_custo_e_o_de_indices(self):
        junto = " ".join(self.textos)

        self.assertIn("Valor Planejado, Custo e Valor Agregado ao Longo do Projeto", junto)
        self.assertIn("Índices de Desempenho SPI e CPI por Release", junto)

    def test_avisa_que_o_ac_e_estimado_e_o_cpi_repete_o_spi(self):
        avisos = " ".join(i.value for i in self.app.info)

        self.assertIn("o AC é estimado pela linha de base", avisos)
        self.assertIn("CPI é sempre igual ao SPI", avisos)

    def test_o_cifrao_do_valor_em_reais_nao_vira_formula(self):
        legenda = next(t for t in self.textos if t.startswith("Hoje, no projeto todo"))

        # O Streamlit lê um par de cifrões como fórmula: o "R$" precisa sair escapado.
        self.assertIn("R\\$", legenda)


if __name__ == "__main__":
    unittest.main()
