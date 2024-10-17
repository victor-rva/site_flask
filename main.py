from flask import Flask, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os

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

@app.route('/usuarios')
def usuarios():
    if logado:
        arquivo = []
        for documento in os.listdir('./arquivos'):
            arquivo.append(documento)
        return render_template('usuarios.html', arquivos=arquivo)
    else:
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
                logado = True
                return redirect('/usuarios')
            
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


@app.route('/upload', methods=['POST'])
def upload():
    global logado
    logado = True
    
    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(' ', '-')
    arquivo.save(os.path.join('./arquivos', nome_arquivo))
    
    flash('Arquivo salvo')
    return redirect('/adm')

@app.route('/download', methods=['POST'])
def download():
    nome_arquivo = request.form.get('arquivos_download')
    return send_from_directory('./arquivos', nome_arquivo, as_attachment=True)

if __name__ in "__main__":
    app.run(debug=True)
