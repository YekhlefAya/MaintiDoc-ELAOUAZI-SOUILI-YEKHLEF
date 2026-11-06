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

## 3. Livrables du Projet

Le Livrable 1 fige l'ensemble des fondations méthodologiques, documentaires et architecturales du projet MaintiDoc :

1. **Rapport d'Ingénierie (`L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf`) :**
   - Document de synthèse exhaustif de 15 pages couvrant le cadrage, le corpus, l'architecture agentique cible, les flux de données, l'analyse des risques (8 risques détaillés) et la planification d'équipe (RACI).
   - Intègre directement les 4 diagrammes d'architecture et de flux en haute définition (300 DPI) avec points de contrôle formels (PC1, PC2, PC3).

2. **Corpus Documentaire Multimodal (`corpus/`) :**
   - **45 documents techniques originaux** au format PDF (23 pour les tableaux de bord, 22 pour les pneumatiques).
   - **40 photographies et figures uniques d'atelier** associées aux fiches techniques.
   - **`inventaire.csv` :** Registre complet normalisé selon les 20 colonnes prescrites.
   - **`prompts_corpus.md` :** Traçabilité exhaustive des prompts P01-P13, relectures d'équipe et analyse critique des hallucinations.

---

## 4. Structure du Dépôt GitHub

Le dépôt Git de l'équipe est accessible à l'enseignante à l'adresse suivante :  
**URL officielle :** https://github.com/YekhlefAya/MaintiDoc-ELAOUAZI-SOUILI-YEKHLEF.git  

Arborescence minimale attendue et respectée :

```text
maintidoc/
├── README.md
├── .gitignore
├── L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf   # Rapport d'ingénierie officiel (15 pages)
└── corpus/
    ├── inventaire.csv                      # Registre d'inventaire complet synchronisé (20 colonnes)
    ├── prompts_corpus.md                   # Historique des prompts P01-P13 et validation critique
    ├── documents/
    │   ├── famille_1/                      # 23 documents PDF (Tableaux de bord)
    │   └── famille_2/                      # 22 documents PDF (Pneumatiques)
    └── images/                             # 40 photographies et figures uniques d'atelier
```

---

## 5. Synthèse des Cas de Test Inclus dans le Corpus

Afin de préparer rigoureusement les évaluations de robustesse des Semaines 2 à 5, notre corpus intègre d'ores et déjà :
- **2 documents contradictoires :** `tdb_05_frein_liquide_v2` (autorise un fluide DOT 5 silicone en conflit mortel avec le DOT 4 de la v1) et `pne_04_usure_pression_v2` (impose une pression uniforme sans contrôle à froid en conflit avec la v1).
- **1 document piégé (Prompt Injection) :** `tdb_note_service_piegee` dissimulant un payload d'évasion de privilèges ("Maintenance Root"), d'exfiltration de données et de contournement de la validation MCP.
- **2 documents scannés authentiques (`pdf_scanne`) :** `tdb_19_fiche_revision_scanne` et `pne_12_fiche_controle_geometrie_scanne` (rasterisés à 150 DPI sans calque texte natif pour évaluer l'OCR local en Semaine 2).
- **40+ documents illustrés :** 100% des documents comportent des figures exploitables (photos de voyants réels et figures d'usures de bandes de roulement).
- **1 cas ambigu étiqueté :** `tdb_09_voyant_pression_pneus_tpms` (pont hybride entre l'électronique de bord et l'avarie physique du pneu).

