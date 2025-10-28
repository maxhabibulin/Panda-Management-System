import json
import copy
import data.services_data as services_data
from typing import Iterator

class ServicesManager:
   """
    Manages services: adding, finding, updating, removing, and storing them.

    The class can be reused across multiple projects. It supports category-based organization and allows saving/loading data to JSON files.

    Features:
    - Category-based service organization
    - Add, update, find, and remove services
    - Price and currency management
    - JSON import/export
    - Name normalization
    """

   # --- Constants for message and validation ---
   SERVICE_NOT_FOUND = "[Service not found]"
   SERVICE_DATA_NOT_FOUND = "[Existing service data not found]"
   PROVIDED_NOT_STR = "[Provided argument must be string]"
   NEGATIVE_NUM_NOT_ALLOWED = "[Negative number not allowed]"
   INVALID_JSON_STRUCTURE = "[Invalid JSON structure]"
   ERROR_DECODING_JSON = "[Error decoding JSON file]"

   # ---  Initialization ---
   def __init__(self, services: dict | None = None, field_name: str = "Panda Spa", default_currency: str = "EUR"):
      """ 
      Initialize a ServicesManager object.

      Args:
         services (dict | None): Optional custom service data. If None, 
                                 uses default services from `services_data`.
         field_name (str): The display name of the system.
      """
      self.field_name = field_name
      self.default_currency = default_currency
      self.services = copy.deepcopy(
         services if services is not None else services_data.services)

      self._apply_default_currency()


   # --- Magic methods ---
   def __len__(self) -> int:
      return sum(len(services) for services in self.services.values())
   
   def __iter__(self) -> Iterator[str]:
      for services in self.services.values():
         yield from services.keys()
   
   def __getitem__(self, service: str) -> dict:
      _, details = self._find_service_data(service)
      
      if not details:
        raise KeyError(f"Service '{service}' not found")
      
      return details
   
   def __setitem__(self, category: str, value: dict) -> None:
      if not isinstance(value, dict):
         raise TypeError("Service category value must be a dictionary")
      
      self.services[self._normalize_name(category)] = value

   def __delitem__(self, category: str) -> None:
      norm_name = self._normalize_name(category)

      if norm_name not in self.services:
         raise KeyError(f"Category \"{category}\" not found")
      
      del self.services[norm_name]

   def __contains__(self, service: str) -> bool:
      if not isinstance(service, str):
         return False
      
      norm_name = self._normalize_name(service)

      for services in self.services.values():
         if norm_name in services:
            return True
         
      return False

   def __eq__(self, other) -> bool:
      if not isinstance(other, ServicesManager):
         return NotImplemented
      
      return self.services == other.services

   def __bool__(self) -> bool:
      return bool(self.services)

   def __str__(self) -> str:
      total_services = sum(len(s) for s in self.services.values())

      return f"{self.field_name} - {len(self.services)} categories, {total_services} services"

   def __repr__(self) -> str:
      """
      Developer-friendly string representation of the object.

      Returns:
         str: Summary showing the field name, number of categories, and total services.
      """
      total_services = sum(len(s) for s in self.services.values())
      return (
         f"ServicesManager(field = '{self.field_name}', "
         f"categories = {len(self.services)}, services = {total_services})"
      )
   

   # --- Utility methods ---
   def _normalize_name(self, name: str) -> str:
      """ 
      Normalize service name to snake_case format.

      Converts user input like "User Input Value" into "user_input_value".

      Args:
         name (str): Service name input from user.

      Returns:
         str: Normalized service name in snake_case, or None if input is not string.
      """
      if not isinstance(name, str):
         return None
      return name.replace(" ", "_").lower()
   
   def _denormalize_name(self, name: str) -> str:
      """
      Convert normalized snake_case name back to human-readable title format.

      Converts internal format like "user_input_value" back to "User Input Value".

      Args:
         name (str): Normalized service name in snake_case.

      Returns:
         str: Human-readable service name in Title Case, or None if input is not string.
      """
      if not isinstance(name, str):
         return None
      return name.replace("_", " ").title()

   def _find_service_data(self, name: str) -> tuple[str | None, dict | None]:
      """
      Locate service in nested structure by name.

      Args:
         name (str): Name of the service to find.

      Returns:
         tuple[str | None, dict | None]: 
         - category (str): The category where the service is found.
         - details (dict): The service details with price, currency, duration, description.
         Returns (None, None) if not found or input invalid.
      """
      if not isinstance(name, str):
         return None, None
      
      norm_name = self._normalize_name(name)

      for category, services in self.services.items():
         for service_name, details in services.items():
            if service_name.lower() == norm_name:
               return category, details
            
      return None, None
   
   def _format_service(self, name: str, details: dict[str, str | int | float]) -> str:
      """
      Format service details into readable string representation.

      Args:
         name (str): Name of the service.
         details (dict): Service details with keys: price, currency, duration, description.

      Returns:
         str: Formatted string containing service details with emojis.
      """
      if not isinstance(name, str) or not isinstance(details, dict):
         return None
      
      return (
        f"{self._denormalize_name(name)}\n"
        f"  💰 Price: {details['price']} {details['currency']}\n"
        f"  ⏱️ Duration: {details['duration']} min\n"
        f"  🌿 Description: {details['description']}\n"
      )
   
   def _apply_default_currency(self) -> None:
      for category in self.services.values():
         for service in category.values():
            service["currency"] = self.default_currency

   def service_exists(self, service_name: str) -> bool:
      """
      Check if a given service exists in the system.

      Args:
         service_name (str): The name of the service (case-insensitive, spaces allowed).

      Returns:
         bool: True if the service exists, False otherwise.
      """
      if not isinstance(service_name, str):
         return False
      
      norm_name = self._normalize_name(service_name)
      result = self._find_service_data(norm_name)

      if not result:
         return False
      
      category, details = result

      return bool(category and details)


   # --- Core functionality ---
   def add_service(self, category: str, name: str, price: float, duration: int, description: str, currency: str = None) -> str:
      """
      Add a new service to the collection.

      Args:
         category (str): Category of the service.
         name (str): Name of the service.
         price (float): Price of the service.
         duration (int): Duration of the service in minutes.
         description (str): Short description of the service.
         currency (str, optional): Currency type. Defaults to "EUR".

      Returns:
         str: Success message or error message if validation fails.
      """
      if not all(isinstance(arg, str) for arg in [category, name, description, currency]):
         return self.PROVIDED_NOT_STR
      
      if not isinstance(price, (int, float)) or price < 0:
         return self.NEGATIVE_NUM_NOT_ALLOWED
      
      if not isinstance(duration, (int, float)) or duration <= 0:
         return self.NEGATIVE_NUM_NOT_ALLOWED
      
      norm_category = self._normalize_name(category)
      norm_name = self._normalize_name(name)

      if norm_category not in self.services:
         self.services[norm_category] = {}

      if norm_name in self.services[norm_category]:
         return f"[Service \"{name.title()}\" already exist in \"{category.title()}\"]"

      currency = currency if currency is not None else self.default_currency

      self.services[norm_category][norm_name] = {
         "price": price, 
         "currency": currency,
         "duration": duration, 
         "description": description
         }
      
      return f"[Service \"{name.title()}\" successfully added to \"{category.title()}\"]"
   
   def update_service(self, category: str, name: str, price: float | None = None, duration: int | None = None, description: str | None = None, currency: str | None = None) -> str:
      """
      Update existing service details.

      Args:
         category (str): Category of the service.
         name (str): Name of the service to update.
         price (float | None, optional): New price. Defaults to None.
         duration (int | None, optional): New duration in minutes. Defaults to None.
         description (str | None, optional): New description. Defaults to None.
         currency (str | None, optional): New currency. Defaults to None.

      Returns:
         str: Success message or error message if service not found or validation fails.
      """
      if not all(isinstance(arg, str) for arg in [category, name]):
         return self.PROVIDED_NOT_STR
      
      norm_category = self._normalize_name(category)
      norm_name = self._normalize_name(name)

      if norm_category not in self.services:
         return f"[Category \"{category.title()}\" not found]"
      
      if norm_name not in self.services[norm_category]:
         return f"[Service \"{name.title()}\" not found in \"{category.title()}\"]"
      
      service = self.services[norm_category][norm_name]

      if price is not None:
         if not isinstance(price, (int, float)) or price < 0:
            return self.NEGATIVE_NUM_NOT_ALLOWED
         service["price"] = price

      if duration is not None:
         if not isinstance(duration, (int, float)) or duration <= 0:
            return self.NEGATIVE_NUM_NOT_ALLOWED
         service["duration"] = duration

      if description is not None:
         if not isinstance(description, str):
            return self.PROVIDED_NOT_STR
         service["description"] = description

      if currency is not None:
         if not isinstance(currency, str):
            return self.PROVIDED_NOT_STR
         service["currency"] = currency

      return f"[Service \"{name.title()}\" in \"{category.title()}\" successfully updated]"

   def find_service(self, name: str) -> str:
      """
      Find and return formatted details of a service by name.

      Args:
         name (str): Name of the service to find.

      Returns:
         str: Formatted service details or error message if not found.
      """
      if not isinstance(name, str):
         return self.PROVIDED_NOT_STR
      
      category, details = self._find_service_data(name)

      if not category or not details:
         return self.SERVICE_NOT_FOUND
      
      return self._format_service(name, details)

   def get_service_data(self, name: str) -> dict | None:
      """
      _

      Args:
         _

      Returns:
         _
      """
      if not isinstance(name, str):
         return None
      
      _, details = self._find_service_data(name)

      return details

   def remove_service(self, name: str) -> str:
      """
      Remove a service by name.

      Args:
         name (str): Name of the service to remove.

      Returns:
         str: Success message or error message if service not found.
      """
      if not isinstance(name, str):
         return self.PROVIDED_NOT_STR
      
      category, details = self._find_service_data(name)

      if not category or not details:
         return self.SERVICE_NOT_FOUND
      
      norm_name = self._normalize_name(name)
      del self.services[category][norm_name]
      cat_disp = self._denormalize_name(category)

      return f"[Service \"{name.title()}\" removed successfully from \"{cat_disp}\"]"
   
   def update_service_price(self, name: str, new_price: float | None = None, currency: str | None = None) -> str: 
      """
      Update the price and/or currency of an existing service.

      Args:
         name (str): Name of the service to update.
         new_price (float | None, optional): New price value. Defaults to None.
         currency (str | None, optional): New currency type. Defaults to None.

      Returns:
         str: Success message or error message if service not found or input invalid.
      """
      if not isinstance(name, str):
         return self.PROVIDED_NOT_STR
   
      _, service = self._find_service_data(name)

      if not service:
         return self.SERVICE_NOT_FOUND
      
      if new_price is not None:
         if not isinstance(new_price, (int, float)) or new_price < 0:
            return self.NEGATIVE_NUM_NOT_ALLOWED
         service["price"] = new_price

      if currency is not None:
         if not isinstance(currency, str):
            return self.PROVIDED_NOT_STR
         service["currency"] = currency

      return f"[Price for \"{name.title()}\" updated to {service['price']} {service['currency']}]"
   
   def change_currency_for_all(self, new_currency: str) -> str:
      """
      Change the currency for all existing services.

      Args:
         new_currency (str): New currency type to apply (e.g., "USD", "DKK").

      Returns:
         str: Confirmation message or error if input type is invalid.
      """
      if not isinstance(new_currency, str):
         return self.PROVIDED_NOT_STR

      for category in self.services.values():
         for service in category.values():
            service["currency"] = new_currency

      self.default_currency = new_currency

      return f"[Currency changed to {new_currency} for all services]"

   def show_services(self) -> None:
      """
      Display all available categories and services in formatted view.
      """
      print(f"\n🌸 Welcome to {self.field_name} 🌸\n")

      for category, services in self.services.items():
         cat_disp = self._denormalize_name(category)
         print(f"\n🧺 {cat_disp}:")

         for name, details in services.items():
            name_disp = self._denormalize_name(name)
            print(self._format_service(name_disp, details))


   # --- JSON storage ---  
   def save_services_to_json(self, filename: str = "services.json") -> str:
      """
      Save all current services to a JSON file.

      Args:
         filename (str, optional): File name for saving. Defaults to "services.json".

      Returns:
         str: Confirmation message after saving.
      """
      with open(filename, "w", encoding="utf-8") as file:
         json.dump(self.services, file, indent=4, ensure_ascii=False)

      return f"[Services saved to \"{filename}\"]"
   
   def load_services_from_json(self, filename: str = "services.json") -> str:
      """
      Load services from a JSON file.

      Args:
         filename (str, optional): File name to load. Defaults to "services.json".

      Returns:
         str: Confirmation message or error if file is missing or invalid.
      """
      try:
         with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, dict):
               return self.INVALID_JSON_STRUCTURE
            
            self.services = data
            self._apply_default_currency()
            return f"[Services loaded from \"{filename}\"]"
         
      except FileNotFoundError:
         return self.SERVICE_DATA_NOT_FOUND
      
      except json.JSONDecodeError:
         return self.ERROR_DECODING_JSON