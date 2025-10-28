from data.expenses_data import expenses
from datetime import datetime

class FinanceManager:
    
    # --- Initialization ---
    def __init__(self, services_manager: object, appointments_manager: object):
        self.services_manager = services_manager
        self.appointments_manager = appointments_manager
        self.expenses = expenses


    # --- Core functionality ---
    def get_total_income(self) -> float:
        income = 0.0

        for details in self.appointments_manager.appointments.values():
            service_name = details["service_name"]
            service_data = self.services_manager.get_service_data(service_name)

            if service_data and "price" in service_data:
                income += service_data["price"]

        return round(income, 2)
    
    def get_total_expenses(self) -> float:
        return sum(self.expenses.values())

    def get_net_profit(self) -> float:
        return round(self.get_total_income() - self.get_total_expenses(), 2)
    
    def show_finances(self) -> None:
        currency = self.services_manager.default_currency
        field_name = self.services_manager.field_name

        income = self.get_total_income()
        expenses = self.get_total_expenses()
        net_profit = self.get_net_profit()

        profit_margin = (net_profit / income * 100) if income > 0 else 0

        status_msg = ("Profitable" if net_profit > 0 else 
                      "Loss Making" if net_profit < 0 else "Break Even")
        
        status_indic = ("🟢" if net_profit > 0 else 
                        "🔴" if net_profit < 0 else "⚪️")
        
        efficiency_msg = ("Highly Efficient" if profit_margin > 20 else 
                          "Efficient" if profit_margin > 10 else 
                          "Low Efficiency" if profit_margin > 0 else
                          "Zero Margin" if profit_margin == 0 else 
                          "Inefficient (Loss)")
        
        efficiency_indic = ("🚀" if profit_margin > 20 else 
                          "✅" if profit_margin > 10 else 
                          "⚠️" if profit_margin > 0 else 
                          "➖" if profit_margin == 0 else
                          "🆘")
       
        print(
            f"\n🌸 {field_name} Financial Report 🌸\n"
            f"{status_indic} Status: {status_msg}\n"
            f"{efficiency_indic} Productivity: {efficiency_msg}\n"
            f"{'-'*40}"
            f"\n💰 Total Income:    {income:>10,.2f} {currency}"
            f"\n💸 Total Expenses:  {expenses:>10,.2f} {currency}"
            f"\n💵 Net Profit:      {net_profit:>10,.2f} {currency}"
            f"\n📊 Profit Margin:   {profit_margin:>9.1f}%"
            f"\n{'-'*40}"
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )