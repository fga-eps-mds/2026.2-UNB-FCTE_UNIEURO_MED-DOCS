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

    def test_com_coluna_guarda_a_coluna_atual_de_cada_issue(self):
        com_coluna = [
            {"id": "A", "number": 5, "estimate": {"value": 13.0},
             "pipelineIssue": {"pipeline": {"name": "Aceitação PO"}}},
            {"id": "B", "number": 6, "estimate": {"value": 3.0}, "pipelineIssue": None},
        ]
        ws = workspace([sprint("Sprint 1", com_coluna)], True)
        ws["issues_com_coluna"] = True

        issues = coleta_zenhub.montar(ws)["sprints_velocity"]["Sprint 1"]["issues"]

        self.assertEqual([i["coluna"] for i in issues], ["Aceitação PO", None])

    def test_com_estado_guarda_se_a_issue_esta_fechada(self):
        com_estado = [
            {"id": "A", "number": 5, "estimate": {"value": 13.0}, "state": "CLOSED",
             "pipelineIssue": {"pipeline": {"name": "Aceitação PO"}}},
            {"id": "B", "number": 46, "estimate": {"value": 8.0}, "state": "OPEN",
             "pipelineIssue": {"pipeline": {"name": "Aceitação PO"}}},
        ]
        ws = workspace([sprint("Sprint 5", com_estado)], True)
        ws["issues_com_coluna"] = True

        issues = coleta_zenhub.montar(ws)["sprints_velocity"]["Sprint 5"]["issues"]

        self.assertEqual([i["fechada"] for i in issues], [True, False])
        self.assertEqual([i["coluna"] for i in issues], ["Aceitação PO", "Aceitação PO"])

    def test_sem_estado_a_issue_nao_ganha_o_campo(self):
        issues = coleta_zenhub.montar(workspace([sprint("Sprint 1", ISSUES)], True))["sprints_velocity"]["Sprint 1"]["issues"]

        self.assertTrue(all("fechada" not in i for i in issues))

    def test_pede_o_estado_na_primeira_variante_e_mantem_as_anteriores(self):
        self.assertIn("state", coleta_zenhub.VARIANTES_ISSUE[0])
        self.assertIn(f"id number {coleta_zenhub.CAMPO_COLUNA}", coleta_zenhub.VARIANTES_ISSUE)

    def test_sem_coluna_coletada_a_issue_nao_ganha_o_campo(self):
        dados = coleta_zenhub.montar(workspace([sprint("Sprint 1", ISSUES)], True))

        self.assertTrue(all("coluna" not in i for i in dados["sprints_velocity"]["Sprint 1"]["issues"]))

    def test_sprint_sem_issues_tem_lista_vazia_quando_ha_detalhe(self):
        dados = coleta_zenhub.montar(workspace([sprint("Sprint 2", [])], True))

        self.assertEqual(dados["sprints_velocity"]["Sprint 2"]["issues"], [])


def coluna(nome, *issues, total=None):
    return {
        "name": nome,
        "issues": {
            "totalCount": len(issues) if total is None else total,
            "nodes": [{"id": id_, "number": numero} for id_, numero in issues],
        },
    }


class ColunasColetadasTest(unittest.TestCase):
    def test_o_json_diz_se_a_coluna_foi_coletada_e_por_qual_forma(self):
        ws = workspace([sprint("Sprint 1", ISSUES)], True)
        ws.update(issues_com_coluna=True, colunas_fonte="workspace", colunas_por_id={"A": "Aceitação PO"})

        dados = coleta_zenhub.montar(ws)

        self.assertTrue(dados["colunas_coletadas"])
        self.assertEqual(dados["colunas_fonte"], "workspace")

    def test_sem_a_coluna_o_json_diz_que_nao_foi_coletada(self):
        dados = coleta_zenhub.montar(workspace([sprint("Sprint 1", ISSUES)], True))

        self.assertFalse(dados["colunas_coletadas"])
        self.assertIsNone(dados["colunas_fonte"])

    def test_resume_as_issues_distintas_por_coluna(self):
        dados = {"sprints_velocity": {
            "Sprint 2": {"issues": [{"id": "A", "coluna": "Aceitação PO"}, {"id": "B", "coluna": "Em andamento"}]},
            "Sprint 3": {"issues": [{"id": "A", "coluna": "Aceitação PO"}, {"id": "C", "coluna": None}]},
            "Sprint 4": {},
        }}

        self.assertEqual(
            coleta_zenhub.resumir_colunas(dados),
            {"Aceitação PO": 1, "Em andamento": 1, "(coluna não identificada)": 1},
        )

    def test_buscar_colunas_recusa_a_resposta_sem_as_colunas(self):
        with mock.patch.object(coleta_zenhub, "executar", return_value={"workspace": {}}):
            with self.assertRaises(RuntimeError):
                coleta_zenhub.buscar_colunas("token")

    def test_buscar_colunas_ignora_issue_sem_id(self):
        resposta = {"workspace": {"pipelinesConnection": {"nodes": [
            {"name": "Aceitação PO", "issues": {"totalCount": 2, "nodes": [{"id": None, "number": 1}, {"id": "A", "number": 5}]}},
        ]}}}
        with mock.patch.object(coleta_zenhub, "executar", return_value=resposta):
            self.assertEqual(coleta_zenhub.buscar_colunas("token"), {"A": "Aceitação PO"})


class MainTest(unittest.TestCase):
    def rodar(self, workspace_coletado):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "zenhub_analytics.json"
            with mock.patch.dict(os.environ, {"ZENHUB_TOKEN": "token"}):
                with mock.patch.object(coleta_zenhub, "DESTINO", destino):
                    with mock.patch.object(coleta_zenhub, "consultar", return_value=workspace_coletado):
                        with mock.patch("builtins.print") as saida:
                            coleta_zenhub.main()
            return " ".join(str(c.args[0]) for c in saida.call_args_list if c.args), destino.read_text(encoding="utf-8")

    def test_o_log_mostra_as_issues_por_coluna_quando_a_coluna_foi_lida(self):
        ws = workspace([sprint("Sprint 1", [
            {"id": "A", "number": 5, "estimate": {"value": 8.0}, "pipelineIssue": {"pipeline": {"name": "Aceitação PO"}}},
        ])], True)
        ws.update(issues_com_coluna=True, colunas_fonte="issue")

        log, arquivo = self.rodar(ws)

        self.assertIn("forma: issue", log)
        self.assertIn("Aceitação PO: 1", log)
        self.assertIn('"colunas_coletadas": true', arquivo)

    def test_o_log_avisa_quando_a_coluna_nao_foi_coletada(self):
        log, arquivo = self.rodar(workspace([sprint("Sprint 1", ISSUES)], True))

        self.assertIn("a coluna das issues não foi coletada", log)
        self.assertIn('"colunas_coletadas": false', arquivo)


class ConsultarTest(unittest.TestCase):
    def consultar_com(self, aceita, colunas=None, esquema=None):
        """
        Simula a API. `aceita` lista os campos de issue que a consulta das sprints aceita.
        `colunas` são as colunas do workspace (None: a consulta é recusada). `esquema` mapeia
        o tipo para os nomes dos campos (None: a introspecção é recusada).
        """
        consultas = []
        self.chamadas = {"colunas": 0, "tipos": []}

        def falsa(token, consulta, variaveis):
            if "scopeChange" in consulta:
                return {"node": {"scopeChange": {"nodes": []}}}
            if "pipelinesConnection" in consulta:
                self.chamadas["colunas"] += 1
                if colunas is None:
                    raise RuntimeError("Cannot query field pipelinesConnection")
                return {"workspace": {"pipelinesConnection": {"nodes": colunas}}}
            if "__type" in consulta:
                self.chamadas["tipos"].append(variaveis["tipo"])
                if esquema is None:
                    raise RuntimeError("introspection is disabled")
                return {"__type": {"fields": [{"name": n} for n in esquema.get(variaveis["tipo"], [])]}}
            consultas.append(consulta)
            if consulta not in [coleta_zenhub.construir_consulta(campos) for campos in aceita]:
                raise RuntimeError("Cannot query field")
            return {"workspace": workspace([sprint("Sprint 1", ISSUES)], False)}

        with mock.patch.object(coleta_zenhub, "executar", side_effect=falsa):
            with mock.patch("builtins.print") as saida:
                resultado = coleta_zenhub.consultar("token")
        self.saida = " ".join(str(c.args[0]) for c in saida.call_args_list if c.args)
        return resultado, consultas

    def test_usa_a_consulta_mais_completa_quando_a_api_aceita(self):
        resultado, consultas = self.consultar_com(list(coleta_zenhub.VARIANTES_ISSUE))

        self.assertEqual(len(consultas), 1)
        self.assertIn("pipelineIssue", consultas[0])
        self.assertIn("id number state", consultas[0])
        self.assertTrue(resultado["issues_detalhadas"])
        self.assertTrue(resultado["issues_com_coluna"])

    def test_mantem_a_coluna_quando_a_api_recusa_so_o_estado(self):
        resultado, consultas = self.consultar_com([f"id number {coleta_zenhub.CAMPO_COLUNA}", "id number", "id", ""])

        self.assertEqual(len(consultas), 2)
        self.assertNotIn("id number state", consultas[1])
        self.assertIn("pipelineIssue", consultas[1])
        self.assertTrue(resultado["issues_com_coluna"])

    def test_tenta_sem_a_coluna_quando_a_api_recusa_o_campo(self):
        resultado, consultas = self.consultar_com(["id number", "id", ""])

        self.assertEqual(len(consultas), 3)
        self.assertNotIn("pipelineIssue", consultas[2])
        self.assertIn("id number", consultas[2])
        self.assertTrue(resultado["issues_detalhadas"])
        self.assertFalse(resultado["issues_com_coluna"])

    def test_tenta_so_o_id_quando_a_api_recusa_o_numero(self):
        resultado, consultas = self.consultar_com(["id", ""])

        self.assertEqual(len(consultas), 4)
        self.assertNotIn("number", consultas[3])
        self.assertIn("estimate { value } id }", consultas[3])
        self.assertTrue(resultado["issues_detalhadas"])
        self.assertFalse(resultado["issues_com_coluna"])

    def test_volta_a_consulta_original_quando_a_api_recusa_os_campos_novos(self):
        resultado, consultas = self.consultar_com([""])

        self.assertEqual(len(consultas), 5)
        self.assertNotIn("__CAMPOS_ISSUE__", consultas[4])
        self.assertFalse(resultado["issues_detalhadas"])
        self.assertFalse(resultado["issues_com_coluna"])

    def test_nao_le_pelo_workspace_quando_a_primeira_forma_funciona(self):
        todas = list(coleta_zenhub.VARIANTES_ISSUE)
        resultado, _ = self.consultar_com(todas, colunas=[coluna("Aceitação PO", ("A", 5))])

        self.assertEqual(resultado["colunas_fonte"], "issue")
        self.assertIsNone(resultado["colunas_por_id"])
        self.assertEqual(self.chamadas["colunas"], 0)

    def test_le_as_colunas_pelo_workspace_quando_a_primeira_forma_e_recusada(self):
        colunas = [coluna("Aceitação PO", ("A", 5)), coluna("Em andamento", ("B", 6))]

        resultado, _ = self.consultar_com(["id number", "id", ""], colunas=colunas)

        self.assertEqual(self.chamadas["colunas"], 1)
        self.assertEqual(resultado["colunas_fonte"], "workspace")
        self.assertTrue(resultado["issues_com_coluna"])
        self.assertEqual(resultado["colunas_por_id"], {"A": "Aceitação PO", "B": "Em andamento"})

    def test_a_coluna_lida_pelo_workspace_chega_as_issues_pelo_id(self):
        colunas = [coluna("Aceitação PO", ("A", 5))]
        resultado, _ = self.consultar_com(["id number", "id", ""], colunas=colunas)

        issues = coleta_zenhub.montar(resultado)["sprints_velocity"]["Sprint 1"]["issues"]

        self.assertEqual([(i["id"], i["coluna"]) for i in issues], [("A", "Aceitação PO"), ("B", None)])

    def test_nao_tenta_o_workspace_sem_o_detalhe_por_issue(self):
        resultado, _ = self.consultar_com([""], colunas=[coluna("Aceitação PO", ("A", 5))])

        self.assertEqual(self.chamadas["colunas"], 0)
        self.assertFalse(resultado["issues_com_coluna"])

    def test_avisa_quando_uma_coluna_tem_mais_issues_do_que_foram_lidas(self):
        colunas = [coluna("Aceitação PO", ("A", 5), total=150)]

        self.consultar_com(["id number", "id", ""], colunas=colunas)

        self.assertIn("'Aceitação PO' tem 150 issues e só 1 foram lidas", self.saida)

    def test_lista_os_campos_do_esquema_no_log_quando_as_duas_formas_falham(self):
        esquema = {"Issue": ["id", "number", "pipelineIssues"], "Pipeline": ["name", "issues"]}

        resultado, _ = self.consultar_com(["id number", "id", ""], esquema=esquema)

        self.assertFalse(resultado["issues_com_coluna"])
        self.assertIn("Leitura das colunas pelo workspace recusada", self.saida)
        self.assertIn("pelas duas formas", self.saida)
        self.assertIn("Esquema: campos de Issue: id, number, pipelineIssues", self.saida)
        self.assertIn("Esquema: campos de Pipeline: name, issues", self.saida)
        self.assertEqual(self.chamadas["tipos"], list(coleta_zenhub.TIPOS_DO_DIAGNOSTICO))

    def test_nao_faz_o_diagnostico_quando_a_coluna_foi_lida(self):
        self.consultar_com(["id number", "id", ""], colunas=[coluna("Aceitação PO", ("A", 5))])

        self.assertEqual(self.chamadas["tipos"], [])
        self.assertNotIn("Esquema:", self.saida)

    def test_o_diagnostico_nao_derruba_a_coleta_se_a_introspeccao_for_recusada(self):
        resultado, _ = self.consultar_com(["id number", "id", ""])

        self.assertFalse(resultado["issues_com_coluna"])
        self.assertIn("não foi possível listar os campos de Issue", self.saida)
        self.assertEqual(self.chamadas["tipos"], ["Issue"])

    def test_propaga_o_erro_quando_nenhuma_consulta_e_aceita(self):
        with mock.patch.object(coleta_zenhub, "executar", side_effect=RuntimeError("fora do ar")):
            with mock.patch("sys.stderr"):
                with self.assertRaises(RuntimeError):
                    coleta_zenhub.consultar("token")


if __name__ == "__main__":
    unittest.main()
