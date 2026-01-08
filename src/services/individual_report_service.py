from typing import List, Optional
from collections import Counter
from datetime import datetime

from src.models.user_model import User
from src.models.idea_models import Idea
from src.models.analytics_models import StatusDistribution, IdeaBasicInfo
from src.models.individual_report_models import IndividualUserReport

class IndividualReportService:
    """
    Service responsible specifically for Individual Performance Reports.
    Isolated from Department Analytics.
    """

    # Palavras-chave para identificar status de conclusão
    IMPLEMENTATION_COMPLETED_KEYWORDS = ["implantada", "implantação", "implantacao", "validada", "concluida"]

    def generate_report(
        self,
        all_users: List[User],
        all_ideas: List[Idea],
        target_year: int,
        user_matricula: str
    ) -> Optional[IndividualUserReport]:
        
        # 1. Encontrar UUID do usuário pela Matrícula (UserName)
        target_user = next((u for u in all_users if u.username == user_matricula), None)
        
        if not target_user:
            print(f"[IndividualService] User with matricula '{user_matricula}' not found.")
            return None

        user_uuid = target_user.id
        
        # 2. Processar Ideias CRIADAS (Filtro: Criador + Ano)
        created_ideas = []
        for idea in all_ideas:
            if idea.created_at and idea.created_at.year == target_year and idea.creator_id == user_uuid:
                created_ideas.append(idea)
        
        # 3. Calcular Distribuição (Lógica local para isolamento)
        dist_list = self._calculate_distribution(created_ideas)

        # 4. Processar Ideias de IMPLANTAÇÃO (Filtro: Lista de Implantadores)
        pending_list = []
        completed_count = 0

        for idea in all_ideas:
            # Verifica se o usuário está na lista de implantadores
            is_implementer = any(imp.user_id == user_uuid for imp in idea.implementers)
            
            if is_implementer:
                status_lower = (idea.current_stage_name or "").lower()
                
                # Check 1: Já acabou?
                if any(k in status_lower for k in self.IMPLEMENTATION_COMPLETED_KEYWORDS):
                    completed_count += 1
                
                # Check 2: Está pendente? (Não acabou E Não foi cancelada/reprovada)
                elif "cancelada" not in status_lower and "reprovada" not in status_lower:
                    pending_list.append(
                        IdeaBasicInfo(
                            id=idea.id,
                            title=idea.title or "Sem Título",
                            status=idea.current_stage_name or "Unknown"
                        )
                    )

        # 5. Retornar Objeto Final
        return IndividualUserReport(
            user_matricula=user_matricula,
            user_name=target_user.full_name,
            target_year=target_year,
            created_count=len(created_ideas),
            created_status_distribution=dist_list,
            pending_implementation_count=len(pending_list),
            pending_implementation_list=pending_list,
            completed_implementation_count=completed_count
        )

    def _calculate_distribution(self, ideas: List[Idea]) -> List[StatusDistribution]:
        """Helper privado para contar status."""
        total = len(ideas)
        if total == 0: return []
        
        counter = Counter([i.current_stage_name or "Sem Status" for i in ideas])
        
        return [
            StatusDistribution(
                status_title=k,
                count=v,
                percentage=round((v / total) * 100, 2)
            )
            for k, v in counter.items()
        ]

# Instância Singleton para uso no main
individual_report_service = IndividualReportService()