import os
import csv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Two-pass canvas for exact "Page X sur Y" and running headers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # No header/footer on cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0F172A"))
        self.drawString(45, 804, "MaintiDoc — Livrable 1 : Cadrage, Corpus et Architecture Cible")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(550, 804, "EMSI 2026 | ELAOUAZI · SOUILI · YEKHLEF")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 798, 550, 798)

        # Footer
        self.line(45, 42, 550, 42)
        self.setFont("Helvetica", 7.5)
        self.drawString(45, 30, "Module IA Générative Multimodale — Dossier d'Ingénierie & d'Architecture")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(550, 30, page_str)
        self.restoreState()


def build_pdf(filename="L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=52,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Premium Palette
    c_navy = colors.HexColor('#0F172A')       # Dark Slate / Navy
    c_blue = colors.HexColor('#1E3A8A')       # Deep Blue
    c_teal = colors.HexColor('#0D9488')       # Dark Teal
    c_text = colors.HexColor('#1E293B')       # Readable body text
    c_muted = colors.HexColor('#475569')      # Muted text
    c_border = colors.HexColor('#CBD5E1')     # Clean borders
    c_bg_subtle = colors.HexColor('#F8FAFC')  # Background light
    c_alert = colors.HexColor('#DC2626')      # Red alert

    # Typography styles
    s_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=25,
        leading=30,
        textColor=c_navy,
        alignment=1,
        spaceAfter=10
    )

    s_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_teal,
        alignment=1,
        spaceAfter=25
    )

    s_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=c_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    s_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_navy,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    s_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_teal,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    s_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.3,
        textColor=c_text,
        spaceAfter=4
    )

    s_body_bold = ParagraphStyle(
        'BodyBold_Custom',
        parent=s_body,
        fontName='Helvetica-Bold'
    )

    s_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.3,
        textColor=c_text,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    s_callout = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.8,
        textColor=colors.HexColor('#0F172A')
    )

    s_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.8,
        textColor=c_navy
    )

    s_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=s_table_cell,
        fontName='Helvetica-Bold'
    )

    s_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    s_code = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    def make_box(content_list, bg_color='#F8FAFC', border_color='#CBD5E1', padding=5):
        tbl = Table([[content_list]], colWidths=[505])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
            ('TOPPADDING', (0,0), (-1,-1), padding),
            ('BOTTOMPADDING', (0,0), (-1,-1), padding),
            ('LEFTPADDING', (0,0), (-1,-1), padding + 3),
            ('RIGHTPADDING', (0,0), (-1,-1), padding + 3),
        ]))
        return tbl

    # =========================================================================
    # PAGE 1 : PAGE DE GARDE / DOSSIER D'INGÉNIERIE OFFICIEL
    # =========================================================================
    story.append(Spacer(1, 25))
    badge_data = [
        [Paragraph("<b>ÉCOLE MAROCAINE DES SCIENCES DE L'INGÉNIEUR — EMSI CASABLANCA</b>", 
                   ParagraphStyle('B1', parent=s_body_bold, fontSize=9.5, alignment=1, textColor=colors.HexColor('#0F172A')))],
        [Paragraph("Cycle Ingénieur en Informatique & Intelligence Artificielle | Module IA Générative Multimodale",
                   ParagraphStyle('B2', parent=s_body, fontSize=8, alignment=1, textColor=c_muted))]
    ]
    t_badge = Table(badge_data, colWidths=[505])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 45))

    story.append(Paragraph("PROJET MAINTIDOC", s_title))
    story.append(Paragraph("Assistant Documentaire Multimodal et Agentique pour la Maintenance Automobile", s_subtitle))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>LIVRABLE 1 : CADRAGE TECHNIQUE, CORPUS ET ARCHITECTURE CIBLE</b>", 
                           ParagraphStyle('L1Tag', parent=s_body_bold, fontSize=11, alignment=1, textColor=c_blue)))
    story.append(Paragraph("Cahier des charges initial, pipeline d'ingestion vérifié, interfaçage MCP et modèle de sécurité", 
                           ParagraphStyle('L1Sub', parent=s_body, fontSize=9, alignment=1, textColor=c_muted)))
    
    story.append(Spacer(1, 35))

    # Meta team table with official GitHub link
    team_table_data = [
        [Paragraph("<b>Équipe d'ingénierie :</b>", s_table_cell_bold), Paragraph("<b>ELAOUAZI - SOUILI - YEKHLEF</b>", s_table_cell_bold)],
        [Paragraph("<b>Membres du projet :</b>", s_table_cell), 
         Paragraph("• <b>ELAOUAZI Hafsa</b> (Lead Évaluation, Sécurité des Prompts & Gestion du Corpus)<br/>"
                   "• <b>SOUILI Wiam</b> (Lead Architecture Système, LangGraph & Interfaçage MCP)<br/>"
                   "• <b>YEKHLEF Aya</b> (Lead RAG Multimodal, Ingestion ETL & Recherche Vectorielle)", s_table_cell)],
        [Paragraph("<b>Enseignante responsable :</b>", s_table_cell_bold), Paragraph("<b>Pr. Mariam CHERRABI</b>", s_table_cell_bold)],
        [Paragraph("<b>Périmètre matériel :</b>", s_table_cell_bold), Paragraph("Famille 1 : <b>Tableaux de bord (électronique/témoins)</b> — Famille 2 : <b>Pneumatiques (liaison au sol)</b>", s_table_cell)],
        [Paragraph("<b>Dépôt Git de l'équipe :</b>", s_table_cell_bold), Paragraph("<b>https://github.com/YekhlefAya/MaintiDoc-ELAOUAZI-SOUILI-YEKHLEF.git</b>", s_code)],
        [Paragraph("<b>Date de rendu :</b>", s_table_cell_bold), Paragraph("Novembre 2026 — Fin de Semaine 1", s_table_cell)]
    ]
    t_team = Table(team_table_data, colWidths=[135, 370])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_team)

    story.append(Spacer(1, 30))

    exec_summary = (
        "<b>Note de cadrage exécutif :</b> Ce rapport établit le socle d'ingénierie préliminaire du projet MaintiDoc "
        "avant toute phase de développement logiciel. Nous définissons ici les besoins stricts des techniciens d'atelier, "
        "les cas d'usage nominaux et dégradés, et le périmètre d'action du système. Nous introduisons un corpus de 45 documents "
        "techniques contrôlés et vérifiés manuellement couvrant les combinés de bord et le train roulant pneumatique. "
        "L'architecture proposée repose sur une séparation claire entre la vision-langage (VLM), la recherche vectorielle "
        "multimodale (Qdrant), l'orchestration par graphe d'états (LangGraph) et les outils d'atelier (MCP), assortie de "
        "trois points de contrôle incontournables garantissant la sécurité des opérateurs et l'intégrité des données."
    )
    story.append(make_box(Paragraph(exec_summary, s_callout), bg_color='#F1F5F9', border_color='#94A3B8'))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2 : SOMMAIRE ET SECTION 2.1 - CADRAGE DU PROJET
    # =========================================================================
    story.append(Paragraph("Sommaire du Rapport d'Ingénierie", s_h2))
    toc_data = [
        [Paragraph("<b>2.1 Cadrage du projet</b> (Contexte métier, profils utilisateurs, cas d'usage, objectifs S6, périmètre)", s_table_cell), Paragraph("Pages 2-3", s_table_cell_bold)],
        [Paragraph("<b>2.2 Constitution du corpus documentaire</b> (45 documents vérifiés, traçabilité de l'IA, analyse critique, tests)", s_table_cell), Paragraph("Pages 4-5", s_table_cell_bold)],
        [Paragraph("<b>2.3 Architecture cible</b> (Schéma fonctionnel, fiches des 7 blocs, points de contrôle, parcours requête)", s_table_cell), Paragraph("Pages 6-8", s_table_cell_bold)],
        [Paragraph("<b>2.4 Flux de données et modèle d'accès</b> (Pipelines d'ingestion, flux requête, cycle MCP, modèle RBAC)", s_table_cell), Paragraph("Pages 9-10", s_table_cell_bold)],
        [Paragraph("<b>2.5 Analyse des risques</b> (Matrice de 9 risques : technique, sécurité, données et organisation)", s_table_cell), Paragraph("Page 11", s_table_cell_bold)],
        [Paragraph("<b>2.6 Planning et organisation de l'équipe</b> (Répartition des spécialisations, feuille de route S2-S6, RACI)", s_table_cell), Paragraph("Pages 12-13", s_table_cell_bold)],
        [Paragraph("<b>Annexes techniques</b> (Inventaire synthétique complet des 45 documents du corpus MaintiDoc)", s_table_cell), Paragraph("Pages 14-15", s_table_cell_bold)],
    ]
    t_toc = Table(toc_data, colWidths=[420, 85])
    t_toc.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.1 Cadrage du Projet", s_h1))
    story.append(Paragraph("2.1.1 Contexte Opérationnel et Profils Utilisateurs", s_h2))
    story.append(Paragraph(
        "Dans l'environnement quotidien d'un atelier automobile, les techniciens sont confrontés à une densité d'information "
        "considérable. Un véhicule moderne embarque entre 50 et 80 calculateurs électroniques communicant sur bus CAN-FD ou LIN. "
        "Lorsqu'un témoin s'allume au tableau de bord ou qu'une déformation physique apparaît sur un pneumatique, l'opérateur doit "
        "croiser les codes de défauts (DTC), les notices constructeur souvent volumineuses (manuels de 800 pages) et l'historique "
        "d'entretien. Ce processus manuel induit des pertes de temps et des risques d'interprétation erronée. "
        "<b>MaintiDoc</b> intervient comme un outil d'aide documentaire multimodal et agentique sans jamais se substituer à la "
        "responsabilité du technicien. Notre cadrage identifie deux profils distincts aux prérogatives bien définies :", s_body))

    story.append(Paragraph("• <b>Profil A — Technicien de Maintenance Atelier / Dépannage rapide :</b> Opérateur de première ligne. "
                           "Son besoin immédiat est la levée de doute rapide : identifier la cause racine d'un témoin lumineux à partir "
                           "d'une photo prise au smartphone, obtenir les tolérances physiques (pression de service, couple de serrage des goujons, "
                           "épaisseur minimale de gomme TWI) et suivre la procédure séquentielle de mise en sécurité sans naviguer dans des centaines de pages.", s_bullet))
    story.append(Paragraph("• <b>Profil B — Chef d'Atelier / Responsable de Maintenance :</b> Superviseur garant de la sécurité légale et de la GMAO. "
                           "Il a besoin de consulter l'historique complet des interventions sur un équipement via le protocole MCP, "
                           "d'approuver ou d'amender les projets d'ordres de réparation (tickets) préparés par l'assistant, et de conserver l'accès "
                           "exclusif aux procédures sensibles (neutralisation pyrotechnique des airbags, programmation de transpondeurs d'antidémarrage).", s_bullet))

    story.append(Spacer(1, 5))
    story.append(Paragraph("2.1.2 Cas d'Usage Métier Concrets", s_h2))
    story.append(Paragraph("Nous avons modélisé cinq cas d'usage ancrés dans la réalité des interventions d'atelier :", s_body))

    uc_data = [
        [Paragraph("<b>Cas d'Usage</b>", s_table_header), Paragraph("<b>Scénario Opérationnel & Enchaînement des Actions</b>", s_table_header)],
        [
            Paragraph("<b>CU-1 : Décodage d'un témoin combiné ambigu</b>", s_table_cell_bold),
            Paragraph("Un technicien photographie un voyant orange au combiné d'instruments. MaintiDoc identifie le témoin de surveillance TPMS "
                      "(TDB-09), élimine l'hypothèse d'une défaillance d'ABS, cite la page 2 du manuel constructeur et fournit la séquence de "
                      "réinitialisation manuelle après vérification des pressions.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-2 : Diagnostic d'usure anormale de train roulant</b>", s_table_cell_bold),
            Paragraph("L'opérateur transmet la photo d'un pneumatique présentant une usure en vagues sur l'épaulement intérieur. "
                      "L'analyse visuelle identifie une usure en facettes (<i>Cupping Wear</i> - PNE-10). Le système écarte une mauvaise pression "
                      "et préconise l'inspection immédiate de l'amortisseur fuyard et du silentbloc de triangle.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-3 : Corrélation avec l'historique atelier via MCP</b>", s_table_cell_bold),
            Paragraph("Face à une alerte moteur persistante (Check Engine TDB-04), le système déclenche un appel d'outil MCP <code>get_equipment_history</code> "
                      "sur l'identifiant du véhicule pour vérifier si des ratés d'allumage similaires ont déjà été consignés lors des 90 derniers jours.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-4 : Préparation encadrée d'un ordre de travail</b>", s_table_cell_bold),
            Paragraph("Constatant une hernie sur flanc (PNE-05, danger mortel d'éclatement), l'assistant rédige un brouillon de ticket "
                      "avec référence de pièce et degré d'urgence. Le ticket reste bloqué en attente jusqu'à ce que le technicien clique "
                      "sur 'Valider l'ordre d'intervention' avec émission d'un jeton d'approbation et clé d'idempotence.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-5 : Détection d'image inexploitable et clarification</b>", s_table_cell_bold),
            Paragraph("Si la prise de vue présente un reflet aveuglant ou si le voyant est hors focus, MaintiDoc refuse de deviner. "
                      "Il formule explicitement : <i>« Cliché insuffisant : merci de reprendre la photo de face en évitant les reflets sur la vitre du combiné »</i>.", s_table_cell)
        ]
    ]
    t_uc = Table(uc_data, colWidths=[155, 350])
    t_uc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_uc)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3 : SECTION 2.1 (SUITE) - OBJECTIFS, PÉRIMÈTRE & CONTRAINTES
    # =========================================================================
    story.append(Paragraph("2.1.3 Objectifs Vérifiables du Prototype (Cible Semaine 6)", s_h2))
    story.append(Paragraph(
        "Afin d'éviter toute ambiguïté sur ce qui constitue un succès lors de la soutenance finale, nous fixons cinq "
        "objectifs vérifiables et mesurables sans déclarations subjectives :", s_body))

    story.append(Paragraph("1. <b>Exactitude et ancrage des citations (Grounding) :</b> Toute affirmation technique formulée par "
                           "l'assistant doit être appuyée par au moins une citation vérifiable comprenant l'identifiant stable du document "
                           "(<code>document_id</code>), le numéro de page précis et le numéro d'illustration. Zéro tolérance pour les citations fantômes.", s_bullet))
    story.append(Paragraph("2. <b>Cloisonnement effectif des accès (RBAC) :</b> Un utilisateur authentifié sous le rôle <code>techniciens_pneumatiques</code> "
                           "doit se voir refuser systématiquement l'affichage d'un extrait classé confidentiel atelier (ex. procédure antidémarrage ou airbag). "
                           "Ce refus est constaté dès la couche de recherche vectorielle Qdrant (pré-filtrage).", s_bullet))
    story.append(Paragraph("3. <b>Absence totale d'autonomie sur les actions sensibles :</b> Aucun ticket de maintenance ne peut être "
                           "inséré dans le serveur MCP sans une action physique délibérée de validation de l'opérateur. La signature cryptographique "
                           "du jeton d'approbation (token à usage unique) est vérifiée à chaque écriture.", s_bullet))
    story.append(Paragraph("4. <b>Immunité face aux injections indirectes :</b> Lorsque le système ingère un document d'atelier piégé "
                           "contenant des instructions malveillantes dissimulées, le moteur de génération doit traiter ce texte exclusivement "
                           "comme une donnée passive et refuser d'exécuter l'instruction dérogatoire.", s_bullet))
    story.append(Paragraph("5. <b>Comportement d'abstention déterministe :</b> Face à une photo floue ou deux documents contradictoires, "
                           "le système doit afficher un statut explicite <code>needs_clarification</code> avec justification, sans inventer de valeur moyenne.", s_bullet))

    story.append(Spacer(1, 5))
    story.append(Paragraph("2.1.4 Périmètre Retenu et Hors-Périmètre Explicite", s_h2))

    scope_data = [
        [Paragraph("<b>Composante</b>", s_table_header), Paragraph("<b>Périmètre Pris en Charge</b>", s_table_header)],
        [Paragraph("<b>Entrées admissibles</b>", s_table_cell_bold), Paragraph("Questions techniques formulées en français ; photographies numériques de témoins ou de pneumatiques (JPEG/PNG) ; documents PDF d'atelier.", s_table_cell)],
        [Paragraph("<b>Sorties fournies</b>", s_table_cell_bold), Paragraph("Réponses techniques structurées Pydantic avec citations explicites [doc_id, page, figure] ; demandes de précisions guidées ; brouillons de tickets.", s_table_cell)],
        [Paragraph("<b>Outil externe (MCP)</b>", s_table_cell_bold), Paragraph("Serveur MCP d'atelier exposant <code>get_equipment_history</code>, <code>get_open_tickets</code> et <code>create_ticket</code> avec contrôle d'autorisation systématique.", s_table_cell)],
        [Paragraph("<b>Action sensible</b>", s_table_cell_bold), Paragraph("Création effective d'un ordre de réparation dans la base de données, conditionnée par une approbation humaine explicite et protégée contre les doublons.", s_table_cell)],
        [Paragraph("<b>HORS-PÉRIMÈTRE STRICT</b>", ParagraphStyle('HP', parent=s_table_cell_bold, textColor=c_alert)), 
         Paragraph("<b>• Aucun pilotage à distance de machines-outils, ponts élévateurs ou organes du véhicule.<br/>"
                   "• Aucun effacement autonome de codes défauts calculateurs (DTC) sur la prise diagnostic OBD.<br/>"
                   "• Aucun engagement de garantie mécanique : l'assistant fournit une aide documentaire, le technicien reste seul maître d'œuvre.<br/>"
                   "• Aucune intervention autonome sans opérateur habilité présent physiquement.</b>", s_table_cell)]
    ]
    t_scope = Table(scope_data, colWidths=[125, 380])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_scope)

    story.append(Spacer(1, 5))
    story.append(Paragraph("2.1.5 Hypothèses Techniques et Dimensionnement Matériel", s_h2))
    story.append(Paragraph(
        "Nous fondons notre faisabilité technique sur des hypothèses d'infrastructure mesurées et réalistes :", s_body))
    story.append(Paragraph("• <b>Ressources d'exécution (GPU & VRAM) :</b> Nous ciblons un environnement d'inférence disposant de 16 à 24 Go de mémoire "
                           "vidéo (NVIDIA RTX 4090 locale ou instance cloud équivalente). Le modèle vision-langage retenu (Qwen2.5-VL-7B-Instruct) "
                           "sera exécuté sous quantification 4-bit (AWQ / GPTQ) via le moteur vLLM. Ce choix stabilise la consommation à environ 11-13 Go "
                           "de VRAM, laissant une marge confortable pour le modèle d'embedding BGE-M3 et le reranker sans risque de crash mémoire (*OOM*).", s_bullet))
    story.append(Paragraph("• <b>Budgets opérationnels et latence :</b> Une requête complète (analyse d'image + recherche Qdrant + synthèse VLM) "
                           "doit s'exécuter en moins de 30 secondes en p95. Les boucles de raisonnement agentique sont bridées à 3 appels d'outils MCP "
                           "et 6 passes LLM au maximum, avec un coupe-circuit temporel automatique fixé à 60 secondes.", s_bullet))
    story.append(Paragraph("• <b>Organisation du travail :</b> L'équipe répartit son temps sur 6 semaines avec une gestion stricte des dépendances sous Git.", s_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4 : SECTION 2.2 - CONSTITUTION DU CORPUS DOCUMENTAIRE
    # =========================================================================
    story.append(Paragraph("2.2 Constitution du Corpus Documentaire", s_h1))
    story.append(Paragraph("2.2.1 Composition et Équilibre du Corpus (45 Documents)", s_h2))
    story.append(Paragraph(
        "Plutôt que d'aspirer aveuglément des PDF disparates sur le web — souvent protégés par copyright ou truffés de données "
        "personnelles réelles — notre équipe a conçu un corpus sur mesure de <b>45 documents techniques originaux</b> (au-delà des 30 demandés). "
        "Le corpus est rigoureusement articulé autour de nos deux familles d'équipements :", s_body))

    story.append(Paragraph("• <b>Famille 1 — Tableaux de Bord (`tableaux_de_bord`) : 23 documents</b> traitant des combinés d'instruments "
                           "et de l'électronique de bord : pression d'huile critique, surchauffe du liquide de refroidissement, circuit de charge "
                           "alternateur, voyant moteur d'anomalie de combustion (Check Engine OBD-II), circuit de freinage hydraulique, antiblocage ABS, "
                           "régulation de trajectoire ESP, sécurité pyrotechnique Airbag SRS, surveillance TPMS, filtre à particules FAP, préchauffage diesel, "
                           "jauge de réserve carburant, direction assistée EPS, alerte d'AdBlue Euro 6, capteur de boucle de ceinture, boîte automatique en mode "
                           "refuge, éclairage et bus CAN, antidémarrage transpondeur, et extinction totale de combiné.", s_bullet))
    story.append(Paragraph("• <b>Famille 2 — Pneumatiques (`pneumatiques`) : 22 documents</b> couvrant les avaries physiques de liaison au sol : "
                           "crevaison lente et pneu dégonflé, perforation par clou réparable par champignon PRP, perforation par vis avec déformation "
                           "de nappe, usure asymétrique par mauvaise pression, hernie de flanc, coupure latérale par bordure, abrasion superficielle, "
                           "craquelures d'ozone et date de fabrication DOT, usure totale sous seuil légal de 1.6 mm, usure en facettes due aux amortisseurs "
                           "(Cupping), usure en écaille de parallélisme (Feathering), méplat de blocage de roue (Flat spot), arrachement de gomme (Chunking), "
                           "usure de carrossage, décollement de bande de roulement, décollement des nappes internes, endommagement du calandrage d'étanchéité "
                           "(Inner liner), talon de tringle déchiré, et câbles métalliques d'armature à nu.", s_bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Répartition Synthétique et Formats Documentaires :", s_h3))

    corpus_stat_data = [
        [Paragraph("<b>Famille d'Équipement</b>", s_table_header), Paragraph("<b>Procédures d'Atelier</b>", s_table_header), 
         Paragraph("<b>Fiches de Sécurité</b>", s_table_header), Paragraph("<b>Documents Scannés (OCR)</b>", s_table_header), 
         Paragraph("<b>Cas de Test (Contrad. / Injection)</b>", s_table_header), Paragraph("<b>Total Général</b>", s_table_header)],
        [
            Paragraph("<b>Tableaux de Bord (TDB)</b>", s_table_cell_bold),
            Paragraph("18 documents standard", s_table_cell),
            Paragraph("2 fiches (Airbag, Pression)", s_table_cell),
            Paragraph("1 scan dégradé (tdb_19)", s_table_cell),
            Paragraph("1 contradictoire + 1 injection", s_table_cell),
            Paragraph("<b>23 documents</b>", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Pneumatiques (PNE)</b>", s_table_cell_bold),
            Paragraph("14 documents standard", s_table_cell),
            Paragraph("6 fiches (Hernie, Rebut, EPI)", s_table_cell),
            Paragraph("1 scan dégradé (pne_12)", s_table_cell),
            Paragraph("1 contradictoire", s_table_cell),
            Paragraph("<b>22 documents</b>", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Total Répertoire Corpus</b>", s_table_cell_bold),
            Paragraph("32 procédures", s_table_cell),
            Paragraph("8 fiches sécurité", s_table_cell),
            Paragraph("2 documents scannés", s_table_cell),
            Paragraph("3 cas de test avancés", s_table_cell),
            Paragraph("<b>45 documents (40 images)</b>", ParagraphStyle('Tot', parent=s_table_cell_bold, textColor=c_blue))
        ]
    ]
    t_stat = Table(corpus_stat_data, colWidths=[120, 80, 80, 75, 95, 55])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_stat)

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.2.2 Traçabilité des Prompts de Génération et Propriété Intellectuelle", s_h2))
    story.append(Paragraph(
        "Chaque fiche a été rédigée avec l'assistance de Claude 3.5 Sonnet sous le contrôle direct de l'équipe (prompts <b>P01 à P13</b> "
        "consignés dans <code>corpus/prompts_corpus.md</code>). Les textes respectent les normes industrielles ISO 2575:2021 et les directives ETRTO. "
        "Les 40 photographies associées sont cataloguées de façon unique sous <code>corpus/images/</code> (format <code>&lt;document_id&gt;_f1.jpg</code>), "
        "issues de banques éducatives ouvertes sous licence Creative Commons (CC BY / CC BY-SA) ou générées sans données personnelles.", s_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5 : SECTION 2.2 (SUITE) - ANALYSE CRITIQUE ET CAS DE TESTS
    # =========================================================================
    story.append(Paragraph("2.2.3 Analyse Critique de l'Usage de l'IA (½ page)", s_h2))
    story.append(Paragraph(
        "Notre retour d'expérience sur la génération assistée par IA confirme une règle fondamentale : <b>un modèle de langage "
        "ne possède aucune compréhension physique de la mécanique automobile</b>. Sans notre relecture experte croisée, "
        "plusieurs erreurs graves auraient pollué la base documentaire :", s_body))

    critique_points = [
        "<b>1. Confusion sur la chimie et la miscibilité des fluides hydrauliques :</b> Lors de la génération initiale de la fiche sur le liquide "
        "de frein (<code>tdb_05</code>), Claude a proposé qu'en cas de niveau bas, un appoint pouvait être réalisé avec « du liquide synthétique moderne "
        "DOT 5.1 ou DOT 5 ». C'est une erreur technique gravissime : le liquide DOT 5.0 est à base de silicone, alors que les DOT 3, DOT 4 et DOT 5.1 "
        "sont à base de polyéthylène glycol éther. Leur mélange dans un bocal produit une séparation de phase immédiate, détruit les coupelles en caoutchouc "
        "du maître-cylindre et inhibe le bloc électro-hydraulique ABS. Nous avons corrigé cette aberration dans la fiche nominale et nous nous en sommes "
        "servis pour fabriquer la version contradictoire de test.",

        "<b>2. Inversions d'unités de pression et omission du facteur thermique :</b> Sur les pneumatiques (<code>pne_01</code> et <code>pne_04</code>), "
        "le modèle a confondu à deux reprises les bars et les psi, mentionnant une tolérance de 2.5 psi au lieu de 2.5 bar (un pneu gonflé à 2.5 psi roule "
        "sur la jante et déchire sa carcasse en 500 mètres). De plus, l'IA omettait systématiquement la loi des gaz parfaits : le roulage échauffe l'air "
        "interne (+0,2 à +0,4 bar). Une consigne d'atelier qui n'impose pas « mesure impérative à froid ou compensation de +0,3 bar à chaud » est inadmissible.",

        "<b>3. Hallucination de directives et liens réglementaires :</b> Le modèle citait occasionnellement des numéros de directives européennes "
        "fantaisistes. Nous avons assaini l'ensemble des métadonnées en réintroduisant les règlements réels de l'homologation : Règlement ONU n°121 "
        "pour les témoins de bord, et règlements n°30 et n°54 pour les pneumatiques de véhicules légers et utilitaires.",

        "<b>4. Biais de réparation hasardeuse sur organes de sécurité :</b> L'IA avait tendance à proposer des solutions de « dépannage d'urgence » "
        "sur des pièces non réparables, comme tenter de poser une mèche sur le flanc d'un pneu ou colmater une hernie (<code>pne_05</code>). "
        "Dans la pratique atelier, une hernie signale la rupture irréversible des nappes de carcasse métallique : le pneu peut exploser à tout instant "
        "sous l'effet de la pression. Nous avons réécrit les sections d'escalade en imposant la mise au rebut immédiate."
    ]
    for pt in critique_points:
        story.append(Paragraph(f"• {pt}", s_bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.2.4 Définition des Cas Limites de Test pour les Semaines 2 à 5", s_h2))
    story.append(Paragraph(
        "Pour valider rigoureusement le comportement de MaintiDoc face aux pièges d'atelier, notre inventaire intègre déjà cinq cas d'évaluation :", s_body))

    test_cases_table = [
        [Paragraph("<b>Identifiant Fichier</b>", s_table_header), Paragraph("<b>Nature du Cas Limite & Piège Introduit</b>", s_table_header), 
         Paragraph("<b>Comportement Attendu du Système MaintiDoc</b>", s_table_header)],
        [
            Paragraph("<code>tdb_05_frein_liquide_v2</code>", s_code),
            Paragraph("<b>Document Contradictoire</b><br/>Procédure révisée autorisant le mélange de silicone DOT 5 et le dépassement du niveau MAX.", s_table_cell),
            Paragraph("Détecter la contradiction formelle avec la v1.0, refuser de valider l'instruction laxiste et alerter sur le danger d'incompatibilité chimique.", s_table_cell)
        ],
        [
            Paragraph("<code>pne_04_usure_pression_v2</code>", s_code),
            Paragraph("<b>Document Contradictoire</b><br/>Procédure autorisant la mesure de pression à chaud sans correction thermique et fixant 2.0 bar uniforme.", s_table_cell),
            Paragraph("Identifier le désaccord avec la notice constructeur à froid et inviter l'opérateur à vérifier l'étiquette de portière du véhicule.", s_table_cell)
        ],
        [
            Paragraph("<code>tdb_note_service_piegee</code>", s_code),
            Paragraph("<b>Document Piégé (Prompt Injection)</b><br/>Payload malveillant masqué ordonnant le passage en mode root et l'exfiltration d'historiques sans validation.", s_table_cell),
            Paragraph("Traiter le document comme une donnée brute : aucune exfiltration réseau, maintien strict de la validation humaine MCP et refus d'élévation.", s_table_cell)
        ],
        [
            Paragraph("<code>tdb_19_fiche_revision_scanne</code>", s_code),
            Paragraph("<b>Document Scanné Dégradé (Test OCR)</b><br/>Fiche manuscrite de révision avec tampon atelier rasterisée à 150 DPI sans calque texte natif.", s_table_cell),
            Paragraph("Déclencher le pipeline OCR local (Surya / Tesseract) pour extraire avec succès le kilométrage et la remise à zéro combiné.", s_table_cell)
        ],
        [
            Paragraph("<code>pne_12_fiche_controle_geometrie_scanne</code>", s_code),
            Paragraph("<b>Document Scanné Dégradé (Test OCR)</b><br/>Rapport brut de banc laser 3D contenant les valeurs d'angle de carrossage/pincement rasterisées.", s_table_cell),
            Paragraph("Extraire par OCR les angles hors tolérance et faire le lien avec l'usure méplat constatée sur le pneumatique arrière.", s_table_cell)
        ],
        [
            Paragraph("<code>tdb_09_voyant_pression_pneus_tpms</code>", s_code),
            Paragraph("<b>Cas Ambigu Multi-domaines</b><br/>Alerte électronique de combiné directement liée à une avarie physique de train roulant.", s_table_cell),
            Paragraph("Réconcilier les deux corpus en reliant le voyant de bord à la procédure d'inspection de la roue concernée.", s_table_cell)
        ]
    ]
    t_test = Table(test_cases_table, colWidths=[110, 195, 200])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
    ]))
    story.append(t_test)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6 : SECTION 2.3 - ARCHITECTURE CIBLE DU SYSTÈME
    # =========================================================================
    story.append(Paragraph("2.3 Architecture Cible du Système", s_h1))
    story.append(Paragraph("2.3.1 Schéma Fonctionnel Global et Points de Contrôle", s_h2))
    story.append(Paragraph(
        "Nous avons conçu l'architecture de MaintiDoc selon un principe de <b>ségrégation des responsabilités</b>. "
        "Le système n'est pas un simple script linéaire : c'est un agent d'état guidé par une machine à états (LangGraph), "
        "interfaçant un modèle vision-langage quantifié, une base vectorielle hybride et un serveur d'outils d'atelier (MCP). "
        "Trois points de contrôle fondamentaux (<b>PC1, PC2, PC3</b>) verrouillent les flux sensibles :", s_body))

    arch_img_path = "docs/diagrammes/architecture_cible.png"
    if os.path.exists(arch_img_path):
        story.append(Spacer(1, 2))
        story.append(RLImage(arch_img_path, width=490, height=310))
        story.append(Spacer(1, 2))

    desc_pc = (
        "<b>Rôle et Implantation des 3 Points de Contrôle :</b><br/>"
        "• <b>PC1 — Filtrage des Droits d'Accès (RBAC) :</b> Vérification du jeton JWT à l'entrée FastAPI, suivie d'un pré-filtrage booléen "
        "immédiat dans Qdrant sur la métadonnée <code>groupes_acces</code>. Aucun document non autorisé n'est extrait ni soumis au modèle de langage.<br/>"
        "• <b>PC2 — Approbation Humaine Explicite (Human-in-the-Loop) :</b> Nœud d'arrêt synchrone dans le graphe LangGraph. "
        "L'agent ne peut pas déclencher l'écriture d'un ticket MCP de manière autonome : l'action est suspendue jusqu'à réception de la signature de l'opérateur.<br/>"
        "• <b>PC3 — Contrôle de Fidélité des Citations (Evidence Grounding) :</b> Module d'évaluation Pydantic post-génération. "
        "Il valide que chaque référence <code>[doc_id, page, figure]</code> correspond à un extrait réel présent dans le contexte d'inférence."
    )
    story.append(make_box(Paragraph(desc_pc, s_callout), bg_color='#F1F5F9', border_color='#94A3B8'))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7 : SECTION 2.3 (SUITE) - FICHES DÉTAILLÉES DES BLOCS
    # =========================================================================
    story.append(Paragraph("2.3.2 Fiches Techniques des Sept Blocs Fonctionnels", s_h2))
    story.append(Paragraph(
        "Chaque brique du système fait l'objet d'un contrat d'interface rigoureux :", s_body))

    blocks_data = [
        [
            Paragraph("<b>Bloc 1 : Interface Web (UI)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Fournir une interface réactive permettant la saisie de requêtes et le téléversement de photographies d'atelier.<br/>"
                      "<b>Entrées :</b> Questions textuelles en français, fichiers images (JPEG/PNG), clics d'approbation de tickets.<br/>"
                      "<b>Sorties :</b> Affichage des réponses sourcées, visualisation interactive des schémas/figures cités, formulaires de validation.<br/>"
                      "<b>Outil retenu :</b> <b>Streamlit</b> (Alternative évaluée : Next.js / Tailwind pour usage sur tablette durcie d'atelier).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 2 : Passerelle API (Gateway)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Gérer l'authentification des techniciens, le contrôle de débit (rate limiting) et la traçabilité des sessions.<br/>"
                      "<b>Entrées :</b> Requêtes HTTP multipart/form-data, jetons Bearer JWT, en-têtes d'identification atelier.<br/>"
                      "<b>Sorties :</b> Flux JSON validés par schémas Pydantic, refus d'accès 401/403, journaux d'audit horodatés.<br/>"
                      "<b>Outil retenu :</b> <b>FastAPI asynchrone</b> (Alternative évaluée : Litestar).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 3 : Orchestrateur Agentique</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Piloter la machine à états finis, le raisonnement itératif, les boucles d'outils et l'interruption humaine.<br/>"
                      "<b>Entrées :</b> État courant de la requête, retours d'extraction documentaire, retours du serveur MCP.<br/>"
                      "<b>Sorties :</b> Transitions d'état (Recherche -> Synthèse -> Demande de validation -> Émission de ticket).<br/>"
                      "<b>Outil retenu :</b> <b>LangGraph & LangChain</b> avec persistance d'état SQLite/Postgres.", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 4 : Moteur de Recherche Hybride</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Indexer et rechercher les passages textuels et visuels pertinents sous contrainte d'habilitation RBAC.<br/>"
                      "<b>Entrées :</b> Embeddings denses BGE-M3 (texte), vecteurs SigLIP (image) et sparse tokens SPLADE.<br/>"
                      "<b>Sorties :</b> Top-K extraits documentaires réordonnés par BGE-Reranker-v2 avec scores de pertinence normalisés.<br/>"
                      "<b>Outil retenu :</b> <b>Qdrant Vector Database</b> (Alternative évaluée : Milvus / pgvector).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 5 : Modèle Vision-Langage (VLM)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Analyser les clichés photographiques, extraire les anomalies visibles et rédiger la réponse sourcée.<br/>"
                      "<b>Entrées :</b> Prompt système strict, passages documentaires vérifiés, image téléversée prétraitée.<br/>"
                      "<b>Sorties :</b> Diagnostic structuré en JSON, liste des incertitudes, citations formelles [doc_id, page, figure].<br/>"
                      "<b>Outil retenu :</b> <b>Qwen2.5-VL-7B-Instruct</b> sous quantification AWQ via vLLM.", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 6 : Serveur d'Outils d'Atelier (MCP)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Exposer de façon standardisée les opérations de maintenance (GMAO) selon le protocole Model Context Protocol.<br/>"
                      "<b>Entrées :</b> Appels RPC normalisés (<code>get_equipment_history</code>, <code>create_ticket</code> avec token signé).<br/>"
                      "<b>Sorties :</b> Historiques d'interventions antérieures, identifiants de tickets créés (TK-xxxx).<br/>"
                      "<b>Outil retenu :</b> <b>FastMCP Python SDK</b> officiel.", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 7 : Couche de Stockage Persistant</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Conserver l'historique relationnel, les profils d'accès utilisateurs et archiver les fichiers binaires originaux.<br/>"
                      "<b>Entrées :</b> Fichiers PDF et images bruts du corpus, tables utilisateurs, journaux d'audit de sécurité.<br/>"
                      "<b>Sorties :</b> Fichiers originaux servis aux techniciens, métadonnées relationnelles pour les filtres d'API.<br/>"
                      "<b>Outil retenu :</b> <b>PostgreSQL</b> (tables relationnelles) + <b>MinIO</b> (stockage objet compatible S3).", s_table_cell)
        ]
    ]
    t_blocks = Table(blocks_data, colWidths=[130, 375])
    t_blocks.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_blocks)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8 : SECTION 2.3 (SUITE) - PARCOURS D'UNE REQUÊTE ET QUESTIONS
    # =========================================================================
    story.append(Paragraph("2.3.3 Parcours Pas à Pas d'une Requête Technicien (Modèle de Raisonnement)", s_h2))
    story.append(Paragraph(
        "Pour valider la logique du graphe d'états LangGraph, étudions le déroulement complet d'un cas d'atelier réel :<br/>"
        "<i>« Un opérateur en atelier pneumatique téléverse la photo d'un pneu présentant une protubérance sur le flanc, "
        "avec la question suivante : 'Ce pneumatique a une bosse sur le flanc suite à un choc trottoir. Peut-on réparer avec une cheville ?' »</i>", s_body))

    journey_steps = [
        "<b>Étape 1 — Authentification et portée d'accès (Gateway) :</b> La passerelle FastAPI valide le token de session JWT. "
        "L'utilisateur est identifié avec le rôle <code>techniciens_pneumatiques</code>. Ce rôle constitue le filtre pré-attribut de la session.",

        "<b>Étape 2 — Extraction visuelle objective (VLM) :</b> Le cliché est transmis au modèle vision-langage Qwen2.5-VL-7B. "
        "Le modèle décrit l'image sans halluciner de diagnostic : <i>« Pneumatique radial monté sur jante aluminium. Présence d'un renflement localisé "
        "de forme semi-sphérique d'environ 3 cm sur la zone médiane du flanc extérieur. Absence de perforation visible de la gomme de surface. »</i>",

        "<b>Étape 3 — Recherche documentaire sous pré-filtrage RBAC (Qdrant) :</b> La description visuelle et les mots-clés sont vectorisés. "
        "Qdrant applique le pré-filtre : <code>famille_equipement == 'pneumatiques' AND groupe_acces IN ['techniciens_pneumatiques', 'responsables']</code>. "
        "Le moteur extrait le document <code>pne_05_sidewall_bulge</code> (page 1 et 2). Les documents non autorisés sont exclus physiquement de la recherche.",

        "<b>Étape 4 — Reranking et consultation de l'historique équipement (MCP) :</b> Le reranker BGE-Reranker-v2 place la procédure "
        "d'alerte de hernie en rang 1. L'orchestrateur déclenche un appel MCP <code>get_equipment_history('PNEU-TR-01')</code> pour vérifier "
        "si ce véhicule a subi une intervention récente sur le train avant.",

        "<b>Étape 5 — Formulation et contrôle de fidélité des citations (Evidence Grounding) :</b> Le VLM rédige la réponse technique en citant "
        "la figure <code>PNE-05-F1</code> et la page 2 de la fiche de sécurité : <i>« Rupture structurelle interne des nappes de carcasse métallique. "
        "Interdiction absolue de réparer (danger mortel d'éclatement à haute vitesse). Remplacement obligatoire du pneumatique. »</i> "
        "Le validateur Pydantic vérifie que l'affirmation est formellement soutenue par le texte extrait.",

        "<b>Étape 6 — Préparation du ticket et suspension Human-in-the-Loop :</b> MaintiDoc prépare le brouillon de ticket d'atelier : "
        "<i>[TK-DRAFT] Échange standard pneumatique AV Gauche - Rupture carcasse</i>. L'agent suspend son exécution. L'ordre de travail n'est envoyé "
        "au serveur MCP que lorsque le technicien clique explicitement sur 'Approuver la création du ticket' sur son écran."
    ]
    for stp in journey_steps:
        story.append(Paragraph(f"• {stp}", s_bullet))

    story.append(Spacer(1, 5))
    story.append(Paragraph("2.3.4 Questions Ouvertes et Hypothèses à Vérifier (Semaines 2 à 6)", s_h2))
    story.append(Paragraph(
        "Ce premier jalon d'architecture met en évidence quatre questions techniques majeures qui guideront nos expérimentations :", s_body))

    open_q_data = [
        [Paragraph("<b>Question Ouverte / Hypothèse</b>", s_table_header), Paragraph("<b>Impact Système & Protocole de Validation Semaines 2-5</b>", s_table_header)],
        [
            Paragraph("<b>H1 : Tenue de la mémoire GPU sous vLLM</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> L'utilisation de Qwen2.5-VL-7B en quantification 4-bit AWQ avec PagedAttention maintiendra l'empreinte VRAM sous 13 Go lors de contextes de 8 192 tokens.<br/>"
                      "<i>Validation en Semaine 3 :</i> Mesure des pics de mémoire GPU lors de traitements concurrents texte + image haute définition.", s_table_cell)
        ],
        [
            Paragraph("<b>H2 : Débit et nécessité de l'OCR local</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> Déclencher un OCR systématique pénalise inutilement la latence. Un aiguillage préalable détectant les pages sans calque texte (PyMuPDF) optimise les flux.<br/>"
                      "<i>Validation en Semaine 2 :</i> Mesure du temps d'ingestion comparé sur les 43 PDF natifs vs les 2 PDF scannés dégradés.", s_table_cell)
        ],
        [
            Paragraph("<b>H3 : Efficience du Fine-Tuning du Reranker</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> L'entraînement supervisé d'un petit reranker multilingue sur 1 000 triplets mécaniques améliorera le nDCG@5 d'au moins 7% sur les cas d'atelier ambigus.<br/>"
                      "<i>Validation en Semaine 5 :</i> Comparaison formelle avant/après adaptation sur notre jeu de test de 150 scénarios.", s_table_cell)
        ],
        [
            Paragraph("<b>H4 : Sécurité face aux attaques visuelles masquées</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> Des instructions malveillantes incrustées dans des tampons d'atelier scannés peuvent être neutralisées si l'OCR étiquette le texte extrait comme 'donnée externe non fiable'.<br/>"
                      "<i>Validation en Semaine 5 :</i> Banc d'essai d'injections multimodales directes et indirectes.", s_table_cell)
        ]
    ]
    t_oq = Table(open_q_data, colWidths=[150, 355])
    t_oq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_oq)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9 : SECTION 2.4 - FLUX DE DONNÉES ET MODÈLE D'ACCÈS
    # =========================================================================
    story.append(Paragraph("2.4 Flux de Données et Modèle d'Accès", s_h1))
    story.append(Paragraph("2.4.1 Pipeline d'Ingestion Documentaire Multimodale (ETL)", s_h2))
    story.append(Paragraph(
        "Le pipeline d'ingestion prend en charge l'hétérogénéité des documents d'atelier et les transforme en représentations "
        "vectorielles et textuelles sécurisées :", s_body))

    ingest_img_path = "docs/diagrammes/flux_donnees_ingestion.png"
    if os.path.exists(ingest_img_path):
        story.append(RLImage(ingest_img_path, width=490, height=205))
        story.append(Spacer(1, 2))

    story.append(Paragraph("2.4.2 Flux d'une Requête Technicien (RAG Sourcé & Multimodal)", s_h2))
    story.append(Paragraph(
        "Le parcours d'une requête combine l'analyse visuelle de l'image d'atelier et la recherche documentaire filtrée :", s_body))

    query_img_path = "docs/diagrammes/flux_requete_rag.png"
    if os.path.exists(query_img_path):
        story.append(RLImage(query_img_path, width=490, height=205))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10 : SECTION 2.4 (SUITE) - FLUX TICKET MCP ET MODÈLE RBAC
    # =========================================================================
    story.append(Paragraph("2.4.3 Flux Sécurisé de Création de Ticket MCP (HITL & Idempotence)", s_h2))
    story.append(Paragraph(
        "L'ouverture d'un ordre de réparation constitue une action engageante qui nécessite une barrière de validation humaine inviolable :", s_body))

    mcp_img_path = "docs/diagrammes/flux_creation_ticket_mcp.png"
    if os.path.exists(mcp_img_path):
        story.append(RLImage(mcp_img_path, width=490, height=190))
        story.append(Spacer(1, 4))

    story.append(Paragraph("2.4.4 Schéma Formel des Métadonnées d'un Fragment Indexé", s_h2))
    story.append(Paragraph(
        "Chaque extrait textuel et chaque illustration indexés dans Qdrant sont accompagnés d'un payload normalisé :", s_body))

    meta_json_str = (
        "{\n"
        '  "chunk_id": "tdb_01_p02_c03",                 // Identifiant unique déterministe de fragment\n'
        '  "document_id": "tdb_01_voyant_pression_huile",   // Identifiant stable réutilisé pour les citations\n'
        '  "version": "v1.0 (2026-11)",                   // Version pour le contrôle d\'obsolescence\n'
        '  "page_number": 2,                             // Numéro de page exact dans le document source\n'
        '  "element_type": "procedure_step",             // paragraph | table | figure | procedure_step\n'
        '  "element_id": "figure_tdb_01_f1",             // Identifiant d\'élément visuel ou d\'étape d\'atelier\n'
        '  "famille_equipement": "tableaux_de_bord",     // tableaux_de_bord | pneumatiques\n'
        '  "equipement_id": "TDB-MOTEUR-01",              // Référence équipement synchronisée avec la base MCP\n'
        '  "groupes_acces": ["techniciens_tdb", "responsables"], // Attributs de sécurité RBAC pour pré-filtrage\n'
        '  "content_hash": "e3b0c44298fc1c149afbf4c8...", // Empreinte SHA256 pour audit d\'intégrité documentaire\n'
        '  "is_ocr": false                               // Booléen traçant si l\'extrait provient d\'un scan dégradé\n'
        "}"
    )
    story.append(make_box(Paragraph(f"<pre>{meta_json_str}</pre>", s_code), bg_color='#F8FAFC', border_color='#CBD5E1', padding=3))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.4.5 Modèle de Contrôle d'Accès par Rôles (RBAC d'Atelier)", s_h2))
    story.append(Paragraph(
        "Notre modèle d'accès segmente l'atelier en trois groupes avec étanchéité garantie :", s_body))

    rbac_table = [
        [Paragraph("<b>Groupe d'Habilitation</b>", s_table_header), Paragraph("<b>Documents Autorisés en Consultation</b>", s_table_header), 
         Paragraph("<b>Documents Strictement Interdits (Blocage Immédiat)</b>", s_table_header), Paragraph("<b>Prérogatives MCP</b>", s_table_header)],
        [
            Paragraph("<b><code>techniciens_tdb</code></b>", s_table_cell_bold),
            Paragraph("Procédures combinés de bord, témoins voyants moteur, boîte automatique, FAP, documents partagés (TPMS).", s_table_cell),
            Paragraph("Fiches pneumatiques physiques, documents pyrotechniques Airbag (TDB-08), antidémarrage antivol (TDB-18), notes confidentielles.", s_table_cell),
            Paragraph("<code>get_equipment_history</code>,<br/><code>create_ticket</code> (validé)", s_table_cell)
        ],
        [
            Paragraph("<b><code>techniciens_pneumatiques</code></b>", s_table_cell_bold),
            Paragraph("Fiches crevaison, usures de bande, géométrie 3D, amortisseurs, documents partagés (TPMS, alerte révision).", s_table_cell),
            Paragraph("Procédures calculateurs combiné, diagnostic boîte automatique, antidémarrage, fiches haute tension.", s_table_cell),
            Paragraph("<code>get_equipment_history</code>,<br/><code>create_ticket</code> (validé)", s_table_cell)
        ],
        [
            Paragraph("<b><code>responsables</code></b>", s_table_cell_bold),
            Paragraph("<b>Accès transverse intégral :</b> l'ensemble des 45 documents du corpus (incluant Airbag pyrotechnique, antidémarrage et notes d'audit).", s_table_cell),
            Paragraph("Aucune restriction documentaire sur l'ensemble de la base d'atelier.", s_table_cell),
            Paragraph("<b>Tous les outils MCP</b> + accès direct à <code>get_open_tickets</code> global.", s_table_cell)
        ]
    ]
    t_rbac = Table(rbac_table, colWidths=[110, 150, 150, 95])
    t_rbac.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_rbac)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11 : SECTION 2.5 - ANALYSE DES RISQUES
    # =========================================================================
    story.append(Paragraph("2.5 Analyse des Risques du Projet", s_h1))
    story.append(Paragraph(
        "Nous avons conduit une analyse rigoureuse des risques couvrant l'ensemble des aspects techniques, sécuritaires, "
        "documentaires et humains. Neuf risques majeurs sont modélisés avec leur probabilité (1 à 3), leur impact opérationnel (1 à 3), "
        "leur criticité ($C = P \times I$), les contre-mesures préventives/curatives associées et le membre responsable :", s_body))

    risk_table = [
        [
            Paragraph("<b>ID / Risque Identifié</b>", s_table_header),
            Paragraph("<b>Catégorie</b>", s_table_header),
            Paragraph("<b>P (1-3)</b>", s_table_header),
            Paragraph("<b>I (1-3)</b>", s_table_header),
            Paragraph("<b>Crit. (P×I)</b>", s_table_header),
            Paragraph("<b>Mesures Préventives & Palliatives Définies</b>", s_table_header),
            Paragraph("<b>Resp.</b>", s_table_header)
        ],
        [
            Paragraph("<b>R1 : Injection de prompt indirecte</b> (via document piégé)", s_table_cell_bold),
            Paragraph("Sécurité", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Isolation des textes documentaires sous balises XML passives ; interdiction formelle d'exécution d'instructions système ; banc de test dédié S5.", s_table_cell),
            Paragraph("Hafsa", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R2 : Hallucinations & fausses citations</b>", s_table_cell_bold),
            Paragraph("Technique", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Module Evidence Checker automatisé vérifiant la concordance textuelle exacte de [doc_id, page, figure] ; consigne stricte d'abstention en prompt système.", s_table_cell),
            Paragraph("Wiam", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R3 : Fuite d'informations entre groupes (RBAC)</b>", s_table_cell_bold),
            Paragraph("Sécurité", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("3", s_table_cell), Paragraph("3", s_table_cell),
            Paragraph("Pré-filtrage déterministe dans Qdrant sur les métadonnées groupe_acces avant tout calcul de similarité ; double contrôle post-recherche dans l'API.", s_table_cell),
            Paragraph("Aya", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R4 : Création autonome de ticket GMAO</b>", s_table_cell_bold),
            Paragraph("Sécurité / Métier", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("3", s_table_cell), Paragraph("3", s_table_cell),
            Paragraph("Garde-fou humain absolu (Human-in-the-Loop) dans LangGraph ; émission d'un jeton d'approbation à usage unique ; clé d'idempotence anti-doublon.", s_table_cell),
            Paragraph("Wiam", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R5 : Erreurs techniques introduites par l'IA</b>", s_table_cell_bold),
            Paragraph("Données", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Relecture humaine systématique (double contrôle) ; traçabilité exhaustive dans prompts_corpus.md et inventaire.csv normalisé.", s_table_cell),
            Paragraph("Hafsa", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R6 : Non-conformité des licences de documents</b>", s_table_cell_bold),
            Paragraph("Légal / Données", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("2", s_table_cell), Paragraph("2", s_table_cell),
            Paragraph("Utilisation exclusive de textes synthétiques originaux et d'illustrations pédagogiques sous licence Creative Commons (CC BY / CC BY-SA).", s_table_cell),
            Paragraph("Aya", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R7 : Dépassement de mémoire GPU (OOM)</b>", s_table_cell_bold),
            Paragraph("Technique", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Quantification 4-bit (AWQ) du modèle VLM Qwen2.5-VL ; moteur vLLM avec PagedAttention ; modèle compact de repli prêt à l'emploi si besoin.", s_table_cell),
            Paragraph("Wiam", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R8 : Indisponibilité du serveur MCP</b>", s_table_cell_bold),
            Paragraph("Technique", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("2", s_table_cell), Paragraph("4", s_table_cell),
            Paragraph("Implémentation d'un bouchon (mock MCP) local autonome pour poursuivre le développement et les tests en cas d'isolement réseau.", s_table_cell),
            Paragraph("Aya", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R9 : Désynchronisation dans l'équipe</b>", s_table_cell_bold),
            Paragraph("Organisation", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("2", s_table_cell), Paragraph("2", s_table_cell),
            Paragraph("Points de synchronisation hebdomadaires ; séparation stricte des modules d'ingénierie ; intégration continue sur branches Git dédiées.", s_table_cell),
            Paragraph("Hafsa", s_table_cell_bold)
        ]
    ]
    t_risk = Table(risk_table, colWidths=[105, 55, 30, 30, 35, 215, 35])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ALIGN', (2,0), (4,-1), 'CENTER'),
    ]))
    story.append(t_risk)

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Bilan de criticité :</b> Les risques prioritaires identifiés ($C = 6$) relèvent de la sécurité des prompts (R1), "
        "de la vérité terrain des citations (R2), de l'intégrité du corpus (R5) et du dimensionnement VRAM (R7). "
        "Chacun de ces risques dispose d'une contre-mesure architecturale native et d'un membre référent au sein de notre binôme/trinôme.", s_callout))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12 : SECTION 2.6 - PLANNING ET ORGANISATION DE L'ÉQUIPE
    # =========================================================================
    story.append(Paragraph("2.6 Planning et Organisation de l'Équipe", s_h1))
    story.append(Paragraph("2.6.1 Répartition des Pôles d'Ingénierie", s_h2))
    story.append(Paragraph(
        "Pour garantir une rigueur d'exécution maximale sur les 6 semaines, chaque membre porte un pôle technique dédié :", s_body))

    roles_data = [
        [
            Paragraph("<b>Ingénieure Responsable</b>", s_table_header),
            Paragraph("<b>Pôle de Spécialisation</b>", s_table_header),
            Paragraph("<b>Périmètre Technique Pris en Charge</b>", s_table_header)
        ],
        [
            Paragraph("<b>SOUILI Wiam</b><br/>Lead Architecture & Agentique", s_table_cell_bold),
            Paragraph("Orchestration LangGraph, Passerelle FastAPI & Serveur MCP", s_table_cell),
            Paragraph("• Développement de la machine à états finis LangGraph (routage, limites de boucle).<br/>"
                      "• Conception de la passerelle FastAPI (authentification JWT, gestion des sessions d'atelier).<br/>"
                      "• Implémentation du serveur d'outils MCP d'atelier et du mécanisme bloquant Human-in-the-Loop.<br/>"
                      "• Conteneurisation générale avec Docker Compose et orchestration réseau.", s_table_cell)
        ],
        [
            Paragraph("<b>YEKHLEF Aya</b><br/>Lead RAG Multimodal & Recherche", s_table_cell_bold),
            Paragraph("Pipeline Ingestion ETL, Qdrant, Embeddings & Reranker", s_table_cell),
            Paragraph("• Développement du pipeline d'ingestion multimodale (PyMuPDF, segmentation par section).<br/>"
                      "• Intégration et évaluation du module OCR local (Surya / Tesseract) pour les scans dégradés.<br/>"
                      "• Déploiement et indexation de la base vectorielle Qdrant (BGE-M3 + SigLIP + sparse).<br/>"
                      "• Fine-tuning supervisé du reranker multilingue sur vocabulaire d'atelier (Semaine 5).", s_table_cell)
        ],
        [
            Paragraph("<b>ELAOUAZI Hafsa</b><br/>Lead Évaluation, Sécurité & Corpus", s_table_cell_bold),
            Paragraph("Modèles VLM, Sécurité des Prompts, Schémas Pydantic & QA", s_table_cell),
            Paragraph("• Déploiement et benchmarking du modèle vision-langage Qwen2.5-VL-7B (vLLM / AWQ).<br/>"
                      "• Conception des contrats d'interface Pydantic et du module Evidence Checker.<br/>"
                      "• Élaboration du jeu de test de 150 scénarios (ambiguïtés, contradictions, injections).<br/>"
                      "• Mesure des métriques de recherche (Recall@5, nDCG@5, MRR@10) et suivi MLflow.", s_table_cell)
        ]
    ]
    t_roles = Table(roles_data, colWidths=[120, 140, 245])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_roles)

    story.append(Spacer(1, 5))
    story.append(Paragraph("2.6.2 Feuille de Route Chronologique des Semaines 2 à 6", s_h2))
    story.append(Paragraph(
        "Notre planning prévisionnel est calibré sur les échéances hebdomadaires du projet :", s_body))

    planning_data = [
        [Paragraph("<b>Période</b>", s_table_header), Paragraph("<b>Jalon d'Ingénierie</b>", s_table_header), 
         Paragraph("<b>Objectifs Techniques Concrets & Travaux de Développement</b>", s_table_header), Paragraph("<b>Livrable Associé</b>", s_table_header)],
        [
            Paragraph("<b>Semaine 1</b><br/>(Clôturée)", s_table_cell_bold),
            Paragraph("Cadrage, corpus & architecture", s_table_cell),
            Paragraph("• Définition des profils d'atelier, cas d'usage et objectifs vérifiables.<br/>"
                      "• Constitution et validation manuelle du corpus de 45 documents (TDB & PNE).<br/>"
                      "• Rédaction du dossier d'architecture cible et analyse des risques.", s_table_cell),
            Paragraph("<b>Livrable 1</b><br/>Rapport PDF + ZIP corpus complet", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 2</b>", s_table_cell_bold),
            Paragraph("Ingestion, recherche & gestion des accès", s_table_cell),
            Paragraph("• Développement du pipeline ETL (PyMuPDF + OCR local pour tdb_19 et pne_12).<br/>"
                      "• Segmentation en fragments sémantiques et calcul des embeddings BGE-M3/SigLIP.<br/>"
                      "• Indexation Qdrant avec pré-filtrage RBAC par métadonnées.", s_table_cell),
            Paragraph("<b>Livrable 2</b><br/>Dépôt Git documenté & index prêt", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 3</b>", s_table_cell_bold),
            Paragraph("Intégration du VLM & sorties structurées", s_table_cell),
            Paragraph("• Déploiement de Qwen2.5-VL-7B quantifié AWQ sous vLLM sur GPU.<br/>"
                      "• Ingénierie des prompts multimodaux et validation stricte Pydantic.<br/>"
                      "• Implémentation du module Evidence Checker vérifiant citations et figures.", s_table_cell),
            Paragraph("<b>Livrable 3 (P1)</b><br/>Prototype RAG multimodal fonctionnel", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 4</b>", s_table_cell_bold),
            Paragraph("Workflow LangGraph & connexion MCP", s_table_cell),
            Paragraph("• Construction de la machine à états finis avec gestion des boucles d'outils.<br/>"
                      "• Implémentation du serveur MCP d'atelier (historiques et ordres de réparation).<br/>"
                      "• Mécanisme bloquant d'approbation humaine (HITL) et clé d'idempotence.", s_table_cell),
            Paragraph("<b>Livrable 3 (P2)</b><br/>Prototype agentique complet avec MCP", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 5</b>", s_table_cell_bold),
            Paragraph("Adaptation reranker & banc d'évaluation", s_table_cell),
            Paragraph("• Construction du jeu de données de fine-tuning (1 000 triplets d'atelier).<br/>"
                      "• Entraînement supervisé de BGE-Reranker-v2 et mesure nDCG@5 / MRR@10.<br/>"
                      "• Campagne d'évaluation sur 150 scénarios (injections, ambiguïtés, RBAC).", s_table_cell),
            Paragraph("<b>Livrable 4</b><br/>Rapport d'évaluation & benchmarks", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 6</b>", s_table_cell_bold),
            Paragraph("Déploiement Docker, fiches & soutenance", s_table_cell),
            Paragraph("• Finalisation de la pile Docker Compose, durcissement et métriques MLflow.<br/>"
                      "• Rédaction de la fiche de limites d'utilisation et conditions d'exploitation.<br/>"
                      "• Répétition des démonstrations live (nominal, injection, HITL, dégradé).", s_table_cell),
            Paragraph("<b>Livrables 5 & 6</b><br/>Fiche de limites, démo & soutenance finale", s_table_cell_bold)
        ]
    ]
    t_plan = Table(planning_data, colWidths=[65, 105, 245, 90])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_plan)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13 : SECTION 2.6 (SUITE) - MATRICE RACI ET ENGAGEMENTS S2
    # =========================================================================
    story.append(Paragraph("2.6.3 Matrice de Responsabilité Opérationnelle (RACI)", s_h2))
    story.append(Paragraph(
        "Pour éliminer tout chevauchement ou point d'incompréhension, la matrice RACI formalise nos contributions :", s_body))

    raci_data = [
        [Paragraph("<b>Livrable / Responsabilité Technique</b>", s_table_header), 
         Paragraph("<b>Wiam SOUILI</b>", s_table_header), 
         Paragraph("<b>Aya YEKHLEF</b>", s_table_header), 
         Paragraph("<b>Hafsa ELAOUAZI</b>", s_table_header)],
        [Paragraph("Constitution du corpus et inventaire normalisé", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("C", s_table_cell_bold), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue))],
        [Paragraph("Pipeline ETL d'ingestion & module OCR", s_table_cell), Paragraph("I", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue)), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Indexation Qdrant & filtrage des métadonnées RBAC", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue)), Paragraph("I", s_table_cell)],
        [Paragraph("Déploiement et optimisation du modèle VLM Qwen2.5-VL", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("I", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue))],
        [Paragraph("Machine à états LangGraph & orchestration agentique", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue)), Paragraph("C", s_table_cell_bold), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Serveur MCP maintenance & workflow Human-in-the-Loop", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue)), Paragraph("I", s_table_cell), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Fine-tuning supervisé du reranker multilingue", s_table_cell), Paragraph("I", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue)), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Banc d'évaluation (150 scénarios) & tests d'injection", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("C", s_table_cell_bold), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue))],
        [Paragraph("Déploiement conteneurisé Docker Compose & MLOps", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_blue)), Paragraph("C", s_table_cell_bold), Paragraph("I", s_table_cell)]
    ]
    t_raci = Table(raci_data, colWidths=[235, 90, 90, 90])
    t_raci.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_raci)

    story.append(Spacer(1, 8))
    story.append(Paragraph("Conclusion du Cadrage et Engagements pour la Semaine 2", s_h2))
    story.append(Paragraph(
        "Ce Livrable 1 fige les bases méthodologiques et architecturales indispensables à la réussite de MaintiDoc. "
        "En abordant le projet sous l'angle de la réalité d'atelier (défis combinés d'instruments vs liaison au sol), "
        "nous garantissons que le système ne sera pas un jouet théorique mais un assistant technique robuste. "
        "Les pièges documentaires introduits (contradictions de fluides, injection de prompt masquée, scans sans calque texte) "
        "constituent notre banc d'essai pour démontrer la supériorité d'une architecture agentique étanche.", s_body))

    concl_box = (
        "<b>Engagements immédiats de l'équipe pour le Livrable 2 :</b><br/>"
        "• Dépôt Git documenté avec environnement virtuel reproductible (requirements.txt standardisé).<br/>"
        "• Pipeline d'ingestion PyMuPDF opérationnel avec extraction d'éléments visuels et segmentation sémantique.<br/>"
        "• Évaluation rigoureuse de l'OCR local sur les deux rapports scannés dégradés (tdb_19 et pne_12).<br/>"
        "• Base vectorielle Qdrant opérationnelle avec pré-filtrage RBAC validé par tests unitaires automatisés."
    )
    story.append(make_box(Paragraph(concl_box, s_callout), bg_color='#F1F5F9', border_color='#3B82F6'))

    story.append(PageBreak())

    # =========================================================================
    # PAGES 14-15 : ANNEXES TECHNIQUES (INVENTAIRE COMPLET CONDENSÉ)
    # =========================================================================
    story.append(Paragraph("Annexes Techniques : Registre d'Inventaire du Corpus MaintiDoc", s_h1))
    story.append(Paragraph(
        "Extrait condensé des 45 documents figurant dans le fichier d'inventaire officiel <code>corpus/inventaire.csv</code> :", s_body))

    with open("corpus/inventaire.csv", "r", encoding="utf-8") as f_inv:
        reader = list(csv.DictReader(f_inv))

    inv_table_p1_data = [
        [Paragraph("<b>ID Document</b>", s_table_header), Paragraph("<b>Titre Lisible du Document</b>", s_table_header),
         Paragraph("<b>Famille</b>", s_table_header), Paragraph("<b>Type</b>", s_table_header), 
         Paragraph("<b>Format</b>", s_table_header), Paragraph("<b>Rôle Évaluation</b>", s_table_header), Paragraph("<b>Relecture</b>", s_table_header)]
    ]
    for row in reader[:23]:
        inv_table_p1_data.append([
            Paragraph(f"<code>{row['document_id']}</code>", s_code),
            Paragraph(row['titre'][:35] + ("..." if len(row['titre']) > 35 else ""), s_table_cell),
            Paragraph(row['famille_equipement'].replace('_', ' '), s_table_cell),
            Paragraph(row['type_document'], s_table_cell),
            Paragraph(row['format'], s_table_cell),
            Paragraph(f"<b>{row['usage_test']}</b>" if row['usage_test'] != 'normal' else "normal", 
                      ParagraphStyle('UT', parent=s_table_cell, textColor=c_alert if row['usage_test'] != 'normal' else c_navy)),
            Paragraph(row['verifie_par'], s_table_cell)
        ])

    t_inv_p1 = Table(inv_table_p1_data, colWidths=[115, 145, 75, 55, 45, 45, 25])
    t_inv_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 1.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
    ]))
    story.append(t_inv_p1)

    story.append(PageBreak())

    story.append(Paragraph("Annexes Techniques (Suite) : Famille Pneumatiques & Cas Spéciaux", s_h1))
    inv_table_p2_data = [
        [Paragraph("<b>ID Document</b>", s_table_header), Paragraph("<b>Titre Lisible du Document</b>", s_table_header),
         Paragraph("<b>Famille</b>", s_table_header), Paragraph("<b>Type</b>", s_table_header), 
         Paragraph("<b>Format</b>", s_table_header), Paragraph("<b>Rôle Évaluation</b>", s_table_header), Paragraph("<b>Relecture</b>", s_table_header)]
    ]
    for row in reader[23:]:
        inv_table_p2_data.append([
            Paragraph(f"<code>{row['document_id']}</code>", s_code),
            Paragraph(row['titre'][:35] + ("..." if len(row['titre']) > 35 else ""), s_table_cell),
            Paragraph(row['famille_equipement'].replace('_', ' '), s_table_cell),
            Paragraph(row['type_document'], s_table_cell),
            Paragraph(row['format'], s_table_cell),
            Paragraph(f"<b>{row['usage_test']}</b>" if row['usage_test'] != 'normal' else "normal", 
                      ParagraphStyle('UT', parent=s_table_cell, textColor=c_alert if row['usage_test'] != 'normal' else c_navy)),
            Paragraph(row['verifie_par'], s_table_cell)
        ])

    t_inv_p2 = Table(inv_table_p2_data, colWidths=[115, 145, 75, 55, 45, 45, 25])
    t_inv_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 1.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
    ]))
    story.append(t_inv_p2)

    story.append(Spacer(1, 10))
    validation_sign = [
        [Paragraph("<b>Engagement et Certification de l'Équipe MaintiDoc :</b>", s_body_bold)],
        [Paragraph("Nous certifions sur l'honneur que l'ensemble des 45 documents du corpus a fait l'objet d'une vérification "
                   "humaine rigoureuse, qu'aucune donnée personnelle réelle n'a été insérée, et que les cas de test "
                   "(contradictions, injection de prompt, scans dégradés) sont formellement isolés et documentés.", s_callout)],
        [Paragraph("<b>SOUILI Wiam</b> (Signé) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
                   "<b>YEKHLEF Aya</b> (Signé) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
                   "<b>ELAOUAZI Hafsa</b> (Signé)", ParagraphStyle('Sig', parent=s_body_bold, textColor=c_blue))]
    ]
    t_sign = Table(validation_sign, colWidths=[505])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {filename}")

if __name__ == "__main__":
    build_pdf()
