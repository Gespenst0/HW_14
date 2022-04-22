import sqlite3
from flask import jsonify
from collections import defaultdict


def search_by_title(title_name):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        params = (title_name,)
        sqlite_query = ("SELECT `title`, `country`, `release_year`, `listed_in`, `description` "
                        "FROM netflix "
                        "WHERE `title` = ?")
        cursor.execute(sqlite_query, params)
        result = cursor.fetchall()
    return result


def search_by_date_interval(first_date, second_date):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        if first_date < second_date:
            params = (first_date, second_date)
            sqlite_query = ("select `title`, release_year "
                            "FROM netflix "
                            "WHERE `release_year` BETWEEN ? AND ? AND type = 'Movie'"
                            "ORDER BY `release_year` "
                            "LIMIT 100")
        else:
            params = (second_date, first_date)
            sqlite_query = ("select `title`, release_year "
                            "FROM netflix "
                            "WHERE `release_year` BETWEEN ? AND ? AND `type` = 'Movie'"
                            "ORDER BY `release_year` DESC "
                            "LIMIT 100")
        cursor.execute(sqlite_query, params)
        result = cursor.fetchall()
    return result


def search_by_rating(group):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        if group == "children":
            params = ("G",)
            sqlite_query = ("select `rating`, `title`, `description` "
                            "FROM netflix "
                            "WHERE rating = ? "
                            "ORDER BY `rating`")
        elif group == "family":
            params = ("G", "PG", "PG-13")
            sqlite_query = ("select `rating`, `title`, `description` "
                            "FROM netflix "
                            "WHERE rating = ? OR rating = ? OR rating = ? "
                            "ORDER BY `rating`")
        elif group == "adult":
            params = ("R", "NC")
            sqlite_query = ("select `rating`, `title`, `description` "
                            "FROM netflix "
                            "WHERE rating = ? OR rating = ? "
                            "ORDER BY `rating`")
        cursor.execute(sqlite_query, params)
        result = cursor.fetchall()
        return result


def search_by_genre(genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        params = ("%" + genre + "%",)
        sqlite_query = ("select `title`, listed_in, description "
                        "FROM netflix "
                        "WHERE listed_in LIKE ? "
                        "AND type = 'Movie'"
                        "ORDER BY release_year DESC "
                        "LIMIT 10")
        cursor.execute(sqlite_query, params)
        result = cursor.fetchall()
    return result


def search_by_three_params(type_, release_year, genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        params = (type_, release_year, "%" + genre + "%")
        sqlite_query = ("select `title`, description "
                        "FROM netflix "
                        "WHERE `type` = ? "
                        "AND `release_year` = ? "
                        "AND listed_in LIKE ?  ")
        cursor.execute(sqlite_query, params)
        result = cursor.fetchall()
    data_list = []
    for item in result:
        title, description = item
        result_data = {"title": title, "description": description}
        data_list.append(result_data)
    return jsonify(data_list)


def search_by_duo(first_actor, second_actor):
    d = defaultdict(int)
    result_list = []
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        params = ("%" + first_actor + "%", "%" + second_actor + "%")
        sqlite_query = ("select `show_id`, `title`, `cast`  "
                        "FROM netflix "
                        "WHERE `cast` LIKE ? "
                        "AND `cast` LIKE ? ")
        cur.execute(sqlite_query, params)
        result = cur.fetchall()
    for item in result:
        cast = item[2]
        actors = (cast.split(", "))
        for actor in actors:
            d[actor] += 1
    for item in d:
        if item != first_actor and item != second_actor and d[item] > 2:
            result_list.append(item)
    return result_list
