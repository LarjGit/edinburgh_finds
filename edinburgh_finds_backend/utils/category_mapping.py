# utils/category_mapping.py

"""
Category Mapping System for Edinburgh Finds

- `categories` (raw LLM output): free-form strings
- `canonical_categories`: your controlled taxonomy used in navigation, WP, SEO

Workflow:
    raw LLM categories  -->  map_categories()  --> canonical categories
"""

# -------------------------------------------------------
# FIXED TAXONOMY - Add over time 
# -------------------------------------------------------
CANONICAL_CATEGORIES = {
    "padel",
    "pickleball",
    "badminton",
    "tennis",
    "squash",
    "table_tennis",
    "gym",
    "swimming",
    "spa",
    "cafe",
    "restaurant",
    "chess",
    "escape room",
    "climbing",
    "martial arts",
    "yoga",
    "pilates",
    "football",
}


# -------------------------------------------------------
# MAPPING TO CANONICAL CATEGORIES (LLM → Canonical)
# -------------------------------------------------------
CATEGORY_SYNONYMS = {
    # -----------------------
    # RACQUET SPORTS
    # -----------------------
    "paddle tennis": "padel",
    "padel tennis": "padel",
    "glass-back squash": "squash",
    "ping pong": "table_tennis",

    # -----------------------
    # GYM / FITNESS
    # -----------------------

    # -----------------------
    # SWIMMING
    # -----------------------
    "swimming pool": "swimming",
    "indoor pool": "swimming",
    "outdoor pool": "swimming",
    "aqua aerobics": "swimming",

    # -----------------------
    # SPA WELLNESS
    # -----------------------
    "wellness": "spa",
    "sauna": "spa",
    "steam room": "spa",
    "hydro pool": "spa",
    "hot tub": "spa",
    "spa retreat": "spa",

    # -----------------------
    # FAMILY / KIDS
    # -----------------------
    "creche": "family",
    "childcare": "family",
    "kids": "family",
    "kids club": "family",
    "junior": "family",
    "holiday club": "family",

    # -----------------------
    # FOOD & DRINK
    # -----------------------
    "dining": "restaurant",
    "coffee": "cafe",

    # -----------------------
    # FOOTBALL
    # -----------------------
    "5-a-side football": "football",
    "7-a-side football": "football",    
}


# -------------------------------------------------------
# 3. MAIN MAPPING FUNCTION
# -------------------------------------------------------
def map_categories(raw_list: list[str]) -> list[str]:
    """
    Convert raw category strings from LLM into canonical categories.
    Unrecognised categories are ignored (safe by design).
    """

    mapped = set()

    for item in raw_list:
        if not item:
            continue

        key = item.lower().strip()

        # exact synonym -> canonical
        if key in CATEGORY_SYNONYMS:
            mapped.add(CATEGORY_SYNONYMS[key])
            continue

        # direct match
        if key in CANONICAL_CATEGORIES:
            mapped.add(key)
            continue

    return sorted(mapped)
