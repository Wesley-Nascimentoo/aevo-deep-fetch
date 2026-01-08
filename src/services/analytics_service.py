from typing import List, Dict, Optional, Tuple, Set
from collections import defaultdict, Counter
from datetime import datetime, timedelta

from src.models.user_model import User
from src.models.idea_models import Idea
from src.models.analytics_models import (
    DepartmentAnalytics, 
    UserRankingEntry, 
    IdeaStatusSummary, 
    StatusDistribution,
    TimelineMetric,
    CreationAnalytics, 
    UserCreationStats, 
    IdeaBasicInfo, 
    TimelineComparison
)

class AnalyticsService:
    
    # --- CONSTANTES ---
    APPROVAL_KEYWORDS = ["aprovadores", "aprovacao", "aprovação"]
    IN_IMPLEMENTATION_KEYWORDS = ["em implantacao", "em implantação", "execucao", "execução"]
    IMPLEMENTATION_KEYWORDS = ["implantada", "implantação", "implantacao", "validada", "concluida"]

    # =========================================================================
    # PART 1: FUNÇÕES GRANULARES (REUTILIZÁVEIS)
    # =========================================================================

    def filter_ideas_by_implementer_dept(self, all_ideas: List[Idea], dept_user_ids: Set[str]) -> List[Idea]:
        """Retorna apenas ideias onde pelo menos um implantador pertence ao set de IDs fornecido."""
        relevant_ideas = []
        for idea in all_ideas:
            for imp in idea.implementers:
                if imp.user_id in dept_user_ids:
                    relevant_ideas.append(idea)
                    break
        return relevant_ideas

    def calculate_status_distribution(self, ideas: List[Idea]) -> List[StatusDistribution]:
        """Calcula a porcentagem de distribuição dos status para uma lista de ideias."""
        total = len(ideas)
        if total == 0:
            return []
            
        counter = Counter([idea.current_stage_name or "Sem Status" for idea in ideas])
        
        dist = [
            StatusDistribution(
                status_title=k, 
                count=v, 
                percentage=round((v / total) * 100, 2)
            )
            for k, v in counter.items()
        ]
        dist.sort(key=lambda x: x.percentage, reverse=True)
        return dist

    def rank_implementers(self, ideas: List[Idea], dept_user_ids: Set[str], dept_user_map: Dict[str, str]) -> List[UserRankingEntry]:
        """Gera o ranking de usuários que atuaram como implantadores nas ideias fornecidas."""
        user_ideas_map = defaultdict(list)

        for idea in ideas:
            status = idea.current_stage_name or "Sem Status"
            for imp in idea.implementers:
                if imp.user_id in dept_user_ids:
                    user_ideas_map[imp.user_id].append(
                        IdeaStatusSummary(title=idea.title or "Sem Título", status=status)
                    )
        
        ranking = [
            UserRankingEntry(
                user_name=dept_user_map.get(uid, f"User {uid}"), 
                total_ideas=len(l), 
                ideas_summary=l
            )
            for uid, l in user_ideas_map.items()
        ]
        ranking.sort(key=lambda x: x.total_ideas, reverse=True)
        return ranking

    def calculate_implementation_timelines(self, ideas: List[Idea], target_year: int) -> Tuple[List[TimelineMetric], List[TimelineMetric]]:
        """
        Processa o funil de execução (Envio -> Validação -> Conclusão).
        Retorna tupla: (monthly_timeline, weekly_timeline)
        """
        now = datetime.now()
        ten_weeks_ago = now - timedelta(weeks=10)

        # Inicializar Buckets
        monthly_data = {f"{target_year}-{m:02d}": {"sent": 0, "sent_val": 0, "validated": 0} for m in range(1, 13)}
        weekly_data = {}
        for i in range(10):
            d = now - timedelta(weeks=i)
            weekly_data[f"{d.isocalendar().year}-W{d.isocalendar().week:02d}"] = {"sent": 0, "sent_val": 0, "validated": 0}

        for idea in ideas:
            # Identificar Etapas
            stage_aprovadores = None
            stage_em_implantacao = None
            stage_implantada = None

            for stage in idea.stages:
                label = (stage.label_pt or "").lower()
                if any(k in label for k in self.APPROVAL_KEYWORDS):
                    stage_aprovadores = stage
                if any(k in label for k in self.IN_IMPLEMENTATION_KEYWORDS):
                    stage_em_implantacao = stage
                if any(k in label for k in self.IMPLEMENTATION_KEYWORDS):
                    stage_implantada = stage

            # Preencher Buckets
            if stage_aprovadores and self._is_valid_date(stage_aprovadores.end_date):
                self._add_to_buckets(stage_aprovadores.end_date.replace(tzinfo=None), "sent", monthly_data, weekly_data, target_year, ten_weeks_ago)

            if stage_em_implantacao and self._is_valid_date(stage_em_implantacao.end_date):
                self._add_to_buckets(stage_em_implantacao.end_date.replace(tzinfo=None), "sent_val", monthly_data, weekly_data, target_year, ten_weeks_ago)

            if stage_implantada and self._is_valid_date(stage_implantada.start_date):
                self._add_to_buckets(stage_implantada.start_date.replace(tzinfo=None), "validated", monthly_data, weekly_data, target_year, ten_weeks_ago)

        return (self._dict_to_timeline_metric_list(monthly_data), self._dict_to_timeline_metric_list(weekly_data))

    def rank_creators(
        self, 
        department_users: List[User], 
        all_ideas: List[Idea], 
        target_year: int,
        plr_target: int,
        dept_target: int
    ) -> List[UserCreationStats]:
        """
        Rankeia usuários por ideias criadas no ano alvo. 
        Inclui usuários com 0 ideias.
        """
        # Inicializar todos com 0
        user_stats_map = {
            u.id: {"user_name": u.full_name, "ideas": []} 
            for u in department_users
        }
        
        # Preencher com ideias
        for idea in all_ideas:
            if not idea.created_at or not idea.creator_id:
                continue
            
            created_at = idea.created_at.replace(tzinfo=None)
            
            # Filtro: Ano Alvo e Usuário pertence ao mapa (departamento)
            if created_at.year == target_year and idea.creator_id in user_stats_map:
                user_stats_map[idea.creator_id]["ideas"].append(
                    IdeaBasicInfo(
                        id=idea.id,
                        title=idea.title or "Sem Título",
                        status=idea.current_stage_name or "Unknown"
                    )
                )

        # Converter para Lista de Objetos
        ranking_list = []
        for uid, data in user_stats_map.items():
            total = len(data["ideas"])
            ranking_list.append(UserCreationStats(
                user_id=uid,
                user_name=data["user_name"],
                total_sent=total,
                has_submitted_idea=(total > 0),
                hit_plr_target=(total >= plr_target),
                hit_dept_individual_target=(total >= dept_target),
                ideas=data["ideas"]
            ))
        
        ranking_list.sort(key=lambda x: x.total_sent, reverse=True)
        return ranking_list

    def calculate_creation_counts(self, all_ideas: List[Idea], dept_user_ids: Set[str], target_year: int) -> Tuple[Dict, Dict]:
        """
        Retorna dicionários com contagem crua de criação de ideias por mês e semana.
        Útil para montar timelines depois.
        """
        now = datetime.now()
        ten_weeks_ago = now - timedelta(weeks=10)
        
        monthly_data = {f"{target_year}-{m:02d}": 0 for m in range(1, 13)}
        weekly_data = {}
        for i in range(10):
            d = now - timedelta(weeks=i)
            weekly_data[f"{d.isocalendar().year}-W{d.isocalendar().week:02d}"] = 0

        for idea in all_ideas:
            if not idea.created_at or idea.creator_id not in dept_user_ids:
                continue
            
            created_at = idea.created_at.replace(tzinfo=None)

            # Mensal (Ano Alvo)
            if created_at.year == target_year:
                m_key = created_at.strftime("%Y-%m")
                if m_key in monthly_data:
                    monthly_data[m_key] += 1
            
            # Semanal (Últimas 10)
            if created_at >= ten_weeks_ago:
                iso_y, iso_w, _ = created_at.isocalendar()
                w_key = f"{iso_y}-W{iso_w:02d}"
                if w_key in weekly_data:
                    weekly_data[w_key] += 1
                    
        return monthly_data, weekly_data

    # =========================================================================
    # PART 2: ORQUESTRADORES DE RELATÓRIO
    # =========================================================================

    def generate_department_summary(
        self, 
        department_users: List[User], 
        all_ideas: List[Idea],
        target_year: int
    ) -> DepartmentAnalytics:
        
        # 1. Preparar IDs
        dept_user_ids = {u.id for u in department_users}
        dept_user_map = {u.id: u.full_name for u in department_users}
        
        # 2. Filtrar
        relevant_ideas = self.filter_ideas_by_implementer_dept(all_ideas, dept_user_ids)
        
        # 3. Calcular Componentes usando funções granulares
        ranking = self.rank_implementers(relevant_ideas, dept_user_ids, dept_user_map)
        dist = self.calculate_status_distribution(relevant_ideas)
        m_timeline, w_timeline = self.calculate_implementation_timelines(relevant_ideas, target_year)

        # 4. Montar Objeto
        return DepartmentAnalytics(
            total_ideas_analyzed=len(relevant_ideas),
            user_ranking=ranking,
            status_distribution=dist,
            monthly_timeline=m_timeline,
            weekly_timeline=w_timeline
        )

    def generate_creation_ranking(
        self,
        department_users: List[User],
        all_ideas: List[Idea],
        target_year: int,
        plr_target_per_user: int,
        dept_individual_target: int,
        monthly_target_aggregate: int,
        weekly_target_aggregate: int
    ) -> CreationAnalytics:
        
        dept_user_ids = {u.id for u in department_users}
        
        # 1. Ranking Individual
        user_ranking = self.rank_creators(
            department_users, all_ideas, target_year, plr_target_per_user, dept_individual_target
        )
        
        # 2. Contagens de Tempo
        raw_monthly, raw_weekly = self.calculate_creation_counts(all_ideas, dept_user_ids, target_year)
        
        # 3. Transformar Contagens em Objetos de Comparação com Meta
        monthly_timeline = [
            TimelineComparison(period=k, total_sent=v, target=monthly_target_aggregate, hit_target=(v >= monthly_target_aggregate))
            for k, v in raw_monthly.items()
        ]
        monthly_timeline.sort(key=lambda x: x.period)

        weekly_timeline = [
            TimelineComparison(period=k, total_sent=v, target=weekly_target_aggregate, hit_target=(v >= weekly_target_aggregate))
            for k, v in raw_weekly.items()
        ]
        weekly_timeline.sort(key=lambda x: x.period)

        return CreationAnalytics(
            target_year=target_year,
            user_ranking=user_ranking,
            monthly_timeline=monthly_timeline,
            weekly_timeline=weekly_timeline
        )

    # =========================================================================
    # PART 3: HELPERS PRIVADOS
    # =========================================================================

    def _is_valid_date(self, dt: Optional[datetime]) -> bool:
        if not dt or dt.year < 1900: return False
        return True

    def _add_to_buckets(self, dt, key, monthly, weekly, target_year, week_cutoff):
        # Mensal
        if dt.year == target_year:
            m_key = dt.strftime("%Y-%m")
            if m_key in monthly:
                monthly[m_key][key] += 1
        # Semanal
        if dt >= week_cutoff:
            iso_y, iso_w, _ = dt.isocalendar()
            w_key = f"{iso_y}-W{iso_w:02d}"
            if w_key in weekly:
                weekly[w_key][key] += 1

    def _dict_to_timeline_metric_list(self, d):
        lst = [
            TimelineMetric(
                period=k, 
                sent_to_implementation_count=v["sent"], 
                sent_for_validation_count=v["sent_val"], 
                validated_implementation_count=v["validated"]
            ) 
            for k, v in d.items()
        ]
        lst.sort(key=lambda x: x.period)
        return lst

analytics_service = AnalyticsService()