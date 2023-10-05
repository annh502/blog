import os
import psycopg2
url = "postgresql://postgres:admin@127.0.0.1:5000/project"
connection = psycopg2.connect(url)