import os
import json
import glob
from typing import Dict, List, Any, Tuple
from .config import RAW_DATA_DIR


def load_json_file(file_path: str) -> Any:
    """Lê um arquivo JSON com codificação UTF-8."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[DATA LAYER] Falha ao ler {file_path}: {e}")
        return None


def get_zenhub_sprints_data() -> Tuple[List[Dict[str, Any]], bool]:
    """
    Carrega dados das sprints do ZenHub ou dados estruturados mock de fallback.
    Retorna uma tupla (dados, is_mock).
    """
    zh_path = os.path.join(RAW_DATA_DIR, "zenhub_analytics.json")
    data = load_json_file(zh_path)

    if data and isinstance(data, dict):
        sprints = data.get("sprints_velocity", {})
        if sprints:
            result = []
            for name, info in sprints.items():
                result.append({
                    "name": name,
                    "delivered_sp": float(info.get("delivered_story_points", info.get("delivered_sp", 0.0))),
                    "points_added": float(info.get("points_added", 0.0)),
                    "status": info.get("state", "CLOSED").upper(),
                    "start_at": info.get("start_at"),
                    "end_at": info.get("end_at")
                })
            return result, False

    # Dados mock de exemplo para a DA-R1
    mock_data = [
        {"name": "Sprint 1", "delivered_sp": 10.0, "points_added": 0.0, "status": "CLOSED"},
        {"name": "Sprint 2", "delivered_sp": 14.0, "points_added": 3.0, "status": "CLOSED"},
        {"name": "Sprint 3", "delivered_sp": 13.0, "points_added": 0.0, "status": "CLOSED"},
        {"name": "Sprint 4", "delivered_sp": 16.0, "points_added": 0.0, "status": "ACTIVE"},
        {"name": "Sprint 5", "delivered_sp": 0.0, "points_added": 0.0, "status": "FUTURE"}
    ]
    return mock_data, True


def get_risks_data() -> Tuple[List[Dict[str, Any]], bool]:
    """
    Carrega os riscos mapeados do projeto ou dados estruturados mock de fallback.
    Retorna uma tupla (dados, is_mock).
    """
    risks_path = os.path.join(RAW_DATA_DIR, "riscos_analytics.json")
    data = load_json_file(risks_path)

    if data and isinstance(data, list):
        return data, False

    mock_risks = [
        {
            "id": "RSK-01",
            "titulo": "Complexidade de integração com modelo de Inteligência Artificial",
            "categoria": "Técnico",
            "probabilidade": 4,
            "impacto": 4,
            "estrategia": "Mitigar",
            "acao": "Desenvolver spikes e protótipos de integração nas Sprints iniciais."
        },
        {
            "id": "RSK-02",
            "titulo": "Atraso na validação de requisitos clínicos com o parceiro UNIEURO",
            "categoria": "Produto",
            "probabilidade": 3,
            "impacto": 4,
            "estrategia": "Prevenir",
            "acao": "Realizar reuniões quinzenais de alinhamento com os envolvidos."
        },
        {
            "id": "RSK-03",
            "titulo": "Curva de aprendizado da equipe MDS nas tecnologias Mobile/Web",
            "categoria": "Equipe",
            "probabilidade": 3,
            "impacto": 3,
            "estrategia": "Mitigar",
            "acao": "Pareamento técnico estruturado entre membros de EPS e MDS."
        },
        {
            "id": "RSK-04",
            "titulo": "Instabilidade ou limites de cota em serviços de nuvem e CI/CD",
            "categoria": "Infraestrutura",
            "probabilidade": 2,
            "impacto": 4,
            "estrategia": "Aceitar",
            "acao": "Monitorar uso de minutos do GitHub Actions."
        },
        {
            "id": "RSK-05",
            "titulo": "Sobrecarga de entregas concomitantes de outras disciplinas",
            "categoria": "Organizacional",
            "probabilidade": 4,
            "impacto": 3,
            "estrategia": "Monitorar",
            "acao": "Ajustar o planejamento de capacidade no Sprint Planning."
        }
    ]
    return mock_risks, True


def get_github_runs_data() -> Tuple[Dict[str, Any], bool]:
    """
    Carrega dados agregados das execuções de CI/CD do GitHub Actions ou dados mock.
    Retorna uma tupla (dados, is_mock).
    """
    pattern = os.path.join(RAW_DATA_DIR, "GitHub_API-Runs-*.json")
    files = glob.glob(pattern)
    
    total_runs = 0
    success_runs = 0
    durations = []
    
    for fpath in files:
        data = load_json_file(fpath)
        if data and "workflow_runs" in data:
            for run in data["workflow_runs"]:
                total_runs += 1
                if run.get("conclusion") == "success":
                    success_runs += 1
                
                if "created_at" in run and "updated_at" in run:
                    from datetime import datetime
                    try:
                        c_at = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
                        u_at = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
                        durations.append((u_at - c_at).total_seconds())
                    except Exception:
                        pass

    if total_runs == 0:
        mock_runs = {
            "total_runs": 28,
            "success_rate": 89.3,
            "avg_duration_min": 3.6,
            "recent_feedback_series": [4.2, 3.8, 3.5, 3.1, 3.6]
        }
        return mock_runs, True

    avg_min = (sum(durations) / len(durations) / 60) if durations else 3.5
    success_rate = (success_runs / total_runs * 100) if total_runs > 0 else 100.0

    real_runs = {
        "total_runs": total_runs,
        "success_rate": round(success_rate, 1),
        "avg_duration_min": round(avg_min, 1),
        "recent_feedback_series": [round(d / 60, 1) for d in durations[-10:]]
    }
    return real_runs, False