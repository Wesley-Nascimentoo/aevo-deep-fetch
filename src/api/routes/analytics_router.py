from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import List

# Services
from src.services.analytics_service import analytics_service
from src.services.external_user_service import external_user_service
from src.services.idea_service import idea_service

# Models
# IMPORTANTE: Importe o novo modelo combinado e o CreationAnalytics
from src.models.analytics_models import DepartmentAnalytics, CreationAnalytics, CombinedDepartmentReport

router = APIRouter(prefix="/analytics", tags=["Department Analytics"])

# MUDANÇA 1: O response_model agora é o Combinado
@router.get("/department/{department_id}", response_model=CombinedDepartmentReport)
async def get_department_analytics(
    department_id: int, 
    year: int = Query(..., description="The target year for analysis (e.g., 2025)")
):
    """
    Generates a complete performance report (Execution + Creation) for a specific department.
    """
    try:
        print(f"[API] Request received: Dept {department_id}, Year {year}")

        # 1. Fetch Users
        dept_users = external_user_service.get_users_by_department_recursive(department_id)
        
        if not dept_users:
            raise HTTPException(status_code=404, detail=f"No users found for Department {department_id}")

        # 2. Fetch Ideas (Starting 2024)
        PROGRAM_START_DATE = datetime(2024, 1, 1)
        end_date = datetime.now()

        print(f"[API] Fetching ideas from {PROGRAM_START_DATE} to {end_date}")
        all_ideas = idea_service.get_ideas_by_period(PROGRAM_START_DATE, end_date)

        # 3. Generate Execution Report
        report_execution = analytics_service.generate_department_summary(
            department_users=dept_users,
            all_ideas=all_ideas,
            target_year=year
        )
        
        # 4. Generate Creation/Ranking Report
        # Dica: Em produção, você pode querer mover essas metas "hardcoded" para variáveis de ambiente ou configs
        report_creation = analytics_service.generate_creation_ranking(
            department_users=dept_users,
            all_ideas=all_ideas,
            target_year=year,
            plr_target_per_user=4,
            dept_individual_target=14,
            monthly_target_aggregate=67,
            weekly_target_aggregate=15
        )

        # MUDANÇA 2: Retornar um objeto compatível com CombinedDepartmentReport
        # Isso cria um JSON: { "execution_analytics": {...}, "creation_analytics": {...} }
        return CombinedDepartmentReport(
            execution_analytics=report_execution,
            creation_analytics=report_creation
        )

    except Exception as e:
        print(f"[API Error] {str(e)}")
        # Importante: O print ajuda a debugar no console, mas o raise retorna o erro pro cliente (Postman/Browser)
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")