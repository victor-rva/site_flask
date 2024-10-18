from flask import Flask, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os
import mysql.connector

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
        connect_db = mysql.connector.connect(
        host='localhost',
        database='usuarios',
        user='root',
        password='' )
        
        if connect_db.is_connected():
            cursor = connect_db.cursor()
            cursor.execute('SELECT * FROM usuarios.usuario;')
            usuarios = cursor.fetchall()
            
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

    try:
        connect_db = mysql.connector.connect(
            host='localhost',
            database='usuarios',
            user='root',
            password='' 
        )
        
        if connect_db.is_connected():
            print('Conectado ao banco de dados')

            cursor = connect_db.cursor()

            query = "SELECT * FROM usuarios.usuario WHERE nome=%s AND senha=%s"
            cursor.execute(query, (nome, senha))
            usuario = cursor.fetchone()

            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')
            
            if usuario:
                logado = True
                return redirect('/usuarios')

            flash('Usuário ou senha inválidos')
            return redirect('/')

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        flash('Erro ao conectar ao banco de dados')
        return redirect('/')
    
    finally:
        if connect_db.is_connected():
            cursor.close()
            connect_db.close()
            print("Conexão com o MySQL foi encerrada.")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    connect_db = mysql.connector.connect(
                host='localhost',
                database='usuarios',
                user='root',
                password='' 
            )
    
    if connect_db.is_connected():
        cursor = connect_db.cursor()

        query = "INSERT INTO usuarios.usuario (nome, senha) VALUES (%s, %s);"
        cursor.execute(query, (nome, senha))
        flash(f'{nome} CADASTRADO!')
    if connect_db.is_connected():
        cursor.close()
        connect_db.close()

    logado = True
    return redirect('/adm')


@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    nome = request.form.get('nome')
    usuario_id = request.form.get('usuario_exclusao')
    connect_db = mysql.connector.connect(
                host='localhost',
                database='usuarios',
                user='root',
                password='' 
            )
    
    if connect_db.is_connected():
        cursor = connect_db.cursor()
        cursor.execute(f"DELETE FROM usuarios.usuario WHERE id='{usuario_id};")

        flash(f'{nome} EXCLUIDO')
    if connect_db.is_connected():
        cursor.close()
        connect_db.close()
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
