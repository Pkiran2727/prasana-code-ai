"""
Razorpay Payment Routes for Prasana Code AI
Handles order creation, payment verification, and webhook callbacks.
"""

import os
import hmac
import hashlib
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/payment", tags=["payment"])

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

# Server-side fixed pricing table (in paise: ₹1 = 100 paise)
PLAN_PRICING = {
    "pro_monthly": 79900,
    "pro_annual": 249900,
    "lifetime": 649900
}

class CreateOrderRequest(BaseModel):
    plan_id: str  # "pro_monthly", "pro_annual", "lifetime"
    amount: Optional[int] = None
    currency: str = "INR"
    user_email: Optional[str] = None

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    user_email: str
    plan_id: str

@router.post("/create-order")
def create_razorpay_order(req: CreateOrderRequest):
    """
    Creates a Razorpay order ID. Amount is enforced server-side from PLAN_PRICING.
    """
    if req.plan_id not in PLAN_PRICING:
        raise HTTPException(status_code=400, detail=f"Invalid plan_id: {req.plan_id}")

    enforced_amount = PLAN_PRICING[req.plan_id]

    try:
        import razorpay
        if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            order_data = {
                "amount": enforced_amount,
                "currency": req.currency,
                "receipt": f"receipt_{req.plan_id}",
                "payment_capture": 1
            }
            order = client.order.create(data=order_data)
            return {
                "status": "success",
                "order_id": order["id"],
                "key_id": RAZORPAY_KEY_ID,
                "amount": enforced_amount,
                "currency": req.currency
            }
        else:
            raise ValueError("Razorpay keys not configured")
    except Exception as e:
        logger.warning(f"Razorpay SDK call fallback: {e}")
        import time
        mock_order_id = f"order_mock_{int(time.time())}"
        return {
            "status": "success",
            "order_id": mock_order_id,
            "key_id": RAZORPAY_KEY_ID or "rzp_test_placeholder",
            "amount": enforced_amount,
            "currency": req.currency,
            "test_mode": True
        }

@router.post("/verify-payment")
def verify_razorpay_payment(req: VerifyPaymentRequest):
    """
    Verifies Razorpay HMAC signature using constant-time compare_digest.
    Mock orders are strictly rejected in production to prevent free activation.
    """
    if req.razorpay_order_id.startswith("order_mock_"):
        raise HTTPException(
            status_code=400,
            detail="Mock order cannot activate a paid plan. Real transaction required."
        )

    if not RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Razorpay secret key not configured on server.")

    try:
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            f"{req.razorpay_order_id}|{req.razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(generated_signature, req.razorpay_signature):
            logger.info(f"Payment verified for user {req.user_email}, plan: {req.plan_id}")
            return {
                "status": "success",
                "message": "Payment verified! Pro access activated.",
                "active_plan": req.plan_id
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid payment signature.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying payment: {e}")
        raise HTTPException(status_code=500, detail="Payment verification failed.")
