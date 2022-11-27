# coding:utf-8

from easyops import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask import redirect, url_for

# Create flask application object
easyops = create_app("develop")
manager = Manager(easyops)
Migrate(easyops, db)
manager.add_command("db", MigrateCommand)

@easyops.route("/", methods=["GET"])
def index():
    return redirect(url_for("api_v1_0.login"))

if __name__ == "__main__":
    manager.run()
