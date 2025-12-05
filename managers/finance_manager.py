from data.expenses_data import expenses
from datetime import datetime

class FinanceManager:
    """
    Handle financial calculations.

    Includes:
    - Income calculation
    - Expense tracking
    - Net profit calculation
    - Summary report display
    """
     
    # --- Constants ---
    LINE_SEPARATOR = "-" * 40
    
    # --- Initialization ---
    def __init__(self, services_manager: object, appointments_manager: object):
        """
        Initialize FinanceManager.

        Args:
            services_manager (object): Provides service prices.
            appointments_manager (object): Provides appointment records.
        """
        self.services_manager = services_manager
        self.appointments_manager = appointments_manager
        self.expenses = expenses


    # --- Core functionality ---
    def get_total_income(self) -> float:
        """
        Calculate total income.

        Returns:
            float: Sum of all earned income from appointments.
        """
        income = 0.0

        for details in self.appointments_manager.appointments.values():
            service_name = details["service_name"]
            service_data = self.services_manager.get_service_data(service_name) or {}

            if service_data and "price" in service_data:
                income += service_data["price"]

        return round(income, 2)
    
    def get_total_expenses(self) -> float:
        """
        Calculate total expenses.

        Returns:
            float: Sum of all fixed expenses.
        """
        return sum(self.expenses.values())

    def get_net_profit(self) -> float:
        """
        Calculate net profit.

        Returns:
            float: Income minus expenses.
        """
        return round(self.get_total_income() - self.get_total_expenses(), 2)
    
    def show_finances(self) -> None:
        """
        Display a formatted financial report.

        Includes:
        - Income
        - Expenses
        - Net profit
        - Profit margin
        - Status and efficiency indicators
        """
        currency = self.services_manager.default_currency
        field_name = self.services_manager.field_name

        income = self.get_total_income()
        expenses = self.get_total_expenses()
        net_profit = self.get_net_profit()

        profit_margin = (net_profit / income * 100) if income > 0 else 0

        status_rules = [
            (net_profit > 0, "🟢", "Profitable"),
            (net_profit < 0, "🔴", "Loss Making"),
            (net_profit == 0, "⚪️", "Break Even"),
        ]

        status_icon, status_msg = next((icon, msg) for cond, icon, msg in status_rules if cond)


        efficiency_rules = [
            (profit_margin > 20, "🚀", "Highly Efficient"),
            (profit_margin > 10, "✅", "Efficient"),
            (profit_margin > 0, "⚠️", "Low Efficiency"),
            (profit_margin == 0, "➖", "Zero Margin"),
            (profit_margin < 0, "🆘", "Inefficient (Loss)")
        ]
        
        efficiency_icon, efficiency_msg = next((icon, msg) for cond, icon, msg in efficiency_rules if cond)
       
        print(
            f"\n🌸 {field_name} Financial Report 🌸\n"
            f"{status_icon} Status: {status_msg}\n"
            f"{efficiency_icon} Productivity: {efficiency_msg}\n"
            f"{self.LINE_SEPARATOR}"
            f"\n💰 Total Income:    {income:>10,.2f} {currency}"
            f"\n💸 Total Expenses:  {expenses:>10,.2f} {currency}"
            f"\n💵 Net Profit:      {net_profit:>10,.2f} {currency}"
            f"\n📊 Profit Margin:   {profit_margin:>9.1f}%"
            f"\n{self.LINE_SEPARATOR}"
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )