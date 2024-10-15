from flask import Flask, render_template, redirect, request, flash
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PROJETOFLASK'


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/adm')


@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    
    # melhorar a lógica 
    with open('usuarios.json') as usuarios_temp:
        usuarios = json.load(usuarios_temp)
        cont = 0
        for usuario in usuarios:
            cont += 1
            # fazer o admin por arquivo json
            if nome == 'adm' and senha == '000':
                return redirect|('/adm')
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template('usuarios.html')
            
            if cont >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect('/')


if __name__ in "__main__":
    app.run(debug=True)
