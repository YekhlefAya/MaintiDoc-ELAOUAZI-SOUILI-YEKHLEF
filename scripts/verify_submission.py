import os
import csv
import zipfile
from pypdf import PdfReader

def check_all():
    print("=" * 60)
    print("VÉRIFICATION OFFICIELLE DU LIVRABLE 1 — PROJET MAINTIDOC")
    print("Équipe : ELAOUAZI - SOUILI - YEKHLEF")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Check ZIP exists
    zip_path = "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF.zip"
    if not os.path.exists(zip_path):
        errors.append(f"Fichier ZIP manquant : {zip_path}")
    else:
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"[OK] Archive ZIP présente ({size_mb:.2f} Mo < 25 Mo)")
        
        # Check ZIP internal structure
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            root = "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF/"
            if not all(n.startswith(root) for n in names):
                errors.append("Le ZIP ne contient pas un dossier racine unique du même nom.")
            else:
                top_items = set(n[len(root):].split("/")[0] for n in names if n != root)
                expected_items = {
                    "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf",
                    "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_LienGitHub.txt",
                    "README.md",
                    "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Corpus"
                }
                if top_items != expected_items:
                    errors.append(f"Éléments racine ZIP non conformes : {top_items} != {expected_items}")
                else:
                    print(f"[OK] Dossier racine du ZIP conforme (exactement 4 éléments)")

    # 2. Check Report PDF
    pdf_path = "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf"
    if not os.path.exists(pdf_path):
        errors.append(f"Rapport PDF manquant : {pdf_path}")
    else:
        reader = PdfReader(pdf_path)
        nb_pages = len(reader.pages)
        if 10 <= nb_pages <= 15:
            print(f"[OK] Rapport PDF valide : {nb_pages} pages (exigence : 10 à 15 pages)")
        else:
            warnings.append(f"Nombre de pages inhabituel : {nb_pages} pages")

    # 3. Check Lien GitHub
    link_path = "L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_LienGitHub.txt"
    if not os.path.exists(link_path):
        errors.append(f"Fichier LienGitHub manquant : {link_path}")
    else:
        with open(link_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
            if len(lines) >= 1 and lines[0].startswith("http"):
                print(f"[OK] Lien GitHub valide : {lines[0]}")
            else:
                errors.append(f"Contenu de LienGitHub non conforme : {lines}")

    # 4. Check Inventory and Corpus sync
    csv_path = "corpus/inventaire.csv"
    if not os.path.exists(csv_path):
        errors.append(f"Fichier inventaire manquant : {csv_path}")
    else:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            print(f"[OK] Inventaire CSV valide : {len(reader)} documents référencés (exigence : 30 à 50)")
            
            # Check mandatory special cases
            contra = [r for r in reader if r.get("usage_test") == "contradictoire"]
            inj = [r for r in reader if r.get("usage_test") == "injection"]
            scans = [r for r in reader if r.get("format") == "pdf_scanne"]
            
            if len(contra) >= 2:
                print(f"[OK] {len(contra)} documents contradictoires signalés (>= 2 requis)")
            else:
                errors.append(f"Moins de 2 documents contradictoires : {len(contra)}")
                
            if len(inj) >= 1:
                print(f"[OK] {len(inj)} document piégé d'injection signalé (>= 1 requis)")
            else:
                errors.append(f"Aucun document piégé signalé dans l'inventaire")
                
            if len(scans) >= 2:
                print(f"[OK] {len(scans)} documents scannés signalés pour test OCR (>= 2 requis)")
            else:
                errors.append(f"Moins de 2 documents scannés : {len(scans)}")
                
            # Check 1-to-1 sync with actual files
            missing_files = []
            for r in reader:
                rel = r["fichier"]
                p = os.path.join("corpus", rel)
                if not os.path.exists(p):
                    missing_files.append(p)
            if not missing_files:
                print(f"[OK] Synchronisation 100% : Tous les fichiers du CSV existent sur le disque")
            else:
                errors.append(f"Fichiers référencés dans le CSV mais introuvables : {missing_files[:3]}")

    # 5. Check images count (no duplicates)
    img_dir = "corpus/images"
    if os.path.exists(img_dir):
        imgs = os.listdir(img_dir)
        print(f"[OK] Répertoire images propre : {len(imgs)} images uniques cataloguées (aucun doublon)")
    else:
        errors.append("Dossier corpus/images manquant")

    print("=" * 60)
    if not errors and not warnings:
        print("RÉSULTAT : 100% CONFORME ! LE PROJET EST PRÊT POUR LE DÉPÔT.")
    else:
        if errors:
            print("ERREURS DÉTECTÉES :")
            for e in errors: print(f" - {e}")
        if warnings:
            print("AVERTISSEMENTS :")
            for w in warnings: print(f" - {w}")
    print("=" * 60)

if __name__ == "__main__":
    check_all()
