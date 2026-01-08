import requests
import json
from typing import List
from pydantic import TypeAdapter

from src.config import Config
from src.models.user_model import User

class ExternalUserService:
    """
    Service to fetch users and convert them directly into Pydantic models.
    """

    def get_users_by_department_recursive(self, department_id: int, current_page: int = 1, accumulated_users: List[User] = None) -> List[User]:
        """
        Recursively fetches users and returns a list of validated User objects.
        """
        if accumulated_users is None:
            accumulated_users = []

        try:
            # 1. Prepare Request
            filters = {
                "DepartamentoId": department_id,
                "Ativo": 1
            }
            
            params = {
                "token": Config.API_TOKEN,
                "filtros": json.dumps(filters),
                "pagina": current_page
            }

            print(f"[ExternalUserService] Fetching page {current_page} for Dept {department_id}...")

            # 2. Execute Request
            url = f"{Config.BASE_URL}/webapi/api/apiExterna/Usuarios"
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            api_data = response.json()

            # 3. Check 'sucesso' flag from supplier description
            if not api_data.get("sucesso"):
                raise Exception(f"API Error: {api_data.get('mensagem')}")

            # 4. Data Conversion (Dict -> Pydantic Model)
            raw_list = api_data.get("resultado", [])
            
            # Use TypeAdapter for efficient list validation (Pydantic V2 recommended way)
            # This ensures every item in the list matches the User schema
            user_adapter = TypeAdapter(List[User])
            new_users = user_adapter.validate_python(raw_list)
            
            # Alternatively, simple list comprehension works too:
            # new_users = [User(**item) for item in raw_list]

            accumulated_users.extend(new_users)

            # 5. Recursion Logic
            total_pages = api_data.get("numeroTotalPaginas", 1)
            current_api_page = api_data.get("paginaAtual", 1)

            if current_api_page < total_pages:
                return self.get_users_by_department_recursive(
                    department_id, 
                    current_page + 1, 
                    accumulated_users
                )

            print(f"[ExternalUserService] Finished. Retrieved {len(accumulated_users)} User objects.")
            return accumulated_users

        except Exception as e:
            print(f"[ExternalUserService] Failed: {e}")
            raise

external_user_service = ExternalUserService()