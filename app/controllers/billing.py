import stripe

from app.settings import STRIPE_API_SECRET
from app.settings import STRIPE_DEFAULT_PLAN_ID

stripe.api_key = STRIPE_API_SECRET

def create_customer(email, full_name, tenant_obj):
    """Create a customer object in stripe."""

    customer_resp = stripe.Customer.create(
        email=email,
        description="Customer for {}".format(email),
        name=full_name,
        metadata={"tenant_id": tenant_obj.id},
    )

    # TODO: Record the customer_id from stripe.
    return customer_resp


def create_subscription(customer_stripe_id, plan_stripe_ids):
    """Subscribe customer to strip plan."""
    plan_stripe_ids = [STRIPE_DEFAULT_PLAN_ID]

    return stripe.Subscription.create(
        customer=customer_stripe_id,
        items=[{"plan": plan_id} for plan_id in plan_stripe_ids],
    )


def cancel_subscription(subscription_stripe_id):
    """Cancel someones subscription."""
    stripe.Subscription.delete(subscription_stripe_id)


def get_product_plans(product_strip_id):
    pass
