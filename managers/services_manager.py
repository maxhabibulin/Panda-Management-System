import json
import copy
import data.services_data as services_data
from typing import Iterator
from utils.formatters import normalize_name, denormalize_name

class ServicesManager:
   """
   Manages services: adding, finding, updating, removing, and storing them.

   The class can be reused across multiple projects. 
   It supports category-based organization and allows saving/loading data to JSON files.

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
      Initialize the ServicesManager.

      Args:
         services (dict | None): Initial service data. If None, 
                                 default data is used.
         field_name (str): The display name of the system.
         default_currency (str): Currency applied to all services.
      """
      self.field_name = field_name
      self.default_currency = default_currency
      self.services = copy.deepcopy(
         services if services is not None else services_data.services)

      self._apply_default_currency()


   # --- Magic methods ---
   def __len__(self) -> int:
      """
      Return the number of services.
        
      Returns:
         int: Total count of services.
      """
      return sum(len(services) for services in self.services.values())
   
   def __iter__(self) -> Iterator[str]:
      """
      Iterate through all service names.

      Returns:
         Iterator[str]: Iterator over service names.
      """
      for services in self.services.values():
         yield from services.keys()
   
   def __getitem__(self, service: str) -> dict:
      """
      Get details of a service by name.

      Args:
         service (str): Service name.

      Returns:
            dict: Service details.

      Raises:
         KeyError: If the service is not found.
      """
      _, details = self._find_service_data(service)
      
      if not details:
        raise KeyError(f"Service '{service}' not found")
      
      return details
   
   def __setitem__(self, category: str, value: dict) -> None:
      """
      Assign a full category with services.

      Args:
         category (str): Category name.
         value (dict): Dictionary of services.

      Raises:
         TypeError: If value is not a dictionary.
      """
      if not isinstance(value, dict):
         raise TypeError("Service category value must be a dictionary")
      
      self.services[normalize_name(category)] = value

   def __delitem__(self, category: str) -> None:
      """
      Delete a category.

      Args:
         category (str): Category name.

      Raises:
         KeyError: If category does not exist.
      """
      norm_name = normalize_name(category)

      if norm_name not in self.services:
         raise KeyError(f"Category \"{category}\" not found")
      
      del self.services[norm_name]

   def __contains__(self, service: str) -> bool:
      """
      Check if a service exists.

      Args:
         service (str): Service name.

      Returns:
         bool: True if the service exists, False otherwise.
      """
      if not isinstance(service, str):
         return False
      
      norm_name = normalize_name(service)

      for services in self.services.values():
         if norm_name in services:
            return True
         
      return False

   def __eq__(self, other) -> bool:
      """
      Compare two ServicesManager objects.

      Args:
         other (ServicesManager): Object to compare with.

      Returns:
         bool: True if equal, False otherwise.
      """
      if not isinstance(other, ServicesManager):
         return NotImplemented
      
      return self.services == other.services

   def __bool__(self) -> bool:
      """
      Check if manager has any services.

      Returns:
         bool: True if not empty.
      """
      return bool(self.services)

   def __str__(self) -> str:
      """
      Return a readable summary.

      Returns:
         str: Summary text.
       """
      total_services = sum(len(s) for s in self.services.values())

      return f"{self.field_name} - {len(self.services)} categories, {total_services} services"

   def __repr__(self) -> str:
      """
      Return technical representation for debugging.

      Returns:
         str: Developer-friendly representation.
      """
      total_services = sum(len(s) for s in self.services.values())
      return (
         f"ServicesManager(field = '{self.field_name}', "
         f"categories = {len(self.services)}, services = {total_services})"
      )
   

   # --- Utility methods ---
   def _find_service_data(self, name: str) -> tuple[str | None, dict | None]:
      """
      Find a service and its category.

      Args:
         name (str): Service name (human-readable format).

      Returns:
         tuple[str | None, dict | None]: (category, service details) or (None, None).
      """ 
      if not isinstance(name, str):
         return None, None
      
      norm_name = denormalize_name(name)

      for category, services in self.services.items():
         for service_name, details in services.items():
            if service_name.lower() == norm_name.lower():
               return category, details
            
      return None, None
   
   def _format_service(self, name: str, details: dict[str, str | int | float]) -> str:
      """
      Format service details for display.

      Args:
         name (str): Service name.
         details (dict): Service attributes.

      Returns:
         str: Formatted multiline text.
      """
      if not isinstance(name, str) or not isinstance(details, dict):
         return ""
      
      return (
        f"{normalize_name(name)}\n"
        f"  💰 Price: {details['price']} {details['currency']}\n"
        f"  ⏱️ Duration: {details['duration']} min\n"
        f"  🌿 Description: {details['description']}\n"
      )
   
   def _apply_default_currency(self) -> None:
      """
      Apply the default currency to all services.
      """
      for category in self.services.values():
         for service in category.values():
            service["currency"] = self.default_currency

   def service_exists(self, service_name: str) -> bool:
      """
      Check if a service exists.

      Args:
         service_name (str): Name to check.

      Returns:
         bool: True if service exists.
      """
      if not isinstance(service_name, str):
         return False
      
      norm_name = normalize_name(service_name)
      result = self._find_service_data(norm_name)

      if not result:
         return False
      
      category, details = result

      return bool(category and details)


   # --- Core functionality ---
   def add_service(self, category: str, name: str, price: float, duration: int, description: str, currency: str = None) -> str:
      """
      Add a new service.

      Args:
         category (str): Category name.
         name (str): Service name.
         price (float): Price value.
         duration (int): Duration in minutes.
         description (str): Short description.
         currency (str, optional): Currency type. Defaults to "EUR".

      Returns:
         str: Success or error message.
      """
      if not all(isinstance(arg, str) for arg in [category, name, description]) or \
           (currency is not None and not isinstance(currency, str)):
         return self.PROVIDED_NOT_STR
      
      if not isinstance(price, (int, float)) or price < 0:
         return self.NEGATIVE_NUM_NOT_ALLOWED
      
      if not isinstance(duration, (int, float)) or duration <= 0:
         return self.NEGATIVE_NUM_NOT_ALLOWED
      
      norm_category = normalize_name(category)
      norm_name = normalize_name(name)

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
      Update existing service.

      Args:
         category (str): Category name.
         name (str): Service name.
         price (float | None, optional): New price. Defaults to None.
         duration (int | None, optional): New duration in minutes. Defaults to None.
         description (str | None, optional): New description. Defaults to None.
         currency (str | None, optional): New currency. Defaults to None.

      Returns:
         str: Success or error message.
      """
      if not all(isinstance(arg, str) for arg in [category, name]):
         return self.PROVIDED_NOT_STR
      
      norm_category = normalize_name(category)
      norm_name = normalize_name(name)

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
      Get formatted details of a service.

      Args:
          name (str): Service name.

      Returns:
         str: Formatted information or an error message.
      """
      if not isinstance(name, str):
         return self.PROVIDED_NOT_STR
      
      category, details = self._find_service_data(name)

      if not category or not details:
         return self.SERVICE_NOT_FOUND
      
      return self._format_service(name, details)

   def get_service_data(self, name: str) -> dict | None:
      """
      Get raw service data.

      Args:
         name (str): Service name.

      Returns:
            dict | None: Service details, or None if not found.
      """
      if not isinstance(name, str):
         return None
      
      _, details = self._find_service_data(name)

      return details

   def remove_service(self, name: str) -> str:
      """
      Remove a service.

      Args:
         name (str): Service name.

      Returns:
         str: Success or error message.
      """
      if not isinstance(name, str):
         return self.PROVIDED_NOT_STR
      
      category, details = self._find_service_data(name)

      if not category or not details:
         return self.SERVICE_NOT_FOUND
      
      norm_name = normalize_name(name)
      del self.services[category][norm_name]
      cat_disp = denormalize_name(category)

      return f"[Service \"{name.title()}\" removed successfully from \"{cat_disp}\"]"
   
   def update_service_price(self, name: str, new_price: float | None = None, currency: str | None = None) -> str: 
      """
      Update the price and/or currency of an existing service.

      Args:
         name (str): Service name.
         new_price (float | None, optional): New price value. Defaults to None.
         currency (str | None, optional): New currency. Defaults to None.

      Returns:
         str: Success or error message.
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
      Update currency for all services.

      Args:
         new_currency (str): New currency type.

      Returns:
         str: Confirmation message.
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
      Print an overview of all categories and services.
      """
      print(f"\n🌸 {self.field_name} Services 🌸\n{24 * '-'}")

      for category, services in self.services.items():
         cat_disp = normalize_name(category)
         print(f"\n🧺 {cat_disp}:\n{70 * '-'}")

         for name, details in services.items():
            print(self._format_service(name, details))


   # --- JSON storage ---  
   def save_services_to_json(self, filename: str = "services.json") -> str:
      """
      Save services to JSON.

      Args:
         filename (str): Output file name.

      Returns:
         str: Confirmation message.
      """
      with open(filename, "w", encoding="utf-8") as file:
         json.dump(self.services, file, indent=4, ensure_ascii=False)

      return f"[Services saved to \"{filename}\"]"
   
   def load_services_from_json(self, filename: str = "services.json") -> str:
      """
      Load services from a JSON file.

      Args:
         filename (str): Input file name.

      Returns:
         str: Confirmation or error message.
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