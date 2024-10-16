from flask import Flask, render_template, redirect, request, flash
import json
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PROJETOFLASK'


logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado:
        with open('usuarios.json') as usuarios_temp:
            usuarios = json.load(usuarios_temp)
        return render_template('administrador.html', usuarios=usuarios)
    if not logado:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    global logado
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
                logado = True
                return redirect('/adm')
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template('usuarios.html')
            
            if cont >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect('/')

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            "nome":nome,
            "senha": senha
        }
    ]
    with open('usuarios.json') as usuarios_temp:
        usuarios = json.load(usuarios_temp)
     
    usuario_novo = usuarios + user
        
    with open('usuarios.json', 'w') as gravar_temp:
        json.dump(usuario_novo, gravar_temp, indent=4)
    logado = True
    flash(f'{nome} CADASTRADO!')
    return redirect('/adm')


@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuario_exclusao')
    usuario_dict = ast.literal_eval(usuario)
    nome = usuario_dict['nome']
    with open('usuarios.json') as usuarios_temp:
        usuarios_json = json.load(usuarios_temp)
        for u in usuarios_json:
        # for u in usuarios_json:
            if u == usuario_dict:
                usuarios_json.remove(usuario_dict)
                with open('usuarios.json', 'w') as usuario_excluir:
                    json.dump(usuarios_json, usuario_excluir, indent=4)
    flash(f'{nome} EXCLUIDO')
    return redirect('/adm')


if __name__ in "__main__":
    app.run(debug=True)
