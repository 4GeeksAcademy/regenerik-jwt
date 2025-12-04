from flask import Flask, request, jsonify, url_for, Blueprint






adm = Blueprint('adm', __name__)


@adm.route('/get_info')
def get_info():
    return "Hola"