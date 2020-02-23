# from app import app
from flask import render_template
from flask import Flask, url_for, flash
from flask import request
from flask import redirect
from collections import deque
from distance_calc import *
from tsp_logic import *
import json

TEMPLATES_AUTO_RELOAD = True
app = Flask(__name__)

coord_list = deque([])
points = []


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/clearcoords", methods=["GET", "POST"])
def clearcoords():
    coord_list.clear()
    return "nothing"


@app.route("/getlatlng", methods=["GET", "POST"])
def getlatlng():
    data = request.form["lat"] + "," + request.form["lng"]
    coord_list.append(data)
    del data
    return "getlatlng finished"


@app.route("/compute_tour", methods=["GET", "POST"])
def compute_tour():
    if len(coord_list) == 0:
        return redirect(url_for("index"))
    else:
        source = ""
        size_coord_list = len(coord_list)
        for i in range(size_coord_list):
            if i != size_coord_list - 1:
                source += coord_list[i] + "|"
            else:
                source += coord_list[i]

        dest = source

        """Stores the data for the problem."""
        data = {}
        try:
            data["distance_matrix"] = get_distance_matrix(source, dest)
            data["num_vehicles"] = 1
            data["depot"] = 0
            optimal_tour = compute_optimal_tour(data)
        except:
            coord_list.clear()
            return redirect(url_for("index"))
        optimal_latlngs = []
        for city in optimal_tour:
            city_latlng = coord_list[city].split(",")
            print(city_latlng)
            opt_latlng_dict = {"lat": city_latlng[0], "lng": city_latlng[1]}
            optimal_latlngs.append(opt_latlng_dict)
            print(optimal_latlngs)

        points = json.dumps(optimal_latlngs)
        print(points)
        return render_template("results.html", points=points)
