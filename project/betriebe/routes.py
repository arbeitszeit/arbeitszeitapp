from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .. import db
from ..models import Angebote, Kaeufe, Betriebe, Nutzer, Produktionsmittel, Arbeit, Arbeiter, Auszahlungen,\
    Kooperationen, KooperationenMitglieder
from ..forms import ProductSearchForm
from ..tables import ProduktionsmittelTable, ArbeiterTable1, ArbeiterTable2, Preiszusammensetzung
from ..composition_of_prices import get_table_of_composition, get_positions_in_table, create_dots
from ..such_vorgang import such_vorgang, get_angebote
from ..kauf_vorgang import kauf_vorgang
from decimal import Decimal
import datetime
from sqlalchemy.sql import func


main_betriebe = Blueprint('main_betriebe', __name__, template_folder='templates',
    static_folder='static')


@main_betriebe.route('/betriebe/profile')
@login_required
def profile():
    user_type = session["user_type"]
    if user_type == "betrieb":
        arbeiter = Arbeiter.query.filter_by(betrieb=current_user.id).first()
        if arbeiter:
            having_workers = True
        else:
            having_workers = False
        return render_template('profile_betriebe.html', having_workers=having_workers)
    elif user_type == "nutzer":
        return redirect(url_for('auth.zurueck'))


@main_betriebe.route('/betriebe/arbeit', methods=['GET', 'POST'])
@login_required
def arbeit():
    arbeiter1 = db.session.query(Nutzer.id, Nutzer.name).\
        select_from(Arbeiter).join(Nutzer).filter(Arbeiter.betrieb==current_user.id).group_by(Nutzer.id).all()
    table1 = ArbeiterTable1(arbeiter1, no_items='(Noch keine Mitarbeiter.)')

    arbeiter2 = db.session.query(Nutzer.id, Nutzer.name,
        func.concat(func.sum(Arbeit.stunden), " Std.").label('summe_stunden')).\
        select_from(Angebote).filter(Angebote.betrieb==current_user.id).\
        join(Arbeit).join(Nutzer).group_by(Nutzer.id).order_by(func.sum(Arbeit.stunden).desc()).all()
    table2 = ArbeiterTable2(arbeiter2, no_items='(Noch keine Stunden gearbeitet.)')
    fik = Betriebe.query.filter_by(id=current_user.id).first().fik

    if request.method == 'POST':
        # check if nutzer exists, if not flash warning
        if not Nutzer.query.filter_by(id=request.form['nutzer']).first():
            flash("Nutzer existiert nicht.")
            return redirect(url_for('main_betriebe.arbeit'))

        # check if nutzer is already arbeiter in betrieb
        req_arbeiter = Arbeiter.query.filter_by(nutzer=request.form['nutzer'], betrieb=current_user.id).first()
        # if so, flash warning
        if req_arbeiter:
            flash("Nutzer ist bereits in diesem Betrieb beschäftigt.")
        else:
            new_arbeiter = Arbeiter(nutzer=request.form['nutzer'], betrieb=current_user.id)
            db.session.add(new_arbeiter)
            db.session.commit()
        return redirect(url_for('main_betriebe.arbeit'))

    return render_template("arbeit.html", table1=table1, table2=table2, fik=fik)


@main_betriebe.route('/betriebe/produktionsmittel')
@login_required
def produktionsmittel():
    produktionsmittel_qry = db.session.query(Kaeufe.id, Angebote.name, Angebote.beschreibung,\
        func.concat(func.round(Kaeufe.kaufpreis, 2), " Std.").label("kaufpreis"),\
        func.concat(func.round(func.coalesce(func.sum(Produktionsmittel.prozent_gebraucht), 0), 2), " %").\
            label("prozent_gebraucht"))\
        .select_from(Kaeufe)\
        .filter(Kaeufe.betrieb==current_user.id).outerjoin(Produktionsmittel,\
        Kaeufe.id==Produktionsmittel.kauf).join(Angebote, Kaeufe.angebot==Angebote.id).\
        group_by(Kaeufe, Angebote, Produktionsmittel.kauf)

    produktionsmittel_aktiv = produktionsmittel_qry.having(func.coalesce(func.sum(Produktionsmittel.prozent_gebraucht).\
    label("prozent_gebraucht"), 0).label("prozent_gebraucht")<100).all()
    produktionsmittel_inaktiv = produktionsmittel_qry.having(func.coalesce(func.sum(Produktionsmittel.prozent_gebraucht).\
    label("prozent_gebraucht"), 0).label("prozent_gebraucht")== 100).all()

    table_aktiv = ProduktionsmittelTable(produktionsmittel_aktiv, no_items="(Keine Produktionsmittel vorhanden.)")
    table_inaktiv = ProduktionsmittelTable(produktionsmittel_inaktiv, no_items="(Noch keine Produktionsmittel verbraucht.)")

    return render_template('produktionsmittel.html', table_aktiv=table_aktiv, table_inaktiv=table_inaktiv)


@main_betriebe.route('/betriebe/suchen', methods=['GET', 'POST'])
@login_required
def suchen():
    return such_vorgang("betriebe", request.form)


@main_betriebe.route('/betriebe/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    table_of_composition =  get_table_of_composition(id)
    cols_dict = get_positions_in_table(table_of_composition)
    dot = create_dots(cols_dict, table_of_composition)
    piped = dot.pipe().decode('utf-8')
    table_preiszus = Preiszusammensetzung(table_of_composition)
    angebot_ = get_angebote().filter(Angebote.id == id).one()
    preise = (angebot_.preis, angebot_.koop_preis)

    if request.method == 'POST':
        return redirect('/betriebe/suchen')

    return render_template('details_betriebe.html', table_preiszus=table_preiszus, piped=piped, preise=preise)


@main_betriebe.route('/betriebe/kaufen/<int:id>', methods=['GET', 'POST'])
@login_required
def kaufen(id):
    qry = db.session.query(Angebote).filter(
                Angebote.id==id)
    angebot = qry.first()

    if angebot:
        if request.method == 'POST':
            kauf_vorgang(kaufender_type="betriebe", angebot=angebot, kaeufer_id=current_user.id)
            flash(f"Kauf von '{angebot.name}' erfolgreich!")
            return redirect('/betriebe/suchen')

        angebot = get_angebote().filter(Angebote.aktiv==True, Angebote.id==id).first()
        return render_template('kaufen_betriebe.html', angebot=angebot)
    else:
        return 'Error loading #{id}'.format(id=id)


@main_betriebe.route('/betriebe/anbieten', methods=['GET', 'POST'])
@login_required
def neues_angebot():
    """
    Ein neues Angebot hinzufügen
    """
    produktionsmittel_aktiv = db.session.query(Kaeufe.id,\
        Angebote.name,\
        Angebote.beschreibung,\
        Kaeufe.kaufpreis,\
        func.coalesce(func.sum(Produktionsmittel.prozent_gebraucht).\
            label("prozent_gebraucht"), 0).label("prozent_gebraucht")).\
        select_from(Kaeufe).\
        filter(Kaeufe.betrieb==current_user.id).outerjoin(Produktionsmittel,\
        Kaeufe.id==Produktionsmittel.kauf).\
        join(Angebote, Kaeufe.angebot==Angebote.id).\
        group_by(Kaeufe, Angebote, Produktionsmittel.kauf).\
        having(func.coalesce(func.sum(Produktionsmittel.prozent_gebraucht).\
            label("prozent_gebraucht"), 0).label("prozent_gebraucht")<100).all()

    arbeiter_all = db.session.\
        query(Nutzer.id, Nutzer.name).\
        select_from(Arbeiter).\
        join(Nutzer, Arbeiter.nutzer==Nutzer.id).\
        filter(Arbeiter.betrieb==current_user.id).\
        all()

    if request.method == 'POST':
        quantity = int(request.form["quantity"])
        # create request dictionary
        request_dict = request.form.to_dict()

        # arbeit
        # dict with arbeit values
        arbeit_dict = dict(filter(lambda elem: elem[0][:7] == 'nutzer_', request_dict.items()))
        # arbeit dict entries that are not zero
        arbeit_dict_not_zero = dict(filter(lambda elem: Decimal(elem[1]) != 0, arbeit_dict.items()))
        kosten_arbeit = 0
        if arbeit_dict_not_zero:
            # calculate kosten arbeit
            nutzer_id_list = []
            stunden_list = []
            for key in list(arbeit_dict_not_zero.keys()):
                nutzer_id_list.append(key[7:])
            for value in list(arbeit_dict_not_zero.values()):
                stunden_list.append(Decimal(value))
            assert len(nutzer_id_list) == len(stunden_list)
            kosten_arbeit = sum(stunden_list) / quantity

        # produktionsmittel
        # dict with produktionsmittel values
        pm_dict = dict(filter(lambda elem: elem[0][:3] == 'id_', request_dict.items()))
        # pm dict entries that are not zero
        pm_dict_not_zero = dict(filter(lambda elem: Decimal(elem[1]) != 0,pm_dict.items()))
        kosten_pm = 0
        if pm_dict_not_zero:
            # calculate kosten pm
            # turning pm-dict into two lists
            kauf_id_list = []
            prozent_list = []
            for key in list(pm_dict_not_zero.keys()):
                kauf_id_list.append(key[3:])
            for value in list(pm_dict_not_zero.values()):
                prozent_list.append(Decimal(value)/100)

            # preise
            preise_list = []
            for idx in kauf_id_list:
                # HIER WERDEN DIE ORIGINALEN KAUFPREISE ANGERECHNET, NICHT DIE AKTUELLEN
                # MARKTPREISE!
                qry = db.session.query(Kaeufe.kaufpreis).select_from(Kaeufe).\
                    filter(Kaeufe.id == idx).first()
                preise_list.append(Decimal(qry.kaufpreis))
            kosten_einzeln = []
            for num1, num2 in zip(prozent_list, preise_list):
                kosten_einzeln.append(num1 * num2)
            kosten_pm = sum(kosten_einzeln) / quantity

        # TO DO LATER: validate input/check if enough guthaben
        # if current_user.guthaben < sum(stunden_list):
        #     flash("Dein Guthaben reicht nicht aus, um die Arbeit zu bezahlen.")

        # save new angebot(e), pay workers and register arbeit and produktionsmittel
        current_time = datetime.datetime.now()
        for quant in range(quantity):
            new_angebot = Angebote(name=request.form["name"], cr_date=current_time,  betrieb=current_user.id,\
                beschreibung=request.form["beschreibung"], kategorie=request.form["kategorie"], p_kosten=kosten_pm,\
                v_kosten=kosten_arbeit, preis=kosten_arbeit + kosten_pm)
            db.session.add(new_angebot)
            db.session.commit()

            # create rows in table "arbeit"
            if arbeit_dict_not_zero:
                assert len(nutzer_id_list) == len(stunden_list)
                for count, i in enumerate(nutzer_id_list):
                    new_arbeit = Arbeit(angebot=new_angebot.id, nutzer=i,\
                        stunden=stunden_list[count] / quantity)
                    db.session.add(new_arbeit)
                    # guthaben der arbeiter erhöhen
                    # TO DO: check if it's inefficient doing this for every quant
                    Nutzer.query.filter_by(id=i).first().guthaben += stunden_list[count] / quantity

            # create new row in produktionsmittel (um gesamten verbrauch zu erhalten, muss gruppiert/summiert werden!)
            if pm_dict_not_zero:
                assert len(kauf_id_list) == len(prozent_list)
                for count, i in enumerate(kauf_id_list):
                    new_produktionsmittel_prd = Produktionsmittel\
                        (angebot=new_angebot.id, kauf=i, prozent_gebraucht=(prozent_list[count]*100 / quantity ))
                    db.session.add(new_produktionsmittel_prd)
            db.session.commit()

        # TO DO: kosten zusammenfassen und bestätigen lassen!
        flash('Angebot erfolgreich gespeichert!')
        return redirect(url_for("main_betriebe.meine_angebote"))

    categ = ["Dienstleistungen", "Elektronik",
    "Freizeit & Hobby", "Haus & Garten", "Haustiere", "Nahrungsmittel", "Musik, Filme und Bücher",
    "Nachbarschaftshilfe", "Unterricht und Kurse"]

    return render_template('neues_angebot.html', produktionsmittel_aktiv=produktionsmittel_aktiv, arbeiter_all=arbeiter_all, categ=categ)


@main_betriebe.route('/betriebe/meine_angebote')
@login_required
def meine_angebote():
    qry = get_angebote()
    aktuelle_angebote = qry.filter(Angebote.aktiv == True, Betriebe.id==current_user.id).all()
    vergangene_angebote = qry.filter(Angebote.aktiv == False, Betriebe.id==current_user.id).all()
    return render_template('meine_angebote.html', aktuelle_angebote=aktuelle_angebote, vergangene_angebote=vergangene_angebote)


@main_betriebe.route('/betriebe/angebot_loeschen', methods=['GET', 'POST'])
@login_required
def angebot_loeschen():
    angebot_id = request.args.get("id")
    angebot = Angebote.query.filter_by(id=angebot_id).first()
    if request.method == 'POST':
        angebot.aktiv = False
        db.session.commit()
        flash("Löschen des Angebots erfolgreich.")
        return redirect(url_for('main_betriebe.meine_angebote'))

    return render_template('angebot_loeschen.html', angebot=angebot)


@main_betriebe.route('/betriebe/angebot_verkaufen', methods=['GET', 'POST'])
@login_required
def angebot_verkaufen():
    angebot_id = request.args.get("id")
    angebot = Angebote.query.filter_by(id=angebot_id).first()

    if request.method == 'POST':
        code_input = request.form["code"]
        auszahlung = Auszahlungen.query.filter_by(code=code_input, entwertet=False).first()
        if not auszahlung:
            flash("Code nicht korrekt oder schon entwertet.")
        else:
            value_code = auszahlung.betrag
            if round(angebot.preis, 2) != round(value_code, 2):
                flash("Wert des Codes entspricht nicht dem Preis.")
            else:
                kaufender_type = "nutzer" if auszahlung.type_nutzer else "betriebe"
                kauf_vorgang(kaufender_type=kaufender_type, angebot=angebot, kaeufer_id=auszahlung.nutzer)
                auszahlung.entwertet = True
                db.session.commit()
                flash("Verkauf erfolgreich")
                return redirect(url_for("main_betriebe.meine_angebote"))

    return render_template('angebot_verkaufen.html', angebot=angebot)


@main_betriebe.route('/betriebe/kooperieren', methods=['GET', 'POST'])
@login_required
def kooperieren():
    if request.method == 'POST':
        angebot_id_eigenes = request.form["angebot_id_eigenes"]
        own = Angebote.query.filter_by(id=angebot_id_eigenes, aktiv=True).first()

        angebot_id_externes = request.form["angebot_id_externes"]
        extern = Angebote.query.filter_by(id=angebot_id_externes, aktiv=True).first()

        if not (own and extern):
            flash("Nicht existente Angebot-IDs")
        elif not Angebote.query.filter_by(id=angebot_id_eigenes, betrieb=current_user.id, aktiv=True).first():
            flash("Das Produkt ist nicht deines.")
        else:
            # one product can only be in one coop!
            eigene_koop = KooperationenMitglieder.query.filter_by(mitglied=angebot_id_eigenes, aktiv=True).first()
            externe_koop = KooperationenMitglieder.query.filter_by(mitglied=angebot_id_externes, aktiv=True).first()
            current_time = datetime.datetime.now()

            if (not eigene_koop and not externe_koop):
                print("neither exists")
                flash("Kooperation wird gestartet.")
                new_koop = Kooperationen(cr_date=current_time)
                db.session.add(new_koop)
                db.session.commit()
                # add all of the batch, not only specified angebot! (defined by cr_date and name) Muss evtl sicherer werden.
                for i in db.session.query(Angebote).filter_by(cr_date=own.cr_date, name=own.name).all():
                    new_koop_mitglieder_1 = KooperationenMitglieder(kooperation=new_koop.id, mitglied=i.id)
                    db.session.add(new_koop_mitglieder_1)
                for j in db.session.query(Angebote).filter_by(cr_date=extern.cr_date, name=extern.name).all():
                    new_koop_mitglieder_2 = KooperationenMitglieder(kooperation=new_koop.id, mitglied=j.id)
                    db.session.add(new_koop_mitglieder_2)
                db.session.commit()

            elif eigene_koop and externe_koop:
                print("both exist")
                if eigene_koop.kooperation == externe_koop.kooperation:
                    flash("Die beiden Produkte sind bereits in Kooperation.")
                else:
                    print("both in different coops")
                    flash("Das Produkt des Kooperationspartners\
                        befindet sich in einer Kooperation - die eigene Kooperation\
                        wird verlassen und der neuen beigetreten.")

                    # find out, how many different group of products you are cooperating with
                    coop_partners = db.session.\
                        query(func.count(Angebote.id)).\
                        select_from(KooperationenMitglieder).\
                        filter_by(kooperation=eigene_koop.kooperation, aktiv=True).\
                        join(Angebote, KooperationenMitglieder.mitglied == Angebote.id).\
                        group_by(Angebote.cr_date, Angebote.name, Angebote.preis).\
                        all()
                    amt_coop_partners = len(coop_partners)
                    eigene_ex_coop_id = eigene_koop.kooperation

                    # change coop
                    for i in db.session.query(Angebote).filter_by(cr_date=own.cr_date, name=own.name).all():
                        x = KooperationenMitglieder.query.filter_by(mitglied=i.id).first()
                        x.kooperation = externe_koop.kooperation
                    db.session.commit()

                    # if only 1 stays in old coop, than delete!
                    if amt_coop_partners == 2:
                        # delete the one remaining coop-member and the kooperative
                        for i in KooperationenMitglieder.query.filter_by(kooperation=eigene_ex_coop_id).all():
                            db.session.delete(i)
                        db.session.delete(Kooperationen.query.filter_by(id=eigene_ex_coop_id).first())
                        db.session.commit()


            elif eigene_koop and not externe_koop:
                print("only eigene exists")
                flash("Du befindest dich bereits in einer Kooperation\
                     - die aktuelle Kooperation wird verlassen und eine neue wird gestartet.")

                # find out, how many different group of products you are cooperating with
                coop_partners = db.session.\
                    query(func.count(Angebote.id)).\
                    select_from(KooperationenMitglieder).\
                    filter_by(kooperation=eigene_koop.kooperation, aktiv=True).\
                    join(Angebote, KooperationenMitglieder.mitglied == Angebote.id).\
                    group_by(Angebote.cr_date, Angebote.name, Angebote.preis).\
                    all()
                amt_coop_partners = len(coop_partners)
                eigene_ex_coop_id = eigene_koop.kooperation

                # start new koop
                new_koop = Kooperationen(cr_date=current_time)
                db.session.add(new_koop)
                db.session.commit()
                # add all of the batch, not only specified angebot! (defined by cr_date and name) Muss evtl sicherer werden.
                for i in db.session.query(Angebote).filter_by(cr_date=own.cr_date, name=own.name).all():
                    x = KooperationenMitglieder.query.filter_by(mitglied=i.id).first()
                    x.kooperation = new_koop.id
                for j in db.session.query(Angebote).filter_by(cr_date=extern.cr_date, name=extern.name).all():
                    new_koop_mitglieder_2 = KooperationenMitglieder(kooperation=new_koop.id, mitglied=j.id)
                    db.session.add(new_koop_mitglieder_2)
                db.session.commit()

                # if only 1 stays in old coop, than delete!
                if amt_coop_partners == 2:
                    # delete the one remaining coop-member and the kooperative
                    for i in KooperationenMitglieder.query.filter_by(kooperation=eigene_ex_coop_id).all():
                        db.session.delete(i)
                    db.session.delete(Kooperationen.query.filter_by(id=eigene_ex_coop_id).first())
                    db.session.commit()



            elif externe_koop and not eigene_koop:
                print("only externe exists")
                flash("Das Produkt des Kooperationspartners\
                    befindet sich in einer Kooperation - dein Produkt tritt dieser Kooperation bei.")
                # which coop to join?
                coop_to_join = externe_koop.kooperation
                # join coop
                for i in db.session.query(Angebote).filter_by(cr_date=own.cr_date, name=own.name).all():
                    new_koop_mitglieder = KooperationenMitglieder(kooperation=coop_to_join, mitglied=i.id)
                    db.session.add(new_koop_mitglieder)
                db.session.commit()


    meine_kooperationen = db.session.\
        query(func.min(Angebote.name).label("name"), func.min(KooperationenMitglieder.kooperation).label("kooperation")).\
        select_from(KooperationenMitglieder).\
        join(Angebote, KooperationenMitglieder.mitglied == Angebote.id).\
        filter(Angebote.betrieb == current_user.id, Angebote.aktiv == True).\
        group_by(Angebote.cr_date, Angebote.name).\
        all()

    eigenes_produkt_from_get = request.args.get("id")


    return render_template('kooperieren.html', meine_kooperationen=meine_kooperationen, prefilled=eigenes_produkt_from_get)


@main_betriebe.route('/betriebe/hilfe')
@login_required
def hilfe():
    return render_template('betriebe_hilfe.html')
