from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='templates')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'db_ti'
}

@app.route('/', methods=['GET'])
def formulario():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    user = request.form['user']
    password = request.form['password']

    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    consulta = "INSERT INTO `cadastro` (`user`, `password`) VALUES (%s, %s)"
    valores = (user, password)
    cursor.execute(consulta, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return "Cadastrado com sucesso"

if __name__ == '__main__':
    app.run(debug=True)
