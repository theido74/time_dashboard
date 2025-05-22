from flask import Flask, render_template, jsonify
import analyse_csv

df = analyse_csv.df
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/statistiques')
def statistiques():
    return render_template('statistiques.html')

@app.route('/temps_total', methods=['GET'])
def get_temps_total():
    result = analyse_csv.temps_total_user()
    return jsonify(result)

@app.route('/top_5', methods=['GET'])
def get_top_5():
    result = analyse_csv.top_5()
    return jsonify(result)

@app.route('/temps_par_projet', methods=['GET'])
def get_temps_par_projet():
    result = analyse_csv.temps_par_projet_et_user(fichier_utilisateurs='utilisateurs_mac.csv')
    return jsonify(result)

@app.route('/TOP_app',methods=['GET'])
def get_top_app():
    result = analyse_csv.find_by_program()
    return jsonify(result)

@app.route('/TOP_folder', methods=['GET'])
def get_top_folder():
    result = analyse_csv.find_directory()
    return jsonify(result)

@app.route('/last_24h', methods=['GET'])
def last_24h():
    result = analyse_csv._24h()
    return jsonify(result)


@app.route('/mois/<mois_choisi>')
def afficher_mois(mois_choisi):
    result = analyse_csv.mois(mois_choisi)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

