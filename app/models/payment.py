from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import requests


# Guidini Pay API Configuration
GUIDINI_PAY_URL = "https://epay.guiddini.dz/api/payment/initiate"
GUIDINI_PAY_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-app-key": "YOUR_APP_KEY",  # Replace with actual key
    "x-app-secret": "YOUR_SECRET_KEY"  # Replace with actual secret
}


class PaymentCreate(BaseModel):
    orderId: int


class PaymentResponse(BaseModel):
    id: int
    paymentId: str  # Guidini Pay transaction ID
    orderId: int
    order: Optional[dict] = None  # Order details
    createdAt: datetime
    
    class Config:
        from_attributes = True


class PaymentInitiateRequest(BaseModel):
    orderId: int
    language: Optional[str] = Field(default="fr", description="Language: fr, en, or ar")


class PaymentInitiateResponse(BaseModel):
    success: bool
    paymentId: Optional[str] = None  # Internal payment record ID
    transactionId: Optional[str] = None  # Guidini Pay transaction ID
    formUrl: Optional[str] = None  # Payment form URL
    amount: Optional[str] = None
    message: str
    error: Optional[str] = None


class PaymentStatusResponse(BaseModel):
    id: int
    paymentId: str
    orderId: int
    orderNumber: Optional[str] = None
    amount: float
    status: str  # From order.paymentStatus
    createdAt: datetime
    
    class Config:
        from_attributes = True


class PaymentListResponse(BaseModel):
    payments: list[PaymentStatusResponse]
    total: int
    page: int
    pageSize: int
