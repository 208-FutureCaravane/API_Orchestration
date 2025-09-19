#!/usr/bin/env python3

import asyncio
from prisma import Prisma

async def check_otp_table():
    """Check if OtpCode table exists and is properly structured."""
    db = Prisma()
    await db.connect()
    
    try:
        # Try to query the OtpCode table
        count = await db.otpcode.count()
        print(f"✅ OtpCode table exists with {count} records")
        
        # Try to create a test OTP record
        from datetime import datetime, timedelta
        
        test_otp = await db.otpcode.create(
            data={
                "userId": 1,  # Assuming admin user exists
                "code": "123456",
                "purpose": "STAFF_AUTH",
                "expiresAt": datetime.utcnow() + timedelta(minutes=20)
            }
        )
        print(f"✅ Successfully created test OTP: {test_otp.id}")
        
        # Clean up test record
        await db.otpcode.delete(where={"id": test_otp.id})
        print("✅ Test OTP cleaned up")
        
    except Exception as e:
        print(f"❌ Error with OtpCode table: {e}")
        print("💡 You may need to run: npx prisma migrate dev")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(check_otp_table())
