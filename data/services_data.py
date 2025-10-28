"""
Default service data for the application.

This file defines a base list of services and configurable 
default currency. It is used by ServicesManagement when no 
custom data is provided.

Structure:
{
    "category_name": {
        "service_name": {
            "price": float,
            "currency": str,
            "duration": int,
            "description": str
        }
    }
}
"""

# --- Default configuration ---
DEFAULT_CURRENCY = "EUR"

# --- Default service data ---
services: dict[str, dict[str, dict[str, str | int | float]]] = {
    "thermal_baths": {
        "classic_bath": {
            "price": 45,
            "currency": DEFAULT_CURRENCY,
            "duration": 60,
            "description": "Traditional hot spring bath with natural minerals."
        },
        "aroma_bath": {
            "price": 55,
            "currency": DEFAULT_CURRENCY,
            "duration": 70,
            "description": "Aromatic bath infused with essential oils."
        },
        "private_bath": {
            "price": 80,
            "currency": DEFAULT_CURRENCY,
            "duration": 90,
            "description": "Private thermal bath experience in a serene room."
        },
    },

    "massages": {
        "bamboo_oil": {
            "price": 70,
            "currency": DEFAULT_CURRENCY,
            "duration": 45,
            "description": "Deep relaxation bamboo oil massage."
        },
        "stone_massage": {
            "price": 85,
            "currency": DEFAULT_CURRENCY,
            "duration": 60,
            "description": "Hot stone massage to relieve tension and stress."
        },
        "foot_reflex": {
            "price": 50,
            "currency": DEFAULT_CURRENCY,
            "duration": 40,
            "description": "Reflexology-based foot massage for energy balance."
        },
    },

    "tea_therapy": {
        "green_tea": {
            "price": 35,
            "currency": DEFAULT_CURRENCY,
            "duration": 30,
            "description": "Green tea ceremony to refresh body and mind."
        },
        "flower_tea": {
            "price": 40,
            "currency": DEFAULT_CURRENCY,
            "duration": 45,
            "description": "Floral tea session promoting relaxation and clarity."
        },
        "detox_tea": {
            "price": 45,
            "currency": DEFAULT_CURRENCY,
            "duration": 50,
            "description": "Detoxifying tea blend for purification and calm."
        },
    },
}
