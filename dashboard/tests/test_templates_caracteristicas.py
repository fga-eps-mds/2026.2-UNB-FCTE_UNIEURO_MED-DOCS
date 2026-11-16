"""
Testes dos textos da aba de qualidade por característica (src/templates.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import unittest
from datetime import datetime, timezone

from src import caracteristicas, templates
from src.config import THEME_COLORS

RELEASES = [
    {"id": "R1", "nome": "Release 1", "inicio": "2026-08-10", "fim": "2026-09-28"},
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26"},
]
HOJE = datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc)


def ponto(data, valor):
    return {"date": data, "value": str(valor)}


def calculadas(**series):
    return caracteristicas.calcular({k: [ponto(d, v) for d, v in pts] for k, pts in series.items()},
                                    RELEASES, hoje=HOJE)


R1_DATA = "2026-09-17T20:50:27+0000"
R2_DATA = "2026-10-14T02:25:16+0000"


class CartaoTest(unittest.TestCase):
    def cartao(self, release, chave):
        item = next(c for c in release["caracteristicas"] if c["chave"] == chave)
        return templates.cartao_caracteristica(item)

    def test_nota_aparece_como_letra_com_a_faixa_e_a_cor(self):
        r1, _ = calculadas(security_rating=[(R1_DATA, 1.0)])

        cartao = self.cartao(r1, "seguranca")

        self.assertEqual(cartao["rotulo"], "Segurança")
        self.assertEqual(cartao["valor"], "A")
        self.assertEqual(cartao["cor"], THEME_COLORS["secondary"])
        self.assertIn("Adequado", cartao["subtexto"])

    def test_o_sentido_da_mudanca_aparece_no_subtexto(self):
        _, r2 = calculadas(reliability_rating=[(R1_DATA, 1.0), (R2_DATA, 3.0)])

        cartao = self.cartao(r2, "confiabilidade")

        self.assertEqual(cartao["valor"], "C")
        self.assertEqual(cartao["cor"], THEME_COLORS["danger"])
        self.assertEqual(cartao["subtexto"], "Crítico · Piorou em relação à release anterior")

    def test_primeira_medicao_nao_diz_que_melhorou_nem_piorou(self):
        r1, _ = calculadas(sqale_rating=[(R1_DATA, 2.0)])

        cartao = self.cartao(r1, "manutenibilidade")

        self.assertEqual(cartao["subtexto"], "Atenção · Primeira medição")
        self.assertEqual(cartao["cor"], THEME_COLORS["warning"])

    def test_cobertura_aparece_em_percentual_com_virgula(self):
        r1, _ = calculadas(coverage=[(R1_DATA, 98.3)])

        cartao = self.cartao(r1, "testabilidade")

        self.assertEqual(cartao["valor"], "98,3%")

    def test_caracteristica_sem_dado_aparece_como_nao_medida_e_nunca_zero(self):
        r1, _ = calculadas()

        for chave in ("seguranca", "confiabilidade", "manutenibilidade", "testabilidade"):
            cartao = self.cartao(r1, chave)
            self.assertEqual(cartao["valor"], templates.NAO_MEDIDO)
            self.assertEqual(cartao["subtexto"], "Não medida")
            self.assertEqual(cartao["cor"], THEME_COLORS["accent"])
            self.assertNotIn("0", cartao["valor"])


class TabelaTest(unittest.TestCase):
    def test_uma_linha_por_caracteristica_e_uma_coluna_por_release(self):
        releases = calculadas(security_rating=[(R1_DATA, 1.0), (R2_DATA, 2.0)],
                              coverage=[(R1_DATA, 95.0)])

        linhas = templates.tabela_caracteristicas(releases)

        self.assertEqual([l["Característica"] for l in linhas],
                         ["Segurança", "Confiabilidade", "Manutenibilidade", "Testabilidade"])
        seguranca = linhas[0]
        self.assertEqual(seguranca["Release 1"], "A · Adequado")
        self.assertEqual(seguranca["Release 2"], "B · Atenção")
        self.assertEqual(linhas[3]["Release 1"], "95,0% · Adequado")

    def test_release_sem_dado_fica_com_nao_medido(self):
        releases = calculadas()

        linhas = templates.tabela_caracteristicas(releases)

        self.assertTrue(all(l["Release 1"] == templates.NAO_MEDIDO and l["Release 2"] == templates.NAO_MEDIDO
                            for l in linhas))

    def test_sem_release_a_tabela_e_vazia(self):
        self.assertEqual(templates.tabela_caracteristicas([]), [])


class DetalheTest(unittest.TestCase):
    def test_traz_rotulo_valor_e_unidade_de_cada_metrica_da_release(self):
        r1, _ = calculadas(ncloc=[(R1_DATA, 7676)], coverage=[(R1_DATA, 98.3)], bugs=[(R1_DATA, 0)],
                           sqale_rating=[(R1_DATA, 1.0)], sqale_index=[(R1_DATA, 195)])

        linhas = {l["Medida"]: l for l in templates.tabela_detalhe(r1)}

        self.assertEqual(linhas["Linhas de código"]["Valor"], "7.676")
        self.assertEqual(linhas["Cobertura"]["Valor"], "98,3%")
        self.assertEqual(linhas["Bugs"]["Valor"], "0")
        self.assertEqual(linhas["Nota de manutenibilidade"]["Valor"], "A")
        self.assertEqual(linhas["Débito técnico"]["Valor"], "195 min")

    def test_metrica_desconhecida_aparece_pelo_nome_do_sonar(self):
        r1, _ = calculadas(coisa_nova=[(R1_DATA, 5)])

        linhas = templates.tabela_detalhe(r1)

        self.assertEqual([l["Medida"] for l in linhas], ["coisa_nova"])

    def test_sem_metrica_na_release_a_tabela_e_vazia(self):
        r1, _ = calculadas()

        self.assertEqual(templates.tabela_detalhe(r1), [])


if __name__ == "__main__":
    unittest.main()
