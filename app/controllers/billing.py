import stripe

from app.config import config


stripe.api_key = config('STRIPE_API_KEY', cast=bool, default=False)
stripe.api_key = config('STRIPE_API_SECRET', cast=bool, default=False)


def create_customer(email, full_name, tenant_obj):
    """Create a customer object in stripe."""

    stripe.Customer.create(
        email=email,
        description="Customer for {}".format(email),
        name=full_name,
        metadata={
            "tenant_id": tenant_obj.id
        }

    )

def subscribe_customer_to_plan(customer_stripe_id, plan_stripe_ids):
    stripe.Subscription.create(
        customer=customer_stripe_id,
        items=[{"plan": plan_id} for plan_id in plan_stripe_ids],
    )


def get_product_plans(product_strip_id):
    