#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")


#-----------------------------------------------------------
# Creature list page - Show all the creatures
#-----------------------------------------------------------
@app.get("/creatures")
def show_all_creatures():
    with connect_db() as db:
        sql = """
            SELECT id, species, name
            FROM creatures
        """
        params = ()
        creatures = db.execute(sql, params).fetchall()
        
        sql = """
            SELECT DISTINCT species
            FROM creatures
            ORDER BY species asc
        """
        
        params = ()
        species_get = db.execute(sql, params).fetchall()
        species_list = [species['species'] for species in species_get]
        return render_template("pages/creature_list.jinja", creatures=creatures, species_list=species_list)


#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")

#-----------------------------------------------------------
# Search route
#-----------------------------------------------------------
@app.get("/search")
def process_search():
    search_term = request.args.get('q', '')
    search_match = f"%{search_term}%"

    species = request.form.get(species)

    with connect_db() as db:
        sql = """
            SELECT id, species, name
            FROM creatures
            WHERE name LIKE ? AND species LIKE ?
        """
        params = (search_match, species)
        creatures = db.execute(sql, params).fetchall()

        sql = """
            SELECT DISTINCT species
            FROM creatures
            ORDER BY species asc
        """
        
        params = ()
        species_get = db.execute(sql, params).fetchall()
        species_list = [species['species'] for species in species_get]
        return render_template("pages/creature_list.jinja", creatures=creatures, search_term=search_term, species_list=species_list)

#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

