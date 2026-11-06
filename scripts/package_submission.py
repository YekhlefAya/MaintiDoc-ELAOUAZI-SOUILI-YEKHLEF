import os
import shutil
import zipfile

TEAM_NAME = "ELAOUAZI-SOUILI-YEKHLEF"
ROOT_DIR_NAME = f"L1_MaintiDoc_{TEAM_NAME}"
ZIP_NAME = f"{ROOT_DIR_NAME}.zip"

# Create temporary packaging directory
if os.path.exists(ROOT_DIR_NAME):
    shutil.rmtree(ROOT_DIR_NAME)

os.makedirs(ROOT_DIR_NAME, exist_ok=True)

# 1. Copy Report
shutil.copy2("L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_Rapport.pdf", os.path.join(ROOT_DIR_NAME, f"{ROOT_DIR_NAME}_Rapport.pdf"))

# 2. Copy LienGitHub.txt
shutil.copy2("L1_MaintiDoc_ELAOUAZI-SOUILI-YEKHLEF_LienGitHub.txt", os.path.join(ROOT_DIR_NAME, f"{ROOT_DIR_NAME}_LienGitHub.txt"))

# 3. Copy README.md
shutil.copy2("README.md", os.path.join(ROOT_DIR_NAME, "README.md"))

# 4. Copy Corpus directory as L1_MaintiDoc_<NomEquipe>_Corpus/
corpus_dest = os.path.join(ROOT_DIR_NAME, f"{ROOT_DIR_NAME}_Corpus")
shutil.copytree("corpus", corpus_dest)

print("Staging directory created successfully.")

# Create the ZIP archive
if os.path.exists(ZIP_NAME):
    os.remove(ZIP_NAME)

with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(ROOT_DIR_NAME):
        for file in files:
            file_path = os.path.join(root, file)
            # Arcname relative to current directory so ROOT_DIR_NAME is preserved as top-level folder
            arcname = os.path.relpath(file_path, start=".")
            zipf.write(file_path, arcname)

print(f"Created ZIP archive: {ZIP_NAME}")

# Verify ZIP structure
print("\nVerifying ZIP archive contents:")
with zipfile.ZipFile(ZIP_NAME, "r") as zipf:
    namelist = zipf.namelist()
    top_level = set(n.split("/")[0] for n in namelist if "/" in n)
    second_level = set(n.split("/")[1] for n in namelist if len(n.split("/")) > 1 and n.split("/")[1])
    print(f"Top-level folder in ZIP: {top_level}")
    print(f"Items in root folder: {second_level}")
    print(f"Total files in ZIP: {len(namelist)}")
    print(f"Archive size: {os.path.getsize(ZIP_NAME) / (1024*1024):.2f} MB")

