import os
import csv
from pypdf import PdfReader

def run_preview():
    print("=" * 60)
    print("PRÉVISUALISATION DU PIPELINE D'INGESTION — SEMAINE 2")
    print("=" * 60)
    
    csv_path = os.path.join("corpus", "inventaire.csv")
    with open(csv_path, "r", encoding="utf-8") as f:
        inventory = list(csv.DictReader(f))
        
    print(f"Total documents dans l'inventaire : {len(inventory)}")
    
    scanned_docs = []
    text_chunks = []
    
    for doc in inventory:
        doc_id = doc["document_id"]
        rel_path = doc["fichier"]
        full_path = os.path.join("corpus", rel_path)
        
        # Identification des formats scannés nécessitant OCR
        if doc["format"] == "pdf_scanne":
            scanned_docs.append(doc_id)
            continue
            
        reader = PdfReader(full_path)
        for pno, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            # Simulation d'un chunking par section / paragraphe
            sections = [s.strip() for s in text.split("\n\n") if len(s.strip()) > 50]
            for s_idx, sec in enumerate(sections, start=1):
                text_chunks.append({
                    "chunk_id": f"{doc_id}_p{pno}_c{s_idx}",
                    "document_id": doc_id,
                    "page": pno,
                    "famille": doc["famille_equipement"],
                    "groupes_acces": [g.strip() for g in doc["groupe_acces"].split(";")],
                    "usage_test": doc["usage_test"],
                    "sample": sec[:80].replace("\n", " ") + "..."
                })
                
    print(f"\n[1] Documents texte ingérés : {len(inventory) - len(scanned_docs)}")
    print(f"    -> Total chunks textuels extraits : {len(text_chunks)}")
    print(f"[2] Documents scannés (en attente OCR local) : {len(scanned_docs)}")
    for s in scanned_docs:
        print(f"    - {s}")
        
    print("\nExemple de structure d'un chunk prêt pour Qdrant :")
    sample = text_chunks[0]
    print(f"  Chunk ID : {sample['chunk_id']}")
    print(f"  Document : {sample['document_id']} (Page {sample['page']})")
    print(f"  Famille  : {sample['famille']}")
    print(f"  RBAC     : {sample['groupes_acces']}")
    print(f"  Extrait  : {sample['sample']}")
    print("=" * 60)
    print("Pipeline d'ingestion prêt pour l'intégration Qdrant en Semaine 2.")
    print("=" * 60)

if __name__ == "__main__":
    run_preview()

