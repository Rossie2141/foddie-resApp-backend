import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
import os
from app.database import SessionLocal
from app.models.dish import Dish


def seed_dishes(json_file_path=None):
    """
    Seed the database with dishes from a JSON file.
    
    Args:
        json_file_path: Path to the JSON file. If None, uses default 'dishes_seed_data.json'
    """
    # Default to dishes_seed_data.json in the same directory
    if json_file_path is None:
        script_dir = Path(__file__).parent
        json_file_path = script_dir / "dishes_seed_data.json"
    
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"❌ Error: JSON file not found at {json_file_path}")
        return
    
    # Load JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing dishes (optional - comment out if you want to keep existing data)
        # db.query(Dish).delete()
        # db.commit()
        
        # Create Dish objects from JSON data
        dishes = []
        for dish_data in data.get('dishes', []):
            dish = Dish(
                name=dish_data['name'],
                description=dish_data['description'],
                price=dish_data['price'],
                rating=dish_data['rating'],
                category=dish_data['category'],
                image_url=dish_data['image_url'],
                is_new=dish_data.get('is_new', False),
                is_popular=dish_data.get('is_popular', False)
            )
            dishes.append(dish)
        
        # Add all dishes to database
        db.add_all(dishes)
        db.commit()
        
        print(f"✅ Successfully seeded {len(dishes)} dishes to the database")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # You can optionally pass a custom JSON file path
    # seed_dishes("/path/to/custom_dishes.json")
    seed_dishes()