#!/usr/bin/env python3
"""
Seed data script for ODiGO - African Cuisine Focus
This script populates the database with categories and origins focused on Cameroon and Africa.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.origin import Origin


def create_categories():
    """Create food categories common in African cuisine"""
    categories = [
        # Main Course Categories
        "Stews & Soups",
        "Rice & Grain Dishes",
        "Meat Dishes",
        "Fish & Seafood",
        "Vegetarian & Vegan",
        "Grilled & Barbecue",

        # Sides & Accompaniments
        "Side Dishes",
        "Sauces & Condiments",
        "Plantain & Banana Dishes",
        "Root Vegetables",

        # Breakfast & Light Meals
        "Breakfast",
        "Street Food",
        "Snacks & Appetizers",

        # Beverages & Desserts
        "Traditional Drinks",
        "Alcoholic Beverages",
        "Desserts & Sweets",
        "Tea & Coffee",

        # Special Categories
        "Ceremonial Dishes",
        "Festival Foods",
        "Health & Wellness",
        "Baby Food",
    ]

    created_categories = []
    for category_name in categories:
        # Check if category already exists
        existing_category = Category.query.filter_by(name=category_name).first()
        if not existing_category:
            category = Category(name=category_name)
            db.session.add(category)
            created_categories.append(category_name)
            print(f"✓ Created category: {category_name}")
        else:
            print(f"- Category already exists: {category_name}")

    return created_categories


def create_origins():
    """Create origins focused on Cameroon and African countries/cultures"""
    origins = [
        # Cameroon Regions
        {"country": "Cameroon", "culture": "Bamiléké", "tribe": "Bamiléké"},
        {"country": "Cameroon", "culture": "Fang-Beti", "tribe": "Ewondo"},
        {"country": "Cameroon", "culture": "Fang-Beti", "tribe": "Bulu"},
        {"country": "Cameroon", "culture": "Fang-Beti", "tribe": "Fang"},
        {"country": "Cameroon", "culture": "Fulani", "tribe": "Fulani"},
        {"country": "Cameroon", "culture": "Duala", "tribe": "Duala"},
        {"country": "Cameroon", "culture": "Bamoun", "tribe": "Bamoun"},
        {"country": "Cameroon", "culture": "Tikar", "tribe": "Tikar"},
        {"country": "Cameroon", "culture": "Grassfields", "tribe": "Kom"},
        {"country": "Cameroon", "culture": "Grassfields", "tribe": "Nso"},
        {"country": "Cameroon", "culture": "Coastal", "tribe": "Bakweri"},
        {"country": "Cameroon", "culture": "Coastal", "tribe": "Bakoko"},

        # West African Countries
        {"country": "Nigeria", "culture": "Yoruba", "tribe": "Yoruba"},
        {"country": "Nigeria", "culture": "Igbo", "tribe": "Igbo"},
        {"country": "Nigeria", "culture": "Hausa-Fulani", "tribe": "Hausa"},
        {"country": "Ghana", "culture": "Akan", "tribe": "Ashanti"},
        {"country": "Ghana", "culture": "Akan", "tribe": "Fante"},
        {"country": "Ghana", "culture": "Ga-Dangme", "tribe": "Ga"},
        {"country": "Senegal", "culture": "Wolof", "tribe": "Wolof"},
        {"country": "Senegal", "culture": "Serer", "tribe": "Serer"},
        {"country": "Mali", "culture": "Mandinka", "tribe": "Mandinka"},
        {"country": "Mali", "culture": "Bambara", "tribe": "Bambara"},
        {"country": "Burkina Faso", "culture": "Mossi", "tribe": "Mossi"},
        {"country": "Ivory Coast", "culture": "Akan", "tribe": "Baoulé"},
        {"country": "Guinea", "culture": "Fula", "tribe": "Fula"},
        {"country": "Sierra Leone", "culture": "Temne", "tribe": "Temne"},
        {"country": "Liberia", "culture": "Kpelle", "tribe": "Kpelle"},

        # Central African Countries
        {"country": "Chad", "culture": "Sara", "tribe": "Sara"},
        {"country": "Central African Republic", "culture": "Gbaya", "tribe": "Gbaya"},
        {"country": "Gabon", "culture": "Fang", "tribe": "Fang"},
        {"country": "Equatorial Guinea", "culture": "Fang", "tribe": "Fang"},
        {"country": "Republic of Congo", "culture": "Kongo", "tribe": "Kongo"},
        {"country": "Democratic Republic of Congo", "culture": "Luba", "tribe": "Luba"},
        {"country": "Democratic Republic of Congo", "culture": "Kongo", "tribe": "Kongo"},
        {"country": "Democratic Republic of Congo", "culture": "Mongo", "tribe": "Mongo"},

        # East African Countries
        {"country": "Kenya", "culture": "Kikuyu", "tribe": "Kikuyu"},
        {"country": "Kenya", "culture": "Luo", "tribe": "Luo"},
        {"country": "Kenya", "culture": "Maasai", "tribe": "Maasai"},
        {"country": "Tanzania", "culture": "Sukuma", "tribe": "Sukuma"},
        {"country": "Tanzania", "culture": "Maasai", "tribe": "Maasai"},
        {"country": "Uganda", "culture": "Baganda", "tribe": "Baganda"},
        {"country": "Ethiopia", "culture": "Oromo", "tribe": "Oromo"},
        {"country": "Ethiopia", "culture": "Amhara", "tribe": "Amhara"},
        {"country": "Ethiopia", "culture": "Tigray", "tribe": "Tigray"},
        {"country": "Rwanda", "culture": "Hutu", "tribe": "Hutu"},
        {"country": "Rwanda", "culture": "Tutsi", "tribe": "Tutsi"},

        # Southern African Countries
        {"country": "South Africa", "culture": "Zulu", "tribe": "Zulu"},
        {"country": "South Africa", "culture": "Xhosa", "tribe": "Xhosa"},
        {"country": "South Africa", "culture": "Afrikaner", "tribe": None},
        {"country": "South Africa", "culture": "Cape Malay", "tribe": None},
        {"country": "Zimbabwe", "culture": "Shona", "tribe": "Shona"},
        {"country": "Zimbabwe", "culture": "Ndebele", "tribe": "Ndebele"},
        {"country": "Botswana", "culture": "Tswana", "tribe": "Tswana"},
        {"country": "Namibia", "culture": "Herero", "tribe": "Herero"},
        {"country": "Zambia", "culture": "Bemba", "tribe": "Bemba"},
        {"country": "Malawi", "culture": "Chewa", "tribe": "Chewa"},
        {"country": "Mozambique", "culture": "Makua", "tribe": "Makua"},

        # North African Countries
        {"country": "Morocco", "culture": "Berber", "tribe": "Amazigh"},
        {"country": "Morocco", "culture": "Arab", "tribe": None},
        {"country": "Algeria", "culture": "Berber", "tribe": "Kabyle"},
        {"country": "Tunisia", "culture": "Arab-Berber", "tribe": None},
        {"country": "Egypt", "culture": "Egyptian Arab", "tribe": None},
        {"country": "Sudan", "culture": "Arab", "tribe": None},
        {"country": "Sudan", "culture": "Nubian", "tribe": "Nubian"},

        # Island Nations
        {"country": "Madagascar", "culture": "Malagasy", "tribe": "Merina"},
        {"country": "Madagascar", "culture": "Malagasy", "tribe": "Betsileo"},
        {"country": "Mauritius", "culture": "Creole", "tribe": None},
        {"country": "Seychelles", "culture": "Creole", "tribe": None},
        {"country": "Cape Verde", "culture": "Creole", "tribe": None},
    ]

    created_origins = []
    for origin_data in origins:
        # Check if origin already exists
        existing_origin = Origin.query.filter_by(
            country=origin_data["country"],
            culture=origin_data["culture"],
            tribe=origin_data["tribe"]
        ).first()

        if not existing_origin:
            origin = Origin(
                country=origin_data["country"],
                culture=origin_data["culture"],
                tribe=origin_data["tribe"]
            )
            db.session.add(origin)
            created_origins.append(origin_data)

            # Create display string for logging
            display_name = origin_data["country"]
            if origin_data["culture"]:
                display_name += f" - {origin_data['culture']}"
            if origin_data["tribe"]:
                display_name += f" ({origin_data['tribe']})"

            print(f"✓ Created origin: {display_name}")
        else:
            display_name = origin_data["country"]
            if origin_data["culture"]:
                display_name += f" - {origin_data['culture']}"
            if origin_data["tribe"]:
                display_name += f" ({origin_data['tribe']})"
            print(f"- Origin already exists: {display_name}")

    return created_origins


def main():
    """Main function to run the seeding process"""
    print("🌍 Starting ODiGO Database Seeding - African Cuisine Focus")
    print("=" * 60)

    # Create Flask app context
    app = create_app()

    with app.app_context():
        try:
            print("\n📂 Creating Categories...")
            print("-" * 30)
            created_categories = create_categories()

            print(f"\n🌍 Creating Origins (Focus: Cameroon & Africa)...")
            print("-" * 50)
            created_origins = create_origins()

            # Commit all changes
            db.session.commit()

            print("\n" + "=" * 60)
            print("✅ SEEDING COMPLETED SUCCESSFULLY!")
            print(f"📊 Summary:")
            print(f"   • Categories created: {len(created_categories)}")
            print(f"   • Origins created: {len(created_origins)}")
            print(f"   • Total categories in DB: {Category.query.count()}")
            print(f"   • Total origins in DB: {Origin.query.count()}")

            if created_categories:
                print(f"\n🏷️  New Categories:")
                for cat in created_categories[:5]:  # Show first 5
                    print(f"   • {cat}")
                if len(created_categories) > 5:
                    print(f"   • ... and {len(created_categories) - 5} more")

            if created_origins:
                print(f"\n🌍 New Origins:")
                for orig in created_origins[:5]:  # Show first 5
                    display = orig["country"]
                    if orig["culture"]:
                        display += f" - {orig['culture']}"
                    print(f"   • {display}")
                if len(created_origins) > 5:
                    print(f"   • ... and {len(created_origins) - 5} more")

            print("\n🎉 Your ODiGO database is now ready for African culinary adventures!")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            db.session.rollback()
            return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
