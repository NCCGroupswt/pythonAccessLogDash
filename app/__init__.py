from flask import Flask
import os, sqlite3

app = Flask(__name__)
from app import views
