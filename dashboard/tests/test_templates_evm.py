import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.templates import dados_dos_indices, tabela_de_custo_por_release  # noqa: E402


def release(id_, spi, cpi, prp=74.0, rpc=0.0, bac=1000.0, acumulado=1000.0, aguardando=0.0):
    return {"id": id_, "spi": spi, "cpi": cpi, "prp": prp, "rpc": rpc, "rpc_aguardando": aguardando,
            "bac": bac, "orcamento_acumulado": acumulado}


class DadosDosIndicesTest(unittest.TestCase):
    def test_spi_e_cpi_iguais_viram_um_indice_so(self):
        dados = dados_dos_indices([release("R1", 0.8, 0.8, rpc=10), release("R2", 1.1, 1.1, rpc=20)])

        self.assertTrue(dados["iguais"])
        self.assertEqual(dados["releases"], ["R1", "R2"])

    def test_spi_e_cpi_diferentes_continuam_separados(self):
        dados = dados_dos_indices([release("R1", 0.8, 0.9, rpc=10)])

        self.assertFalse(dados["iguais"])

    def test_release_sem_indice_fica_de_fora(self):
        dados = dados_dos_indices([release("R1", None, None), release("R2", 1.0, 1.0, rpc=5)])

        self.assertEqual(dados["releases"], ["R2"])

    def test_sem_nenhum_indice_a_lista_vem_vazia(self):
        dados = dados_dos_indices([release("R1", None, None)])

        self.assertEqual(dados["releases"], [])
        self.assertEqual(dados["topo"], 1.5)

    def test_indice_zero_sem_entrega_diz_que_esta_aguardando_aceite(self):
        dados = dados_dos_indices([release("R2", 0.0, 0.0, prp=74, rpc=0, aguardando=61)])

        self.assertEqual(dados["aguardando_aceite"], [True])
        self.assertEqual(dados["rotulos_spi"], ["0.00 (aguardando aceite)"])

    def test_indice_zero_sem_nada_em_aceitacao_nao_e_espera_de_aceite(self):
        # Nenhum ponto aceito e nenhum em Aceitação PO: é entrega zero de fato, e o rótulo não pode dizer que há espera.
        dados = dados_dos_indices([release("R2", 0.0, 0.0, prp=74, rpc=0, aguardando=0)])

        self.assertEqual(dados["aguardando_aceite"], [False])
        self.assertEqual(dados["rotulos_spi"], ["0.00"])

    def test_indice_com_entrega_nao_e_marcado_como_aguardando(self):
        dados = dados_dos_indices([release("R2", 0.5, 0.5, prp=74, rpc=20)])

        self.assertEqual(dados["aguardando_aceite"], [False])
        self.assertEqual(dados["rotulos_spi"], ["0.50"])

    def test_o_eixo_sempre_alcanca_a_referencia_1_0_com_folga(self):
        self.assertGreaterEqual(dados_dos_indices([release("R1", 0.2, 0.2, rpc=1)])["topo"], 1.5)

    def test_o_eixo_cresce_com_um_indice_alto(self):
        # 7,21 foi o SPI que a R3 chegou a mostrar na coleta de 30/10.
        dados = dados_dos_indices([release("R3", 7.21, 7.21, rpc=61)])

        self.assertGreater(dados["topo"], 7.21)


class TabelaDeCustoTest(unittest.TestCase):
    def test_mostra_o_bac_da_release_e_o_acumulado_do_projeto(self):
        tabela = tabela_de_custo_por_release([
            release("R1", None, None, bac=62746.77, acumulado=62746.77),
            release("R2", None, None, bac=12595.73, acumulado=75342.50),
        ])

        self.assertEqual(list(tabela["Release"]), ["R1", "R2"])
        self.assertEqual(tabela.loc[1, "Custo planejado da release (BAC)"], "R$ 12,595.73")
        self.assertEqual(tabela.loc[1, "Acumulado do projeto até a release"], "R$ 75,342.50")


if __name__ == "__main__":
    unittest.main()
