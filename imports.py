
#project urgent
from __future__ import print_function
import os
import json
import yaml
import warnings
import requests
import random
import numpy as np
from decouple import config
from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging, jsonify, Response
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SubmitField, ValidationError
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mail import Mail, Message




import hug
from tinydb import TinyDB, where
from understanding.tasks import understand_recording

from flask import Flask, render_template
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop