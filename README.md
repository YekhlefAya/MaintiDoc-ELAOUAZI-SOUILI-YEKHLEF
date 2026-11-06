# Projet MaintiDoc — Livrable 1 : Cadrage, Corpus et Architecture

**Module :** IA Générative Multimodale (EMSI — Promotion 2026)  
**Enseignante :** Pr. Mariam CHERRABI  
**Équipe :** `ELAOUAZI-SOUILI-YEKHLEF`  
- **ELAOUAZI Hafsa** (hafsa.elaouazi@emsi-edu.ma) — Lead Évaluation, Sécurité & Gestion du Corpus
- **SOUILI Wiam** (wiam.souili@emsi-edu.ma) — Lead Architecture & Intégration Agentique
- **YEKHLEF Aya** (aya.yekhlef@emsi-edu.ma) — Lead RAG Multimodal & Recherche Vectorielle

---

## 1. Objectif du Projet

**MaintiDoc** est un assistant documentaire multimodal et agentique conçu pour assister les techniciens et responsables de maintenance automobile lors de leurs interventions d'atelier et de terrain. Le système permet :
- L'analyse conjointe de requêtes textuelles et d'images (photographies de témoins au tableau de bord, combinés d'instruments, avaries ou usures pneumatiques).
- Une recherche documentaire hybride et multimodale hautement précise et sourcée (citant systématiquement l'identifiant du document, la page exacte et la figure associée).
- L'interfaçage agentique sécurisé avec la GMAO d'atelier via le protocole standardisé **MCP (Model Context Protocol)** pour consulter l'historique d'un équipement (`get_equipment_history`) et préparer des ordres de réparation (`create_ticket`).
- Une gouvernance stricte de la sécurité et des actions sensibles : aucun ticket n'est créé sans approbation humaine explicite (*Human-in-the-Loop*) avec clé d'idempotence, contrôle d'accès documentaire granulaire (RBAC) et résistance aux injections indirectes de prompt.

---

## 2. Familles d'Équipements Retenues

1. **Tableaux de Bord (`tableaux_de_bord`) :** Témoins d'alerte critiques (rouge), avertisseurs de maintenance (ambre/orange), combinés d'instruments, calculateurs et systèmes de surveillance électronique (TPMS, ABS, ESP, SRS, FAP, AdBlue, injection).
2. **Pneumatiques (`pneumatiques`) :** Avaries physiques de bande de roulement, flancs, talons et carcasses (crevaisons clou/vis, hernies, décollements, craquelures, usures anormales par sous-gonflage ou défaut de géométrie 3D).

---

## 3. Contenu de l'Archive de Rendu (`L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF.zip`)

Conformément aux consignes formelles du Livrable 1, l'archive contient un dossier unique racine nommé `L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF/` renfermant exactement les 4 éléments suivants :

```text
L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF.zip
└── L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF/
    ├── L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf    # Rapport complet (10 à 15 pages hors annexes, sections 2.1 à 2.6)
    ├── L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_LienGitHub.txt  # Fichier texte contenant l'URL officielle du dépôt Git
    ├── README.md                                           # Le présent document de synthèse
    └── L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Corpus/       # Corpus documentaire complet (45 documents)
        ├── inventaire.csv                                 # Inventaire exhaustif normalisé (UTF-8, 20 colonnes)
        ├── prompts_corpus.md                              # Traçabilité des prompts P01-P13, relectures et analyse critique
        ├── documents/
        │   ├── famille_1/                                 # 23 documents PDF (Tableaux de bord, dont 1 piégé, 1 scanné, 1 contradictoire)
        │   └── famille_2/                                 # 22 documents PDF (Pneumatiques, dont 1 scanné, 1 contradictoire)
        └── images/                                        # 40 photographies et figures uniques cataloguées (1 par fiche)
```

---

## 4. Structure du Dépôt GitHub

Le dépôt Git de l'équipe est accessible à l'enseignante à l'adresse suivante :  
**URL officielle :** https://github.com/YekhlefAya/MaintiDoc-ELAOUAZI-SOUILI-YEKHLEF.git  

Arborescence minimale attendue et respectée :

```text
maintidoc/
├── README.md
├── .gitignore
├── docs/
│   └── diagrammes/
│       ├── architecture_cible.mmd          # Source Mermaid de l'architecture fonctionnelle
│       ├── architecture_cible.png          # Rendu haute définition (300 DPI)
│       ├── flux_donnees_ingestion.mmd      # Source Mermaid du pipeline ETL multimodal
│       ├── flux_donnees_ingestion.png      # Schéma haute définition du flux d'ingestion
│       ├── flux_requete_rag.mmd            # Source Mermaid du parcours de requête
│       ├── flux_requete_rag.png            # Schéma haute définition du flux RAG
│       ├── flux_creation_ticket_mcp.mmd    # Source Mermaid du workflow MCP sécurisé
│       └── flux_creation_ticket_mcp.png    # Schéma haute définition du Human-in-the-Loop
└── corpus/
    ├── inventaire.csv                      # Registre d'inventaire complet synchronisé
    ├── prompts_corpus.md                   # Historique des prompts et validation critique
    ├── documents/
    │   ├── famille_1/                      # Documents Tableaux de bord
    │   └── famille_2/                      # Documents Pneumatiques
    └── images/                             # Banque d'images associées aux documents
```

---

## 5. Synthèse des Cas de Test Inclus dans le Corpus

Afin de préparer rigoureusement les évaluations de robustesse des Semaines 2 à 5, notre corpus intègre d'ores et déjà :
- **2 documents contradictoires :** `tdb_05_frein_liquide_v2` (autorise un fluide DOT 5 silicone en conflit mortel avec le DOT 4 de la v1) et `pne_04_usure_pression_v2` (impose une pression uniforme sans contrôle à froid en conflit avec la v1).
- **1 document piégé (Prompt Injection) :** `tdb_note_service_piegee` dissimulant un payload d'évasion de privilèges ("Maintenance Root"), d'exfiltration de données et de contournement de la validation MCP.
- **2 documents scannés authentiques (`pdf_scanne`) :** `tdb_19_fiche_revision_scanne` et `pne_12_fiche_controle_geometrie_scanne` (rasterisés à 150 DPI sans calque texte natif pour évaluer l'OCR local en Semaine 2).
- **40+ documents illustrés :** 100% des documents comportent des figures exploitables (photos de voyants réels et figures d'usures de bandes de roulement).
- **1 cas ambigu étiqueté :** `tdb_09_voyant_pression_pneus_tpms` (pont hybride entre l'électronique de bord et l'avarie physique du pneu).

