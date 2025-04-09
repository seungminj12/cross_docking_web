from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

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

# Render 배포용 포트 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
