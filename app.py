from flask import Flask, request, jsonify
import requests

hatch_api = "https://api.hatchways.io/assessment/blog/posts"

app = Flask(__name__)

cache = dict()

@app.route("/api/ping", methods=["GET"])
def ping():
    response = requests.get(hatch_api+"?tag=tech")
    if response.status_code == 200:
        return jsonify({"succuss":True}), 200
    else:
        return jsonify({"succuss":False}), 400

@app.route("/api/posts", methods=["GET"])
def posts():

    post_data = request.get_json()
    tags = post_data["tags"]

    if post_data["sortBy"] != None:
        sortBy = post_data["sortBy"]
    else:
        sortBy = "id"

    if post_data["direction"] != None:
        direction = post_data["direction"]
    else: 
        direction = "asc"

    if not tags:
        return jsonify({"error":"Tags parameter is required"}), 400
    
    tags = tags.split(",")
    data = {"posts":[]}
    for t in tags:
        if t in cache.keys():
            for j in cache[t]:
                if j not in data["posts"]:
                    data["posts"].append(j)
        else:
            response = requests.get(hatch_api+"?tag="+t)
            result = response.json()
            cache[t] = result["posts"]
            for i in result["posts"]:
                if i not in data["posts"]:
                    data["posts"].append(i)


    if sortBy != "id" and sortBy != "reads" and sortBy != "likes" and sortBy != "popularity":
        return jsonify({"error":"sortBy parameter is invalid"}), 400
    
    if direction != "desc" and direction != "asc":
        return jsonify({"error":"direction parameter is invalid"}), 400

    if direction == "asc":
        direction = False
    else:
        direction = True

    data["posts"] = sorted(data["posts"], key=lambda x: x[sortBy], reverse=direction)
    
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True)