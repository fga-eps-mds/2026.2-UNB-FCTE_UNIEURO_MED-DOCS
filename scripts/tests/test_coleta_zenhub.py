import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import coleta_zenhub  # noqa: E402


def sprint(nome, issues, total=None):
    return {
        "name": nome,
        "state": "OPEN",
        "startAt": "2026-10-12T03:59:00Z",
        "endAt": "2026-10-26T02:59:00Z",
        "totalPoints": 21.0,
        "completedPoints": 0.0,
        "closedIssuesCount": 0,
        "id": f"sprint-{nome}",
        "issues": {"totalCount": len(issues) if total is None else total, "nodes": issues},
    }


def workspace(sprints, detalhadas):
    return {
        "displayName": "UNB/FCTE-UNIEURO/MED",
        "sprints": {"nodes": sprints},
        "issues_detalhadas": detalhadas,
    }


ISSUES = [
    {"id": "A", "number": 5, "estimate": {"value": 13.0}},
    {"id": "B", "number": 6, "estimate": None},
]


class MontarTest(unittest.TestCase):
    def test_sem_detalhe_mantem_o_formato_anterior(self):
        dados = coleta_zenhub.montar(workspace([sprint("Sprint 1", ISSUES)], False))

        resultado = dados["sprints_velocity"]["Sprint 1"]
        self.assertNotIn("issues", resultado)
        self.assertEqual(resultado["issues_total"], 2)
        self.assertEqual(resultado["issues_sem_estimativa"], 1)

    def test_com_detalhe_guarda_o_id_o_numero_e_a_estimativa_de_cada_issue(self):
        dados = coleta_zenhub.montar(workspace([sprint("Sprint 1", ISSUES)], True))

        self.assertEqual(
            dados["sprints_velocity"]["Sprint 1"]["issues"],
            [
                {"id": "A", "numero": 5, "estimativa": 13.0},
                {"id": "B", "numero": 6, "estimativa": None},
            ],
        )

    def test_sprint_sem_issues_tem_lista_vazia_quando_ha_detalhe(self):
        dados = coleta_zenhub.montar(workspace([sprint("Sprint 2", [])], True))

        self.assertEqual(dados["sprints_velocity"]["Sprint 2"]["issues"], [])


class ConsultarTest(unittest.TestCase):
    def consultar_com(self, aceita):
        """Simula a API: aceita só as consultas cujos campos de issue estão em `aceita`."""
        consultas = []

        def falsa(token, consulta, variaveis):
            if "scopeChange" in consulta:
                return {"node": {"scopeChange": {"nodes": []}}}
            consultas.append(consulta)
            if consulta not in [coleta_zenhub.construir_consulta(campos) for campos in aceita]:
                raise RuntimeError("Cannot query field")
            return {"workspace": workspace([sprint("Sprint 1", ISSUES)], False)}

        with mock.patch.object(coleta_zenhub, "executar", side_effect=falsa):
            with mock.patch("sys.stderr"):
                resultado = coleta_zenhub.consultar("token")
        return resultado, consultas

    def test_usa_a_consulta_mais_completa_quando_a_api_aceita(self):
        resultado, consultas = self.consultar_com(["id number", "id", ""])

        self.assertEqual(len(consultas), 1)
        self.assertIn("id number", consultas[0])
        self.assertTrue(resultado["issues_detalhadas"])

    def test_tenta_so_o_id_quando_a_api_recusa_o_numero(self):
        resultado, consultas = self.consultar_com(["id", ""])

        self.assertEqual(len(consultas), 2)
        self.assertNotIn("number", consultas[1])
        self.assertIn("estimate { value } id }", consultas[1])
        self.assertTrue(resultado["issues_detalhadas"])

    def test_volta_a_consulta_original_quando_a_api_recusa_os_campos_novos(self):
        resultado, consultas = self.consultar_com([""])

        self.assertEqual(len(consultas), 3)
        self.assertNotIn("__CAMPOS_ISSUE__", consultas[2])
        self.assertFalse(resultado["issues_detalhadas"])

    def test_propaga_o_erro_quando_nenhuma_consulta_e_aceita(self):
        with mock.patch.object(coleta_zenhub, "executar", side_effect=RuntimeError("fora do ar")):
            with mock.patch("sys.stderr"):
                with self.assertRaises(RuntimeError):
                    coleta_zenhub.consultar("token")


if __name__ == "__main__":
    unittest.main()
