from datetime import datetime
from src.services.idea_service import idea_service

def main():
    # 1. Define the period (Example: Last Month)
    start_period = datetime(2025, 1, 1, 0, 0, 0)
    end_period = datetime(2025, 12, 31, 23, 59, 59)

    print(f"Starting fetch for period: {start_period} to {end_period}")

    try:
        # Call the service passing ONLY the period
        all_ideas = idea_service.get_ideas_by_period(start_period, end_period)

        # Process results
        print("\n--- Summary ---")
        print(f"Total Ideas Found: {len(all_ideas)}")
        
        if all_ideas:
            first_idea = all_ideas[0]
            print(f"Example Idea: '{first_idea.title}' (ID: {first_idea.id})")
            print(f"Current Stage: {first_idea.current_stage_name}")
            print(f"Implementers: {len(first_idea.implementers)}")

    except Exception as error:
        print(f"Process failed: {error}")

if __name__ == "__main__":
    main()