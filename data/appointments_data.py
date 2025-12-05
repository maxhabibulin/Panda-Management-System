"""
Test appointment data for development and demonstration.

This module provides a dataset of appointments spanning
past, present, and future dates. Used to test appointment filtering,
sorting, and recommendation systems.

Structure:
{
    phone_id: {
        "first_name": str,
        "last_name": str,
        "service_name": str,
        "date_time": datetime
    }
}

Time categories:
- Past: 5–15 days ago (for historical data testing)
- Boundary: ±1 hour from now (for edge case testing)  
- Future: 1–14 days ahead (for upcoming appointments)
"""

from datetime import datetime, timedelta

now = datetime.now()

appointments = {
    # === Past Appointments (≈ 5–15 days ago) ===
    21098432: {
        "first_name": "red",
        "last_name": "fox",
        "service_name": "stone_massage",
        "date_time": now - timedelta(days=15, hours=2)
    },
    21745098: {
        "first_name": "steppe",
        "last_name": "eagle",
        "service_name": "aroma_bath",
        "date_time": now - timedelta(days=10, hours=1)
    },
    22987541: {
        "first_name": "eurasian",
        "last_name": "badger",
        "service_name": "detox_tea",
        "date_time": now - timedelta(days=5, hours=3)
    },

    # === Around Today (boundary cases) ===
    23804503: {
        "first_name": "eastern",
        "last_name": "wolf",
        "service_name": "classic_bath",
        "date_time": now - timedelta(hours=1)  # just passed
    },
    21234789: {
        "first_name": "pale",
        "last_name": "fox",
        "service_name": "foot_reflex",
        "date_time": now + timedelta(hours=1)  # upcoming soon
    },

    # === Future Appointments (next 3–15 days) ===
    25124512: {
        "first_name": "pallas",
        "last_name": "cat",
        "service_name": "detox_tea",
        "date_time": now + timedelta(days=1, hours=2)
    },
    27891234: {
        "first_name": "snow",
        "last_name": "leopard",
        "service_name": "bamboo_oil",
        "date_time": now + timedelta(days=2, hours=3)
    },
    29451872: {
        "first_name": "red",
        "last_name": "panda",
        "service_name": "aroma_bath",
        "date_time": now + timedelta(days=3, hours=4)
    },
    20347689: {
        "first_name": "tibetan",
        "last_name": "fox",
        "service_name": "stone_massage",
        "date_time": now + timedelta(days=4, hours=5)
    },
    24567123: {
        "first_name": "black",
        "last_name": "bear",
        "service_name": "green_tea",
        "date_time": now + timedelta(days=5, hours=6)
    },
    27890156: {
        "first_name": "golden",
        "last_name": "monkey",
        "service_name": "flower_tea",
        "date_time": now + timedelta(days=6, hours=7)
    },
    29873456: {
        "first_name": "eurasian",
        "last_name": "lynx",
        "service_name": "private_bath",
        "date_time": now + timedelta(days=8, hours=1)
    },
    25908345: {
        "first_name": "malayan",
        "last_name": "tapir",
        "service_name": "bamboo_oil",
        "date_time": now + timedelta(days=10, hours=2)
    },
    21789456: {
        "first_name": "giant",
        "last_name": "panda",
        "service_name": "classic_bath",
        "date_time": now + timedelta(days=12, hours=3)
    },
    23456781: {
        "first_name": "siberian",
        "last_name": "tiger",
        "service_name": "stone_massage",
        "date_time": now + timedelta(days=13, hours=4)
    },
    20398476: {
        "first_name": "japanese",
        "last_name": "macaque",
        "service_name": "aroma_bath",
        "date_time": now + timedelta(days=14, hours=5)
    }
}