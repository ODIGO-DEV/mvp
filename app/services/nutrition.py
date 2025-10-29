from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

# Very simple heuristic nutrition database for demo purposes only.
# Values are approximate and per unit type.
NUTRITION_DB: Dict[str, Dict[str, Dict[str, float]]] = {
    # per_100g: grams of macros, calories per 100 g
    "chicken": {
        "per_100g": {"protein": 31, "carbs": 0, "fats": 3.6, "calories": 165}
    },
    "beef": {"per_100g": {"protein": 26, "carbs": 0, "fats": 15, "calories": 250}},
    "tofu": {"per_100g": {"protein": 8, "carbs": 2, "fats": 4, "calories": 76}},
    "egg": {"per_piece": {"protein": 6, "carbs": 0.6, "fats": 5, "calories": 72}},
    "rice": {"per_cup": {"protein": 4.3, "carbs": 45, "fats": 0.4, "calories": 205}},
    "pasta": {"per_cup": {"protein": 8, "carbs": 43, "fats": 1.3, "calories": 221}},
    "bread": {"per_slice": {"protein": 3, "carbs": 12, "fats": 1, "calories": 66}},
    "avocado": {"per_100g": {"protein": 2, "carbs": 9, "fats": 15, "calories": 160}},
    "olive oil": {"per_tbsp": {"protein": 0, "carbs": 0, "fats": 14, "calories": 119}},
    "banana": {"per_piece": {"protein": 1.3, "carbs": 27, "fats": 0.4, "calories": 105}},
    "milk": {"per_cup": {"protein": 8, "carbs": 12, "fats": 8, "calories": 150}},
    "yogurt": {"per_cup": {"protein": 9, "carbs": 17, "fats": 4, "calories": 149}},
    "peanut": {"per_100g": {"protein": 26, "carbs": 16, "fats": 49, "calories": 567}},
    "bean": {"per_cup": {"protein": 15, "carbs": 45, "fats": 1, "calories": 240}},
    "fish": {"per_100g": {"protein": 22, "carbs": 0, "fats": 12, "calories": 206}},
    "potato": {"per_100g": {"protein": 2, "carbs": 17, "fats": 0.1, "calories": 77}},
    "sweet potato": {"per_100g": {"protein": 1.6, "carbs": 20, "fats": 0, "calories": 86}},
    "quinoa": {"per_cup": {"protein": 8, "carbs": 39, "fats": 3.5, "calories": 222}},
    "cheese": {"per_100g": {"protein": 25, "carbs": 1.3, "fats": 33, "calories": 402}},
    "spinach": {"per_100g": {"protein": 2.9, "carbs": 3.6, "fats": 0.4, "calories": 23}},
    "tomato": {"per_100g": {"protein": 0.9, "carbs": 3.9, "fats": 0.2, "calories": 18}},
}


def _match_entry(name: str) -> tuple[str, Dict[str, float]] | None:
    key = name.lower()
    for token, forms in NUTRITION_DB.items():
        if token in key:
            # pick a default representation preference
            for per_key in ("per_100g", "per_cup", "per_piece", "per_slice", "per_tbsp"):
                if per_key in forms:
                    return per_key, forms[per_key]
    return None


def estimate_ingredient_macros(name: str, quantity: float | None, unit: str | None) -> Dict[str, float]:
    """Very rough estimate based on name, quantity and unit.
    Returns dict with protein, carbs, fats, calories.
    """
    quantity = quantity or 0
    unit = (unit or "").lower()

    match = _match_entry(name)
    if not match:
        return {"protein": 0.0, "carbs": 0.0, "fats": 0.0, "calories": 0.0}

    per_key, base = match
    factor = 1.0

    if per_key == "per_100g":
        # interpret quantity by grams if unit suggests weight
        if unit in ("g", "gram", "grams"):
            factor = (quantity or 0) / 100.0
        elif unit in ("kg", "kilogram", "kilograms"):
            factor = (quantity or 0) * 10.0
        else:
            # fallback: treat quantity as serving count
            factor = max(quantity, 1) / 1.0
    elif per_key == "per_cup":
        if unit in ("cup", "cups"):
            factor = quantity or 1.0
        else:
            factor = max(quantity, 1.0)
    elif per_key == "per_piece":
        if unit in ("piece", "pieces", "pc", "pcs"):
            factor = quantity or 1.0
        else:
            factor = max(quantity, 1.0)
    elif per_key == "per_slice":
        if unit in ("slice", "slices"):
            factor = quantity or 1.0
        else:
            factor = max(quantity, 1.0)
    elif per_key == "per_tbsp":
        if unit in ("tbsp", "tablespoon", "tablespoons"):
            factor = quantity or 1.0
        else:
            factor = max(quantity, 1.0)

    return {
        "protein": base["protein"] * factor,
        "carbs": base["carbs"] * factor,
        "fats": base["fats"] * factor,
        "calories": base["calories"] * factor,
    }


def estimate_recipe_macros(recipe) -> Dict[str, float]:
    totals = {"protein": 0.0, "carbs": 0.0, "fats": 0.0, "calories": 0.0}
    for ing in recipe.ingredients:
        m = estimate_ingredient_macros(ing.name or "", ing.quantity, ing.unit)
        for k in totals:
            totals[k] += m[k]
    return totals


def score_recipe_for_goal(recipe, goal: str) -> float:
    m = estimate_recipe_macros(recipe)
    cals = max(m["calories"], 1)
    if goal == "high_protein":
        return (m["protein"] / cals) * 100
    if goal == "low_carb":
        return -(m["carbs"] / cals) * 100
    if goal == "balanced":
        # simplistic balance score: penalize dominance
        ratios = [m["protein"], m["carbs"], m["fats"]]
        total = sum(ratios) or 1
        ratios = [x / total for x in ratios]
        # closer to 1/3 each is better
        return -sum(abs(r - (1 / 3)) for r in ratios)
    return 0.0

