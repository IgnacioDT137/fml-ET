from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prediccion", methods=["POST", "GET"])
def prediccion():
    if request.method == "POST":
        #CARGA DEL MODELO
        modelo = pickle.load(open("modelo.pkl", "rb"))

        #ARRAY PREDICTOR
        data = []

        #CAPTURA DE DATOS DEL FORMUALRIO
        mapa = int(request.form["map"])
        gl = int(request.form["gl"])
        gnl = int(request.form["gnl"])
        kills = int(request.form["kills"])
        assists = int(request.form["assists"])
        ace = int(request.form["ace"])
        mvp = int(request.form["mvp"])
        phs = float(request.form["phs"])
        pfk = float(request.form["pfk"])
        dinero = int(request.form["dinero"])
        pdinero = float(request.form["pdinero"])
        total_granadas = gl + gnl
        p_gl = (gl / total_granadas) * 100
        p_gnl = (gnl / total_granadas) * 100

        #AÑADIENDO LOS DATOS AL ARREGLO A PREDECIR
        data.append(mapa)
        data.append(gl)
        data.append(gnl)
        data.append(kills)
        data.append(assists)
        data.append(ace)
        data.append(mvp)
        data.append(phs)
        data.append(pfk)
        data.append(total_granadas)
        data.append(p_gl)
        data.append(p_gnl)
        data.append(dinero)
        data.append(pdinero)

        prediction_raw = modelo.predict([data])[0]
        prediction = ""
        if prediction_raw == 0:
            prediction = "Terrorista"
        elif prediction_raw == 1:
            prediction = "Anti-Terrorista"
        else:
            prediction = "ERROR"

        return render_template("prediccion.html", prediction=prediction)
    elif request.method == "GET":
        prediction = "NO SE HAN RECIBIDO DATOS"
        return render_template("prediccion.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)