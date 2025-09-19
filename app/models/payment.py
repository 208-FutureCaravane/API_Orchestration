from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    CASH = "CASH"
    CIB = "CIB"
    EDAHABIA = "EDAHABIA"
    PAYPAL = "PAYPAL"
    STRIPE = "STRIPE"
    GUIDINI_PAY = "GUIDINI_PAY"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentCreate(BaseModel):
    orderId: int
    amount: float = Field(..., gt=0)
    method: PaymentMethod
    externalId: Optional[str] = None  # Payment gateway transaction ID
    providerResponse: Optional[Dict[str, Any]] = None  # Payment gateway response
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Payment amount must be greater than 0')
        return round(v, 2)


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    externalId: Optional[str] = None
    providerResponse: Optional[Dict[str, Any]] = None


class PaymentResponse(BaseModel):
    id: int
    orderId: int
    order: Optional[dict] = None  # Order details
    amount: float
    method: PaymentMethod
    status: PaymentStatus
    externalId: Optional[str]
    providerResponse: Optional[Dict[str, Any]]
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class PaymentListResponse(BaseModel):
    id: int
    orderId: int
    orderNumber: Optional[str] = None
    restaurantId: Optional[int] = None
    restaurantName: Optional[str] = None
    customerId: Optional[int] = None
    customerName: Optional[str] = None
    amount: float
    method: PaymentMethod
    status: PaymentStatus
    externalId: Optional[str]
    createdAt: datetime
    
    class Config:
        from_attributes = True


class PaymentProcessRequest(BaseModel):
    orderId: int
    method: PaymentMethod
    # Payment gateway specific fields
    cardToken: Optional[str] = None  # For card payments
    phoneNumber: Optional[str] = None  # For mobile payments
    returnUrl: Optional[str] = None  # For redirect-based payments


class PaymentProcessResponse(BaseModel):
    paymentId: int
    status: PaymentStatus
    redirectUrl: Optional[str] = None  # For payments requiring redirect
    qrCode: Optional[str] = None  # For QR code payments
    message: str


class RefundRequest(BaseModel):
    paymentId: int
    amount: Optional[float] = None  # Partial refund amount, None for full refund
    reason: Optional[str] = None


class RefundResponse(BaseModel):
    success: bool
    refundAmount: float
    refundId: Optional[str] = None  # External refund ID
    message: str


class PaymentStatsResponse(BaseModel):
    totalPayments: int
    totalAmount: float
    paidAmount: float
    pendingAmount: float
    failedAmount: float
    refundedAmount: float
    methodBreakdown: Dict[str, int]  # Count by payment method
    statusBreakdown: Dict[str, int]  # Count by status
    averagePaymentAmount: float


class RestaurantPaymentStatsResponse(BaseModel):
    restaurantId: int
    restaurantName: str
    todayStats: PaymentStatsResponse
    monthStats: PaymentStatsResponse
    recentPayments: List[PaymentListResponse]
