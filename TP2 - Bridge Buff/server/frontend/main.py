from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form.get('action1') == 'Procurar um identificador':
            return redirect('/input_sag')
        elif  request.form.get('action2') == 'Max navios afundados':
            return redirect('/max_navios')
        elif  request.form.get('action3') == 'Min navios escapados':
            return redirect('/min_navios')
        else:
            redirect('/')

    elif request.method == 'GET':
        return render_template('index.html',titulo = "Escolha uma das opções abaixo:")

@app.route('/input_sag')
def input_sag():
    return render_template('input_sag.html', titulo = 'Recuperar informações do jogo com um dado identificador')

@app.route('/max_navios')
def max_navios():
    return render_template('max_navios.html', titulo = 'Quantidade de navios afundados')

@app.route('/min_navios')
def min_navios():
    return render_template('min_navios.html', titulo = 'Quantidade de navios escapados')

app.run(debug=True)