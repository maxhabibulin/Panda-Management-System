from collections import Counter

class RecommendationsManager:

     # --- Constants for message and validation ---
    SERVICE_NOT_FOUND = "[Service not found]"
    APPOINTMENT_DATA_NOT_FOUND = "[Existing appointment data not found]"
    PROVIDED_NOT_INT = "[Provided argument must be integer]"
    NEGATIVE_NUM_NOT_ALLOWED = "[Negative number not allowed]"
    WRONG_ID_NUM_LEN = "[Phone ID must contain exactly 8 digits]"
    
    # --- Initialization ---
    def __init__(self, appointments_manager: object):
        self.appointments_manager = appointments_manager


    # --- Utility methods ---
    def _normalize_name(self, name: str) -> str:
        if not isinstance(name, str):
            return " "
        
        return name.replace("_", " ").title()
    
    def _validate_phone_id(self, phone_id: int) -> str | None:
        if not isinstance(phone_id, int):
            return self.PROVIDED_NOT_INT
        
        if phone_id < 0:
            return self.NEGATIVE_NUM_NOT_ALLOWED

        if len(str(phone_id)) != 8:
            return self.WRONG_ID_NUM_LEN
        
        if phone_id not in self.appointments_manager.appointments:
            return self.APPOINTMENT_DATA_NOT_FOUND
        
        return None

    # --- Core functionality ---
    def get_popular_services(self, top_n: int = 3) -> list[tuple[str, int]]:
        if not isinstance(top_n, int) or top_n <= 0:
            return []

        services = [
            details["service_name"] 
            for details in self.appointments_manager.appointments.values()
            if "service_name" in details
        ]

        if not services:
            return []

        service_counts = Counter(services)
        return service_counts.most_common(top_n)
    
    def recommend_for_customer(self, phone_id: int) -> None:
        validation_error = self._validate_phone_id(phone_id)

        if validation_error:
            print(validation_error)
            return 
        
        service_name = "service_name"
        appointments_values = self.appointments_manager.appointments.values() 

        target_appointment = self.appointments_manager.appointments[phone_id]
        target_first_name = target_appointment["first_name"]
        target_last_name = target_appointment["last_name"]
        
        customer_services = [
            details["service_name"]
            for details in appointments_values
            if (details["first_name"] == target_first_name and 
                details["last_name"] == target_last_name and
                service_name in details)
        ]

        all_services = [
            details["service_name"]
            for details in appointments_values
            if service_name in details
        ]

        untried_services = set(all_services) - set(customer_services)

        if not untried_services:
            print(f"[{target_first_name.title()} has tried all available services]")
            return
        
        popular_services = [s for s, _ in self.get_popular_services()]

        recommended_from_popular = [s for s in popular_services if s in untried_services]
        other_services = list(untried_services - set(recommended_from_popular))

        final_recommendations = recommended_from_popular + other_services[:3]

        customer_name = f"{target_first_name.title()} {target_last_name.title()}"

        print(
            f"\n🎯 Personal Recommendations for {customer_name}\n"
            f"{47 * "-"}"
        )

        if not final_recommendations:
            print(
                f"\n🐼 Wow! You've tried all our services! 🎉\n"
                f"Maybe it’s time to revisit your favorite relaxation session 💆‍♀️🍵\n"
                )

            favorite_services = [s for s, _ in self.get_popular_services(3) if s in set(customer_services)]

            for service in favorite_services:
                print(f"⭐ {self._normalize_name(service)}")
        else:
            for index, service in enumerate(final_recommendations[:5], 1):
                if service in recommended_from_popular:
                    print(f"{index}. {self._normalize_name(service)} 🔥")

                else:
                    print(f"{index}. {self._normalize_name(service)}")

        print(f"{47 * "-"}")

    def show_recommendations(self, top_n: int = 3) -> None:
        popular_services = self.get_popular_services(top_n)

        print(
            f"\n⭐️ Recommended Services ⭐️\n"
            f"{47 * "-"}"
        )

        if not popular_services:
            print("[No data available for recommendations]")
            return
        
        total_bookings = sum(Counter(
            details["service_name"]
            for details in self.appointments_manager.appointments.values()
            if "service_name" in details
        ).values())
        
        for index, (service, count) in enumerate(popular_services, 1):
            times = "time" if count == 1 else "times"

            percentage = (count / total_bookings) * 100 if total_bookings > 0 else 0

            norm_service_name = self._normalize_name(service)

            print(f"{index}. {norm_service_name:<20} (booked {count} {times}, {percentage:.1f}%)")

        print(f"{47 * "-"}")