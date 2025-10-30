import copy
import json
import data.appointments_data as appointments_data
from datetime import datetime
from utils.validators import validate_phone_id
from utils.formatters import normalize_name, denormalize_name, parse_datetime

class AppointmentsManager:

    # --- Constants ---
    APPOINTMENTS_NOT_FOUND = "[Appointments not found]"
    APPOINTMENT_DATA_NOT_FOUND = "[Existing appointment data not found]"
    PROVIDED_NOT_STR = "[Provided argument must be string]"
    PAST_APPT_NOT_ALLOWED = "[Cannot create appointment in the past]"
    INVALID_DATE_FORMAT = "[Invalid date format. Use YYYY-MM-DD HH:MM or DD-MM-YYYY HH:MM]"
    INVALID_JSON_STRUCTURE = "[Invalid JSON structure]"
    ERROR_DECODING_JSON = "[Error decoding JSON file]"

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # --- Initialization ---
    def __init__(self, services_manager: object, appointments: dict | None = None):
        self.services_manager = services_manager
        self.appointments = copy.deepcopy(
            appointments if appointments is not None else appointments_data.appointments
        )


    #  --- Magic methods ---
    def __len__(self) -> int:
        return len(self.appointments)

    def __iter__(self):
        return iter(self.appointments)

    def __getitem__(self, phone_id: int) -> dict:
       if not isinstance(phone_id, int):
           raise TypeError("Phone ID must be an integer")
       
       if phone_id not in self.appointments:
           raise KeyError(f"Appointments with ID {phone_id} not found")
       
       return self.appointments[phone_id]

    def __setitem__(self, phone_id: int, details: dict) -> None:
        if not isinstance(phone_id, int):
            raise TypeError("Phone ID must be an integer")
        
        if not isinstance(details, dict):
            raise TypeError("Appointment details must be a dictionary")

        self.appointments[phone_id] = details

    def __delitem__(self, phone_id: int) -> None:
        if phone_id not in self.appointments:
            raise KeyError(f"Appointment with ID {phone_id} not found")

        del self.appointments[phone_id]

    def __eq__(self, other) -> bool:
        if not isinstance(other, AppointmentsManager):
            return NotImplemented
        
        return self.appointments == other.appointments

    def __contains__(self, phone_id: int) -> bool:
        return isinstance(phone_id, int) and phone_id in self.appointments

    def __bool__(self) -> bool:
        return bool(self.appointments)

    def __str__(self) -> str:
        return f"Total appointments: {len(self.appointments)}"

    def __repr__(self) -> str:
        total_appointments = len(self.appointments)
        upcoming_appointments = len([
            a for a in self.appointments.values()
            if a["date_time"] >= datetime.now()
        ])
        
        return (
            f"AppointmentsManager(appointments={total_appointments}, "
            f"upcoming_appointments={upcoming_appointments})"
        )


    # --- Utility methods ---
    def _find_appointment_data(self, phone_id: int) -> tuple[int | None, dict | None]:
        if validate_phone_id(phone_id) or phone_id not in self.appointments:
            return None, None

        return phone_id, self.appointments[phone_id]

    def _format_appointment(self, phone_id: int, details: dict[str, str]) -> str:
        if not isinstance(phone_id, int) or not isinstance(details, dict):
            return self.APPOINTMENT_DATA_NOT_FOUND

        full_name = normalize_name(f"{details['first_name']} {details['last_name']}")
        
        return (
            f"\n🪪 ID: {phone_id}"
            f"\n👤 Name: {full_name}"
            f"\n💆 Service: {normalize_name(details['service_name'])}"
            f"\n🕒 Date: {details['date_time'].strftime('%Y-%m-%d %H:%M')}"
        )


    # --- Core functionality ---
    def add_appointment(self, phone_id: int, firstname: str, lastname: str, service_name: str, date_time: str) -> str:
        if not all(isinstance(arg, str) for arg in [firstname, lastname, service_name, date_time]):
            return self.PROVIDED_NOT_STR

        validation_error = validate_phone_id(phone_id)

        if validation_error:
            return validation_error
        
        if phone_id in self.appointments:
            return f"[Appointment for \"ID: {phone_id}\" already exist]"
        
        if not self.services_manager.service_exists(service_name):
            return f"[Service \"{service_name.title()}\" not found]"
        
        date_time_parsed = parse_datetime(date_time)

        if not date_time_parsed:
            return self.INVALID_DATE_FORMAT
        
        if date_time_parsed < datetime.now():
            return self.PAST_APPT_NOT_ALLOWED
        
        norm_service_name = normalize_name(service_name)

        self.appointments[phone_id] = {
            "first_name": firstname.lower(),
            "last_name": lastname.lower(),
            "service_name": norm_service_name,
            "date_time": date_time_parsed
        }

        return f"[Appointment \"ID: {phone_id}\" successfully added]"
        
    def update_appointment(self, phone_id: int, firstname: str | None = None, lastname: str | None = None, service_name: str | None = None, date_time: str | None = None) -> str:
        validation_error = validate_phone_id(phone_id)

        if validation_error:
            return validation_error

        if phone_id not in self.appointments:
            return self.APPOINTMENT_DATA_NOT_FOUND
        
        appointment = self.appointments[phone_id]

        if firstname is not None:
            if not isinstance(firstname, str):
                return self.PROVIDED_NOT_STR
            appointment["first_name"] = firstname.lower()

        if lastname is not None:
            if not isinstance(lastname, str):
                return self.PROVIDED_NOT_STR
            appointment["last_name"] = lastname.lower()

        if service_name is not None:
            if not self.services_manager.service_exists(service_name):
                return f"[Service \"{service_name.title()}\" not found]"
            
            norm_service_name = normalize_name(service_name)
            appointment["service_name"] = norm_service_name

        if date_time is not None:
            date_time_parsed = parse_datetime(date_time)

            if not date_time_parsed:
                return self.INVALID_DATE_FORMAT
            
            if date_time_parsed < datetime.now():
                return self.PAST_APPT_NOT_ALLOWED
            
            appointment["date_time"] = date_time_parsed
        
        return f"[Appointment \"ID: {phone_id}\" successfully updated]"

    def find_appointment(self, phone_id: int) -> str:
        validation_error = validate_phone_id(phone_id)

        if validation_error:
            return validation_error

        if phone_id not in self.appointments:
            return self.APPOINTMENT_DATA_NOT_FOUND
        
        ph_id, details = self._find_appointment_data(phone_id)

        return self._format_appointment(ph_id, details)

    def remove_appointment(self, phone_id: int) -> str:
        validation_error = validate_phone_id(phone_id)

        if validation_error:
            return validation_error

        if phone_id not in self.appointments:
            return self.APPOINTMENT_DATA_NOT_FOUND
        
        del self.appointments[phone_id]

        return f"[Appointment for \"ID: {phone_id}\" removed successfully]"

    def show_appointments(self, include_past: bool = False) -> None:
        if not self.appointments:
            print(self.APPOINTMENTS_NOT_FOUND)
            return
        
        now = datetime.now()

        data = (
            self.appointments
            if include_past
            else {phone_id: details for phone_id, details in self.appointments.items() 
                  if details["date_time"] >= now}
        )

        if not data:
            print(
                "[No upcoming appointments]"
                if not include_past 
                else self.APPOINTMENTS_NOT_FOUND
            )
            return
        
        sorted_appointments = sorted(
            data.items(), 
            key=lambda item: item[1]["date_time"]
        )

        current_date = None

        for phone_id, details in sorted_appointments:
            appointment_date = details["date_time"].date()

            if appointment_date != current_date:
                current_date = appointment_date
                print(f"\n{"-" * 25}\n📅 {current_date.strftime('%Y-%m-%d')}")

            print(self._format_appointment(phone_id, details))


    # -- JSON storage --
    def save_appointments_to_json(self, filename: str = "appointments.json") -> str:
        serializable_data = {}

        for phone_id, details in self.appointments.items():
            serializable_data[phone_id] = details.copy()
            serializable_data[phone_id]["date_time"] = details["date_time"].strftime(self.DATE_FORMAT)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(serializable_data, file, indent=4, ensure_ascii=False)
        
        return f"[Appointments saved to \"{filename}\"]"

    def load_appointments_from_json(self, filename: str = "appointments.json") -> str:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                if not isinstance(data, dict):
                    return self.INVALID_JSON_STRUCTURE
            
                fixed_data = {}

                for phone_id, details in data.items():
                    fixed_data[int(phone_id)] = details
                    details["date_time"] = datetime.strptime(details["date_time"], self.DATE_FORMAT)

                self.appointments = fixed_data
                return f"[Appointments loaded from \"{filename}\"]"

        except FileNotFoundError:
            return self.APPOINTMENT_DATA_NOT_FOUND
        
        except json.JSONDecodeError:
            return self.ERROR_DECODING_JSON