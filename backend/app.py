from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/get_pdbs", methods=["GET"])
def get_pdbs():
    uniprot_id = request.args.get("uniprot_id")
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_polymer_entity_container_identifiers.uniprot_ids.value",
                "operator": "exact_match",
                "value": uniprot_id
            }
        },
        "return_type": "entry"
    }
    res = requests.post("https://search.rcsb.org/rcsbsearch/v1/query", json=query)
    pdb_ids = [r["identifier"] for r in res.json().get("result_set", [])]
    return jsonify(pdb_ids)

@app.route("/download_pdb", methods=["GET"])
def download_pdb():
    pdb_id = request.args.get("pdb_id").upper()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    file_path = os.path.join(DOWNLOAD_DIR, f"{pdb_id}.pdb")

    res = requests.get(url)
    if res.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(res.content)
        return send_file(file_path, as_attachment=True)
    else:
        return "Download failed", 404

@app.route("/download_sdf", methods=["GET"])
def download_sdf():
    ligand_id = request.args.get("ligand_id")
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{ligand_id}/SDF"
    file_path = os.path.join(DOWNLOAD_DIR, f"{ligand_id}.sdf")

    res = requests.get(url)
    if res.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(res.content)
        return send_file(file_path, as_attachment=True)
    else:
        return "Download failed", 404

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 내부에서 제공하는 포트 사용
    app.run(host="0.0.0.0", port=port)