from decimal import Decimal
from typing import Optional
from uuid import UUID

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from arbeitszeit import entities, errors, use_cases
from arbeitszeit.use_cases import (
    CreateOffer,
    CreateOfferRequest,
    CreatePlan,
    DeletePlan,
    GetPlanSummary,
    PlanProposal,
)
from arbeitszeit_web.create_offer import CreateOfferPresenter
from arbeitszeit_web.query_products import QueryProductsPresenter
from project import database, error
from project.database import (
    AccountRepository,
    CompanyRepository,
    CompanyWorkerRepository,
    MemberRepository,
    PlanRepository,
    ProductOfferRepository,
)
from project.dependency_injection import with_injection
from project.forms import ProductSearchForm
from project.models import Company, Plan

main_company = Blueprint(
    "main_company", __name__, template_folder="templates", static_folder="static"
)


def user_is_company():
    return True if session["user_type"] == "company" else False


@main_company.route("/company/profile")
@login_required
@with_injection
def profile(
    company_repository: CompanyRepository,
    company_worker_repository: CompanyWorkerRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    company = company_repository.get_by_id(current_user.id)
    worker = company_worker_repository.get_company_workers(company)
    if worker:
        having_workers = True
    else:
        having_workers = False
    return render_template("company/profile.html", having_workers=having_workers)


@main_company.route("/company/work", methods=["GET", "POST"])
@login_required
@with_injection
def arbeit(
    company_repository: CompanyRepository,
    member_repository: MemberRepository,
    company_worker_repository: CompanyWorkerRepository,
):
    """shows workers and add workers to company."""
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    if request.method == "POST":  # add worker to company
        company = company_repository.get_by_id(current_user.id)
        member = member_repository.get_member_by_id(request.form["member"])
        try:
            use_cases.add_worker_to_company(
                company_worker_repository,
                company,
                member,
            )
        except errors.WorkerAlreadyAtCompany:
            flash("Mitglied ist bereits in diesem Betrieb beschäftigt.")
        database.commit_changes()
        return redirect(url_for("main_company.arbeit"))
    elif request.method == "GET":
        workers_list = company_worker_repository.get_company_workers(
            company_repository.get_by_id(current_user.id)
        )
        return render_template("company/work.html", workers_list=workers_list)


@main_company.route("/company/suchen", methods=["GET", "POST"])
@login_required
@with_injection
def suchen(
    query_products: use_cases.QueryProducts,
    presenter: QueryProductsPresenter,
):
    """search products in catalog."""
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    template_name = "company/query_products.html"
    search_form = ProductSearchForm(request.form)
    if request.method == "POST":
        query = search_form.data["search"] or None
        search_field = search_form.data["select"]  # Name, Beschr., Kategorie
        if search_field == "Name":
            product_filter = use_cases.ProductFilter.by_name
        elif search_field == "Beschreibung":
            product_filter = use_cases.ProductFilter.by_description
        response = query_products(query, product_filter)
        view_model = presenter.present(response)
        return render_template(template_name, form=search_form, view_model=view_model)
    else:
        view_model = presenter.get_empty_view_model()
        return render_template(template_name, form=search_form, view_model=view_model)


@main_company.route("/company/kaeufe")
@login_required
@with_injection
def my_purchases(
    query_purchases: use_cases.QueryPurchases,
    company_repository: CompanyRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    company = company_repository.get_by_id(current_user.id)
    purchases = list(query_purchases(company))
    return render_template("company/my_purchases.html", purchases=purchases)


@main_company.route("/company/create_plan", methods=["GET", "POST"])
@login_required
@with_injection
def create_plan(
    create_plan_from_proposal: CreatePlan,
    get_plan_summary: GetPlanSummary,
    seek_approval: use_cases.SeekApproval,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    original_plan_id: Optional[str] = request.args.get("original_plan_id")
    original_plan_uuid: Optional[UUID] = (
        UUID(original_plan_id) if original_plan_id else None
    )

    if request.method == "POST":  # Button "Plan erstellen"
        plan_data = dict(request.form)
        proposal = PlanProposal(
            costs=entities.ProductionCosts(
                labour_cost=Decimal(plan_data["costs_a"]),
                resource_cost=Decimal(plan_data["costs_r"]),
                means_cost=Decimal(plan_data["costs_p"]),
            ),
            product_name=plan_data["prd_name"],
            production_unit=plan_data["prd_unit"],
            production_amount=int(plan_data["prd_amount"]),
            description=plan_data["description"],
            timeframe_in_days=plan_data["timeframe"],
            is_public_service=True
            if plan_data["productive_or_public"] == "public"
            else False,
        )
        new_plan = create_plan_from_proposal(
            current_user.id, proposal, original_plan_id
        )
        approval_response = seek_approval(new_plan.plan_id)
        database.commit_changes()

        if approval_response.is_approved:
            flash(
                "Plan erfolgreich erstellt und genehmigt. Die Aktivierung des Plans und Gewährung der Kredite erfolgt um 10 Uhr morgens."
            )
            return redirect("/company/my_plans")
        else:
            flash(f"Plan nicht genehmigt. Grund:\n{approval_response.reason}")
            return redirect(
                url_for("main_company.create_plan", original_plan_id=original_plan_id)
            )

    original_plan = (
        None if original_plan_uuid is None else get_plan_summary(original_plan_uuid)
    )
    return render_template("company/create_plan.html", original_plan=original_plan)


@main_company.route("/company/my_plans", methods=["GET", "POST"])
@login_required
@with_injection
def my_plans(
    plan_repository: PlanRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    plans_approved = [
        plan_repository.object_from_orm(plan)
        for plan in current_user.plans.filter_by(
            approved=True,
        ).all()
    ]

    plans_not_expired_and_active = [
        plan for plan in plans_approved if (not plan.expired and plan.is_active)
    ]
    plans_not_expired_and_inactive = [
        plan for plan in plans_approved if (not plan.expired and not plan.is_active)
    ]
    plans_expired = [plan for plan in plans_approved if plan.expired]

    return render_template(
        "company/my_plans.html",
        plans=plans_not_expired_and_active,
        plans_waiting_for_activation=plans_not_expired_and_inactive,
        plans_expired=plans_expired,
    )


@main_company.route("/company/delete_plan/<uuid:plan_id>", methods=["GET", "POST"])
@login_required
@with_injection
def delete_plan(plan_id: UUID, delete_offer: DeletePlan):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    response = delete_offer(plan_id)
    if response.is_success:
        flash(f"Löschen des Plans {response.plan_id} erfolgreich.")
    return redirect(url_for("main_company.my_plans"))


@main_company.route("/company/create_offer/<uuid:plan_id>", methods=["GET", "POST"])
@login_required
@with_injection
def create_offer(
    plan_id: UUID, create_offer: CreateOffer, presenter: CreateOfferPresenter
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    if request.method == "POST":  # create offer
        name = request.form["name"]
        description = request.form["description"]

        offer = CreateOfferRequest(
            name=name,
            description=description,
            plan_id=plan_id,
        )
        use_case_response = create_offer(offer)
        view_model = presenter.present(use_case_response)
        return render_template(
            "company/create_offer_in_app.html", view_model=view_model
        )

    plan = Plan.query.filter_by(id=str(plan_id)).first()
    return render_template("company/create_offer.html", plan=plan)


@main_company.route("/company/my_accounts")
@login_required
@with_injection
def my_accounts(
    company_repository: CompanyRepository,
    get_transaction_infos: use_cases.GetTransactionInfos,
    account_repository: AccountRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    company = company_repository.object_from_orm(current_user)
    all_trans_infos = get_transaction_infos(company)
    my_balances = [
        account_repository.get_account_balance(account)
        for account in company.accounts()
    ]

    return render_template(
        "company/my_accounts.html",
        my_balances=my_balances,
        all_transactions=all_trans_infos,
    )


@main_company.route("/company/transfer_to_worker", methods=["GET", "POST"])
@login_required
@with_injection
def transfer_to_worker(
    send_work_certificates_to_worker: use_cases.SendWorkCertificatesToWorker,
    company_repository: CompanyRepository,
    member_repository: MemberRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    if request.method == "POST":
        company = company_repository.get_by_id(current_user.id)
        try:
            worker = member_repository.get_member_by_id(request.form["member_id"])
        except error.MemberNotFound:
            flash("Mitglied existiert nicht.")
            redirect(url_for("main_company.transfer_to_work"))
        amount = Decimal(request.form["amount"])

        try:
            send_work_certificates_to_worker(
                company,
                worker,
                amount,
            )
            database.commit_changes()
            flash("Erfolgreich überwiesen.")
        except errors.WorkerNotAtCompany:
            flash("Mitglied ist nicht in diesem Betrieb beschäftigt.")

    return render_template("company/transfer_to_worker.html")


@main_company.route("/company/transfer_to_company", methods=["GET", "POST"])
@login_required
@with_injection
def transfer_to_company(
    pay_means_of_production: use_cases.PayMeansOfProduction,
    company_repository: CompanyRepository,
    plan_repository: PlanRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    if request.method == "POST":
        sender = company_repository.get_by_id(current_user.id)
        try:
            plan = plan_repository.get_plan_by_id(request.form["plan_id"])
        except error.PlanNotFound:
            flash("Plan existiert nicht.")
            return redirect(url_for("main_company.transfer_to_company"))
        pieces = int(request.form["amount"])
        purpose = (
            entities.PurposesOfPurchases.means_of_prod
            if request.form["category"] == "Produktionsmittel"
            else entities.PurposesOfPurchases.raw_materials
        )
        try:
            pay_means_of_production(
                sender,
                plan,
                pieces,
                purpose,
            )
            database.commit_changes()
            flash("Erfolgreich bezahlt.")
        except errors.PlanIsInactive:
            flash(
                "Der angegebene Plan ist nicht aktuell. Bitte wende dich an den Verkäufer, um eine aktuelle Plan-ID zu erhalten."
            )
        except errors.CompanyCantBuyPublicServices:
            flash(
                "Bezahlung nicht erfolgreich. Betriebe können keine öffentlichen Dienstleistungen oder Produkte erwerben."
            )

    return render_template("company/transfer_to_company.html")


@main_company.route("/company/my_offers")
@login_required
@with_injection
def my_offers(offer_repository: ProductOfferRepository):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    my_company = Company.query.filter_by(id=current_user.id).first()
    my_plans = my_company.plans.all()
    my_offers = []
    for plan in my_plans:
        active_offers = plan.offers.filter_by(active=True).all()
        for offer in active_offers:
            my_offers.append(offer)
    my_offers = [offer_repository.object_from_orm(offer) for offer in my_offers]

    return render_template("company/my_offers.html", offers=my_offers)


@main_company.route("/company/delete_offer", methods=["GET", "POST"])
@login_required
@with_injection
def delete_offer(
    product_offer_repository: ProductOfferRepository,
):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    offer_id = request.args.get("id")
    assert offer_id
    product_offer = product_offer_repository.get_by_id(offer_id)
    if request.method == "POST":
        use_cases.deactivate_offer(product_offer)
        database.commit_changes()
        flash("Löschen des Angebots erfolgreich.")
        return redirect(url_for("main_company.my_offers"))

    return render_template("company/delete_offer.html", offer=product_offer)


@main_company.route("/company/statistics")
@login_required
@with_injection
def statistics(get_statistics: use_cases.GetStatistics):
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    stats = get_statistics()
    return render_template("company/statistics.html", stats=stats)


@main_company.route("/company/cooperate", methods=["GET", "POST"])
@login_required
def cooperate():
    # under construction
    pass
    return render_template("company/cooperate.html")


@main_company.route("/company/hilfe")
@login_required
def hilfe():
    if not user_is_company():
        return redirect(url_for("auth.zurueck"))

    return render_template("company/help.html")
