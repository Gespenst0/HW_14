from flask import Flask, jsonify
import json
import utils
app = Flask(__name__)



@app.route("/movie/<title_name>")
def movie_title(title_name):
    result = utils.search_by_title(title_name)
    title, country, release_year, listed_in, description = result[0]
    result_data = {"title":title, "country":country, "release_year":release_year, "genre":listed_in, "description":description}
    return result_data


@app.route("/movie/<int:first_year>/to/<int:second_year>")
def year_interval(first_year, second_year):
    result = utils.search_by_date_interval(first_year, second_year)
    data_list = []
    for item in result:
        title, release_year = item
        result_data = {"title": title, "release_year": release_year}
        data_list.append(result_data)
        a = json.dumps(data_list)
    return jsonify(a)


@app.route("/rating/<group>")
def age_group(group):
    res = utils.search_by_rating(group)
    data_list = []
    for item in res:
        title, rating, description = item
        result_data = {"title": title, "rating": rating, "description": description}
        data_list.append(result_data)
        a = json.dumps(data_list)
    return jsonify(a)


@app.route("/movie/genre/<genre>")
def movie_genre(genre):
    result = utils.search_by_genre(genre)
    data_list = []
    for item in result:
        title, listed_in, description = item
        result_data = {"title":title, "genre":listed_in, "description":description}
        data_list.append(result_data)
        a = json.dumps(data_list)
    return jsonify(a)


if __name__ == '__main__':
    app.run()

