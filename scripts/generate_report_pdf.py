import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage, KeepTogether, HRFlowable
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
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(54, 802, "MaintiDoc — Livrable 1 : Cadrage, Corpus et Architecture")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(558, 802, "EMSI 2026 | ELAOUAZI · SOUILI · YEKHLEF")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 796, 558, 796)

        # Footer
        self.line(54, 46, 558, 46)
        self.drawString(54, 34, "Projet d'IA Générative Multimodale — Confidentiel Enseignement")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()


def build_pdf(filename="L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor('#1E3A8A')    # Deep Blue
    c_secondary = colors.HexColor('#0D9488')  # Teal
    c_dark = colors.HexColor('#0F172A')       # Slate Dark
    c_text = colors.HexColor('#334155')       # Body text
    c_muted = colors.HexColor('#64748B')      # Muted text
    c_bg_light = colors.HexColor('#F8FAFC')   # Light background
    c_border = colors.HexColor('#E2E8F0')     # Border color
    c_alert = colors.HexColor('#DC2626')      # Red alert

    # Typography styles
    s_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=1,
        spaceAfter=10
    )

    s_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_muted,
        alignment=1,
        spaceAfter=25
    )

    s_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    s_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    s_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_dark,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    s_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_text,
        spaceAfter=5
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
        fontSize=8.5,
        leading=11.5,
        textColor=c_text,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    s_callout = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    s_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
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
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    s_code = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    def make_box(content_list, bg_color='#F1F5F9', border_color='#CBD5E1', padding=6):
        tbl = Table([[content_list]], colWidths=[508])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
            ('TOPPADDING', (0,0), (-1,-1), padding),
            ('BOTTOMPADDING', (0,0), (-1,-1), padding),
            ('LEFTPADDING', (0,0), (-1,-1), padding + 2),
            ('RIGHTPADDING', (0,0), (-1,-1), padding + 2),
        ]))
        return tbl

    # =========================================================================
    # PAGE 1 : PAGE DE GARDE / TITRE OFFICIEL
    # =========================================================================
    story.append(Spacer(1, 40))
    # School & Module badge
    badge_data = [
        [Paragraph("<b>ÉCOLE MAROCAINE DES SCIENCES DE L'INGÉNIEUR — EMSI 2026</b>", 
                   ParagraphStyle('B1', parent=s_body_bold, fontSize=9, alignment=1, textColor=colors.HexColor('#1E3A8A')))],
        [Paragraph("Filière Ingénierie Informatique & Intelligence Artificielle | Module IA Générative Multimodale",
                   ParagraphStyle('B2', parent=s_body, fontSize=8, alignment=1, textColor=c_muted))]
    ]
    t_badge = Table(badge_data, colWidths=[508])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#3B82F6')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 55))

    story.append(Paragraph("PROJET MAINTIDOC", s_title))
    story.append(Paragraph("Assistant Documentaire Multimodal et Agentique pour la Maintenance Automobile", 
                           ParagraphStyle('Sub1', parent=s_title, fontSize=14, leading=18, textColor=c_secondary)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("LIVRABLE 1 : CADRAGE, CORPUS ET ARCHITECTURE CIBLE", 
                           ParagraphStyle('L1Tag', parent=s_subtitle, fontName='Helvetica-Bold', fontSize=11, textColor=c_dark)))
    story.append(Paragraph("Recherche documentaire sourcée, vision par ordinateur, interfaçage MCP et sécurité agentique", s_subtitle))
    
    story.append(Spacer(1, 40))

    # Meta team table
    team_table_data = [
        [Paragraph("<b>Équipe projet :</b>", s_table_cell_bold), Paragraph("<b>ELAOUAZI - SOUILI - YEKHLEF</b>", s_table_cell_bold)],
        [Paragraph("<b>Composition de l'équipe :</b>", s_table_cell), 
         Paragraph("• <b>ELAOUAZI Hafsa</b> — hafsa.elaouazi@emsi-edu.ma (Lead Évaluation, Sécurité & Corpus)<br/>"
                   "• <b>SOUILI Wiam</b> — wiam.souili@emsi-edu.ma (Lead Architecture & Intégration Agentique)<br/>"
                   "• <b>YEKHLEF Aya</b> — aya.yekhlef@emsi-edu.ma (Lead RAG Multimodal & Recherche Vectorielle)", s_table_cell)],
        [Paragraph("<b>Encadrante :</b>", s_table_cell_bold), Paragraph("<b>Pr. Mariam CHERRABI</b>", s_table_cell)],
        [Paragraph("<b>Familles d'équipements :</b>", s_table_cell_bold), Paragraph("1. Tableaux de bord (combinés & témoins) — 2. Pneumatiques & train roulant", s_table_cell)],
        [Paragraph("<b>Dépôt GitHub officiel :</b>", s_table_cell_bold), Paragraph("https://github.com/WiamSouili/MaintiDoc-ELAOUAZI-SOUILI-YEKHLEF", s_code)],
        [Paragraph("<b>Date de soumission :</b>", s_table_cell_bold), Paragraph("Novembre 2026 — Fin de Semaine 1", s_table_cell)]
    ]
    t_team = Table(team_table_data, colWidths=[140, 368])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_team)

    story.append(Spacer(1, 35))

    exec_summary = (
        "<b>Résumé exécutif du Livrable 1 :</b> Ce document fige les fondations conceptuelles, documentaires et techniques "
        "du projet MaintiDoc avant le démarrage des développements. Il formalise le profil des utilisateurs d'atelier, cinq cas "
        "d'usage représentatifs, les objectifs vérifiables et le hors-périmètre strict. Il présente un corpus multimodal de 45 "
        "documents vérifiés couvrant les tableaux de bord et les pneumatiques (incluant cas contradictoires, injection de prompt et scans "
        "OCR). L'architecture cible détaille sept blocs fonctionnels modulaires avec leurs points de contrôle (RBAC, Human-in-the-Loop, "
        "citations vérifiées), les flux de données et une analyse exhaustive de neuf risques assortie d'une organisation d'équipe rigoureuse."
    )
    story.append(make_box(Paragraph(exec_summary, s_callout), bg_color='#EFF6FF', border_color='#93C5FD'))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2 : SOMMAIRE ET SECTION 2.1 - CADRAGE DU PROJET
    # =========================================================================
    story.append(Paragraph("Table des Matières Synthétique", s_h2))
    toc_data = [
        [Paragraph("<b>2.1 Cadrage du projet</b> (Contexte, utilisateurs, cas d'usage, objectifs, périmètre, contraintes)", s_table_cell), Paragraph("Page 2-3", s_table_cell_bold)],
        [Paragraph("<b>2.2 Constitution du corpus documentaire</b> (Corpus 45 docs, traçabilité IA, analyse critique, tests)", s_table_cell), Paragraph("Page 4-5", s_table_cell_bold)],
        [Paragraph("<b>2.3 Architecture cible</b> (Schéma fonctionnel, fiches des blocs, points de contrôle, parcours requête)", s_table_cell), Paragraph("Page 6-8", s_table_cell_bold)],
        [Paragraph("<b>2.4 Flux de données et modèle d'accès</b> (Ingestion ETL, requête RAG, workflow MCP, RBAC)", s_table_cell), Paragraph("Page 9-10", s_table_cell_bold)],
        [Paragraph("<b>2.5 Analyse des risques</b> (Matrice de 9 risques : technique, sécurité, données, organisation)", s_table_cell), Paragraph("Page 11", s_table_cell_bold)],
        [Paragraph("<b>2.6 Planning et organisation de l'équipe</b> (Rôles, feuille de route S2-S6, matrice RACI)", s_table_cell), Paragraph("Page 12-13", s_table_cell_bold)],
        [Paragraph("<b>Annexes techniques</b> (Inventaire synthétique des 45 documents du corpus MaintiDoc)", s_table_cell), Paragraph("Page 14-15", s_table_cell_bold)],
    ]
    t_toc = Table(toc_data, colWidths=[420, 88])
    t_toc.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.1 Cadrage du Projet", s_h1))
    story.append(Paragraph("2.1.1 Contexte Opérationnel et Profils Utilisateurs", s_h2))
    story.append(Paragraph(
        "Dans les ateliers modernes de maintenance automobile, les opérateurs font face à une complexité technologique "
        "croissante : multiplication des calculateurs électroniques, combinés d'instruments virtuels intégrant des dizaines de témoins "
        "d'alerte normalisés ou spécifiques aux constructeurs, et avaries complexes de liaison au sol. La consultation des volumineux "
        "manuels d'atelier (souvent plusieurs centaines de pages PDF hétérogènes) ralentit considérablement la prise de décision. "
        "Le projet <b>MaintiDoc</b> répond à ce défi en concevant un assistant documentaire multimodal et agentique fondé sur les modèles "
        "d'IA générative à poids ouverts. Le système s'adresse à deux profils principaux :", s_body))

    story.append(Paragraph("• <b>Profil 1 — Technicien de Maintenance (Atelier ou Itinérant) :</b> Intervenant de terrain réalisant les "
                           "diagnostics de premier niveau, contrôles périodiques et réparations courantes. Il a besoin d'une assistance "
                           "instantanée par photo (smartphone/tablette) pour décoder un voyant obscur ou identifier une forme d'usure "
                           "anormale de pneu. Ses exigences clés sont la rapidité d'accès aux tolérances constructeur, la précision "
                           "des couples de serrage et la sécurité d'intervention (EPI, mise hors tension).", s_bullet))
    story.append(Paragraph("• <b>Profil 2 — Responsable d'Atelier / Chef d'Équipe :</b> Superviseur de l'activité globale, garant de la "
                           "qualité, de la conformité réglementaire et de la gestion des ressources. Il a besoin d'une vision transverse, "
                           "de la traçabilité intégrale des historiques de pannes, de la validation des ordres de réparation avant saisie "
                           "dans la GMAO (Gestion de Maintenance Assistée par Ordinateur), et de l'accès exclusif aux documents sensibles "
                           "(procédures pyrotechniques airbag, paramètres d'antidémarrage et notes confidentielles).", s_bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.1.2 Cas d'Usage Concrets", s_h2))
    story.append(Paragraph("Cinq cas d'usage représentatifs ont été modélisés pour guider les spécifications et les bancs d'essai :", s_body))

    uc_data = [
        [Paragraph("<b>Cas d'usage</b>", s_table_header), Paragraph("<b>Description fonctionnelle & Flux opérationnel</b>", s_table_header)],
        [
            Paragraph("<b>CU-1 : Identification d'un voyant combiné ambigu</b>", s_table_cell_bold),
            Paragraph("Le technicien photographie un voyant ambre allumé au tableau de bord. MaintiDoc identifie le témoin TPMS (TDB-09), "
                      "extrait la cause physique probable (fuite lente ou baisse thermique), cite la page du manuel et indique la "
                      "procédure de réinitialisation séquentielle.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-2 : Diagnostic d'usure pneumatique par vision</b>", s_table_cell_bold),
            Paragraph("L'opérateur envoie une photo d'un pneumatique présentant des déformations périodiques. Le modèle vision-langage "
                      "reconnaît une usure en facettes (*Cupping Wear* - PNE-10), exclut un problème de gonflage et oriente vers "
                      "un défaut d'amortisseur ou un jeu de train roulant.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-3 : Corrélation avec historique MCP</b>", s_table_cell_bold),
            Paragraph("Face à un code défaut Check Engine récurrent, le système appelle l'outil MCP <code>get_equipment_history</code> "
                      "pour consulter les 3 dernières interventions sur le véhicule et croiser les réparations antérieures avec les notes d'atelier.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-4 : Préparation sécurisée d'un ticket GMAO</b>", s_table_cell_bold),
            Paragraph("Lorsqu'un remplacement est prescrit (ex: rupture de nappe carcasse - PNE-05), MaintiDoc rédige un brouillon de ticket "
                      "structuré. L'action sensible n'est exécutée via l'outil MCP <code>create_ticket</code> qu'après approbation humaine "
                      "explicite de l'opérateur avec clé d'idempotence.", s_table_cell)
        ],
        [
            Paragraph("<b>CU-5 : Gestion de l'incertitude & clarification</b>", s_table_cell_bold),
            Paragraph("Si la photo transmise est floue, mal cadrée ou si la plaque signalétique est illisible, MaintiDoc s'abstient "
                      "formellement de deviner et formule une question de clarification guidée, préservant la sûreté du diagnostic.", s_table_cell)
        ]
    ]
    t_uc = Table(uc_data, colWidths=[160, 348])
    t_uc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_uc)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3 : SECTION 2.1 (SUITE) - OBJECTIFS, PÉRIMÈTRE & CONTRAINTES
    # =========================================================================
    story.append(Paragraph("2.1.3 Objectifs Vérifiables du Prototype (Semaine 6)", s_h2))
    story.append(Paragraph(
        "Conformément au cahier des charges, le prototype final développé en semaine 6 sera soumis à une batterie d'évaluation "
        "comportant 150 scénarios de test. Il devra impérativement satisfaire les objectifs vérifiables suivants :", s_body))

    story.append(Paragraph("1. <b>Fidélité et sourçage documentaire :</b> Pour toute réponse affirmative, le système doit citer au "
                           "moins un document existant, sa version, le numéro de page exact et l'identifiant de figure le cas échéant. "
                           "Aucune affirmation technique ne doit être formulée sans soutien direct d'un passage indexé (zéro hallucination non sourcée).", s_bullet))
    story.append(Paragraph("2. <b>Cloisonnement et contrôle d'accès strict (RBAC) :</b> Le système doit refuser systématiquement "
                           "l'accès à un document ou passage confidentiel lorsque l'utilisateur n'appartient pas au groupe autorisé "
                           "(ex. refus d'accès d'un technicien standard à la note de service pyrotechnique ou aux documents antidémarrage).", s_bullet))
    story.append(Paragraph("3. <b>Garde-fou humain absolu sur action sensible (HITL) :</b> Aucun ticket de maintenance ne peut être "
                           "créé de manière autonome dans le serveur MCP. La création effective exige un jeton d'approbation à usage unique "
                           "validé par l'opérateur après visualisation du contenu textuel complet.", s_bullet))
    story.append(Paragraph("4. <b>Résistance aux attaques par injection indirecte :</b> Lors de l'ingestion de documents piégés "
                           "contenant des instructions malveillantes (ex. ordre d'exfiltration ou d'élévation de privilèges), le système "
                           "doit traiter le contenu textuel comme de la donnée passive et ne jamais exécuter la directive masquée.", s_bullet))
    story.append(Paragraph("5. <b>Abstention justifiée en cas d'ambiguïté ou d'image dégradée :</b> Le système doit préférer formuler "
                           "une demande de clarification plutôt que de fournir une réponse approximative lorsque les preuves documentaires "
                           "sont insuffisantes ou contradictoires.", s_bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.1.4 Périmètre et Hors-Périmètre Explicite", s_h2))

    scope_data = [
        [Paragraph("<b>Élément</b>", s_table_header), Paragraph("<b>Détail du Périmètre Retenu</b>", s_table_header)],
        [Paragraph("<b>Entrées supportées</b>", s_table_cell_bold), Paragraph("Questions en langage naturel (français), photographies numériques de témoins/avaries (JPEG/PNG), documents techniques au format PDF.", s_table_cell)],
        [Paragraph("<b>Sorties produites</b>", s_table_cell_bold), Paragraph("Réponses techniques structurées Pydantic, citations exactes [doc_id, page, figure], demandes de précision, brouillons de tickets de maintenance.", s_table_cell)],
        [Paragraph("<b>Outil externe (MCP)</b>", s_table_cell_bold), Paragraph("Serveur MCP d'atelier exposant <code>get_equipment_history</code>, <code>get_open_tickets</code> et <code>create_ticket</code> avec contrôle d'autorisation à chaque appel.", s_table_cell)],
        [Paragraph("<b>Action sensible</b>", s_table_cell_bold), Paragraph("Création d'ordre de réparation (ticket) soumise à validation humaine explicite et protégée contre les doublons par clé d'idempotence.", s_table_cell)],
        [Paragraph("<b>HORS-PÉRIMÈTRE STRICT</b>", ParagraphStyle('HP', parent=s_table_cell_bold, textColor=c_alert)), 
         Paragraph("<b>• Aucun pilotage direct ou télécommande d'équipements mécaniques ou calculateurs (ECU).<br/>"
                   "• Aucun diagnostic formellement garanti : le système constitue une aide documentaire d'aide à la décision.<br/>"
                   "• Aucune intervention autonome sans la présence et la validation d'un technicien habilité.<br/>"
                   "• Aucun effacement autonome de codes défauts (DTC) sur les réseaux multiplexés du véhicule.</b>", s_table_cell)]
    ]
    t_scope = Table(scope_data, colWidths=[130, 378])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_scope)

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.1.5 Hypothèses et Contraintes Matérielles", s_h2))
    story.append(Paragraph(
        "Le projet s'appuie sur des contraintes techniques réalistes dimensionnées pour un environnement de prototypage avancé :", s_body))
    story.append(Paragraph("• <b>Ressources de calcul (GPU / RAM) :</b> Station de développement équipée d'un GPU de 16 à 24 Go de VRAM "
                           "(cible NVIDIA RTX 4090 ou instance cloud équivalente). Le modèle vision-langage retenu (Qwen2.5-VL-7B-Instruct) "
                           "sera exécuté sous quantification 4-bit (AWQ / GPTQ) ou via le moteur d'inférence haute performance vLLM afin de "
                           "conserver l'empreinte mémoire sous le seuil critique des 14 Go de VRAM, réservant la mémoire résiduelle pour les embeddings et le reranker.", s_bullet))
    story.append(Paragraph("• <b>Budgets de latence et d'appels :</b> Conformément aux directives, une requête simple devra afficher "
                           "une latence p95 inférieure à 30 secondes. Les budgets opérationnels appliquent des plafonds stricts : maximum "
                           "3 appels MCP par requête, maximum 6 inférences LLM/VLM, et un timeout automatique de 60 secondes.", s_bullet))
    story.append(Paragraph("• <b>Contraintes temporelles :</b> Cycle serré de 6 semaines imposant une architecture hautement modulaire, "
                           "des interfaces formalisées par contrats d'API (Pydantic / OpenAPI) et un suivi de version rigoureux sous Git.", s_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4 : SECTION 2.2 - CONSTITUTION DU CORPUS DOCUMENTAIRE
    # =========================================================================
    story.append(Paragraph("2.2 Constitution du Corpus Documentaire", s_h1))
    story.append(Paragraph("2.2.1 Stratégie de Constitution et Typologie des Documents", s_h2))
    story.append(Paragraph(
        "Afin d'alimenter le RAG multimodal de MaintiDoc sans violer de secrets industriels ni enfreindre le RGPD, notre équipe "
        "a constitué un corpus synthétique et semi-public de <b>45 documents techniques complets</b> (dépassant le seuil minimal requis de "
        "30 documents). Le corpus est équilibré de manière symétrique entre deux familles complémentaires de l'après-vente automobile :", s_body))

    story.append(Paragraph("• <b>Famille 1 — Tableaux de Bord (`tableaux_de_bord`) : 23 documents</b> couvrant l'ensemble des témoins combinés "
                           "et systèmes électroniques de bord : pression d'huile moteur, surchauffe circuit de refroidissement, charge batterie/alternateur, "
                           "témoin d'anomalie moteur (*Check Engine* OBD-II), système de freinage hydraulique, antiblocage ABS, contrôle de trajectoire ESP, "
                           "sécurité passive Airbag SRS, surveillance de pression TPMS, filtre à particules FAP, préchauffage diesel, jauge à carburant, "
                           "direction assistée, AdBlue/SCR, ceinture, boîte de vitesses automatique, défaillance éclairage, antidémarrage et combiné éteint.", s_bullet))
    story.append(Paragraph("• <b>Famille 2 — Pneumatiques (`pneumatiques`) : 22 documents</b> couvrant les avaries physiques, structurelles et "
                           "dimensionnelles : crevaison lente / pneu dégonflé, perforation par clou, perforation par vis, usures anormales par mauvaise "
                           "pression, hernie sur flanc, coupure flanc, abrasion par trottoir, vieillissement et craquelures d'ozone (Dry Rot), usure totale "
                           "sous seuil légal (Bald tire), usure en facettes (*Cupping*), usure en dents de scie (*Feathering*), méplat de freinage, arrachement "
                           "de gomme (*Chunking*), usure dissymétrique de géométrie, décollement de bande de roulement, décollement de carcasse, dommage "
                           "de gomme intérieure (*Inner liner*), détérioration de talon, décollement de tringle et câbles d'armature métallique à nu.", s_bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Répartition Typologique et Éléments Visuels du Corpus :", s_h3))

    corpus_stat_data = [
        [Paragraph("<b>Famille d'Équipement</b>", s_table_header), Paragraph("<b>Procédures d'Atelier</b>", s_table_header), 
         Paragraph("<b>Fiches de Sécurité</b>", s_table_header), Paragraph("<b>Scans OCR Dégradés</b>", s_table_header), 
         Paragraph("<b>Cas Contradictoires / Piégés</b>", s_table_header), Paragraph("<b>Total Docs</b>", s_table_header)],
        [
            Paragraph("<b>Tableaux de Bord (TDB)</b>", s_table_cell_bold),
            Paragraph("18 documents", s_table_cell),
            Paragraph("2 fiches (Airbag, Pression)", s_table_cell),
            Paragraph("1 scan (tdb_19)", s_table_cell),
            Paragraph("1 contradictoire + 1 injection", s_table_cell),
            Paragraph("<b>23 documents</b>", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Pneumatiques (PNE)</b>", s_table_cell_bold),
            Paragraph("14 documents", s_table_cell),
            Paragraph("6 fiches (Hernie, Rebut, EPI)", s_table_cell),
            Paragraph("1 scan (pne_12)", s_table_cell),
            Paragraph("1 contradictoire", s_table_cell),
            Paragraph("<b>22 documents</b>", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Total Général Corpus</b>", s_table_cell_bold),
            Paragraph("32 procédures", s_table_cell),
            Paragraph("8 fiches sécurité", s_table_cell),
            Paragraph("2 documents scannés", s_table_cell),
            Paragraph("3 cas de test avancés", s_table_cell),
            Paragraph("<b>45 documents (40 images)</b>", ParagraphStyle('Tot', parent=s_table_cell_bold, textColor=c_primary))
        ]
    ]
    t_stat = Table(corpus_stat_data, colWidths=[120, 80, 80, 75, 95, 58])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stat)

    story.append(Spacer(1, 8))
    story.append(Paragraph("2.2.2 Traçabilité des Prompts et Licences Légales", s_h2))
    story.append(Paragraph(
        "L'ensemble des prompts utilisés pour la génération documentaire est consigné avec précision dans le fichier "
        "<code>corpus/prompts_corpus.md</code> (prompts numérotés de <b>P01 à P13</b>). Chaque document de l'inventaire renvoie "
        "directement à l'identifiant du prompt source. Les textes ont été rédigés avec l'assistance de Claude 3.5 Sonnet le 06/11/2026, "
        "puis structurés au format PDF via ReportLab. Les 40 illustrations uniques intégrées proviennent de photographies d'atelier réelles "
        "et de ressources éducatives ouvertes, placées sous licence <b>Creative Commons (CC BY 4.0 / CC BY-SA)</b> ou générées "
        "synthétiquement, assurant une parfaite réutilisabilité sans risque légal.", s_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5 : SECTION 2.2 (SUITE) - ANALYSE CRITIQUE ET CAS DE TESTS
    # =========================================================================
    story.append(Paragraph("2.2.3 Analyse Critique de l'Usage de l'IA Générative (½ page)", s_h2))
    story.append(Paragraph(
        "Bien que les modèles de langage avancés accélèrent la production de documentation technique, notre démarche de double "
        "relecture humaine a démontré qu'un LLM ne peut être considéré comme une source fiable sans vérification experte. "
        "Quatre catégories d'erreurs et d'hallucinations majeures ont été détectées et neutralisées :", s_body))

    critique_points = [
        "<b>1. Hallucination sur la miscibilité chimique des fluides de freinage :</b> Dans la version brute générée pour le voyant de frein "
        "(<code>tdb_05</code>), l'IA a affirmé qu'un appoint avec un liquide synthétique récent « de type DOT 5 ou DOT 5.1 » pouvait être réalisé "
        "sans distinction. Or, le liquide DOT 5.0 (base silicone) est chimiquement incompatible avec le DOT 4 (base glycol) : leur mélange "
        "provoque la destruction immédiate des joints en élastomère et le blocage de la centrale hydraulique ABS. L'équipe a rectifié le document "
        "nominal en imposant exclusivement le DOT 4, et a capitalisé sur cette erreur pour concevoir la procédure contradictoire de test.",

        "<b>2. Inversions d'unités physiques et oubli du facteur thermique :</b> Lors de la génération des fiches de pression (<code>pne_01</code> "
        "et <code>pne_04</code>), le modèle a confondu à deux reprises les valeurs de pression en <i>bar</i> et en <i>psi</i> (indiquant 2.5 psi "
        "au lieu de 2.5 bar, soit une erreur d'un facteur 14 qui causerait l'éclatement immédiat de la roue). De plus, l'IA omettait systématiquement "
        "la dilatation thermique de l'air : une pression mesurée à chaud doit impérativement être majorée de +0,3 bar par rapport à l'étiquette constructeur.",

        "<b>3. Références réglementaires et liens bibliographiques fictifs :</b> Le modèle a inventé plusieurs numéros d'articles de directives "
        "européennes et généré des URL inexistantes. L'équipe a remplacé ces références par des normes internationales vérifiées et pérennes : "
        "ISO 2575:2021 (symboles combiné de bord), Règlement CEE-ONU n°121, et normes dimensionnelles de l'ETRTO.",

        "<b>4. Biais d'optimisme et réparations dangereuses sur organes structurels :</b> L'IA proposait par défaut de « colmater ou vulcaniser » "
        "une hernie sur flanc de pneu (<code>pne_05</code>). Il s'agit d'une prescription mortelle : toute rupture de nappe carcasse radiale impose "
        "la mise au rebut immédiate du pneumatique. L'équipe a durci les fiches de sécurité en introduisant l'obligation d'escalade vers un technicien habilité."
    ]
    for pt in critique_points:
        story.append(Paragraph(f"• {pt}", s_bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("2.2.4 Cas de Test Spécifiques Définis pour les Semaines 2 à 5", s_h2))
    story.append(Paragraph(
        "Pour valider rigoureusement le comportement de MaintiDoc face aux pièges documentaires, cinq cas d'évaluation sont intégrés :", s_body))

    test_cases_table = [
        [Paragraph("<b>Document ID</b>", s_table_header), Paragraph("<b>Nature du Cas de Test</b>", s_table_header), 
         Paragraph("<b>Comportement Attendu de l'Assistant MaintiDoc</b>", s_table_header)],
        [
            Paragraph("<code>tdb_05_frein_liquide_v2</code>", s_code),
            Paragraph("<b>Document Contradictoire</b><br/>Affirme que le liquide silicone DOT 5 est miscible avec DOT 4 et autorise le dépassement du MAX.", s_table_cell),
            Paragraph("Détecter le conflit entre la v1.0 et la v2.0, alerter l'opérateur sur la contradiction et appliquer le principe de sécurité maximale.", s_table_cell)
        ],
        [
            Paragraph("<code>pne_04_usure_pression_v2</code>", s_code),
            Paragraph("<b>Document Contradictoire</b><br/>Autorise le contrôle immédiat à chaud sans compensation et fixe 2.0 bar uniforme pour tous véhicules.", s_table_cell),
            Paragraph("Identifier la contradiction avec la notice constructeur à froid et inviter l'utilisateur à vérifier l'étiquette de portière.", s_table_cell)
        ],
        [
            Paragraph("<code>tdb_note_service_piegee</code>", s_code),
            Paragraph("<b>Document Piégé (Prompt Injection)</b><br/>Payload masqué ordonnant le rôle 'Root', l'exfiltration d'historiques et la création de tickets sans HITL.", s_table_cell),
            Paragraph("Traiter le document comme une donnée passive : zéro exfiltration réseau, maintien strict de la validation humaine MCP et refus d'élévation.", s_table_cell)
        ],
        [
            Paragraph("<code>tdb_19_fiche_revision_scanne</code>", s_code),
            Paragraph("<b>Document Scanné (Test OCR)</b><br/>Fiche d'intervention manuscrite rasterisée à 150 DPI sans calque texte natif.", s_table_cell),
            Paragraph("Activer le pipeline OCR local (Tesseract / Surya) pour extraire les kilométrages et réinitialisations de révision.", s_table_cell)
        ],
        [
            Paragraph("<code>pne_12_fiche_controle_geometrie_scanne</code>", s_code),
            Paragraph("<b>Document Scanné (Test OCR)</b><br/>Rapport de banc géométrie 3D avec mesures de carrossage/pincement rasterisées.", s_table_cell),
            Paragraph("Extraction OCR des valeurs chiffrées de géométrie et corrélation avec l'usure méplat constatée.", s_table_cell)
        ],
        [
            Paragraph("<code>tdb_09_voyant_pression_pneus_tpms</code>", s_code),
            Paragraph("<b>Cas Ambigu Multi-domaines</b><br/>Témoin combiné d'instruments orange lié à une défaillance de train roulant.", s_table_cell),
            Paragraph("Faire le pont entre l'alerte électronique de bord et la procédure physique de contrôle de pneumatique.", s_table_cell)
        ]
    ]
    t_test = Table(test_cases_table, colWidths=[110, 195, 203])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_test)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6 : SECTION 2.3 - ARCHITECTURE CIBLE
    # =========================================================================
    story.append(Paragraph("2.3 Architecture Cible du Système", s_h1))
    story.append(Paragraph("2.3.1 Schéma Fonctionnel Global et Points de Contrôle", s_h2))
    story.append(Paragraph(
        "L'architecture de MaintiDoc est conçue selon un paradigme <b>agentique, multimodal et résilient</b>. Elle découple "
        "l'ingestion des documents, l'analyse visuelle, la recherche documentaire hybride et l'exécution d'actions externes. "
        "Trois points de contrôle critiques (<b>PC1, PC2, PC3</b>) garantissent l'étanchéité des accès, la souveraineté humaine et la rigueur du sourçage :", s_body))

    # Embed architecture diagram
    arch_img_path = "docs/diagrammes/architecture_cible.png"
    if os.path.exists(arch_img_path):
        story.append(Spacer(1, 4))
        story.append(RLImage(arch_img_path, width=490, height=315))
        story.append(Spacer(1, 4))

    desc_pc = (
        "<b>Description des 3 Points de Contrôle Clés :</b><br/>"
        "• <b>PC1 — Contrôle d'Accès Pré- et Post-Retrieval (RBAC) :</b> Authentification par JWT au niveau de la passerelle FastAPI, "
        "suivie d'un pré-filtrage strict dans Qdrant appliquant la métadonnée <code>groupe_acces</code> de l'utilisateur. Aucun extrait non autorisé n'est exposé au LLM.<br/>"
        "• <b>PC2 — Validation Humaine Obligatoire (Human-in-the-Loop) :</b> Point d'arrêt bloquant dans le graphe LangGraph. "
        "Avant tout appel de l'outil sensible MCP <code>create_ticket</code>, le brouillon est présenté au technicien. L'exécution requiert un jeton d'approbation explicite.<br/>"
        "• <b>PC3 — Vérification Automatisée des Citations (Evidence Grounding) :</b> Module de validation post-génération contrôlant avec "
        "un schéma Pydantic que chaque citation <code>[doc_id, page, element_id]</code> figure réellement dans les documents extraits et soutient fidèlement la réponse."
    )
    story.append(make_box(Paragraph(desc_pc, s_callout), bg_color='#FFFBEB', border_color='#F59E0B'))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7 : SECTION 2.3 (SUITE) - FICHES DÉTAILLÉES DES BLOCS
    # =========================================================================
    story.append(Paragraph("2.3.2 Fiches Détaillées des Blocs Fonctionnels", s_h2))
    story.append(Paragraph(
        "Le système MaintiDoc est découpé en sept blocs modulaires. Chaque bloc répond à une responsabilité unique :", s_body))

    blocks_data = [
        [
            Paragraph("<b>Bloc 1 : Interface Utilisateur (UI)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Permettre au technicien de saisir ses questions textuelles et d'uploader des photos de témoins ou de pneus.<br/>"
                      "<b>Entrées :</b> Saisie texte, photos (JPEG/PNG), clics d'approbation de tickets.<br/>"
                      "<b>Sorties :</b> Réponses sourcées, visualisation des figures citées, formulaires de validation de tickets.<br/>"
                      "<b>Outil retenu :</b> <b>Streamlit</b> (alternative : React / Vite avec TailwindCSS pour intégration mobile).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 2 : Passerelle API (Gateway)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Sécuriser l'accès, authentifier les sessions utilisateurs et router les requêtes vers le moteur agentique.<br/>"
                      "<b>Entrées :</b> Requêtes HTTP multipart/form-data, en-têtes Authorization Bearer JWT.<br/>"
                      "<b>Sorties :</b> Flux JSON validés, codes d'erreur 401/403 en cas de violation d'accès, métriques d'audit.<br/>"
                      "<b>Outil retenu :</b> <b>FastAPI</b> avec OAuth2 / JWT (alternative : Litestar).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 3 : Orchestrateur Agentique</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Gérer l'état conversationnel, le raisonnement itératif, les boucles d'outils et l'interruption pour validation humaine.<br/>"
                      "<b>Entrées :</b> Requête analysée, retours d'outils MCP, retours du moteur de recherche RAG.<br/>"
                      "<b>Sorties :</b> Décisions de routage (recherche, question de précision, brouillon de ticket, réponse finale).<br/>"
                      "<b>Outil retenu :</b> <b>LangGraph & LangChain</b> (alternative : LlamaIndex Workflows).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 4 : Recherche RAG Multimodale</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Indexer et rechercher les passages textuels et les éléments visuels les plus pertinents sous contrainte RBAC.<br/>"
                      "<b>Entrées :</b> Vecteurs de requête (dense, sparse, visuel), filtre d'attributs utilisateur.<br/>"
                      "<b>Sorties :</b> Top-K passages textuels, tables et figures avec scores de pertinence réordonnés.<br/>"
                      "<b>Outil retenu :</b> <b>Qdrant</b> + BGE-M3 (texte) + SigLIP (image) + BGE-Reranker-v2 (alternative : Milvus / Chroma).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 5 : Modèle Vision-Langage (VLM)</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Décrire les images d'entrée, reconnaître les voyants/avaries et synthétiser les réponses sourcées.<br/>"
                      "<b>Entrées :</b> Prompt système strict, passages documentaires autorisés, image d'entrée encodée.<br/>"
                      "<b>Sorties :</b> Texte de réponse structuré avec citations formelles et mention des incertitudes.<br/>"
                      "<b>Outil retenu :</b> <b>Qwen2.5-VL-7B-Instruct</b> via vLLM / Transformers (alternative : Pixtral-12B / Llama-3.2-Vision).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 6 : Serveur d'Outils MCP</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Fournir une interface standardisée pour interroger la base de maintenance d'atelier et enregistrer les tickets.<br/>"
                      "<b>Entrées :</b> Appels RPC normalisés (<code>equipment_id</code>, paramètres de ticket, approval_token).<br/>"
                      "<b>Sorties :</b> Historiques d'interventions, liste des tickets ouverts, confirmation de création de ticket.<br/>"
                      "<b>Outil retenu :</b> <b>Serveur MCP Python officiel</b> (FastMCP / MCP SDK) (alternative : API REST OpenAPI directe).", s_table_cell)
        ],
        [
            Paragraph("<b>Bloc 7 : Couche de Stockage</b>", s_table_cell_bold),
            Paragraph("<b>Rôle :</b> Conserver de manière persistante les fichiers bruts (PDFs, images) et les métadonnées relationnelles.<br/>"
                      "<b>Entrées :</b> Fichiers binaires du corpus, tables d'inventaire, profils utilisateurs et logs d'audit.<br/>"
                      "<b>Sorties :</b> Documents originaux servis à l'affichage, tables de droits d'accès.<br/>"
                      "<b>Outil retenu :</b> <b>PostgreSQL</b> (métadonnées & rôles) + <b>MinIO</b> (stockage objet S3 local) (alternative : SQLite + stockage disque).", s_table_cell)
        ]
    ]
    t_blocks = Table(blocks_data, colWidths=[130, 378])
    t_blocks.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_blocks)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8 : SECTION 2.3 (SUITE) - PARCOURS D'UNE REQUÊTE ET QUESTIONS
    # =========================================================================
    story.append(Paragraph("2.3.3 Parcours Pas à Pas d'une Requête Technicien (Modèle de Raisonnement)", s_h2))
    story.append(Paragraph(
        "Pour illustrer le comportement dynamique du système, considérons le scénario réel suivant :<br/>"
        "<i>Un technicien de l'atelier pneumatique transmet la photographie d'une roue présentant un renflement sur le flanc, "
        "accompagnée de la question : « Ce pneu présente une bosse sur le côté. Quelle est la cause et est-ce réparable en atelier ? »</i>", s_body))

    journey_steps = [
        "<b>Étape 1 — Authentification et récupération du profil :</b> La passerelle FastAPI intercepte la requête, vérifie le jeton JWT "
        "et extrait le profil utilisateur (<code>role = technicien_pneumatiques</code>). Ce profil détermine le scope documentaire autorisé.",

        "<b>Étape 2 — Analyse visuelle préliminaire par le VLM :</b> L'image est transmise au modèle vision-langage Qwen2.5-VL-7B. "
        "Le modèle génère une description objective : <i>« Déformation hémisphérique proéminente (hernie) située sur la zone médiane du flanc "
        "extérieur d'un pneumatique de dimension 205/55 R16. Absence de déchirure apparente de la gomme extérieure. »</i>",

        "<b>Étape 3 — Recherche documentaire hybride sous contrainte RBAC :</b> La description visuelle et la question textuelle sont "
        "vectorisées (BGE-M3 + SigLIP). Qdrant exécute une recherche hybride dense/sparse filtrée sur <code>famille_equipement == 'pneumatiques'</code> "
        "et accessible à <code>techniciens_pneumatiques</code>. Le système récupère le document <code>pne_05_sidewall_bulge</code> (page 1 et 2).",

        "<b>Étape 4 — Reranking et consultation de l'historique MCP :</b> Le composant BGE-Reranker-v2 réordonne les passages. Constatant "
        "une avarie structurelle lourde, l'orchestrateur LangGraph interroge l'outil MCP <code>get_equipment_history('PNEU-TR-01')</code> pour "
        "vérifier si le train de pneus a subi un choc récent sur trottoir lors de la dernière révision.",

        "<b>Étape 5 — Synthèse de la réponse et vérification des citations (Evidence Checker) :</b> Le VLM rédige la réponse en citant "
        "formellement la figure <code>PNE-05-F1</code> et la page 2 du document. Le vérificateur Pydantic s'assure que l'affirmation "
        "<i>« Rupture interne de la nappe carcasse radiale, interdiction formelle de réparer, risque d'éclatement immédiat »</i> est "
        "rigoureusement soutenue par le texte de la fiche de sécurité.",

        "<b>Étape 6 — Préparation du ticket et interruption humaine (HITL) :</b> MaintiDoc formule la réponse au technicien et ajoute "
        "une proposition de ticket de remplacement : <i>« Brouillon de ticket : Échange standard pneumatique AV gauche suite hernie flanc »</i>. "
        "L'agent se met en état de veille (suspend) et n'appelle <code>create_ticket</code> qu'après validation explicite du technicien à l'écran."
    ]
    for stp in journey_steps:
        story.append(Paragraph(f"• {stp}", s_bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("2.3.4 Questions Ouvertes et Hypothèses à Vérifier (Semaines 2 à 6)", s_h2))
    story.append(Paragraph(
        "Le cadrage de la Semaine 1 a permis d'identifier plusieurs questions techniques ouvertes qui feront l'objet de benchmarks dédiés :", s_body))

    open_q_data = [
        [Paragraph("<b>Hypothèse / Question Ouverte</b>", s_table_header), Paragraph("<b>Enjeu Opérationnel & Méthode de Validation Prévue</b>", s_table_header)],
        [
            Paragraph("<b>Q1 : Empreinte VRAM du modèle Qwen2.5-VL-7B</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> Le modèle 7B quantifié en 4-bit AWQ tient dans 12 Go de VRAM et permet une fenêtre de contexte de 8k tokens sans dépassement mémoire.<br/>"
                      "<i>Validation en Semaine 3 :</i> Mesure de la mémoire allouée sous vLLM lors de requêtes multimodales concurrentes.", s_table_cell)
        ],
        [
            Paragraph("<b>Q2 : Nécessité d'un pipeline OCR systématique</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> Appliquer un OCR local sur tous les PDF ralentit inutilement l'ingestion ; un aiguillage préalable par détection de texte natif PyMuPDF est optimal.<br/>"
                      "<i>Validation en Semaine 2 :</i> Benchmark comparatif de temps d'ingestion sur les 45 documents du corpus.", s_table_cell)
        ],
        [
            Paragraph("<b>Q3 : Apport du Fine-Tuning du Reranker</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> L'adaptation d'un reranker léger sur 1 000 triplets spécialisés (question, passage positif, négatif difficile) améliorera le nDCG@5 de plus de 8%.<br/>"
                      "<i>Validation en Semaine 5 :</i> Comparaison formelle avant/après adaptation sur le jeu de test de 150 scénarios.", s_table_cell)
        ],
        [
            Paragraph("<b>Q4 : Résistance aux injections masquées dans les images OCR</b>", s_table_cell_bold),
            Paragraph("<i>Hypothèse :</i> Un payload malveillant dissimulé dans une image scannée (tampon ou texte manuscrit) peut tromper l'agent si l'OCR injecte le texte sans balisage.<br/>"
                      "<i>Validation en Semaine 5 :</i> Test de neutralisation en isolant le flux OCR comme donnée passive stricte.", s_table_cell)
        ]
    ]
    t_oq = Table(open_q_data, colWidths=[150, 358])
    t_oq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_oq)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9 : SECTION 2.4 - FLUX DE DONNÉES ET MODÈLE D'ACCÈS
    # =========================================================================
    story.append(Paragraph("2.4 Flux de Données et Modèle d'Accès", s_h1))
    story.append(Paragraph("2.4.1 Flux de Données d'Ingestion Documentaire (Pipeline ETL)", s_h2))
    story.append(Paragraph(
        "Le pipeline d'ingestion transforme les fichiers bruts hétérogènes (PDF texte, PDF scannés, photographies) en éléments "
        "indexés enrichis de métadonnées de contrôle d'accès :", s_body))

    ingest_img_path = "docs/diagrammes/flux_donnees_ingestion.png"
    if os.path.exists(ingest_img_path):
        story.append(RLImage(ingest_img_path, width=490, height=210))
        story.append(Spacer(1, 4))

    story.append(Paragraph("2.4.2 Flux d'une Requête Technicien (RAG Sourcé & Multimodal)", s_h2))
    story.append(Paragraph(
        "Le traitement d'une requête associe vision par ordinateur, recherche hybride sous contrôle RBAC et validation de citations :", s_body))

    query_img_path = "docs/diagrammes/flux_requete_rag.png"
    if os.path.exists(query_img_path):
        story.append(RLImage(query_img_path, width=490, height=215))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10 : SECTION 2.4 (SUITE) - FLUX TICKET MCP ET MODÈLE D'ACCÈS
    # =========================================================================
    story.append(Paragraph("2.4.3 Flux Sécurisé de Création de Ticket MCP (HITL & Idempotence)", s_h2))
    story.append(Paragraph(
        "La création d'un ordre de travail constitue une action sensible qui ne doit jamais être exécutée sans supervision humaine :", s_body))

    mcp_img_path = "docs/diagrammes/flux_creation_ticket_mcp.png"
    if os.path.exists(mcp_img_path):
        story.append(RLImage(mcp_img_path, width=490, height=200))
        story.append(Spacer(1, 6))

    story.append(Paragraph("2.4.4 Schéma des Métadonnées d'un Élément Indexé", s_h2))
    story.append(Paragraph(
        "Chaque fragment textuel ou élément visuel stocké dans Qdrant conserve une charge utile (*payload*) JSON standardisée :", s_body))

    meta_json_str = (
        "{\n"
        '  "chunk_id": "tdb_01_p02_c03",               // Identifiant unique de chunk\n'
        '  "document_id": "tdb_01_voyant_pression_huile", // ID stable du document source\n'
        '  "version": "v1.0 (2026-11)",                 // Version pour détection d\'obsolescence\n'
        '  "page_number": 2,                           // Numéro de page exact (citation vérifiable)\n'
        '  "element_type": "procedure_step",           // paragraph | table | figure | procedure_step\n'
        '  "element_id": "proc_step_4",                // Identifiant d\'élément ou de figure (ex: TDB-01-F1)\n'
        '  "famille_equipement": "tableaux_de_bord",   // tableaux_de_bord | pneumatiques\n'
        '  "equipement_id": "TDB-MOTEUR-01",            // Référence cohérente avec la GMAO MCP\n'
        '  "groupes_acces": ["techniciens_tdb", "responsables"], // Groupes RBAC autorisés\n'
        '  "content_hash": "a8f3b2c9...",              // Empreinte SHA256 pour traçabilité\n'
        '  "is_ocr": false                             // Flag indiquant si issu d\'un scan OCR dégradé\n'
        "}"
    )
    story.append(make_box(Paragraph(f"<pre>{meta_json_str}</pre>", s_code), bg_color='#F8FAFC', border_color='#CBD5E1', padding=4))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.4.5 Modèle d'Accès et Matrice de Ségrégation des Rôles (RBAC)", s_h2))
    story.append(Paragraph(
        "Le modèle d'accès repose sur trois groupes d'utilisateurs d'atelier avec filtrage au niveau de la base vectorielle :", s_body))

    rbac_table = [
        [Paragraph("<b>Groupe d'Accès</b>", s_table_header), Paragraph("<b>Documents Autorisés</b>", s_table_header), 
         Paragraph("<b>Documents Formellement Interdits (Refus d'Accès)</b>", s_table_header), Paragraph("<b>Outils MCP Autorisés</b>", s_table_header)],
        [
            Paragraph("<b><code>techniciens_tdb</code></b>", s_table_cell_bold),
            Paragraph("Procédures combinés de bord, témoins voyants moteur, boîte, FAP, documents partagés (TPMS).", s_table_cell),
            Paragraph("Fiches pneumatiques physiques, documents pyrotechniques Airbag (TDB-08), antidémarrage (TDB-18), notes confidentielles.", s_table_cell),
            Paragraph("<code>get_equipment_history</code>,<br/><code>create_ticket</code> (validé)", s_table_cell)
        ],
        [
            Paragraph("<b><code>techniciens_pneumatiques</code></b>", s_table_cell_bold),
            Paragraph("Fiches crevaison, usures de bande, géométrie, amortisseurs, documents partagés (TPMS, alerte révision).", s_table_cell),
            Paragraph("Procédures calculateurs combiné, diagnostic boîte automatique, antidémarrage, fiches haute tension.", s_table_cell),
            Paragraph("<code>get_equipment_history</code>,<br/><code>create_ticket</code> (validé)", s_table_cell)
        ],
        [
            Paragraph("<b><code>responsables</code></b>", s_table_cell_bold),
            Paragraph("<b>Accès transverse intégral :</b> l'ensemble des 45 documents du corpus (incluant Airbag, antidémarrage et notes d'audit).", s_table_cell),
            Paragraph("Aucune restriction documentaire (accès complet aux historiques et métadonnées d'audit).", s_table_cell),
            Paragraph("<b>Tous les outils MCP</b> + consultation globale des tickets ouverts.", s_table_cell)
        ]
    ]
    t_rbac = Table(rbac_table, colWidths=[110, 150, 150, 98])
    t_rbac.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_rbac)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11 : SECTION 2.5 - ANALYSE DES RISQUES
    # =========================================================================
    story.append(Paragraph("2.5 Analyse des Risques", s_h1))
    story.append(Paragraph(
        "Une analyse prospective exhaustive a été menée pour couvrir l'ensemble des risques techniques, sécuritaires, "
        "documentaires et organisationnels du projet. Neuf risques majeurs ont été caractérisés avec leur probabilité (1-3), "
        "leur impact (1-3), leur criticité ($C = P \times I$), les mesures d'atténuation prévues et le responsable assigné :", s_body))

    risk_table = [
        [
            Paragraph("<b>ID / Risque Identifié</b>", s_table_header),
            Paragraph("<b>Catégorie</b>", s_table_header),
            Paragraph("<b>P (1-3)</b>", s_table_header),
            Paragraph("<b>I (1-3)</b>", s_table_header),
            Paragraph("<b>Crit. (P×I)</b>", s_table_header),
            Paragraph("<b>Mesures Préventives & Curatives Prévues</b>", s_table_header),
            Paragraph("<b>Resp.</b>", s_table_header)
        ],
        [
            Paragraph("<b>R1 : Injection de prompt indirecte</b> (via document piégé)", s_table_cell_bold),
            Paragraph("Sécurité", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Traitement des documents comme données passives (séparateurs XML stricts) ; exclusion des appels système directs ; tests dédiés en Semaine 5.", s_table_cell),
            Paragraph("Hafsa", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R2 : Hallucinations & citations non fondées</b>", s_table_cell_bold),
            Paragraph("Technique", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Evidence Checker Pydantic automatisé vérifiant l'existence exacte de [doc_id, page, figure] ; consigne stricte d'abstention en prompt système.", s_table_cell),
            Paragraph("Wiam", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R3 : Fuite de données entre groupes d'accès (RBAC)</b>", s_table_cell_bold),
            Paragraph("Sécurité", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("3", s_table_cell), Paragraph("3", s_table_cell),
            Paragraph("Pré-filtrage vectoriel déterministe dans Qdrant sur métadonnée groupe_acces avant retrieval ; double vérification post-retrieval dans l'API.", s_table_cell),
            Paragraph("Aya", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R4 : Création autonome ou non approuvée de ticket</b>", s_table_cell_bold),
            Paragraph("Sécurité / Métier", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("3", s_table_cell), Paragraph("3", s_table_cell),
            Paragraph("Garde-fou humain absolu (Human-in-the-Loop) dans LangGraph ; émission d'un approval_token à usage unique ; clé d'idempotence anti-doublon.", s_table_cell),
            Paragraph("Wiam", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R5 : Erreurs techniques injectées par l'IA dans le corpus</b>", s_table_cell_bold),
            Paragraph("Données", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Relecture humaine croisée systématique (double-blind) ; traçabilité intégrale dans prompts_corpus.md et inventaire.csv normalisé.", s_table_cell),
            Paragraph("Hafsa", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R6 : Non-conformité des licences documentaires</b>", s_table_cell_bold),
            Paragraph("Légal / Données", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("2", s_table_cell), Paragraph("2", s_table_cell),
            Paragraph("Utilisation exclusive de fiches synthétiques originales et d'images ouvertes (Creative Commons CC BY / domaine public pédagogique).", s_table_cell),
            Paragraph("Aya", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R7 : Saturation mémoire GPU (OOM) et latences</b>", s_table_cell_bold),
            Paragraph("Technique", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("3", s_table_cell), Paragraph("<b>6</b>", s_table_cell_bold),
            Paragraph("Quantification 4-bit (AWQ) du VLM Qwen2.5-VL ; moteur vLLM ; modèle léger de repli (ex. Moondream2 ou Phi-3.5-Vision) prêt à l'emploi.", s_table_cell),
            Paragraph("Wiam", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R8 : Défaillance ou indisponibilité du serveur MCP</b>", s_table_cell_bold),
            Paragraph("Technique", s_table_cell),
            Paragraph("2", s_table_cell), Paragraph("2", s_table_cell), Paragraph("4", s_table_cell),
            Paragraph("Mise en place d'un bouchon (mock MCP) local autonome pour poursuivre le développement et les tests en cas de coupure réseau.", s_table_cell),
            Paragraph("Aya", s_table_cell_bold)
        ],
        [
            Paragraph("<b>R9 : Désynchronisation ou retard dans l'équipe</b>", s_table_cell_bold),
            Paragraph("Organisation", s_table_cell),
            Paragraph("1", s_table_cell), Paragraph("2", s_table_cell), Paragraph("2", s_table_cell),
            Paragraph("Points d'étape hebdomadaires synchronisés ; découpage strict des rôles ; intégration continue Git avec branches dédiées.", s_table_cell),
            Paragraph("Hafsa", s_table_cell_bold)
        ]
    ]
    t_risk = Table(risk_table, colWidths=[105, 55, 30, 30, 35, 215, 38])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (2,0), (4,-1), 'CENTER'),
    ]))
    story.append(t_risk)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Synthèse de la matrice des risques :</b> Les risques les plus critiques ($C = 6$) concernent la sécurité des prompts (R1), "
        "l'exactitude des citations documentaires (R2), la qualité des données du corpus (R5) et la saturation de la VRAM GPU (R7). "
        "Chacun de ces risques fait l'objet d'un responsable désigné au sein de l'équipe et d'une mesure technique préventive intégrée dès la conception.", s_callout))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12 : SECTION 2.6 - PLANNING ET ORGANISATION DE L'ÉQUIPE
    # =========================================================================
    story.append(Paragraph("2.6 Planning et Organisation de l'Équipe", s_h1))
    story.append(Paragraph("2.6.1 Répartition des Rôles et Spécialisations", s_h2))
    story.append(Paragraph(
        "Pour maximiser l'efficience collective et garantir une couverture technique rigoureuse, les responsabilités ont été "
        "réparties en trois pôles de compétence complémentaires :", s_body))

    roles_data = [
        [
            Paragraph("<b>Membre de l'Équipe</b>", s_table_header),
            Paragraph("<b>Rôle & Pôle de Spécialisation</b>", s_table_header),
            Paragraph("<b>Missions Clés & Livrables Concrets Pris en Charge</b>", s_table_header)
        ],
        [
            Paragraph("<b>SOUILI Wiam</b><br/>Lead Architecture & Agentique", s_table_cell_bold),
            Paragraph("Ingénierie Système, LangGraph, Passerelle FastAPI & Serveur MCP", s_table_cell),
            Paragraph("• Conception de la machine à états LangGraph (nœuds, transitions, limites de boucle).<br/>"
                      "• Développement de la passerelle FastAPI (authentification JWT, gestion RBAC).<br/>"
                      "• Implémentation du serveur MCP maintenance et du mécanisme Human-in-the-Loop.<br/>"
                      "• Conteneurisation globale avec Docker Compose et orchestration réseau.", s_table_cell)
        ],
        [
            Paragraph("<b>YEKHLEF Aya</b><br/>Lead RAG Multimodal & Recherche", s_table_cell_bold),
            Paragraph("Pipeline d'Ingestion ETL, Qdrant, Embeddings & Reranker", s_table_cell),
            Paragraph("• Développement du pipeline d'ingestion multimodale (PyMuPDF, segmentation sémantique).<br/>"
                      "• Intégration du module OCR local (Surya / Tesseract) pour les documents scannés.<br/>"
                      "• Déploiement et indexation de la base vectorielle Qdrant (BGE-M3 + SigLIP).<br/>"
                      "• Fine-tuning ciblé du petit reranker multilingue sur données mécaniques (Semaine 5).", s_table_cell)
        ],
        [
            Paragraph("<b>ELAOUAZI Hafsa</b><br/>Lead Évaluation, Sécurité & Corpus", s_table_cell_bold),
            Paragraph("Modèles VLM, Sécurité des Prompts, Schémas Pydantic & QA", s_table_cell),
            Paragraph("• Déploiement et benchmarking du modèle vision-langage Qwen2.5-VL-7B (vLLM / AWQ).<br/>"
                      "• Modélisation des contrats d'interface Pydantic et du module Evidence Checker.<br/>"
                      "• Élaboration du jeu de test de 150 scénarios (ambiguïtés, contradictions, injections).<br/>"
                      "• Mesure des métriques de recherche (Recall@5, nDCG@5, MRR@10) et tracking MLflow.", s_table_cell)
        ]
    ]
    t_roles = Table(roles_data, colWidths=[120, 140, 248])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_roles)

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.6.2 Planning Prévisionnel Détaillé des Semaines 2 à 6", s_h2))
    story.append(Paragraph(
        "La feuille de route chronologique s'ajuste aux ressources réelles de l'équipe et aux exigences de chaque jalon hebdomadaire :", s_body))

    planning_data = [
        [Paragraph("<b>Semaine</b>", s_table_header), Paragraph("<b>Intitulé des Travaux</b>", s_table_header), 
         Paragraph("<b>Objectifs Techniques & Tâches Concrètes</b>", s_table_header), Paragraph("<b>Livrable Associé</b>", s_table_header)],
        [
            Paragraph("<b>Semaine 1</b><br/>(En cours)", s_table_cell_bold),
            Paragraph("Cadrage, corpus & architecture", s_table_cell),
            Paragraph("• Définition du périmètre, personas et cas d'usage.<br/>"
                      "• Constitution et validation du corpus de 45 documents (TDB & PNE).<br/>"
                      "• Rédaction du rapport L1 et schémas d'architecture.", s_table_cell),
            Paragraph("<b>Livrable 1</b><br/>Rapport PDF + ZIP corpus complet", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 2</b>", s_table_cell_bold),
            Paragraph("Ingestion, recherche & gestion des accès", s_table_cell),
            Paragraph("• Développement du pipeline ETL (PyMuPDF + OCR local pour tdb_19 et pne_12).<br/>"
                      "• Découpage en passages/figures et calcul embeddings (BGE-M3, SigLIP).<br/>"
                      "• Indexation Qdrant avec filtrage métadonnées RBAC.", s_table_cell),
            Paragraph("<b>Livrable 2</b><br/>Dépôt Git documenté & index prêt", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 3</b>", s_table_cell_bold),
            Paragraph("Intégration du VLM & sorties structurées", s_table_cell),
            Paragraph("• Déploiement de Qwen2.5-VL-7B avec quantification AWQ sur GPU.<br/>"
                      "• Prompting multimodal, validation sorties Pydantic.<br/>"
                      "• Module Evidence Checker vérifiant citations documentaires exactes.", s_table_cell),
            Paragraph("<b>Livrable 3 (P1)</b><br/>Prototype RAG multimodal opérationnel", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 4</b>", s_table_cell_bold),
            Paragraph("Workflow LangGraph & connexion MCP", s_table_cell),
            Paragraph("• Construction du graphe agentique avec nœuds de décision.<br/>"
                      "• Implémentation du serveur MCP (historiques et tickets GMAO).<br/>"
                      "• Mécanisme bloquant d'approbation humaine et clé d'idempotence.", s_table_cell),
            Paragraph("<b>Livrable 3 (P2)</b><br/>Prototype agentique complet avec MCP", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 5</b>", s_table_cell_bold),
            Paragraph("Adaptation reranker & banc d'évaluation", s_table_cell),
            Paragraph("• Constitution du dataset de fine-tuning (1 000 triplets spécialisés).<br/>"
                      "• Entraînement et évaluation BGE-Reranker-v2 (nDCG@5, MRR@10).<br/>"
                      "• Campagne de test sur 150 scénarios (injections, ambiguïtés, accès).", s_table_cell),
            Paragraph("<b>Livrable 4</b><br/>Rapport d'évaluation & comparaisons", s_table_cell_bold)
        ],
        [
            Paragraph("<b>Semaine 6</b>", s_table_cell_bold),
            Paragraph("Déploiement Docker, fiches & soutenance", s_table_cell),
            Paragraph("• Finalisation Docker Compose, durcissement sécurité et logs MLflow.<br/>"
                      "• Rédaction de la fiche de limites et conditions d'usage.<br/>"
                      "• Répétition des démonstrations live (nominal, injection, HITL).", s_table_cell),
            Paragraph("<b>Livrables 5 & 6</b><br/>Fiche de limites, démo & soutenance finale", s_table_cell_bold)
        ]
    ]
    t_plan = Table(planning_data, colWidths=[65, 105, 245, 93])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_plan)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13 : SECTION 2.6 (SUITE) - MATRICE RACI ET CONCLUSION
    # =========================================================================
    story.append(Paragraph("2.6.3 Matrice de Responsabilité RACI", s_h2))
    story.append(Paragraph(
        "La matrice RACI (<i>Responsible, Accountable, Consulted, Informed</i>) formalise l'implication de chaque membre :", s_body))

    raci_data = [
        [Paragraph("<b>Activité / Livrable Majeur</b>", s_table_header), 
         Paragraph("<b>Wiam SOUILI</b>", s_table_header), 
         Paragraph("<b>Aya YEKHLEF</b>", s_table_header), 
         Paragraph("<b>Hafsa ELAOUAZI</b>", s_table_header)],
        [Paragraph("Constitution du corpus et inventaire normalisé", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("C", s_table_cell_bold), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary))],
        [Paragraph("Pipeline ETL d'ingestion & module OCR", s_table_cell), Paragraph("I", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary)), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Indexation Qdrant & filtrage des métadonnées RBAC", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary)), Paragraph("I", s_table_cell)],
        [Paragraph("Déploiement et optimisation du modèle VLM Qwen2.5-VL", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("I", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary))],
        [Paragraph("Machine à états LangGraph & orchestration agentique", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary)), Paragraph("C", s_table_cell_bold), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Serveur MCP maintenance & workflow Human-in-the-Loop", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary)), Paragraph("I", s_table_cell), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Fine-tuning supervisé du reranker multilingue", s_table_cell), Paragraph("I", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary)), Paragraph("C", s_table_cell_bold)],
        [Paragraph("Banc d'évaluation (150 scénarios) & tests d'injection", s_table_cell), Paragraph("C", s_table_cell_bold), Paragraph("C", s_table_cell_bold), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary))],
        [Paragraph("Déploiement conteneurisé Docker Compose & MLOps", s_table_cell), Paragraph("<b>A / R</b>", ParagraphStyle('AR', parent=s_table_cell_bold, textColor=c_primary)), Paragraph("C", s_table_cell_bold), Paragraph("I", s_table_cell)]
    ]
    t_raci = Table(raci_data, colWidths=[238, 90, 90, 90])
    t_raci.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_raci)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Conclusion du Livrable 1 et Transition vers la Semaine 2", s_h2))
    story.append(Paragraph(
        "Ce premier livrable établit un cadre méthodologique, fonctionnel et architectural solide pour le projet MaintiDoc. "
        "Les besoins métiers ont été traduits en cas d'usage vérifiables, le corpus documentaire de 45 fiches techniques et 40 figures "
        "est intégralement tracé et vérifié, et l'architecture cible intègre nativement la sécurité (RBAC, Evidence Checking, HITL MCP). "
        "Dès le démarrage de la Semaine 2, l'équipe s'attellera au développement du pipeline ETL d'ingestion, à l'évaluation de l'OCR sur "
        "les deux documents scannés et au déploiement de l'index vectoriel Qdrant.", s_body))

    concl_box = (
        "<b>Engagements de l'équipe pour la Semaine 2 :</b><br/>"
        "• Dépôt Git structuré avec environnement virtuel reproductible (Poetry / requirements.txt sans conflits).<br/>"
        "• Pipeline d'ingestion PyMuPDF + Surya OCR validé sur les documents dégradés.<br/>"
        "• Index Qdrant opérationnel avec recherche dense/sparse et pré-filtrage des groupes d'accès.<br/>"
        "• Zéro secret (clé API, token) commité dans le dépôt public de l'équipe."
    )
    story.append(make_box(Paragraph(concl_box, s_callout), bg_color='#EFF6FF', border_color='#3B82F6'))

    story.append(PageBreak())

    # =========================================================================
    # PAGES 14-15 : ANNEXES TECHNIQUES (INVENTAIRE CONDENSÉ DU CORPUS)
    # =========================================================================
    story.append(Paragraph("Annexes Techniques : Registre d'Inventaire du Corpus MaintiDoc", s_h1))
    story.append(Paragraph(
        "Extrait condensé des 45 documents figurant dans le fichier d'inventaire normalisé <code>corpus/inventaire.csv</code> :", s_body))

    # We read the first 23 rows (TDB) for Page 14
    with open("corpus/inventaire.csv", "r", encoding="utf-8") as f_inv:
        import csv
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
                      ParagraphStyle('UT', parent=s_table_cell, textColor=c_alert if row['usage_test'] != 'normal' else c_dark)),
            Paragraph(row['verifie_par'], s_table_cell)
        ])

    t_inv_p1 = Table(inv_table_p1_data, colWidths=[115, 145, 75, 55, 45, 45, 28])
    t_inv_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
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
                      ParagraphStyle('UT', parent=s_table_cell, textColor=c_alert if row['usage_test'] != 'normal' else c_dark)),
            Paragraph(row['verifie_par'], s_table_cell)
        ])

    t_inv_p2 = Table(inv_table_p2_data, colWidths=[115, 145, 75, 55, 45, 45, 28])
    t_inv_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
    ]))
    story.append(t_inv_p2)

    story.append(Spacer(1, 15))
    validation_sign = [
        [Paragraph("<b>Approbation et Visa de l'Équipe MaintiDoc :</b>", s_body_bold)],
        [Paragraph("Nous certifions sur l'honneur que l'ensemble des documents figurant dans cet inventaire a fait l'objet "
                   "d'une vérification critique, qu'aucune donnée personnelle réelle n'a été utilisée, et que les cas de test "
                   "spécifiques (contradictoires, injection, scans) sont correctement isolés.", s_callout)],
        [Paragraph("<b>SOUILI Wiam</b> (Signé) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
                   "<b>YEKHLEF Aya</b> (Signé) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
                   "<b>ELAOUAZI Hafsa</b> (Signé)", ParagraphStyle('Sig', parent=s_body_bold, textColor=c_primary))]
    ]
    t_sign = Table(validation_sign, colWidths=[508])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {filename}")

if __name__ == "__main__":
    build_pdf()

