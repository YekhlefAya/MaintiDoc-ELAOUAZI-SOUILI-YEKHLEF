import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("docs/diagrammes", exist_ok=True)

# Set global styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Architecture Cible Diagram
def draw_architecture():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background title
    ax.text(50, 96, "Architecture Cible MaintiDoc - Vue Fonctionnelle & Points de Contrôle", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1E293B')
    ax.text(50, 93, "EMSI 2026 | Projet d'IA Générative Multimodale & Agentique | Équipe ELAOUAZI - SOUILI - YEKHLEF", 
            ha='center', va='center', fontsize=10, color='#64748B')

    def draw_box(x, y, w, h, title, subtitle, color_bg, color_border, tag=None):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=1.2,rounding_size=2",
                                     fc=color_bg, ec=color_border, lw=1.8, zorder=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(x + w/2, y + h*0.32, subtitle, ha='center', va='center', fontsize=8, color='#334155', zorder=3)
        if tag:
            tbox = patches.FancyBboxPatch((x + w - 18, y + h - 5), 18, 5, boxstyle="round,pad=0.4,rounding_size=1",
                                          fc='#EF4444' if 'PC' in tag else '#3B82F6', ec='none', zorder=4)
            ax.add_patch(tbox)
            ax.text(x + w - 9, y + h - 2.5, tag, ha='center', va='center', fontsize=6.5, fontweight='bold', color='white', zorder=5)

    def draw_arrow(x1, y1, x2, y2, label=None, color='#475569', rad=0.0):
        connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.8,
                                    connectionstyle=connectionstyle, shrinkA=3, shrinkB=3), zorder=1)
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 1.5, label, ha='center', va='center', fontsize=7.5,
                    fontweight='bold', color=color, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85), zorder=3)

    # Blocks
    # Layer 1: Client
    draw_box(35, 80, 30, 9, "Interface Utilisateur (UI)", "Streamlit / Web App (Photo + Question)", '#EFF6FF', '#3B82F6')

    # Layer 2: API Gateway
    draw_box(35, 64, 30, 9, "Passerelle API (FastAPI)", "Auth JWT, Rate Limiting, Audit Logs", '#F0FDF4', '#22C55E', tag="PC1: Auth")

    # Layer 3: Orchestrator
    draw_box(30, 44, 40, 12, "Orchestrateur Agentique (LangGraph)", "Machine à états, Routage, Human-in-the-Loop", '#FEF3C7', '#F59E0B', tag="PC2: HITL")

    # Side Blocks
    # VLM (Left)
    draw_box(3, 44, 22, 12, "Modèle Vision-Langage", "Qwen2.5-VL-7B (Inférence vLLM)", '#F3E8FF', '#9333EA')

    # MCP Client & Server (Right)
    draw_box(75, 44, 22, 12, "Client & Serveur MCP", "Service Maintenance (Historique / Tickets)", '#FCE7F3', '#DB2777', tag="PC2: Valid")

    # Layer 4: RAG & Storage
    draw_box(8, 16, 38, 16, "Moteur RAG Multimodal & Qdrant", "Embeddings BGE-M3 + SigLIP\nReranker BGE-Reranker-v2", '#E0F2FE', '#0284C7', tag="PC1: RBAC Doc")
    draw_box(54, 16, 38, 16, "Stockage Persistant", "PostgreSQL (Métadonnées & Rôles)\nMinIO Object Storage (PDFs & Images)", '#F1F5F9', '#64748B')

    # Verification Block (Evidence Checker)
    draw_box(32, 2, 36, 8, "Vérificateur de Preuves & Citations", "Validation schéma Pydantic, Grounding Check", '#FEF2F2', '#EF4444', tag="PC3: Citations")

    # Connectors
    draw_arrow(50, 80, 50, 73, "Requête HTTP / Upload")
    draw_arrow(50, 64, 50, 56, "Requête authentifiée")
    draw_arrow(50, 44, 50, 10, "Contrôle citations", rad=0.25)
    draw_arrow(48, 10, 48, 44, "Réponse validée", rad=0.25)

    # LangGraph to VLM
    draw_arrow(30, 51, 25, 51, "Image + Prompt")
    draw_arrow(25, 47, 30, 47, "Description / Extraction")

    # LangGraph to MCP
    draw_arrow(70, 51, 75, 51, "Appel get_history")
    draw_arrow(75, 47, 70, 47, "Historique équipements")

    # LangGraph to RAG
    draw_arrow(40, 44, 30, 32, "Requête filtrée (RBAC)")
    draw_arrow(25, 32, 37, 44, "Passages + Figures pertinents")

    # Storage to RAG
    draw_arrow(54, 24, 46, 24, "Synchronisation vecteurs")

    # Annotation box for Control Points
    cp_box = patches.FancyBboxPatch((3, 76), 28, 17, boxstyle="round,pad=0.8,rounding_size=1",
                                    fc='#FFFBEB', ec='#B45309', lw=1.2)
    ax.add_patch(cp_box)
    ax.text(17, 90, "Points de Contrôle Clés :", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400E')
    ax.text(4.5, 86, "• PC1 (Accès) : Auth FastAPI + Pré-filtrage Qdrant (RBAC)", ha='left', va='center', fontsize=7.2, color='#78350F')
    ax.text(4.5, 82, "• PC2 (Humain) : Approbation obligatoire avant ticket MCP", ha='left', va='center', fontsize=7.2, color='#78350F')
    ax.text(4.5, 78, "• PC3 (Preuves) : Vérification d'existence des citations", ha='left', va='center', fontsize=7.2, color='#78350F')

    plt.tight_layout()
    plt.savefig("docs/diagrammes/architecture_cible.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved architecture_cible.png")

# 2. Ingestion Data Flow
def draw_ingestion():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    ax.text(50, 46, "Flux de Données d'Ingestion Documentaire Multimodale (ETL)", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1E293B')

    steps = [
        (4, 20, 15, 14, "1. Source PDF / Img", "Documents TDB & PNE\n(Originaux)", '#F1F5F9', '#64748B'),
        (23, 20, 16, 14, "2. Analyse & OCR", "PyMuPDF (Textes)\nOCR Surya / Tesseract", '#FEF3C7', '#F59E0B'),
        (43, 20, 16, 14, "3. Découpage", "Passages, Figures\n& Tableaux", '#E0F2FE', '#0284C7'),
        (63, 20, 16, 14, "4. Embeddings", "BGE-M3 (dense/sparse)\nSigLIP (visuel)", '#F3E8FF', '#9333EA'),
        (83, 20, 14, 14, "5. Indexation", "Qdrant Vector DB\n+ MinIO / Postgres", '#F0FDF4', '#22C55E')
    ]

    for x, y, w, h, t, s, c_bg, c_ec in steps:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                                     fc=c_bg, ec=c_ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.65, t, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')
        ax.text(x + w/2, y + h*0.35, s, ha='center', va='center', fontsize=7.5, color='#334155')

    for i in range(len(steps)-1):
        x1 = steps[i][0] + steps[i][2]
        y1 = steps[i][1] + steps[i][3]/2
        x2 = steps[i+1][0]
        y2 = steps[i+1][1] + steps[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#475569', lw=1.6, shrinkA=2, shrinkB=2))

    ax.text(50, 7, "Métadonnées attachées : document_id, version, page, element_id, type_equipement, groupe_acces",
            ha='center', va='center', fontsize=8.5, style='italic', color='#475569',
            bbox=dict(boxstyle='round,pad=0.5', fc='#F8FAFC', ec='#CBD5E1'))

    plt.tight_layout()
    plt.savefig("docs/diagrammes/flux_donnees_ingestion.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved flux_donnees_ingestion.png")

# 3. Query RAG Flow
def draw_query_flow():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    ax.text(50, 56, "Flux d'une Requête Technicien (RAG Sourcé & Multimodal)", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1E293B')

    nodes = [
        (3, 30, 14, 14, "1. Question + Photo", "Technicien connecté\n(Rôle d'atelier)", '#EFF6FF', '#3B82F6'),
        (20, 30, 15, 14, "2. Auth & Droits", "FastAPI vérifie token\n& groupe d'accès", '#F0FDF4', '#22C55E'),
        (38, 30, 16, 14, "3. Analyse VLM", "Qwen2.5-VL décrit\nle voyant / avarie", '#F3E8FF', '#9333EA'),
        (57, 30, 17, 14, "4. Recherche Qdrant", "Filtrage RBAC +\nDense, Sparse, Rerank", '#E0F2FE', '#0284C7'),
        (77, 30, 20, 14, "5. Synthèse & Evidence", "Génération réponse +\nVérification citations", '#FEF3C7', '#F59E0B')
    ]

    for x, y, w, h, t, s, c_bg, c_ec in nodes:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                                     fc=c_bg, ec=c_ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.65, t, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')
        ax.text(x + w/2, y + h*0.35, s, ha='center', va='center', fontsize=7.2, color='#334155')

    for i in range(len(nodes)-1):
        x1 = nodes[i][0] + nodes[i][2]
        y1 = nodes[i][1] + nodes[i][3]/2
        x2 = nodes[i+1][0]
        y2 = nodes[i+1][1] + nodes[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#475569', lw=1.6, shrinkA=2, shrinkB=2))

    # Output boxes (Ambiguity / Response)
    box_ok = patches.FancyBboxPatch((60, 6), 37, 14, boxstyle="round,pad=0.6,rounding_size=1.2",
                                    fc='#DCFCE7', ec='#16A34A', lw=1.4)
    ax.add_patch(box_ok)
    ax.text(78.5, 15, "Sortie Nominale : Réponse Sourcée", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#15803D')
    ax.text(78.5, 9.5, "Affichage des citations [doc_id, page, figure]\n+ Proposition de draft de ticket si avarie confirmée", ha='center', va='center', fontsize=7, color='#166534')

    box_alt = patches.FancyBboxPatch((5, 6), 45, 14, boxstyle="round,pad=0.6,rounding_size=1.2",
                                     fc='#FEF2F2', ec='#DC2626', lw=1.4)
    ax.add_patch(box_alt)
    ax.text(27.5, 15, "Sortie Dégradée : Abstention / Clarification", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#B91C1C')
    ax.text(27.5, 9.5, "Image floue ou documents contradictoires :\nLe système formule une question précise sans inventer", ha='center', va='center', fontsize=7, color='#991B1B')

    # Arrow from node 5 to outputs
    ax.annotate('', xy=(78, 20), xytext=(87, 30),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.5, shrinkA=2, shrinkB=2))
    ax.annotate('', xy=(35, 20), xytext=(83, 30),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.5, shrinkA=2, shrinkB=2, connectionstyle="arc3,rad=-0.2"))

    plt.tight_layout()
    plt.savefig("docs/diagrammes/flux_requete_rag.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved flux_requete_rag.png")

# 4. MCP Ticket Creation Flow
def draw_mcp_flow():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    ax.text(50, 46, "Flux Sécurisé de Création de Ticket MCP (Human-in-the-Loop & Idempotence)", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1E293B')

    steps = [
        (4, 18, 15, 16, "1. Préparation", "MaintiDoc structure\nle brouillon de ticket\n(Titre, desc, équip)", '#EFF6FF', '#3B82F6'),
        (23, 18, 16, 16, "2. Restitution UI", "Affichage à l'écran du\ntechnicien avec bouton\n'Approuver le ticket'", '#FEF3C7', '#F59E0B'),
        (43, 18, 16, 16, "3. Approbation", "Technicien clique\nValidation explicite\n+ Token à usage unique", '#DCFCE7', '#16A34A'),
        (63, 18, 16, 16, "4. Appel MCP", "create_ticket(\n token, idemp_key)\nSécurité & anti-doublon", '#F3E8FF', '#9333EA'),
        (83, 18, 14, 16, "5. Confirmation", "Ticket n° TK-xxxx\nenregistré dans GMAO\n& log d'audit signé", '#F0FDF4', '#22C55E')
    ]

    for x, y, w, h, t, s, c_bg, c_ec in steps:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                                     fc=c_bg, ec=c_ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.7, t, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')
        ax.text(x + w/2, y + h*0.35, s, ha='center', va='center', fontsize=7.2, color='#334155')

    for i in range(len(steps)-1):
        x1 = steps[i][0] + steps[i][2]
        y1 = steps[i][1] + steps[i][3]/2
        x2 = steps[i+1][0]
        y2 = steps[i+1][1] + steps[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#475569', lw=1.6, shrinkA=2, shrinkB=2))

    ax.text(50, 7, "Garantie critique : Aucun ticket n'est créé de façon autonome par l'agent. Toute modification du ticket régénère un token.",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#B91C1C',
            bbox=dict(boxstyle='round,pad=0.5', fc='#FEF2F2', ec='#EF4444'))

    plt.tight_layout()
    plt.savefig("docs/diagrammes/flux_creation_ticket_mcp.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved flux_creation_ticket_mcp.png")

# Also write Mermaid files
def write_mermaid_files():
    mmd_arch = """flowchart TD
    UI["Interface Web (Streamlit)"] -->|Upload Photo + Question| API["Passerelle API (FastAPI)"]
    API -->|Point de Contrôle PC1: Auth & RBAC| ORCH["Orchestrateur (LangGraph)"]
    
    subgraph Core ["Cœur Agentique & Multimodal"]
        ORCH <-->|Extraction visuelle| VLM["Modèle Vision-Langage (Qwen2.5-VL-7B)"]
        ORCH <-->|Recherche textuelle & visuelle| RAG["Moteur RAG (Qdrant + BGE-M3/SigLIP + Reranker)"]
        ORCH <-->|Point de Contrôle PC2: HITL Approbation| MCP["Serveur MCP Maintenance (GMAO)"]
    end
    
    subgraph Storage ["Stockage Persistant"]
        RAG <--> DB["PostgreSQL (Métadonnées & Accès)"]
        RAG <--> S3["MinIO (Documents PDF & Images)"]
    end
    
    ORCH -->|Point de Contrôle PC3: Validation Citations| CHECK["Vérificateur de Preuves (Pydantic)"]
    CHECK -->|Réponse sourcée / Clarification| UI
"""
    with open("docs/diagrammes/architecture_cible.mmd", "w", encoding="utf-8") as f:
        f.write(mmd_arch)

    mmd_ingest = """flowchart LR
    PDF["Documents PDF & Images"] --> SCAN{"PDF Scanné ?"}
    SCAN -->|Oui| OCR["OCR Local (Surya / Tesseract)"]
    SCAN -->|Non| PYM["Extraction PyMuPDF"]
    OCR --> CHUNK["Découpage Sémantique (Passages & Figures)"]
    PYM --> CHUNK
    CHUNK --> EMB["Embeddings BGE-M3 (Texte) + SigLIP (Visuel)"]
    EMB --> QDRANT["Indexation Qdrant (Dense + Sparse + Visuel)"]
    CHUNK --> META["PostgreSQL (Métadonnées RBAC)"]
    PDF --> MINIO["MinIO (Fichiers Originaux)"]
"""
    with open("docs/diagrammes/flux_donnees_ingestion.mmd", "w", encoding="utf-8") as f:
        f.write(mmd_ingest)

    mmd_query = """flowchart LR
    REQ["Question + Photo"] --> AUTH["Auth & Contrôle RBAC"]
    AUTH --> VLM["Analyse Visuelle VLM"]
    VLM --> RET["Recherche Hybride (Qdrant)"]
    RET --> RERANK["Reranking BGE-Reranker-v2"]
    RERANK --> MCP_HIST["Consultation Historique MCP"]
    MCP_HIST --> SYNTH["Génération Réponse Sourcée"]
    SYNTH --> EVAL{"Sources & Citations Valides ?"}
    EVAL -->|Oui| REP["Réponse avec Citations [Doc, Page, Fig]"]
    EVAL -->|Non / Contradiction| CLARIF["Demande de Clarification"]
"""
    with open("docs/diagrammes/flux_requete_rag.mmd", "w", encoding="utf-8") as f:
        f.write(mmd_query)

    mmd_mcp = """flowchart LR
    DIAG["Diagnostic confirmé nécessitant action"] --> DRAFT["Préparation Brouillon de Ticket (Pydantic)"]
    DRAFT --> UI_SHOW["Affichage du Ticket sur l'Interface Technicien"]
    UI_SHOW --> USER_ACT{"Validation Technicien ?"}
    USER_ACT -->|Refus / Modification| MODIF["Révision du brouillon"]
    USER_ACT -->|Approbation explicite| TOKEN["Génération Approval Token & Idempotency Key"]
    TOKEN --> CALL_MCP["Appel MCP create_ticket()"]
    CALL_MCP --> GMAO["Création effective dans le système de maintenance"]
"""
    with open("docs/diagrammes/flux_creation_ticket_mcp.mmd", "w", encoding="utf-8") as f:
        f.write(mmd_mcp)

    print("Mermaid files created in docs/diagrammes/")

if __name__ == "__main__":
    draw_architecture()
    draw_ingestion()
    draw_query_flow()
    draw_mcp_flow()
    write_mermaid_files()

