"""
Testes da qualidade por característica (src/caracteristicas.py).

Uso, a partir da pasta dashboard/:
    python3 -m unittest discover tests
"""

import unittest
from datetime import datetime, timezone

from src import caracteristicas
from src.caracteristicas import (
    ADEQUADO, ATENCAO, CRITICO, NAO_MEDIDA, MELHOROU, PIOROU, MANTEVE, PRIMEIRA, SEM_COMPARACAO,
)

RELEASES = [
    {"id": "R1", "nome": "Release 1", "inicio": "2026-08-10", "fim": "2026-09-28"},
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26"},
    {"id": "R3", "nome": "Release 3", "inicio": "2026-10-27", "fim": "2026-11-30"},
    {"id": "RF", "nome": "Release final", "inicio": "2026-12-01", "fim": "2026-12-07"},
]
HOJE = datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc)


def serie(*pontos):
    return [{"date": data, "value": str(valor)} for data, valor in pontos]


def historico(**series):
    return {nome: lista for nome, lista in series.items()}


def por_chave(release):
    return {c["chave"]: c for c in release["caracteristicas"]}


class ValorNaDataTest(unittest.TestCase):
    PONTOS = serie(("2026-09-17T20:50:27+0000", "1.0"), ("2026-10-14T02:25:16+0000", "3.0"))

    def test_pega_o_ultimo_ponto_ate_o_fim_da_release(self):
        limite = caracteristicas.fim_da_release(RELEASES[1])

        self.assertEqual(caracteristicas.valor_ate(self.PONTOS, limite), 3.0)

    def test_nao_usa_ponto_posterior_ao_fim_da_release(self):
        limite = caracteristicas.fim_da_release(RELEASES[0])

        self.assertEqual(caracteristicas.valor_ate(self.PONTOS, limite), 1.0)

    def test_sem_ponto_ate_a_data_devolve_none_e_nao_zero(self):
        limite = caracteristicas.fim_da_release({"fim": "2026-09-01"})

        self.assertIsNone(caracteristicas.valor_ate(self.PONTOS, limite))

    def test_serie_vazia_ou_ausente_devolve_none(self):
        limite = caracteristicas.fim_da_release(RELEASES[2])

        self.assertIsNone(caracteristicas.valor_ate([], limite))
        self.assertIsNone(caracteristicas.valor_ate(None, limite))

    def test_ignora_ponto_sem_valor_ou_com_valor_invalido(self):
        pontos = [{"date": "2026-09-17T20:50:27+0000"}, {"date": "2026-09-18T00:00:00+0000", "value": "x"},
                  {"date": "2026-09-19T00:00:00+0000", "value": "2.0"}]

        self.assertEqual(caracteristicas.valor_ate(pontos, caracteristicas.fim_da_release(RELEASES[0])), 2.0)

    def test_o_fim_da_release_e_o_fim_do_dia_em_brasilia(self):
        # 28/09 às 23h30 em Brasília ainda é a R1, mesmo que em UTC já seja 29/09.
        pontos = serie(("2026-09-29T02:30:00+0000", "2.0"))

        self.assertEqual(caracteristicas.valor_ate(pontos, caracteristicas.fim_da_release(RELEASES[0])), 2.0)
        self.assertIsNone(caracteristicas.valor_ate(
            serie(("2026-09-29T03:30:00+0000", "2.0")), caracteristicas.fim_da_release(RELEASES[0])))


class FaixaTest(unittest.TestCase):
    def test_nota_a_e_adequada_b_pede_atencao_e_c_a_e_critica(self):
        self.assertEqual(caracteristicas.faixa_nota(1.0), ADEQUADO)
        self.assertEqual(caracteristicas.faixa_nota(2.0), ATENCAO)
        for nota in (3.0, 4.0, 5.0):
            self.assertEqual(caracteristicas.faixa_nota(nota), CRITICO)

    def test_nota_ausente_nao_e_medida(self):
        self.assertEqual(caracteristicas.faixa_nota(None), NAO_MEDIDA)

    def test_cobertura_segue_as_metas_do_plano_de_qualidade(self):
        self.assertEqual(caracteristicas.faixa_cobertura(90.0), ADEQUADO)
        self.assertEqual(caracteristicas.faixa_cobertura(89.9), ATENCAO)
        self.assertEqual(caracteristicas.faixa_cobertura(80.0), ATENCAO)
        self.assertEqual(caracteristicas.faixa_cobertura(79.9), CRITICO)

    def test_cobertura_ausente_nao_e_medida_nem_zero(self):
        self.assertEqual(caracteristicas.faixa_cobertura(None), NAO_MEDIDA)

    def test_converte_a_nota_numerica_em_letra(self):
        self.assertEqual(caracteristicas.letra(1.0), "A")
        self.assertEqual(caracteristicas.letra(5.0), "E")
        self.assertIsNone(caracteristicas.letra(None))
        self.assertIsNone(caracteristicas.letra(7.0))


class SentidoTest(unittest.TestCase):
    def test_nota_menor_e_melhor(self):
        self.assertEqual(caracteristicas.sentido(1.0, 3.0, menor_e_melhor=True), MELHOROU)
        self.assertEqual(caracteristicas.sentido(3.0, 1.0, menor_e_melhor=True), PIOROU)
        self.assertEqual(caracteristicas.sentido(2.0, 2.0, menor_e_melhor=True), MANTEVE)

    def test_cobertura_maior_e_melhor(self):
        self.assertEqual(caracteristicas.sentido(95.0, 90.0, menor_e_melhor=False), MELHOROU)
        self.assertEqual(caracteristicas.sentido(85.0, 90.0, menor_e_melhor=False), PIOROU)

    def test_variacao_pequena_de_cobertura_mantem(self):
        self.assertEqual(caracteristicas.sentido(90.2, 90.0, menor_e_melhor=False), MANTEVE)

    def test_sem_valor_atual_nao_ha_o_que_comparar(self):
        self.assertEqual(caracteristicas.sentido(None, 1.0, menor_e_melhor=True), SEM_COMPARACAO)

    def test_sem_release_anterior_e_a_primeira_medicao(self):
        self.assertEqual(caracteristicas.sentido(1.0, None, menor_e_melhor=True, ha_anterior=False), PRIMEIRA)

    def test_release_anterior_sem_valor_nao_compara(self):
        self.assertEqual(caracteristicas.sentido(1.0, None, menor_e_melhor=True, ha_anterior=True), SEM_COMPARACAO)


class CaracteristicasPorReleaseTest(unittest.TestCase):
    def setUp(self):
        self.hist = historico(
            security_rating=serie(("2026-09-17T20:50:27+0000", "1.0")),
            vulnerabilities=serie(("2026-09-17T20:50:27+0000", "0")),
            security_hotspots=serie(("2026-09-17T20:50:27+0000", "0")),
            reliability_rating=serie(("2026-09-17T20:50:27+0000", "1.0"), ("2026-10-26T05:21:45+0000", "3.0"),
                                     ("2026-11-10T02:52:31+0000", "1.0")),
            bugs=serie(("2026-09-17T20:50:27+0000", "0"), ("2026-10-26T05:21:45+0000", "4")),
            sqale_rating=serie(("2026-09-17T20:50:27+0000", "1.0"), ("2026-10-26T05:21:45+0000", "2.0")),
            code_smells=serie(("2026-09-17T20:50:27+0000", "3"), ("2026-10-26T05:21:45+0000", "20")),
            coverage=serie(("2026-09-17T20:50:27+0000", "95.0"), ("2026-10-26T05:21:45+0000", "82.0"),
                           ("2026-11-10T02:52:31+0000", "98.3")),
            tests=serie(("2026-09-17T20:50:27+0000", "100"), ("2026-11-10T02:52:31+0000", "1158")),
        )
        self.releases = caracteristicas.calcular(self.hist, RELEASES, hoje=HOJE)

    def test_so_aparecem_as_releases_que_ja_comecaram(self):
        self.assertEqual([r["release"] for r in self.releases], ["R1", "R2", "R3"])

    def test_cada_release_traz_as_quatro_caracteristicas_na_ordem_do_plano(self):
        for release in self.releases:
            self.assertEqual([c["chave"] for c in release["caracteristicas"]],
                             ["seguranca", "confiabilidade", "manutenibilidade", "testabilidade"])
            self.assertEqual([c["nome"] for c in release["caracteristicas"]],
                             ["Segurança", "Confiabilidade", "Manutenibilidade", "Testabilidade"])

    def test_a_release_em_andamento_e_marcada(self):
        self.assertEqual([r["em_andamento"] for r in self.releases], [False, False, True])

    def test_confiabilidade_cai_na_r2_e_se_recupera_na_r3(self):
        r1, r2, r3 = (por_chave(r)["confiabilidade"] for r in self.releases)

        self.assertEqual((r1["nota"], r1["faixa"], r1["sentido"]), ("A", ADEQUADO, PRIMEIRA))
        self.assertEqual((r2["nota"], r2["faixa"], r2["sentido"]), ("C", CRITICO, PIOROU))
        self.assertEqual((r3["nota"], r3["faixa"], r3["sentido"]), ("A", ADEQUADO, MELHOROU))

    def test_manutenibilidade_na_r2_pede_atencao(self):
        r2 = por_chave(self.releases[1])["manutenibilidade"]

        self.assertEqual((r2["nota"], r2["faixa"], r2["sentido"]), ("B", ATENCAO, PIOROU))

    def test_testabilidade_usa_a_cobertura_e_mostra_o_total_de_testes(self):
        r2 = por_chave(self.releases[1])["testabilidade"]
        r3 = por_chave(self.releases[2])["testabilidade"]

        self.assertEqual((r2["valor"], r2["faixa"], r2["sentido"]), (82.0, ATENCAO, PIOROU))
        self.assertEqual((r3["valor"], r3["faixa"], r3["sentido"]), (98.3, ADEQUADO, MELHOROU))
        self.assertEqual(r3["apoio"]["tests"], 1158.0)

    def test_testabilidade_diz_que_o_nivel_do_teste_nao_e_medido(self):
        testabilidade = por_chave(self.releases[2])["testabilidade"]

        self.assertFalse(testabilidade["niveis_medidos"])
        self.assertIn("unitário", testabilidade["observacao"])
        self.assertIn("integração", testabilidade["observacao"])

    def test_seguranca_diz_que_hotspots_revisados_nao_sao_coletados(self):
        seguranca = por_chave(self.releases[0])["seguranca"]

        self.assertEqual(seguranca["nota"], "A")
        self.assertIn("hotspots revisados", seguranca["observacao"])
        self.assertEqual(seguranca["apoio"]["vulnerabilities"], 0.0)
        self.assertEqual(seguranca["apoio"]["security_hotspots"], 0.0)

    def test_o_apoio_vem_da_mesma_data_da_nota(self):
        r2 = por_chave(self.releases[1])["confiabilidade"]

        self.assertEqual(r2["apoio"]["bugs"], 4.0)


class NaoMedidaTest(unittest.TestCase):
    def test_sem_historico_nenhuma_caracteristica_e_medida(self):
        releases = caracteristicas.calcular({}, RELEASES, hoje=HOJE)

        for release in releases:
            for c in release["caracteristicas"]:
                self.assertEqual(c["faixa"], NAO_MEDIDA)
                self.assertIsNone(c["valor"])
                self.assertIsNone(c["nota"])

    def test_release_anterior_ao_primeiro_ponto_fica_nao_medida_sem_virar_zero(self):
        hist = historico(security_rating=serie(("2026-10-14T00:00:00+0000", "1.0")))

        r1, r2, _ = caracteristicas.calcular(hist, RELEASES, hoje=HOJE)

        self.assertEqual(por_chave(r1)["seguranca"]["faixa"], NAO_MEDIDA)
        self.assertIsNone(por_chave(r1)["seguranca"]["valor"])
        self.assertEqual(por_chave(r2)["seguranca"]["faixa"], ADEQUADO)

    def test_projeto_sem_cobertura_nao_mede_a_testabilidade(self):
        hist = historico(tests=serie(("2026-09-17T20:50:27+0000", "10")))

        testabilidade = por_chave(caracteristicas.calcular(hist, RELEASES, hoje=HOJE)[0])["testabilidade"]

        self.assertEqual(testabilidade["faixa"], NAO_MEDIDA)
        self.assertIsNone(testabilidade["valor"])

    def test_comparacao_com_release_sem_medida_nao_inventa_sentido(self):
        hist = historico(security_rating=serie(("2026-10-14T00:00:00+0000", "1.0")))

        r2 = por_chave(caracteristicas.calcular(hist, RELEASES, hoje=HOJE)[1])["seguranca"]

        self.assertEqual(r2["sentido"], SEM_COMPARACAO)


class DetalheTest(unittest.TestCase):
    def test_o_detalhe_traz_todas_as_metricas_do_historico_na_data_da_release(self):
        hist = historico(
            ncloc=serie(("2026-09-17T20:50:27+0000", "1000"), ("2026-11-10T02:52:31+0000", "7676")),
            coverage=serie(("2026-09-17T20:50:27+0000", "95.0")),
        )

        r1, _, r3 = caracteristicas.calcular(hist, RELEASES, hoje=HOJE)

        self.assertEqual(r1["detalhe"], {"ncloc": 1000.0, "coverage": 95.0})
        self.assertEqual(r3["detalhe"]["ncloc"], 7676.0)

    def test_o_detalhe_omite_a_metrica_sem_valor_na_release(self):
        hist = historico(ncloc=serie(("2026-11-10T02:52:31+0000", "7676")))

        r1 = caracteristicas.calcular(hist, RELEASES, hoje=HOJE)[0]

        self.assertNotIn("ncloc", r1["detalhe"])


class CarregarHistoricoTest(unittest.TestCase):
    def test_le_o_historico_do_json_de_medidas_do_sonar(self):
        dados = {"historico": [
            {"metric": "coverage", "history": [{"date": "2026-09-17T20:50:27+0000", "value": "95.0"}]},
            {"metric": "bugs", "history": []},
        ]}

        self.assertEqual(caracteristicas.historico_por_metrica(dados), {
            "coverage": [{"date": "2026-09-17T20:50:27+0000", "value": "95.0"}], "bugs": []})

    def test_a_ultima_coleta_entra_como_o_ponto_mais_recente(self):
        dados = {
            "coletado_em": "2026-11-12T09:12:25Z",
            "medidas": {"coverage": "98.3", "alert_status": "OK"},
            "historico": [{"metric": "coverage", "history": [{"date": "2026-11-10T02:38:20+0000", "value": "97.0"}]}],
        }

        historico = caracteristicas.historico_por_metrica(dados)

        self.assertEqual(caracteristicas.valor_ate(historico["coverage"], datetime(2027, 1, 1, tzinfo=timezone.utc)), 98.3)
        self.assertIsNone(caracteristicas.valor_ate(historico["alert_status"], datetime(2027, 1, 1, tzinfo=timezone.utc)))

    def test_json_sem_historico_devolve_vazio(self):
        self.assertEqual(caracteristicas.historico_por_metrica({}), {})
        self.assertEqual(caracteristicas.historico_por_metrica(None), {})
        self.assertEqual(caracteristicas.historico_por_metrica({"historico": [{"history": []}]}), {})


if __name__ == "__main__":
    unittest.main()
