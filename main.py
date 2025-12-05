"""
Panda Spa - Command Line Interface

Main entry point for the Panda Spa Management System.
Provides a simple menu-driven interface to interact with all system modules.

Modules used:
- ServicesManager: Manage spa services
- AppointmentsManager: Handle client bookings  
- FinanceManager: Track income and expenses
- RecommendationsManager: Generate service suggestions

Usage:
Run this script to start the interactive CLI menu.
"""

import os
from managers.services_manager import ServicesManager
from managers.appointments_manager import AppointmentsManager
from managers.finance_manager import FinanceManager
from managers.recommendations_manager import RecommendationsManager


def main():
    # --- Initialize Managers ---
    services_manager = ServicesManager()
    appointments_manager = AppointmentsManager(services_manager)
    finance_manager = FinanceManager(services_manager, appointments_manager)
    recommendations_manager = RecommendationsManager(appointments_manager)

    menu = """
🐼 Panda Spa Internal Management System DEMO 🌿
----------------------------------------------
1.💆 View all services
2.📅 View all appointments
3.💰 Show financial report
4.🌟 Show popular recommendations
5.🎯 Get personal recommendations
0.🚪 Exit
----------------------------------------------
"""

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(menu)

        choice = input("Select option: ").strip()

        match choice:
            case "1":
                services_manager.show_services()

            case "2":
                appointments_manager.show_appointments()

            case "3":
                finance_manager.show_finances()

            case "4":
                recommendations_manager.show_recommendations()

            case "5":
                try:
                    phone_id = int(input("Enter 8-digit phone ID: "))
                    recommendations_manager.recommend_for_customer(phone_id)
                
                except ValueError:
                    print("[Invalid input: phone ID must be an integer]")
            
            case "0":
                print("\n Bye 🐼")
                break

            case _:
                print("[Invalid choice. Try again 🐼]")

        input("\n Press Enter to continue...")
                

if __name__ == "__main__":
    main() 