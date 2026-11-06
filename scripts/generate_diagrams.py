import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("docs/diagrammes", exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# =============================================================================
# 1. ARCHITECTURE CIBLE : Vue Haute Définition Modulaire & Contrôles
# =============================================================================
def draw_architecture():
    fig, ax = plt.subplots(figsize=(17, 12), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Cartouche supérieur
    ax.text(50, 98.2, "Architecture Cible MaintiDoc — Système Agentique & Multimodal", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(50, 96.0, "EMSI 2026 | IA Générative Multimodale | Équipe : ELAOUAZI Hafsa · SOUILI Wiam · YEKHLEF Aya", 
            ha='center', va='center', fontsize=9.5, color='#475569')

    def draw_card(x, y, w, h, num, title, lines, bg_color, border_color, badge=None, badge_bg='#EF4444'):
        # Ombre portée subtile
        shadow = patches.FancyBboxPatch((x + 0.35, y - 0.35), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                       fc='#CBD5E1', ec='none', alpha=0.35, zorder=1)
        ax.add_patch(shadow)

        # Carte principale
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                     fc=bg_color, ec=border_color, lw=1.5, zorder=2)
        ax.add_patch(card)

        # En-tête : Titre aligné à gauche
        full_title = f"{num}. {title}" if num else title
        ax.text(x + 1.8, y + h - 2.6, full_title, ha='left', va='center', fontsize=9.2, fontweight='bold', color='#0F172A', zorder=4)

        # Badge compact à l'extrême droite de l'en-tête
        if badge:
            bw = len(badge) * 0.58 + 2.2
            bx = x + w - bw - 1.5
            by = y + h - 3.7
            b_patch = patches.FancyBboxPatch((bx, by), bw, 2.0, boxstyle="round,pad=0.15,rounding_size=0.5",
                                            fc=badge_bg, ec='none', zorder=5)
            ax.add_patch(b_patch)
            ax.text(bx + bw/2, by + 1.0, badge, ha='center', va='center', fontsize=6.0, fontweight='bold', color='#FFFFFF', zorder=6)

        # Ligne de séparation sous l'en-tête
        ax.plot([x + 1.2, x + w - 1.2], [y + h - 4.4, y + h - 4.4], color=border_color, lw=0.8, alpha=0.5, zorder=3)

        # Lignes de contenu
        y_text = y + h - 6.6
        for line in lines:
            ax.text(x + 1.8, y_text, line, ha='left', va='center', fontsize=7.4, color='#334155', zorder=4)
            y_text -= 2.2

    def draw_wire(x1, y1, x2, y2, label=None, color='#334155', rad=0.0, label_pos=0.5, label_offset=(0, 0), label_fs=6.6):
        connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5,
                                    connectionstyle=connectionstyle, shrinkA=3, shrinkB=3), zorder=3)
        if label:
            mx = x1 + (x2 - x1) * label_pos + label_offset[0]
            my = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(mx, my, label, ha='center', va='center', fontsize=label_fs, fontweight='bold',
                    color=color, bbox=dict(boxstyle='round,pad=0.22', fc='#FFFFFF', ec=color, lw=0.6, alpha=0.95), zorder=5)

    # ------------------ NIVEAU 1 : Interface Client ------------------
    draw_card(33, 84, 34, 9.5, "1", "Interface Utilisateur (Streamlit)",
              ["• Application Web mobile d'atelier (smartphone & tablette)",
               "• Formulaire de saisie bilingue (FR/AR) & upload photo HD"],
              '#EFF6FF', '#3B82F6')

    # ------------------ NIVEAU 2 : Passerelle API ------------------
    draw_card(33, 69, 34, 10.0, "2", "Passerelle d'API (FastAPI)",
              ["• Authentification sécurisée par jeton JWT & Rate-Limiting",
               "• Contrôle RBAC sur en-tête et injection des privilèges"],
              '#F0FDF4', '#22C55E', badge="PC1 : JWT RBAC", badge_bg='#16A34A')

    # Fil N1 -> N2
    draw_wire(50, 84, 50, 79, label="Photo HD + Question texte", color='#2563EB', label_offset=(10.5, 0))

    # ------------------ NIVEAU 3 : Cœur Orchestrateur & Flancs ------------------
    # Flanc Gauche : VLM (x: 2 à 27, w=25)
    draw_card(2, 44, 25, 20.0, "4", "Modèle Vision (VLM)",
              ["• Qwen2.5-VL-7B (4-bit AWQ)",
               "• Inférence accélérée vLLM",
               "• Détection des témoins (TDB)",
               "• Analyse avaries pneus (PNE)",
               "• Extraction factuelle objective"],
              '#F3E8FF', '#9333EA')

    # Centre : LangGraph (x: 35 à 65, w=30)
    draw_card(35, 44, 30, 20.0, "3", "Orchestrateur (LangGraph)",
              ["• Machine à états finis & persistance",
               "• Nœud 1 : Routage d'intention",
               "• Nœud 2 : Orchestration RAG & MCP",
               "• Nœud 3 : Contrôle d'arrêt HITL",
               "• Gestionnaire de timeouts d'atelier"],
              '#FEF3C7', '#F59E0B')

    # Flanc Droit : Serveur MCP (x: 73 à 98, w=25)
    draw_card(73, 44, 25, 20.0, "5", "Serveur Outils (MCP)",
              ["• Protocole standardisé MCP",
               "• get_equipment_history() [R]",
               "• create_ticket() [W protégé]",
               "• Jeton signé & UUID idempotence",
               "• Interfaçage avec GMAO atelier"],
              '#FCE7F3', '#DB2777', badge="PC2 : HITL", badge_bg='#EF4444')

    # Fil N2 -> N3
    draw_wire(50, 69, 50, 64, label="Requête validée + Rôle", color='#16A34A', label_offset=(10.5, 0))

    # Liaisons Horizontales N3 (dégagées, gap de 8 units)
    # LangGraph -> VLM
    draw_wire(35, 57, 27, 57, label="Image + Prompt", color='#9333EA', label_offset=(0, 1.4), label_fs=6.2)
    # VLM -> LangGraph
    draw_wire(27, 50, 35, 50, label="Faits visuels", color='#9333EA', label_offset=(0, -1.4), label_fs=6.2)

    # LangGraph -> MCP
    draw_wire(65, 57, 73, 57, label="get_history(id)", color='#DB2777', label_offset=(0, 1.4), label_fs=6.2)
    # MCP -> LangGraph
    draw_wire(73, 50, 65, 50, label="Historique GMAO", color='#DB2777', label_offset=(0, -1.4), label_fs=6.2)

    # ------------------ NIVEAU 4 : Moteur RAG & Stockage Persistant ------------------
    # Gauche : Qdrant (x: 2 à 42, w=40)
    draw_card(2, 21, 40, 18.0, "6", "Moteur RAG Multimodal (Qdrant)",
              ["• Base vectorielle Qdrant (dense BGE-M3 + sparse SPLADE)",
               "• Indexation visuelle des figures et schémas techniques",
               "• Re-ranking contextuel par BGE-Reranker-v2 sur les Top-K",
               "• Pré-filtrage matériel déterministe sur groupes_acces",
               "• Métadonnées riches : doc_id, version, page, equipement"],
              '#E0F2FE', '#0284C7', badge="PC1 : RBAC", badge_bg='#0284C7')

    # Droite : Stockage (x: 58 à 98, w=40)
    draw_card(58, 21, 40, 18.0, "7", "Couche de Stockage & Traçabilité",
              ["• MinIO S3 : Dépôt sécurisé des PDF constructeurs & images",
               "• PostgreSQL : Métadonnées relationnelles, comptes & rôles",
               "• Base SQLite locale : Checkpoints de reprise d'état LangGraph",
               "• Journal d'audit immuable : Horodatage SHA-256 de chaque inférence",
               "• Traçabilité complète des interventions et requêtes"],
              '#F1F5F9', '#64748B')

    # Liaisons N3 -> N4
    # LangGraph vers Qdrant
    draw_wire(37, 44, 25, 39, label="Requête RAG (Filtre RBAC)", color='#0284C7', label_offset=(-5, 1.0), label_fs=6.3)
    # Qdrant vers LangGraph
    draw_wire(31, 39, 41, 44, label="Extraits & Figures vérifiés", color='#0284C7', label_offset=(4, -1.0), label_fs=6.3)

    # LangGraph vers Stockage
    draw_wire(62, 44, 72, 39, label="Persistance session & logs", color='#64748B', label_offset=(5, 1.0), label_fs=6.3)

    # ------------------ NIVEAU 5 : Contrôleur de Preuves (PC3) ------------------
    draw_card(16, 2, 68, 14.5, "8", "Contrôleur de Preuves & Citations (Evidence Grounding)",
              ["• Validation automatique Pydantic du schéma de réponse finale de l'assistant",
               "• Contrôle strict d'ancrage : chaque citation [doc_id, page, figure] doit figurer dans les extraits",
               "• Règle de sécurité absolue : en cas de contradiction ou d'absence de preuve, l'agent s'abstient",
               "• Certification formelle de la réponse avant restitution à l'opérateur"],
              '#FEF2F2', '#EF4444', badge="PC3 : EVIDENCE CHECKING", badge_bg='#DC2626')

    # Couloir central dégagé (x: 42..58 = 16 units)
    # LangGraph vers Evidence Grounding (x = 48)
    draw_wire(48, 44, 48, 16.5, color='#DC2626')
    ax.text(48, 32, "1. Soumission réponse candidate", ha='center', va='center', fontsize=6.3, fontweight='bold',
            color='#DC2626', bbox=dict(boxstyle='round,pad=0.22', fc='#FFFFFF', ec='#DC2626', lw=0.6, alpha=0.95), zorder=5)

    # Evidence Grounding vers LangGraph (x = 52)
    draw_wire(52, 16.5, 52, 44, color='#16A34A')
    ax.text(52, 25, "2. Certification conforme", ha='center', va='center', fontsize=6.3, fontweight='bold',
            color='#16A34A', bbox=dict(boxstyle='round,pad=0.22', fc='#FFFFFF', ec='#16A34A', lw=0.6, alpha=0.95), zorder=5)

    # Cartouche des 3 Points de Contrôle Obligatoires (En haut à droite)
    box_legend = patches.FancyBboxPatch((70, 78.5), 28, 15.0, boxstyle="round,pad=0.4,rounding_size=0.8",
                                       fc='#FFFBEB', ec='#B45309', lw=1.2, zorder=3)
    ax.add_patch(box_legend)
    ax.text(84, 91.5, "Points de Contrôle Fondamentaux :", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#92400E', zorder=4)
    ax.text(71.5, 87.8, "• PC1 (Droits) : Token JWT + Pré-filtre Qdrant", ha='left', va='center', fontsize=7.2, color='#78350F', zorder=4)
    ax.text(71.5, 84.3, "• PC2 (Humain) : Barrière bloquante avant ticket MCP", ha='left', va='center', fontsize=7.2, color='#78350F', zorder=4)
    ax.text(71.5, 80.8, "• PC3 (Preuves) : Validation Pydantic des citations", ha='left', va='center', fontsize=7.2, color='#78350F', zorder=4)

    plt.tight_layout()
    plt.savefig("docs/diagrammes/architecture_cible.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Regenerated clean architecture_cible.png")


# =============================================================================
# 2. FLUX D'INGESTION ETL : Disposition Séquentielle HD
# =============================================================================
def draw_ingestion():
    fig, ax = plt.subplots(figsize=(16, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    ax.text(50, 56, "Pipeline d'Ingestion Documentaire Multimodale (ETL)", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0F172A')
    ax.text(50, 52.8, "Traitement automatisé, découpage sémantique et vectorisation hybride du corpus", 
            ha='center', va='center', fontsize=9.2, color='#475569')

    steps = [
        (2, 22, 17.5, 24, "1", "Documents Sources", 
         ["• 45 PDF originaux", "• 23 Tableaux de bord", "• 22 Pneumatiques", "• 40 Images extraites", "• Fiches atelier terrain"], 
         '#F1F5F9', '#64748B'),
        (21.5, 22, 17.5, 24, "2", "Détection & OCR", 
         ["• PyMuPDF (43 PDF)", "• Aiguillage automatique", "• OCR Surya / Tesseract", "• Détection 2 scans", "• Calque texte propre"], 
         '#FEF3C7', '#F59E0B'),
        (41, 22, 18, 24, "3", "Découpage (Chunk)", 
         ["• Découpage sémantique", "• Extraction paragraphes", "• Isolation figures/tables", "• Conservation métadonnées", "• Ancrage [doc_id, page]"], 
         '#E0F2FE', '#0284C7'),
        (61, 22, 17.5, 24, "4", "Embeddings", 
         ["• BGE-M3 (dense 1024-d)", "• SPLADE (sparse lexical)", "• SigLIP (visuel figures)", "• Multi-représentation", "• Indexation hybride"], 
         '#F3E8FF', '#9333EA'),
        (80.5, 22, 17.5, 24, "5", "Indexation Qdrant", 
         ["• Collections vectorielles", "• Payload JSON enrichi", "• Pré-filtre groupes_acces", "• Stockage MinIO S3", "• Audit SHA-256 corpus"], 
         '#F0FDF4', '#22C55E')
    ]

    for x, y, w, h, num, title, lines, c_bg, c_ec in steps:
        # Ombre
        shadow = patches.FancyBboxPatch((x + 0.35, y - 0.35), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                       fc='#CBD5E1', ec='none', alpha=0.35, zorder=1)
        ax.add_patch(shadow)

        # Carte
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                     fc=c_bg, ec=c_ec, lw=1.5, zorder=2)
        ax.add_patch(box)

        # En-tête
        ax.text(x + 1.5, y + h - 2.8, f"{num}. {title}", ha='left', va='center', fontsize=8.8, fontweight='bold', color='#0F172A', zorder=4)
        ax.plot([x + 1.0, x + w - 1.0], [y + h - 4.6, y + h - 4.6], color=c_ec, lw=0.8, alpha=0.5, zorder=3)

        # Contenu
        y_l = y + h - 7.2
        for l in lines:
            ax.text(x + 1.5, y_l, l, ha='left', va='center', fontsize=7.2, color='#334155', zorder=4)
            y_l -= 3.2

    # Flèches horizontales bien espacées
    for i in range(len(steps)-1):
        x1 = steps[i][0] + steps[i][2]
        y1 = steps[i][1] + steps[i][3]/2
        x2 = steps[i+1][0]
        y2 = steps[i+1][1] + steps[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#0F172A', lw=1.6, shrinkA=2, shrinkB=2), zorder=3)

    # Cartouche de métadonnées préservées
    meta_box = patches.FancyBboxPatch((8, 4), 84, 11, boxstyle="round,pad=0.5,rounding_size=1.0",
                                     fc='#F8FAFC', ec='#CBD5E1', lw=1.2, zorder=2)
    ax.add_patch(meta_box)
    ax.text(50, 11.5, "Schéma Standard des Métadonnées Injectées dans Qdrant (Traçabilité & RBAC) :", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.text(50, 7.5, "document_id · version · page_number · element_id · famille_equipement · equipement_id · groupes_acces [N1, N2, N3]", 
            ha='center', va='center', fontsize=8.0, color='#0284C7', fontweight='bold')

    plt.tight_layout()
    plt.savefig("docs/diagrammes/flux_donnees_ingestion.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Regenerated clean flux_donnees_ingestion.png")


# =============================================================================
# 3. FLUX REQUÊTE TECHNICIEN : Parcours Complet Sans Chevauchement
# =============================================================================
def draw_query_flow():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Titre et cartouche
    ax.text(50, 97.8, "Parcours Complet d'une Requête Technicien (RAG Sourcé & Multimodal)", 
            ha='center', va='center', fontsize=15.5, fontweight='bold', color='#0F172A')
    ax.text(50, 95.5, "Cycle de vie complet : De la capture photo sur le terrain à la certification de la réponse et l'action d'atelier", 
            ha='center', va='center', fontsize=9.0, color='#475569')

    def draw_card(x, y, w, h, num, title, lines, bg_color, border_color, badge=None, badge_bg='#EF4444'):
        shadow = patches.FancyBboxPatch((x + 0.35, y - 0.35), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                       fc='#CBD5E1', ec='none', alpha=0.35, zorder=1)
        ax.add_patch(shadow)

        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                     fc=bg_color, ec=border_color, lw=1.5, zorder=2)
        ax.add_patch(card)

        full_title = f"{num}. {title}" if num else title
        ax.text(x + 1.8, y + h - 2.8, full_title, ha='left', va='center', fontsize=9.2, fontweight='bold', color='#0F172A', zorder=4)

        if badge:
            bw = len(badge) * 0.58 + 2.2
            bx = x + w - bw - 1.5
            by = y + h - 3.8
            b_patch = patches.FancyBboxPatch((bx, by), bw, 2.0, boxstyle="round,pad=0.15,rounding_size=0.5",
                                            fc=badge_bg, ec='none', zorder=5)
            ax.add_patch(b_patch)
            ax.text(bx + bw/2, by + 1.0, badge, ha='center', va='center', fontsize=6.0, fontweight='bold', color='#FFFFFF', zorder=6)

        ax.plot([x + 1.2, x + w - 1.2], [y + h - 4.6, y + h - 4.6], color=border_color, lw=0.8, alpha=0.5, zorder=3)

        y_text = y + h - 7.0
        for line in lines:
            ax.text(x + 2.0, y_text, line, ha='left', va='center', fontsize=7.4, color='#334155', zorder=4)
            y_text -= 2.3

    def draw_wire(x1, y1, x2, y2, label=None, color='#334155', rad=0.0, label_pos=0.5, label_offset=(0, 0), label_fs=6.6):
        connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5,
                                    connectionstyle=connectionstyle, shrinkA=3, shrinkB=3), zorder=3)
        if label:
            mx = x1 + (x2 - x1) * label_pos + label_offset[0]
            my = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(mx, my, label, ha='center', va='center', fontsize=label_fs, fontweight='bold',
                    color=color, bbox=dict(boxstyle='round,pad=0.22', fc='#FFFFFF', ec=color, lw=0.6, alpha=0.95), zorder=5)

    # ------------------ RANGÉE 1 : Acquisition & Recherche (Haut : y=69..89) ------------------
    draw_card(2, 69, 21.5, 20, "1", "Requête Atelier",
              ["• Question en langage naturel",
               "• Photo HD du témoin / avarie",
               "• Métadonnées véhicule (VIN)",
               "• Déclenchement smartphone"],
              '#EFF6FF', '#3B82F6')

    draw_card(26.5, 69, 22.5, 20, "2", "Contrôle RBAC",
              ["• Validation du jeton JWT",
               "• Extraction du profil atelier",
               "• Détermination des droits",
               "• Injection du filtre Qdrant"],
              '#F0FDF4', '#22C55E', badge="PC1 : JWT", badge_bg='#16A34A')

    draw_card(52, 69, 22.5, 20, "3", "Perception VLM",
              ["• Modèle Qwen2.5-VL-7B",
               "• Détection des témoins TDB",
               "• Classification usure pneus",
               "• Extraction factuelle stricte"],
              '#F3E8FF', '#9333EA')

    draw_card(77.5, 69, 20.5, 20, "4", "Recherche RAG",
              ["• Pré-filtrage groupes_acces",
               "• Hybride Dense + Sparse",
               "• Extraction figures & texte",
               "• Reranking BGE-Reranker"],
              '#E0F2FE', '#0284C7', badge="PC1 : RBAC", badge_bg='#0284C7')

    # Liaisons Rangée 1
    draw_wire(23.5, 79, 26.5, 79, color='#2563EB')
    draw_wire(49.0, 79, 52.0, 79, color='#16A34A')
    draw_wire(74.5, 79, 77.5, 79, color='#9333EA')

    # ------------------ RANGÉE 2 : Synthèse & Contrôle (Milieu : y=38..59) ------------------
    # Descente de l'Étape 4 (RAG) vers l'Étape 5 (Synthèse)
    draw_wire(87.5, 69, 87.5, 59, label="Top-K Documents + Figures", color='#0284C7', label_offset=(0, 0), label_fs=6.5)

    # Étape 5 à Droite (x: 54..98, w=44)
    draw_card(54, 38, 44, 21, "5", "Synthèse & Ancrage Documentaire",
              ["• Rédaction de la consigne d'atelier guidée par les extraits documentaires",
               "• Evidence Grounding obligatoire : validation Pydantic du schéma de sortie",
               "• Contrôle PC3 : chaque consigne doit citer [document_id, page, figure]",
               "• Tolérance zéro hallucination : vérification de la véracité des références"],
              '#FEF3C7', '#F59E0B', badge="PC3 : EVIDENCE CHECKING", badge_bg='#DC2626')

    # Étape 6 à Gauche (x: 2..46, w=44)
    draw_card(2, 38, 44, 21, "6", "Évaluation de Certitude & Contrôle HITL",
              ["• Analyse des contradictions (ex: versions v1 vs v2 des procédures de frein)",
               "• Évaluation du niveau de confiance de la capture d'image d'atelier",
               "• Préparation conditionnelle du brouillon d'intervention GMAO (MCP)",
               "• Barrière PC2 : l'agent suspend son exécution pour approbation humaine"],
              '#FCE7F3', '#DB2777', badge="PC2 : HITL STOP", badge_bg='#EF4444')

    # Liaison Rangée 2 (Horizontale dégagée de 5 vers 6, gap de 8 units : 46 à 54)
    draw_wire(54, 48.5, 46, 48.5, label="Analyse & État avarie", color='#F59E0B', label_offset=(0, 1.4), label_fs=6.5)

    # ------------------ RANGÉE 3 : Sorties Spécifiques (Bas : y=5..28) ------------------
    # Branche A : Sortie Dégradée (Gauche : x=2..46)
    draw_card(2, 5, 44, 23, "7A", "Sortie Dégradée : Abstention ou Clarification",
              ["• Cas Déclenchant 1 : Photo floue ou témoin lumineux non identifiable",
               "• Cas Déclenchant 2 : Contradiction documentaire non résolue sans certitude",
               "• Cas Déclenchant 3 : Document hors périmètre ou absence de source vérifiée",
               "• Action Système : L'assistant refuse formellement de spéculer ou d'inventer",
               "• Guidance Opérateur : Invitation à reprendre la photo ou saisir le modèle exact"],
              '#FEF2F2', '#DC2626', badge="SÉCURITÉ ATELIER", badge_bg='#B91C1C')

    # Branche B : Sortie Nominale (Droite : x=54..98)
    draw_card(54, 5, 44, 23, "7B", "Sortie Nominale : Diagnostic Sourcé & Action Validée",
              ["• Réponse Certifiée : Procédure officielle de maintenance pas-à-pas",
               "• Citations Formelles : [document_id, page, figure] vérifiables immédiatement",
               "• Affichage Schémas : Visualisation des figures techniques extraites du corpus",
               "• Action Sensible Détectée (ex: hernie pneu) : Présentation du brouillon de ticket",
               "• Clic 'Approuver' Opérateur -> Appel MCP create_ticket() avec jeton cryptographique"],
              '#F0FDF4', '#16A34A', badge="RÉPONSE CERTIFIÉE", badge_bg='#15803D')

    # Flèches de branchement depuis le nœud 6 (Bottom y=38) vers les blocs du bas (Top y=28)
    # Vers 7A (Incertitude / Contradiction)
    draw_wire(18, 38, 18, 28, label="Doute / Flou / Contradiction", color='#DC2626', label_offset=(-7.0, 1.5), label_fs=6.5)

    # Vers 7B (Nominal / Preuves conformes)
    draw_wire(36, 38, 68, 28, label="Preuves vérifiées & diagnostic certain", color='#16A34A', label_offset=(7.5, 1.2), label_fs=6.5)

    plt.tight_layout()
    plt.savefig("docs/diagrammes/flux_requete_rag.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Regenerated clean flux_requete_rag.png")


# =============================================================================
# 4. FLUX MCP : Création de Ticket Sécurisée (HITL & Idempotence)
# =============================================================================
def draw_mcp_flow():
    fig, ax = plt.subplots(figsize=(16, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    ax.text(50, 56, "Workflow Sécurisé de Création de Ticket MCP (Human-in-the-Loop & Idempotence)", 
            ha='center', va='center', fontsize=14.5, fontweight='bold', color='#0F172A')
    ax.text(50, 52.8, "Garantie absolue d'intégrité : barrière d'approbation humaine et protection anti-doublon cryptographique", 
            ha='center', va='center', fontsize=9.2, color='#475569')

    steps = [
        (2, 21, 17.5, 25, "1", "Détection Avarie", 
         ["• Diagnostic formel établi", "• ex: Hernie flanc (PNE-05)", "• Remplacement requis", "• Action sensible identifiée", "• Déclenchement flux MCP"], 
         '#EFF6FF', '#3B82F6'),
        (21.5, 21, 17.5, 25, "2", "Brouillon Pydantic", 
         ["• Formatage structure GMAO", "• Titre, équipement_id", "• Description de l'anomalie", "• Niveau de criticité", "• Statut : PENDING_HUMAN"], 
         '#FEF3C7', '#F59E0B'),
        (41, 21, 18, 25, "3", "Contrôle HITL", 
         ["• Formulaire UI d'atelier", "• Agent suspend son état", "• Vérification opérateur", "• Clic 'Approuver ticket'", "• Modification possible"], 
         '#FEE2E2', '#EF4444', "PC2 : HITL", '#DC2626'),
        (61, 21, 17.5, 25, "4", "Signature & Jeton", 
         ["• Génération approval_token", "• Jeton signé usage unique", "• Clé UUIDv4 idempotence", "• Protection anti-rejeu", "• Validation intégrité payload"], 
         '#F3E8FF', '#9333EA'),
        (80.5, 21, 17.5, 25, "5", "Appel MCP Sécurisé", 
         ["• Exécution create_ticket()", "• Contrôle token serveur", "• Écriture base GMAO", "• Clé d'idempotence vérifiée", "• Retour : TK-2026-xxxx"], 
         '#F0FDF4', '#22C55E')
    ]

    for step in steps:
        x, y, w, h, num, title, lines, c_bg, c_ec = step[:9]
        badge = step[9] if len(step) > 9 else None
        badge_bg = step[10] if len(step) > 10 else '#EF4444'

        # Ombre
        shadow = patches.FancyBboxPatch((x + 0.35, y - 0.35), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                       fc='#CBD5E1', ec='none', alpha=0.35, zorder=1)
        ax.add_patch(shadow)

        # Carte
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                     fc=c_bg, ec=c_ec, lw=1.5, zorder=2)
        ax.add_patch(box)

        # En-tête
        ax.text(x + 1.5, y + h - 2.8, f"{num}. {title}", ha='left', va='center', fontsize=8.6, fontweight='bold', color='#0F172A', zorder=4)

        if badge:
            bw = len(badge) * 0.6 + 2.0
            bx = x + w - bw - 1.2
            by = y + h - 3.8
            b_patch = patches.FancyBboxPatch((bx, by), bw, 2.0, boxstyle="round,pad=0.15,rounding_size=0.5",
                                            fc=badge_bg, ec='none', zorder=5)
            ax.add_patch(b_patch)
            ax.text(bx + bw/2, by + 1.0, badge, ha='center', va='center', fontsize=5.8, fontweight='bold', color='#FFFFFF', zorder=6)

        ax.plot([x + 1.0, x + w - 1.0], [y + h - 4.6, y + h - 4.6], color=c_ec, lw=0.8, alpha=0.5, zorder=3)

        # Contenu
        y_l = y + h - 7.2
        for l in lines:
            ax.text(x + 1.5, y_l, l, ha='left', va='center', fontsize=7.2, color='#334155', zorder=4)
            y_l -= 3.2

    # Flèches horizontales bien espacées
    for i in range(len(steps)-1):
        x1 = steps[i][0] + steps[i][2]
        y1 = steps[i][1] + steps[i][3]/2
        x2 = steps[i+1][0]
        y2 = steps[i+1][1] + steps[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#0F172A', lw=1.6, shrinkA=2, shrinkB=2), zorder=3)

    # Avertissement de sécurité formel
    alert_box = patches.FancyBboxPatch((8, 4), 84, 11, boxstyle="round,pad=0.5,rounding_size=1.0",
                                      fc='#FEF2F2', ec='#DC2626', lw=1.2, zorder=2)
    ax.add_patch(alert_box)
    ax.text(50, 11.5, "GARANTIE DE SÉCURITÉ OPÉRATIONNELLE ABSOLUE (HUMAN-IN-THE-LOOP) :", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#B91C1C')
    ax.text(50, 7.5, "Aucun ticket ne peut être créé de façon autonome par l'IA. Toute modification du contenu textuel invalide le jeton et impose une réapprobation.", 
            ha='center', va='center', fontsize=7.8, color='#7F1D1D')

    plt.tight_layout()
    plt.savefig("docs/diagrammes/flux_creation_ticket_mcp.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Regenerated clean flux_creation_ticket_mcp.png")


if __name__ == "__main__":
    draw_architecture()
    draw_ingestion()
    draw_query_flow()
    draw_mcp_flow()
