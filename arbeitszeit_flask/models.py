"""
Definition of database tables.
"""

import uuid
from enum import Enum

from flask_login import UserMixin

from arbeitszeit_flask.extensions import db


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)

    def __str__(self) -> str:
        return f"User {self.email} ({self.id})"


class SocialAccounting(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    account = db.Column(db.ForeignKey("account.id"), nullable=False)


# Association table Company - Member
jobs = db.Table(
    "jobs",
    db.Column("member_id", db.String, db.ForeignKey("member.id")),
    db.Column("company_id", db.String, db.ForeignKey("company.id")),
)


class Member(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False, unique=True)
    name = db.Column(db.String(1000), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    account = db.Column(db.ForeignKey("account.id"), nullable=False)

    user = db.relationship(
        "User",
        lazy=True,
        uselist=False,
        backref=db.backref("member", cascade_backrefs=False),
    )
    workplaces = db.relationship(
        "Company",
        secondary=jobs,
        lazy="dynamic",
        backref=db.backref("workers", lazy="dynamic", cascade_backrefs=False),
    )


class Company(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False, unique=True)
    name = db.Column(db.String(1000), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    p_account = db.Column(db.ForeignKey("account.id"), nullable=False)
    r_account = db.Column(db.ForeignKey("account.id"), nullable=False)
    a_account = db.Column(db.ForeignKey("account.id"), nullable=False)
    prd_account = db.Column(db.ForeignKey("account.id"), nullable=False)

    drafts = db.relationship("PlanDraft", lazy="dynamic")
    user = db.relationship(
        "User",
        lazy=True,
        uselist=False,
        backref=db.backref("company", cascade_backrefs=False),
    )
    plans = db.relationship(
        "Plan",
        lazy="dynamic",
        backref=db.backref("company", cascade_backrefs=False),
    )

    def __repr__(self):
        return "<Company(name='%s')>" % (self.name,)


class Accountant(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False, unique=True)
    name = db.Column(db.String(1000), nullable=False)

    user = db.relationship(
        "User",
        lazy=True,
        uselist=False,
        backref=db.backref("accountant", cascade_backrefs=False),
    )


class PlanDraft(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    plan_creation_date = db.Column(db.DateTime, nullable=False)
    planner = db.Column(db.String, db.ForeignKey("company.id"), nullable=False)
    costs_p = db.Column(db.Numeric(), nullable=False)
    costs_r = db.Column(db.Numeric(), nullable=False)
    costs_a = db.Column(db.Numeric(), nullable=False)
    prd_name = db.Column(db.String(100), nullable=False)
    prd_unit = db.Column(db.String(100), nullable=False)
    prd_amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    timeframe = db.Column(db.Numeric(), nullable=False)
    is_public_service = db.Column(db.Boolean, nullable=False, default=False)


class Plan(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    plan_creation_date = db.Column(db.DateTime, nullable=False)
    planner = db.Column(db.String, db.ForeignKey("company.id"), nullable=False)
    costs_p = db.Column(db.Numeric(), nullable=False)
    costs_r = db.Column(db.Numeric(), nullable=False)
    costs_a = db.Column(db.Numeric(), nullable=False)
    prd_name = db.Column(db.String(100), nullable=False)
    prd_unit = db.Column(db.String(100), nullable=False)
    prd_amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    timeframe = db.Column(db.Numeric(), nullable=False)
    is_public_service = db.Column(db.Boolean, nullable=False, default=False)
    activation_date = db.Column(db.DateTime, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    requested_cooperation = db.Column(
        db.String, db.ForeignKey("cooperation.id"), nullable=True
    )
    cooperation = db.Column(db.String, db.ForeignKey("cooperation.id"), nullable=True)
    hidden_by_user = db.Column(db.Boolean, nullable=False, default=False)

    review = db.relationship(
        "PlanReview", uselist=False, back_populates="plan", cascade_backrefs=False
    )


class PlanReview(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    approval_date = db.Column(db.DateTime, nullable=True, default=None)
    plan_id = db.Column(db.String, db.ForeignKey("plan.id"), nullable=False)

    plan = db.relationship("Plan", back_populates="review", cascade_backrefs=False)

    def __repr__(self) -> str:
        return f"PlanReview(id={self.id!r}, plan_id={self.plan_id!r}, approval_date={self.approval_date!r})"


class AccountTypes(Enum):
    p = "p"
    r = "r"
    a = "a"
    prd = "prd"
    member = "member"
    accounting = "accounting"


class Account(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)

    transactions_sent = db.relationship(
        "Transaction",
        foreign_keys="Transaction.sending_account",
        lazy="dynamic",
        backref=db.backref("account_from", cascade_backrefs=False),
    )
    transactions_received = db.relationship(
        "Transaction",
        foreign_keys="Transaction.receiving_account",
        lazy="dynamic",
        backref=db.backref("account_to", cascade_backrefs=False),
    )


class Transaction(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    date = db.Column(db.DateTime, nullable=False)
    sending_account = db.Column(db.String, db.ForeignKey("account.id"), nullable=False)
    receiving_account = db.Column(
        db.String, db.ForeignKey("account.id"), nullable=False
    )
    amount_sent = db.Column(db.Numeric(), nullable=False)
    amount_received = db.Column(db.Numeric(), nullable=False)
    purpose = db.Column(db.String(1000), nullable=True)  # Verwendungszweck

    def __repr__(self) -> str:
        fields = ", ".join(
            [
                f"id={self.id!r}",
                f"date={self.date!r}",
                f"sending_account={self.sending_account!r}",
                f"receiving_account={self.receiving_account!r}",
                f"amount_sent={self.amount_sent!r}",
                f"amount_received={self.amount_received!r}",
                f"purpose={self.purpose!r}",
            ]
        )
        return f"Transaction({fields})"


class ConsumerPurchase(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    plan_id = db.Column(db.String, db.ForeignKey("plan.id"), nullable=False)
    transaction_id = db.Column(
        db.String, db.ForeignKey("transaction.id"), nullable=True
    )
    amount = db.Column(db.Integer, nullable=False)


class CompanyPurchase(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    plan_id = db.Column(db.String, db.ForeignKey("plan.id"), nullable=False)
    transaction_id = db.Column(
        db.String, db.ForeignKey("transaction.id"), nullable=True
    )
    amount = db.Column(db.Integer, nullable=False)


class LabourCertificatesPayout(db.Model):
    transaction_id = db.Column(
        db.String,
        db.ForeignKey("transaction.id"),
        nullable=False,
        primary_key=True,
    )
    plan_id = db.Column(db.String, db.ForeignKey("plan.id"), nullable=False)

    def __repr__(self) -> str:
        fields = ", ".join(
            [
                f"transaction_id={self.transaction_id!r}",
                f"plan_id={self.plan_id!r}",
            ]
        )
        return f"LabourCertificatesPayout({fields})"


class CompanyWorkInvite(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    company = db.Column(db.String, db.ForeignKey("company.id"), nullable=False)
    member = db.Column(db.String, db.ForeignKey("member.id"), nullable=False)


class Cooperation(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    creation_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.String(5000), nullable=False)
    coordinator = db.Column(db.String, db.ForeignKey("company.id"), nullable=False)

    plans = db.relationship(
        "Plan",
        foreign_keys="Plan.cooperation",
        lazy="dynamic",
        backref=db.backref("coop", cascade_backrefs=False),
    )


class PayoutFactor(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    timestamp = db.Column(db.DateTime, nullable=False)
    payout_factor = db.Column(db.Numeric(), nullable=False)
