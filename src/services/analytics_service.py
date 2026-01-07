from typing import List, Dict, Optional
from collections import defaultdict, Counter
from datetime import datetime, timedelta

from src.models.user_model import User
from src.models.idea_models import Idea
# Importar os novos modelos
from src.models.analytics_models import (
    DepartmentAnalytics, UserRankingEntry, IdeaStatusSummary, StatusDistribution, TimelineMetric,
    # Novos:
    CreationAnalytics, UserCreationStats, IdeaBasicInfo, TimelineComparison
)

class AnalyticsService:
    
    # ... (Constantes e método generate_department_summary mantidos iguais) ...
    # ... (Reutilize o código anterior para a parte de implantação) ...
    
    # --- NOVO MÉTODO: RANKING DE ENVIO (CRIAÇÃO) ---
    def generate_creation_ranking(
        self,
        department_users: List[User],
        all_ideas: List[Idea],
        target_year: int,
        # Parâmetros de Metas
        plr_target_per_user: int,           # Meta individual PLR (ex: 1 ideia/ano)
        dept_individual_target: int,        # Meta individual Dept (ex: 3 ideias/ano)
        monthly_target_aggregate: int,      # Meta coletiva do dept por Mês
        weekly_target_aggregate: int        # Meta coletiva do dept por Semana
    ) -> CreationAnalytics:
        
        # 1. Preparação: Inicializar Todos os Usuários com 0
        # Isso garante que quem não mandou ideia apareça na lista com 0
        user_stats_map = {}
        for u in department_users:
            user_stats_map[u.id] = {
                "user_name": u.full_name,
                "ideas": []
            }

        # 2. Configurar Buckets de Tempo (Mensal e Semanal)
        now = datetime.now()
        ten_weeks_ago = now - timedelta(weeks=10)
        
        # Mensal (Ano Alvo)
        monthly_data = {f"{target_year}-{m:02d}": 0 for m in range(1, 13)}
        
        # Semanal (Últimas 10 semanas)
        weekly_data = {}
        for i in range(10):
            d = now - timedelta(weeks=i)
            key = f"{d.isocalendar().year}-W{d.isocalendar().week:02d}"
            weekly_data[key] = 0

        # 3. Processar Ideias
        # Filtramos apenas ideias criadas no ANO ALVO para o Ranking e Mensal
        # Mas para o Semanal precisamos checar a data independentemente do ano (caso vire o ano)
        
        for idea in all_ideas:
            # Ignora ideias sem data de criação
            if not idea.created_at:
                continue
                
            created_at = idea.created_at.replace(tzinfo=None)
            creator_id = idea.creator_id

            # --- A. Ranking Individual (Apenas Ano Alvo e Usuários do Dept) ---
            if created_at.year == target_year and creator_id in user_stats_map:
                user_stats_map[creator_id]["ideas"].append(
                    IdeaBasicInfo(
                        id=idea.id,
                        title=idea.title or "Sem Título",
                        status=idea.current_stage_name or "Unknown"
                    )
                )

            # --- B. Timeline Mensal (Apenas Ano Alvo e Criadores do Dept) ---
            if created_at.year == target_year and creator_id in user_stats_map:
                m_key = created_at.strftime("%Y-%m")
                if m_key in monthly_data:
                    monthly_data[m_key] += 1

            # --- C. Timeline Semanal (Últimas 10 semanas e Criadores do Dept) ---
            if created_at >= ten_weeks_ago and creator_id in user_stats_map:
                iso_y, iso_w, _ = created_at.isocalendar()
                w_key = f"{iso_y}-W{iso_w:02d}"
                if w_key in weekly_data:
                    weekly_data[w_key] += 1

        # 4. Construir Objetos de Resposta

        # A. Lista de Usuários
        ranking_list = []
        for uid, data in user_stats_map.items():
            total = len(data["ideas"])
            ranking_list.append(UserCreationStats(
                user_id=uid,
                user_name=data["user_name"],
                total_sent=total,
                has_submitted_idea=(total > 0),
                hit_plr_target=(total >= plr_target_per_user),
                hit_dept_individual_target=(total >= dept_individual_target),
                ideas=data["ideas"]
            ))
        
        # Ordenar por quem enviou mais
        ranking_list.sort(key=lambda x: x.total_sent, reverse=True)

        # B. Timelines
        monthly_timeline = [
            TimelineComparison(
                period=k,
                total_sent=v,
                target=monthly_target_aggregate,
                hit_target=(v >= monthly_target_aggregate)
            )
            for k, v in monthly_data.items()
        ]
        monthly_timeline.sort(key=lambda x: x.period)

        weekly_timeline = [
            TimelineComparison(
                period=k,
                total_sent=v,
                target=weekly_target_aggregate,
                hit_target=(v >= weekly_target_aggregate)
            )
            for k, v in weekly_data.items()
        ]
        weekly_timeline.sort(key=lambda x: x.period)

        return CreationAnalytics(
            target_year=target_year,
            user_ranking=ranking_list,
            monthly_timeline=monthly_timeline,
            weekly_timeline=weekly_timeline
        )

    # ... (Métodos auxiliares _is_valid_date etc) ...

analytics_service = AnalyticsService()