from src.services.external_user_service import external_user_service

def main():
    dept_id = 38
    try:
        users = external_user_service.get_users_by_department_recursive(dept_id)
        
        for user in users:

            print(f"Name: {user.full_name} | Role: {user.job_title}")
            print(f"Created at: {user.created_at.strftime('%d/%m/%Y')}")
            print(f"Dept Manager: {user.department.manager_id}")
            print("---")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()