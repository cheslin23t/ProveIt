from flask import render_template, Blueprint, session, redirect, request
from dotenv import load_dotenv
import os
load_dotenv()
import mysql.connector

mydb = mysql.connector.connect(
  host=os.getenv('dbhost'),
  user=os.getenv('dbuser'),
  password=os.getenv('dbpassword'),
  database=os.getenv('database')
)
