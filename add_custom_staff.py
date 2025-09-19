#!/usr/bin/env python3

import asyncio
from prisma import Prisma
from app.auth.jwt import get_password_hash

async def add_custom_staff():
    """Add a staff member with specific phone number."""
    db = Prisma()
    await db.connect()
    
    try:
        # Check if user already exists
        existing_user = await db.user.find_unique(where={"phone": 213784127256})
        
        if existing_user:
            print(f"❌ User with phone +213784127256 already exists:")
            print(f"   Name: {existing_user.firstName} {existing_user.lastName}")
            print(f"   Role: {existing_user.role}")
            print(f"   Email: {existing_user.email}")
            return
        
        # Get first restaurant for assignment
        restaurant = await db.restaurant.find_first()
        if not restaurant:
            print("❌ No restaurant found! Please run the main seed script first.")
            return
        
        # Create the staff user
        staff_user = await db.user.create({
            'firstName': 'Custom',
            'lastName': 'Staff',
            'email': 'custom.staff@caravane.com',
            'phone': 213784127256,  # +213784127256 without the +
            'role': 'WAITER',
            'isActive': True,
            'password': get_password_hash('staff123'),  # Same password as other staff
            'restaurantId': restaurant.id
        })
        
        print("✅ Successfully created custom staff user:")
        print(f"   Phone: +213784127256")
        print(f"   Name: {staff_user.firstName} {staff_user.lastName}")
        print(f"   Role: {staff_user.role}")
        print(f"   Email: {staff_user.email}")
        print(f"   Restaurant: {restaurant.name}")
        print(f"   Password: staff123")
        print("\n🔐 You can now login with:")
        print(f"   Phone: 213784127256")
        print(f"   Password: staff123")
        
    except Exception as e:
        print(f"❌ Error creating staff user: {e}")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(add_custom_staff())
