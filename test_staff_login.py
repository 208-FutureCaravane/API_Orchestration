#!/usr/bin/env python3

import asyncio
from prisma import Prisma
from app.auth.jwt import verify_password

async def test_staff_users():
    """Test script to show staff users and verify login credentials."""
    db = Prisma()
    await db.connect()
    
    try:
        # Get all staff users
        staff_users = await db.user.find_many(
            where={
                "role": {"in": ["WAITER", "CHEF", "MANAGER", "ADMIN"]}
            },
            include={
                "restaurant": True
            }
        )
        
        print("🧑‍💼 Staff Users in Database:")
        print("=" * 60)
        
        for user in staff_users:
            restaurant_name = user.restaurant.name if user.restaurant else "No Restaurant"
            print(f"📱 Phone: {user.phone}")
            print(f"👤 Name: {user.firstName} {user.lastName}")
            print(f"📧 Email: {user.email}")
            print(f"🏢 Role: {user.role}")
            print(f"🍽️ Restaurant: {restaurant_name}")
            print(f"✅ Active: {user.isActive}")
            
            # Test password verification
            password_valid = verify_password("staff123", user.password)
            print(f"🔐 Password 'staff123' valid: {password_valid}")
            print("-" * 40)
        
        print(f"\n📊 Total staff users found: {len(staff_users)}")
        
        # Test specific phone number
        test_phone = 333333331  # First staff member
        test_user = await db.user.find_unique(where={"phone": test_phone})
        
        if test_user:
            print(f"\n🎯 Testing login for phone {test_phone}:")
            print(f"User found: {test_user.firstName} {test_user.lastName}")
            print(f"Role: {test_user.role}")
            password_valid = verify_password("staff123", test_user.password)
            print(f"Password valid: {password_valid}")
        else:
            print(f"\n❌ No user found with phone {test_phone}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(test_staff_users())
