# coding=utf-8
from flask import Blueprint

demo_blue = Blueprint('demo', __name__)
from .demo import *
