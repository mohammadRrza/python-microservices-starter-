from fastapi import APIRouter, Depends

from app.application.dto import AuthorizePaymentCommand
from app.application.use_cases.authorize_payment import AuthorizePaymentUseCase
from app.interfaces.api.dependencies import get_authorize_payment_use_case
from app.interfaces.api.schemas import AuthorizePaymentRequest, PaymentResponse


router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.post(
    "/authorize",
    response_model=PaymentResponse,
)
def authorize_payment(
    payload: AuthorizePaymentRequest,
    use_case: AuthorizePaymentUseCase = Depends(get_authorize_payment_use_case),
):
    result = use_case.execute(
        AuthorizePaymentCommand(
            order_id=payload.order_id,
            amount=payload.amount,
            currency=payload.currency,
        )
    )

    return PaymentResponse(
        payment_id=result.payment_id,
        order_id=result.order_id,
        status=result.status,
    )