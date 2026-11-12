import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

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

    def test_o_eixo_do_tempo_da_curva_de_custo_usa_dia_e_mes(self):
        especificacoes = [json.loads(g.proto.spec) for g in self.app.get("plotly_chart")]
        curva = next(s for s in especificacoes
                     if "PV, AC e EV acumulados do projeto" in s["layout"].get("title", {}).get("text", ""))

        # Sem o formato, o Plotly escreve datas como "Aug 9", em inglês.
        self.assertEqual(curva["layout"]["xaxis"]["tickformat"], "%d/%m")

    def test_o_cifrao_do_valor_em_reais_nao_vira_formula(self):
        legenda = next(t for t in self.textos if t.startswith("Hoje, no projeto todo"))

        # O Streamlit lê um par de cifrões como fórmula: o "R$" precisa sair escapado.
        self.assertIn("R\\$", legenda)


class AbaEvmAceiteTardioTest(unittest.TestCase):
    """Painel com uma coleta em que o PO aceitou na Sprint 5 histórias entregues na Sprint 4."""

    @classmethod
    def setUpClass(cls):
        from src import config, data_layer, processo
        cls.pasta = tempfile.mkdtemp()
        shutil.copytree(config.RAW_DATA_DIR, cls.pasta, dirs_exist_ok=True)
        caminho = os.path.join(cls.pasta, "zenhub_analytics.json")
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        for sprint in dados["sprints_velocity"].values():
            for issue in sprint.get("issues", []):
                fechada = issue.get("numero") in (5, 6, 7, 9, 11, 21, 23) and issue.get("estimativa")
                issue["fechada"] = bool(fechada)
                issue["fechada_em"] = "2026-11-11T01:39:20Z" if fechada else None
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo)
        cls.patches = [mock.patch.object(m, "RAW_DATA_DIR", cls.pasta) for m in (data_layer, processo, config)]
        for patch in cls.patches:
            patch.start()
        cls.app = AppTest.from_file(DASHBOARD, default_timeout=120)
        cls.app.run()

    @classmethod
    def tearDownClass(cls):
        for patch in cls.patches:
            patch.stop()
        shutil.rmtree(cls.pasta, ignore_errors=True)

    def test_a_aba_abre_sem_erro(self):
        self.assertEqual([e.value for e in self.app.exception], [])

    def test_diz_que_a_sprint_4_teve_historias_aceitas_depois_do_fim(self):
        legendas = [c.value for c in self.app.caption]

        self.assertTrue(any(
            c.startswith("Sprint 4: 53 SP de 7 história(s) foram aceitas pelo PO depois do fim da sprint")
            for c in legendas
        ))

    def test_a_velocity_separa_os_aceites_tardios_da_sprint_4(self):
        especificacoes = [json.loads(g.proto.spec) for g in self.app.get("plotly_chart")]
        velocity = next(s for s in especificacoes
                        if "Velocity por Sprint" in s["layout"].get("title", {}).get("text", ""))
        tardios = next(b for b in velocity["data"] if b["name"].startswith("Aceitos pelo PO depois"))

        self.assertEqual(max(tardios["y"]), 53.0)


if __name__ == "__main__":
    unittest.main()
