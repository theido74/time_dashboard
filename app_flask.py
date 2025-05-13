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
    print('temps pas projet',result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)  # Lancer l'application en mode debug

