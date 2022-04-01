import json, mysql.connector

class LamConfig():
    cfg = json.loads(open("config.json", "r").read())

    database = mysql.connector.connect(
        host = cfg["db-host"],
        user = cfg["db-username"],
        password = cfg["db-password"],
        database = cfg["db-database"]
    )
