import os
import shutil
import csv
import re
from pypdf import PdfReader

# Directory definitions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")
DOCS_F1 = os.path.join(CORPUS_DIR, "documents", "famille_1")
DOCS_F2 = os.path.join(CORPUS_DIR, "documents", "famille_2")
IMAGES_DIR = os.path.join(CORPUS_DIR, "images")

os.makedirs(DOCS_F1, exist_ok=True)
os.makedirs(DOCS_F2, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Verifiers distribution among team members
VERIFIERS = ["Wiam", "Aya", "Hafsa"]

# Mapping and metadata definitions
# TDB Files
tdb_mapping = [
    {
        "src": "TDB/TDB-01_voyant_pression_huile.pdf",
        "doc_id": "tdb_01_voyant_pression_huile",
        "titre": "Voyant de pression d'huile moteur",
        "equip_id": "TDB-MOTEUR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-01-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P01)",
        "verifie_par": "Wiam",
        "corrections": "Précision du délai d'attente à 10 min avant contrôle de jauge",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Alerte critique rouge : arrêt immédiat obligatoire"
    },
    {
        "src": "TDB/TDB-02_surchauffe_liquide_refroidissement.pdf",
        "doc_id": "tdb_02_surchauffe_liquide_refroidissement",
        "titre": "Surchauffe du liquide de refroidissement",
        "equip_id": "TDB-MOTEUR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-02-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P01)",
        "verifie_par": "Aya",
        "corrections": "Ajout de la mise en garde contre l'ouverture du bocal sous pression",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Témoin thermomètre rouge d'arrêt moteur d'urgence"
    },
    {
        "src": "TDB/TDB-03_defaut_batterie_alternateur.pdf",
        "doc_id": "tdb_03_defaut_batterie_alternateur",
        "titre": "Défaut de batterie / circuit de charge (alternateur)",
        "equip_id": "TDB-ELEC-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-03-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P01)",
        "verifie_par": "Hafsa",
        "corrections": "Correction de la tension normale d'alternateur fixée entre 13.8V et 14.4V",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Voyant batterie rouge signalant une absence de charge"
    },
    {
        "src": "TDB/TDB-04_voyant_moteur_check_engine.pdf",
        "doc_id": "tdb_04_voyant_moteur_check_engine",
        "titre": "Voyant moteur (Check Engine)",
        "equip_id": "TDB-MOTEUR-01 ; TDB-ELEC-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-04-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P01)",
        "verifie_par": "Wiam",
        "corrections": "Distinction claire entre voyant fixe (dépollution) et clignotant (ratés d'allumage destructeurs)",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Codes DTC OBD-II standardisés P0300 à P0420"
    },
    {
        "src": "TDB/TDB-05_frein_a_main_liquide_de_frein.pdf",
        "doc_id": "tdb_05_frein_a_main_liquide_de_frein",
        "titre": "Voyant de frein (frein à main / niveau de liquide de frein)",
        "equip_id": "TDB-FREIN-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-05-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P01)",
        "verifie_par": "Aya",
        "corrections": "Précision sur la purge exclusive en fluide synthétique DOT 4",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Version nominale contredite par tdb_05_frein_liquide_v2 pour les tests"
    },
    {
        "src": "TDB/TDB-06_voyant_abs.pdf",
        "doc_id": "tdb_06_voyant_abs",
        "titre": "Voyant ABS (antiblocage des roues)",
        "equip_id": "TDB-FREIN-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-06-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P02)",
        "verifie_par": "Hafsa",
        "corrections": "Explicitation du maintien du freinage conventionnel sans assistance ABS",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Diagnostic capteur inductif / effet Hall de roue"
    },
    {
        "src": "TDB/TDB-07_voyant_esp_controle_stabilite.pdf",
        "doc_id": "tdb_07_voyant_esp_controle_stabilite",
        "titre": "Voyant ESP / contrôle de stabilité",
        "equip_id": "TDB-FREIN-01 ; TDB-CHASSIS-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-07-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P02)",
        "verifie_par": "Wiam",
        "corrections": "Clarification du clignotement lors de régulation active vs témoin fixe de défaillance",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Liaison capteur d'angle de braquage et lacet"
    },
    {
        "src": "TDB/TDB-08_voyant_airbag_srs.pdf",
        "doc_id": "tdb_08_voyant_airbag_srs",
        "titre": "Voyant d'airbag (SRS)",
        "equip_id": "TDB-SEC-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-08-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P02)",
        "verifie_par": "Aya",
        "corrections": "Interdiction absolue d'utilisation d'ohmmètre classique sur déclencheurs pyrotechniques",
        "groupe_acces": "responsables",
        "usage_test": "normal",
        "remarques": "Fiche de sécurité pyrotechnique à accès restreint"
    },
    {
        "src": "TDB/TDB-09_voyant_pression_pneus_tpms.pdf",
        "doc_id": "tdb_09_voyant_pression_pneus_tpms",
        "titre": "Voyant de pression des pneus (TPMS)",
        "equip_id": "TDB-TPMS-01 ; PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-09-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P02)",
        "verifie_par": "Hafsa",
        "corrections": "Ajout du protocole de réinitialisation manuelle via menu combiné",
        "groupe_acces": "techniciens_tdb ; techniciens_pneumatiques ; responsables",
        "usage_test": "ambigu",
        "remarques": "Cas pivot faisant le pont entre tableaux de bord et pneumatiques ; risque d'ambiguïté visuelle"
    },
    {
        "src": "TDB/TDB-10_voyant_filtre_a_particules_fap.pdf",
        "doc_id": "tdb_10_voyant_filtre_a_particules_fap",
        "titre": "Voyant du filtre à particules (FAP / DPF)",
        "equip_id": "TDB-ECHAP-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-10-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P03)",
        "verifie_par": "Wiam",
        "corrections": "Précision de la vitesse mini (70 km/h à 2500 tr/min) pour cycle de régénération passive",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Surveillance pression différentielle amont/aval FAP"
    },
    {
        "src": "TDB/TDB-11_voyant_prechauffage_diesel.pdf",
        "doc_id": "tdb_11_voyant_prechauffage_diesel",
        "titre": "Voyant de préchauffage diesel",
        "equip_id": "TDB-MOTEUR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-11-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P03)",
        "verifie_par": "Aya",
        "corrections": "Précision sur la fonction de voyant de défaut gestion moteur en cas de clignotement en roulant",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Témoin spirale jaune / ambre"
    },
    {
        "src": "TDB/TDB-12_niveau_carburant_bas.pdf",
        "doc_id": "tdb_12_niveau_carburant_bas",
        "titre": "Voyant de niveau de carburant bas (réserve)",
        "equip_id": "TDB-COMB-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-12-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P03)",
        "verifie_par": "Hafsa",
        "corrections": "Mise en garde contre le désamorçage de pompe immergée et surchauffe",
        "groupe_acces": "techniciens_tdb ; techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Seuil d'alerte configuré à 10% du volume réservoir"
    },
    {
        "src": "TDB/TDB-13_defaut_direction_assistee.pdf",
        "doc_id": "tdb_13_defaut_direction_assistee",
        "titre": "Défaut de direction assistée",
        "equip_id": "TDB-CHASSIS-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-13-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P03)",
        "verifie_par": "Wiam",
        "corrections": "Distinction direction électromécanique (EPS) vs hydraulique classique",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Volant orange ou rouge sur combiné d'instruments"
    },
    {
        "src": "TDB/TDB-14_voyant_adblue.pdf",
        "doc_id": "tdb_14_voyant_adblue",
        "titre": "Voyant d'AdBlue (niveau ou défaut de dépollution)",
        "equip_id": "TDB-ECHAP-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-14-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P04)",
        "verifie_par": "Aya",
        "corrections": "Ajout du compte à rebours de non-redémarrage réglementaire (norme Euro 6)",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Défaut de cristallisation d'injecteur SCR fréquent"
    },
    {
        "src": "TDB/TDB-15_voyant_ceinture_securite.pdf",
        "doc_id": "tdb_15_voyant_ceinture_securite",
        "titre": "Voyant de ceinture de sécurité",
        "equip_id": "TDB-SEC-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-15-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P04)",
        "verifie_par": "Hafsa",
        "corrections": "Interdiction formelle de leurres de boucle de ceinture",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Contrôle capteur de présence passager (nappe de siège)"
    },
    {
        "src": "TDB/TDB-16_defaut_boite_automatique.pdf",
        "doc_id": "tdb_16_defaut_boite_automatique",
        "titre": "Défaut de transmission / boîte automatique",
        "equip_id": "TDB-TRANS-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-16-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P04)",
        "verifie_par": "Wiam",
        "corrections": "Procédure de déverrouillage manuel du sélecteur en position N/P",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Mode dégradé bloquant le 3e rapport hydraulique"
    },
    {
        "src": "TDB/TDB-17_defaut_feux_ampoule.pdf",
        "doc_id": "tdb_17_defaut_feux_ampoule",
        "titre": "Défaut des feux / ampoule grillée",
        "equip_id": "TDB-ELEC-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-17-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P04)",
        "verifie_par": "Aya",
        "corrections": "Mise en garde sur les faux positifs causés par les ampoules LED non canbus",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Témoin ampoule jaune avec point d'exclamation"
    },
    {
        "src": "TDB/TDB-18_defaut_antidemarrage_immobilisateur.pdf",
        "doc_id": "tdb_18_defaut_antidemarrage_immobilisateur",
        "titre": "Défaut d'antidémarrage (immobilisateur)",
        "equip_id": "TDB-SEC-01 ; TDB-ELEC-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-18-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P05)",
        "verifie_par": "Hafsa",
        "corrections": "Protocole de contrôle de la bague transpondeur Neiman",
        "groupe_acces": "responsables",
        "usage_test": "normal",
        "remarques": "Accès restreint aux responsables d'atelier pour raisons de sécurité vol"
    },
    {
        "src": "TDB/TDB-19_voyant_maintenance_revision.pdf",
        "doc_id": "tdb_19_voyant_maintenance_revision",
        "titre": "Voyant de maintenance / révision (clé à molette)",
        "equip_id": "TDB-MAINT-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-19-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P05)",
        "verifie_par": "Wiam",
        "corrections": "Détail de la manipulation de remise à zéro manuelle au comodo",
        "groupe_acces": "techniciens_tdb ; techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Témoin service révision périodique"
    },
    {
        "src": "TDB/TDB-20_tableau_de_bord_eteint_defaillant.pdf",
        "doc_id": "tdb_20_tableau_de_bord_eteint_defaillant",
        "titre": "Tableau de bord éteint ou défaillant",
        "equip_id": "TDB-COMB-01 ; TDB-ELEC-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure TDB-20-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P05)",
        "verifie_par": "Aya",
        "corrections": "Schéma de contrôle des fusibles d'alimentation permanente et après-contact",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Panne générale combiné d'instruments / bus CAN habitacle"
    }
]

# PNE Files
pne_mapping = [
    {
        "src": "PNE/PNE-01_Flat_Tire.pdf",
        "doc_id": "pne_01_flat_tire",
        "titre": "Pneu dégonflé (Flat Tire)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-01-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P06)",
        "verifie_par": "Wiam",
        "corrections": "Interdiction absolue de rouler à plat pour préserver la carcasse",
        "groupe_acces": "techniciens_pneumatiques ; techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Corrélation directe avec alerte TPMS TDB-09"
    },
    {
        "src": "PNE/PNE-02_Nail_Puncture.pdf",
        "doc_id": "pne_02_nail_puncture",
        "titre": "Crevaison par clou (Nail Puncture)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-02-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P06)",
        "verifie_par": "Aya",
        "corrections": "Rappel de la zone réparable (bande de roulement centrale, zone T)",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Réparation par cheville champignon (PRP) après démontage obligatoire"
    },
    {
        "src": "PNE/PNE-03_Screw_Puncture.pdf",
        "doc_id": "pne_03_screw_puncture",
        "titre": "Crevaison par vis (Screw Puncture)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-03-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P06)",
        "verifie_par": "Hafsa",
        "corrections": "Interdiction de dévisser la vis sans matériel de mise sous pression disponible",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Perforation filetée risquant d'endommager les nappes métalliques"
    },
    {
        "src": "PNE/PNE-04_Incorrect_Inflation_Wear.pdf",
        "doc_id": "pne_04_incorrect_inflation_wear",
        "titre": "Usure due à une mauvaise pression de gonflage (Incorrect Inflation Wear)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-04-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P06)",
        "verifie_par": "Wiam",
        "corrections": "Distinction usure centrale (surpression) vs usure des deux épaulements (sous-gonflage)",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Version de référence contredite par pne_04_usure_pression_v2"
    },
    {
        "src": "PNE/PNE-05_Sidewall_Bulge.pdf",
        "doc_id": "pne_05_sidewall_bulge",
        "titre": "Hernie sur le flanc du pneu (Sidewall Bulge)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-05-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P07)",
        "verifie_par": "Aya",
        "corrections": "Remplacement obligatoire immédiat : rupture de carcasse non réparable",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Risque majeur d'éclatement instantané sous charge"
    },
    {
        "src": "PNE/PNE-06_Sidewall_Cut.pdf",
        "doc_id": "pne_06_sidewall_cut",
        "titre": "Coupure sur le flanc du pneu (Sidewall Cut)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-06-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P07)",
        "verifie_par": "Hafsa",
        "corrections": "Critère de mise au rebut : si les câbles textiles ou aciers sont visibles",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Dégât par trottoir ou objet tranchant"
    },
    {
        "src": "PNE/PNE-07_Sidewall_Abrasion.pdf",
        "doc_id": "pne_07_sidewall_abrasion",
        "titre": "Abrasion du flanc du pneu (Sidewall Abrasion)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-07-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P07)",
        "verifie_par": "Wiam",
        "corrections": "Contrôle de profondeur du cordon de protection de jante",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Frottement répété le long des bordures"
    },
    {
        "src": "PNE/PNE-08_Tire_Cracking_Dry_Rot.pdf",
        "doc_id": "pne_08_tire_cracking_dry_rot",
        "titre": "Craquelures et vieillissement du caoutchouc (Tire Cracking / Dry Rot)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-08-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P07)",
        "verifie_par": "Aya",
        "corrections": "Vérification du code DOT (semaine/année) : limite de vie recommandée à 5-6 ans",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Oxydation et vieillissement par UV et ozone"
    },
    {
        "src": "PNE/PNE-09_Bald_Tire.pdf",
        "doc_id": "pne_09_bald_tire",
        "titre": "Usure excessive de la bande de roulement (Bald Tire)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-09-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P08)",
        "verifie_par": "Hafsa",
        "corrections": "Rappel de la limite légale stricte de 1.6 mm (témoins TWI)",
        "groupe_acces": "techniciens_pneumatiques ; techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Perte totale d'évacuation d'eau : risque d'aquaplaning critique"
    },
    {
        "src": "PNE/PNE-10_Cupping_Wear.pdf",
        "doc_id": "pne_10_cupping_wear",
        "titre": "Usure en facettes ou en dents de scie (Cupping Wear)",
        "equip_id": "PNEU-SUSP-01 ; PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-10-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P08)",
        "verifie_par": "Wiam",
        "corrections": "Diagnostic lié aux amortisseurs usés ou silentblocs de train défaillants",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Génère bruit de roulement sourd et vibrations volant"
    },
    {
        "src": "PNE/PNE-11_Feathering_Wear.pdf",
        "doc_id": "pne_11_feathering_wear",
        "titre": "Usure en écaille (Feathering Wear)",
        "equip_id": "PNEU-SUSP-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-11-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P08)",
        "verifie_par": "Aya",
        "corrections": "Corrélation directe avec un défaut de parallélisme (pincement ou ouverture)",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Bord tranchant sensible au toucher transversal sur la bande"
    },
    {
        "src": "PNE/PNE-12_Flat_Spot.pdf",
        "doc_id": "pne_12_flat_spot",
        "titre": "Méplat sur le pneu (Flat Spot)",
        "equip_id": "PNEU-TR-01 ; TDB-FREIN-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-12-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P08)",
        "verifie_par": "Hafsa",
        "corrections": "Distinction méplat temporaire (stationnement hivernal) vs définitif (blocage de roue)",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Souvent causé par un défaut du système antiblocage ABS"
    },
    {
        "src": "PNE/PNE-13_Tread_Chunking.pdf",
        "doc_id": "pne_13_tread_chunking",
        "titre": "Arrachement de morceaux de gomme (Tread Chunking)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-13-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P09)",
        "verifie_par": "Wiam",
        "corrections": "Évaluation de la profondeur des cratères par rapport aux toiles internes",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Consécutif à un roulage agressif sur graviers ou circuit"
    },
    {
        "src": "PNE/PNE-14_Uneven_Tread_Wear.pdf",
        "doc_id": "pne_14_uneven_tread_wear",
        "titre": "Usure irrégulière de la bande de roulement (Uneven Tread Wear)",
        "equip_id": "PNEU-SUSP-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-14-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P09)",
        "verifie_par": "Aya",
        "corrections": "Prise en compte du carrossage négatif excessif provoquant usure intérieure",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Nécessite passage complet sur banc de géométrie 3D"
    },
    {
        "src": "PNE/PNE-15_Tread_Separation.pdf",
        "doc_id": "pne_15_tread_separation",
        "titre": "Décollement de la bande de roulement (Tread Separation)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-15-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P09)",
        "verifie_par": "Hafsa",
        "corrections": "Interdiction de rouler et immobilisation immédiate",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Rupture de cohésion vulcanisée entre nappes sommet"
    },
    {
        "src": "PNE/PNE-16_Casing_Separation.pdf",
        "doc_id": "pne_16_casing_separation",
        "titre": "Décollement des couches internes du pneu (Casing Separation)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-16-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P09)",
        "verifie_par": "Wiam",
        "corrections": "Rebut obligatoire : défaut structurel interne irréversible",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Détection au toucher (ondulations floues sur le pneu gonflé)"
    },
    {
        "src": "PNE/PNE-17_Inner_Liner_Damage.pdf",
        "doc_id": "pne_17_inner_liner_damage",
        "titre": "Détérioration de la doublure intérieure (Inner Liner Damage)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-17-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P10)",
        "verifie_par": "Aya",
        "corrections": "Explication de la perte d'étanchéité par abrasion interne lors de roulage à plat",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Présence caractéristique de poudre de gomme noire à l'intérieur"
    },
    {
        "src": "PNE/PNE-18_Bead_Damage.pdf",
        "doc_id": "pne_18_bead_damage",
        "titre": "Détérioration du talon du pneu (Bead Damage)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-18-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P10)",
        "verifie_par": "Hafsa",
        "corrections": "Sensibilisation à l'utilisation correcte du levier de montage et de pâte lubrifiante",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Déchirure de tringle empêchant le maintien de pression sur jante"
    },
    {
        "src": "PNE/PNE-19_Bead_Separation.pdf",
        "doc_id": "pne_19_bead_separation",
        "titre": "Décollement du talon du pneu (Bead Separation)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-19-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P10)",
        "verifie_par": "Wiam",
        "corrections": "Mise au rebut sans tentative de réparation",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Survient généralement après échauffement extrême des freins"
    },
    {
        "src": "PNE/PNE-20_Exposed_Steel_Cords.pdf",
        "doc_id": "pne_20_exposed_steel_cords",
        "titre": "Câbles métalliques apparents (Exposed Steel Cords)",
        "equip_id": "PNEU-TR-01",
        "type_doc": "fiche_securite",
        "version": "v1.0 (2026-11)",
        "elements_visuels": "Figure PNE-20-F1 p.1 ; tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P10)",
        "verifie_par": "Aya",
        "corrections": "Port d'EPI renforcé (gants anti-coupure) obligatoire lors de la manipulation",
        "groupe_acces": "techniciens_pneumatiques ; techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Danger de crevaison explosive et blessure physique par fils d'acier acérés"
    }
]

# Additional Test Documents
special_docs = [
    # 1. Contradictory TDB v2
    {
        "src": "test_special/tdb_05_procedure_liquide_frein_v2.pdf",
        "dest_folder": DOCS_F1,
        "doc_id": "tdb_05_frein_liquide_v2",
        "titre": "Procédure d'appoint et purge liquide de frein (v2 - Révisée)",
        "famille_equipement": "tableaux_de_bord",
        "equip_id": "TDB-FREIN-01",
        "type_doc": "procedure",
        "version": "v2.0 (2026-11)",
        "nb_pages": 2,
        "format": "pdf_texte",
        "elements_visuels": "tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P11)",
        "verifie_par": "Wiam",
        "corrections": "Création intentionnelle de contradiction sur fluide DOT 5 vs DOT 4",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "contradictoire",
        "remarques": "Contredit expressément tdb_05_frein_a_main_liquide_de_frein sur les fluides autorisés"
    },
    # 2. Contradictory PNE v2
    {
        "src": "test_special/pne_04_procedure_pression_pneus_v2.pdf",
        "dest_folder": DOCS_F2,
        "doc_id": "pne_04_usure_pression_v2",
        "titre": "Procédure d'ajustement pression pneumatiques (v2 - Révisée)",
        "famille_equipement": "pneumatiques",
        "equip_id": "PNEU-TR-01",
        "type_doc": "procedure",
        "version": "v2.0 (2026-11)",
        "nb_pages": 2,
        "format": "pdf_texte",
        "elements_visuels": "tableau p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P11)",
        "verifie_par": "Aya",
        "corrections": "Création intentionnelle de contradiction sur la mesure de pression à chaud",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "contradictoire",
        "remarques": "Contredit expressément pne_04_incorrect_inflation_wear sur les tolérances à chaud"
    },
    # 3. Injection Document
    {
        "src": "test_special/tdb_note_service_piegee.pdf",
        "dest_folder": DOCS_F1,
        "doc_id": "tdb_note_service_piegee",
        "titre": "Note de service confidentielle : Audit et étalonnage combiné",
        "famille_equipement": "tableaux_de_bord",
        "equip_id": "TDB-COMB-01 ; TDB-ELEC-02",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "nb_pages": 2,
        "format": "pdf_texte",
        "elements_visuels": "encadré alerte p.1",
        "outil_ia": "Claude 3.5 Sonnet (prompt P12)",
        "verifie_par": "Hafsa",
        "corrections": "Intégration d'un payload d'injection indirecte de prompt en p.1",
        "groupe_acces": "responsables",
        "usage_test": "injection",
        "remarques": "Document piégé pour tester l'exfiltration et le contournement MCP en Semaine 5"
    },
    # 4. Scanned TDB (OCR test)
    {
        "src": "test_special/tdb_19_fiche_revision_scanne.pdf",
        "dest_folder": DOCS_F1,
        "doc_id": "tdb_19_fiche_revision_scanne",
        "titre": "Fiche de révision atelier et remise à zéro combiné (Scan)",
        "famille_equipement": "tableaux_de_bord",
        "equip_id": "TDB-MAINT-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "nb_pages": 1,
        "format": "pdf_scanne",
        "elements_visuels": "Page scannée avec tampon et tableau manuscrit p.1",
        "outil_ia": "Génération image Pillow (prompt P13)",
        "verifie_par": "Wiam",
        "corrections": "Rasterisation 150 DPI sans calque texte pour test OCR",
        "groupe_acces": "techniciens_tdb ; responsables",
        "usage_test": "normal",
        "remarques": "Document scanné pour valider le pipeline OCR multimodal en Semaine 2"
    },
    # 5. Scanned PNE (OCR test)
    {
        "src": "test_special/pne_12_fiche_controle_geometrie_scanne.pdf",
        "dest_folder": DOCS_F2,
        "doc_id": "pne_12_fiche_controle_geometrie_scanne",
        "titre": "Rapport banc de géométrie et usure méplat (Scan)",
        "famille_equipement": "pneumatiques",
        "equip_id": "PNEU-SUSP-01",
        "type_doc": "procedure",
        "version": "v1.0 (2026-11)",
        "nb_pages": 1,
        "format": "pdf_scanne",
        "elements_visuels": "Rapport scanné avec valeurs de carrossage et tampon p.1",
        "outil_ia": "Génération image Pillow (prompt P13)",
        "verifie_par": "Hafsa",
        "corrections": "Rasterisation 150 DPI sans calque texte pour test OCR",
        "groupe_acces": "techniciens_pneumatiques ; responsables",
        "usage_test": "normal",
        "remarques": "Document scanné pour valider le pipeline OCR multimodal en Semaine 2"
    }
]

# Process and copy files
all_inventory_rows = []

# Process TDB
for item in tdb_mapping:
    src_path = os.path.join(BASE_DIR, item["src"])
    dest_path = os.path.join(DOCS_F1, f"{item['doc_id']}.pdf")
    shutil.copy2(src_path, dest_path)
    
    # Extract images to corpus/images/
    r = PdfReader(dest_path)
    for p_idx, page in enumerate(r.pages):
        for img_idx, img in enumerate(page.images):
            ext = 'jpg' if 'jp' in img.name.lower() else 'png'
            img_dest = os.path.join(IMAGES_DIR, f"{item['doc_id']}_f{img_idx+1}.{ext}")
            with open(img_dest, 'wb') as f_img:
                f_img.write(img.data)
                
    row = {
        "document_id": item["doc_id"],
        "fichier": f"documents/famille_1/{item['doc_id']}.pdf",
        "titre": item["titre"],
        "famille_equipement": "tableaux_de_bord",
        "equipement_id": item["equip_id"],
        "type_document": item["type_doc"],
        "version": item["version"],
        "nb_pages": len(r.pages),
        "langue": "fr",
        "format": "pdf_texte",
        "elements_visuels": item["elements_visuels"],
        "provenance": "synthetique",
        "licence": "synthetique (CC BY-SA 4.0 pédagogique)",
        "genere_par_ia": "oui",
        "outil_ia": item["outil_ia"],
        "verifie_par": item["verifie_par"],
        "corrections": item["corrections"],
        "groupe_acces": item["groupe_acces"],
        "usage_test": item["usage_test"],
        "remarques": item["remarques"]
    }
    all_inventory_rows.append(row)

# Process PNE
for item in pne_mapping:
    src_path = os.path.join(BASE_DIR, item["src"])
    dest_path = os.path.join(DOCS_F2, f"{item['doc_id']}.pdf")
    shutil.copy2(src_path, dest_path)
    
    # Extract images to corpus/images/
    r = PdfReader(dest_path)
    for p_idx, page in enumerate(r.pages):
        for img_idx, img in enumerate(page.images):
            ext = 'jpg' if 'jp' in img.name.lower() else 'png'
            img_dest = os.path.join(IMAGES_DIR, f"{item['doc_id']}_f{img_idx+1}.{ext}")
            with open(img_dest, 'wb') as f_img:
                f_img.write(img.data)
                
    row = {
        "document_id": item["doc_id"],
        "fichier": f"documents/famille_2/{item['doc_id']}.pdf",
        "titre": item["titre"],
        "famille_equipement": "pneumatiques",
        "equipement_id": item["equip_id"],
        "type_document": item["type_doc"],
        "version": item["version"],
        "nb_pages": len(r.pages),
        "langue": "fr",
        "format": "pdf_texte",
        "elements_visuels": item["elements_visuels"],
        "provenance": "synthetique",
        "licence": "synthetique (CC BY-SA 4.0 pédagogique)",
        "genere_par_ia": "oui",
        "outil_ia": item["outil_ia"],
        "verifie_par": item["verifie_par"],
        "corrections": item["corrections"],
        "groupe_acces": item["groupe_acces"],
        "usage_test": item["usage_test"],
        "remarques": item["remarques"]
    }
    all_inventory_rows.append(row)

# Process Special Docs
for item in special_docs:
    src_path = os.path.join(BASE_DIR, item["src"])
    dest_path = os.path.join(item["dest_folder"], f"{item['doc_id']}.pdf")
    shutil.copy2(src_path, dest_path)
    
    folder_rel = "famille_1" if item["dest_folder"] == DOCS_F1 else "famille_2"
    row = {
        "document_id": item["doc_id"],
        "fichier": f"documents/{folder_rel}/{item['doc_id']}.pdf",
        "titre": item["titre"],
        "famille_equipement": item["famille_equipement"],
        "equipement_id": item["equip_id"],
        "type_document": item["type_doc"],
        "version": item["version"],
        "nb_pages": item["nb_pages"],
        "langue": "fr",
        "format": item["format"],
        "elements_visuels": item["elements_visuels"],
        "provenance": "synthetique",
        "licence": "synthetique (CC BY-SA 4.0 pédagogique)",
        "genere_par_ia": "oui",
        "outil_ia": item["outil_ia"],
        "verifie_par": item["verifie_par"],
        "corrections": item["corrections"],
        "groupe_acces": item["groupe_acces"],
        "usage_test": item["usage_test"],
        "remarques": item["remarques"]
    }
    all_inventory_rows.append(row)

# Write corpus/inventaire.csv
csv_path = os.path.join(CORPUS_DIR, "inventaire.csv")
fieldnames = [
    "document_id", "fichier", "titre", "famille_equipement", "equipement_id",
    "type_document", "version", "nb_pages", "langue", "format",
    "elements_visuels", "provenance", "licence", "genere_par_ia",
    "outil_ia", "verifie_par", "corrections", "groupe_acces",
    "usage_test", "remarques"
]

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in all_inventory_rows:
        writer.writerow(r)

print(f"Generated {csv_path} with {len(all_inventory_rows)} documents.")
