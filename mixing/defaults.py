from __future__ import unicode_literals

from mezzanine.conf import register_setting


register_setting(
    name="STRIPE_SK",
    label="Stripe secret key",
    editable=True,
    default="",
)

register_setting(
    name="STRIPE_PK",
    label="Stripe public key",
    editable=True,
    default="",
)

register_setting(
    name="PURCHASE_CREDIT_PRICE",
    label="Credit price",
    description="The price of each Track Credit",
    editable=True,
    default=10,
)

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    default=("PURCHASE_CREDIT_PRICE", "STRIPE_PK"),
    append=True
)
