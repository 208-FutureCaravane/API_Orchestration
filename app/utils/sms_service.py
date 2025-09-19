import os
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

from app.core.config import settings
from app.core.database import get_db


class SMSService:
    """Service for sending SMS messages using Twilio."""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            raise ValueError("Twilio credentials not properly configured")
            
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send SMS message to a phone number.
        
        Args:
            to_phone: Destination phone number (international format)
            message: Message content
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            # Ensure phone number is in international format
            if not to_phone.startswith('+'):
                # Assume Algerian number if no country code
                to_phone = f"+213{to_phone.lstrip('0')}"
            
            message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_phone
            )
            
            print(f"SMS sent successfully. SID: {message.sid}")
            return True
            
        except TwilioException as e:
            print(f"Twilio error: {e}")
            return False
        except Exception as e:
            print(f"SMS sending error: {e}")
            return False
    
    def generate_otp_code(self, length: int = 6) -> str:
        """Generate a random OTP code."""
        return ''.join(random.choices(string.digits, k=length))
    
    async def send_otp(self, user_id: int, phone: str, purpose: str = "STAFF_AUTH") -> Optional[str]:
        """
        Generate and send OTP code to user.
        
        Args:
            user_id: User ID
            phone: Phone number to send to
            purpose: Purpose of OTP (STAFF_AUTH, PAYMENT_CONFIRMATION, etc.)
            
        Returns:
            str: OTP code if sent successfully, None otherwise
        """
        db = get_db()
        
        try:
            # Generate OTP code
            otp_code = self.generate_otp_code()
            
            # Set expiration time (20 minutes from now)
            expires_at = datetime.utcnow() + timedelta(minutes=20)
            
            # Invalidate previous unused OTP codes for this user and purpose
            await db.otpcode.update_many(
                where={
                    "userId": user_id,
                    "purpose": purpose,
                    "isUsed": False
                },
                data={"isUsed": True}
            )
            
            # Create new OTP record
            await db.otpcode.create(
                data={
                    "userId": user_id,
                    "code": otp_code,
                    "purpose": purpose,
                    "expiresAt": expires_at
                }
            )
            
            # Send SMS
            message = f"Your Caravane verification code is: {otp_code}. Valid for 20 minutes."
            
            if self.send_sms(phone, message):
                return otp_code
            else:
                # Mark OTP as used if SMS failed
                await db.otpcode.update_many(
                    where={
                        "userId": user_id,
                        "code": otp_code,
                        "isUsed": False
                    },
                    data={"isUsed": True}
                )
                return None
                
        except Exception as e:
            print(f"Error sending OTP: {e}")
            return None
    
    async def verify_otp(self, user_id: int, code: str, purpose: str = "STAFF_AUTH") -> bool:
        """
        Verify OTP code for user.
        
        Args:
            user_id: User ID
            code: OTP code to verify
            purpose: Purpose of OTP
            
        Returns:
            bool: True if code is valid, False otherwise
        """
        db = get_db()
        
        try:
            # Find valid OTP code
            otp_record = await db.otpcode.find_first(
                where={
                    "userId": user_id,
                    "code": code,
                    "purpose": purpose,
                    "isUsed": False,
                    "expiresAt": {"gt": datetime.utcnow()}
                }
            )
            
            if otp_record:
                # Mark OTP as used
                await db.otpcode.update(
                    where={"id": otp_record.id},
                    data={"isUsed": True}
                )
                return True
            
            return False
            
        except Exception as e:
            print(f"Error verifying OTP: {e}")
            return False


# Create global SMS service instance
def get_sms_service() -> Optional[SMSService]:
    """Get SMS service instance if properly configured."""
    try:
        return SMSService()
    except ValueError:
        print("SMS service not available - Twilio not configured")
        return None


sms_service = get_sms_service()
