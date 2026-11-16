import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.testing.v1 import AppTest  # noqa: E402

DASHBOARD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard.py")


def textos(app):
    return " ".join([m.value for m in app.markdown] + [c.value for c in app.caption] + [i.value for i in app.info])


class AbaQualidadePorCaracteristicaTest(unittest.TestCase):
    """Renderiza o painel de verdade, com os dados de analytics-raw-data, e olha a aba de qualidade."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppTest.from_file(DASHBOARD, default_timeout=120)
        cls.app.run()

    def test_a_aba_abre_sem_erro(self):
        self.assertEqual([e.value for e in self.app.exception], [])

    def test_abre_com_as_quatro_caracteristicas(self):
        junto = textos(self.app)

        self.assertIn("Qualidade por característica (ISO/IEC 25010)", junto)
        for nome in ("Segurança", "Confiabilidade", "Manutenibilidade", "Testabilidade"):
            self.assertIn(f'<span class="kpi-tag">{nome}', junto)

    def test_cada_caracteristica_mostra_a_faixa_e_o_sentido_da_mudanca(self):
        junto = textos(self.app)

        self.assertRegex(junto, r"(Adequado|Atenção|Crítico) · (Primeira medição|Melhorou|Piorou|Manteve|Sem comparação)")

    def test_a_release_mais_recente_vem_escolhida_e_todas_as_releases_ja_iniciadas_aparecem(self):
        seletor = self.app.radio(key="quality_release_selector")

        self.assertEqual(seletor.options[-1], seletor.value)
        self.assertEqual(seletor.options[0], "Release 1")

    def test_trocar_a_release_muda_o_que_a_aba_mostra(self):
        app = AppTest.from_file(DASHBOARD, default_timeout=120).run()
        app.radio(key="quality_release_selector").set_value("Release 1").run()
        primeira = textos(app)

        self.assertEqual([e.value for e in app.exception], [])
        self.assertIn("Primeira medição", primeira)

    def test_as_medidas_soltas_ficam_no_bloco_de_detalhe_recolhido(self):
        junto = textos(self.app)

        self.assertIn("Detalhe das medidas do SonarCloud", junto)
        self.assertNotIn("Achados Estáticos", junto)
        self.assertNotIn('<span class="kpi-tag">Linhas de Código', junto)
        self.assertFalse(self.app.toggle(key="quality_detalhe_toggle").value)

    def test_o_detalhe_mostra_as_medidas_da_release_e_a_ultima_coleta(self):
        app = AppTest.from_file(DASHBOARD, default_timeout=120).run()
        app.toggle(key="quality_detalhe_toggle").set_value(True).run()
        junto = textos(app)

        self.assertEqual([e.value for e in app.exception], [])
        self.assertIn("Última coleta", junto)
        self.assertIn("Achados Estáticos", junto)
        self.assertIn("Medidas na Release", junto)


if __name__ == "__main__":
    unittest.main()
