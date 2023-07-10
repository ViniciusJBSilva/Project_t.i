from flask import Flask, render_template, request, redirect
import mysql.connector
import json
import shutil
from gmplot import *
import datetime
from geopy.distance import geodesic
import requests
from marshmallow import Schema, fields


app = Flask(__name__, template_folder='templates')

loginwr = "preencher"
passwordwr = "preencher"


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'db_ti'
}

#renderização das html vini

@app.route('/', methods=['GET'])
def exibir_login():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET'])
def exibir_cadastro():
    return render_template('cadastro.html')


@app.route('/cadastrook', methods=['GET'])
def exibit_cadastro_feito():
    return render_template('cadastrook.html')


@app.route('/map', methods=['GET'])
def exibir_map():
    return render_template('map.html')


@app.route('/posicao', methods=['GET'])
def exibir_posicao():
    return render_template('posicao.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():
    user = request.form['user']
    password = request.form['password']

    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    consulta = "SELECT * FROM cadastro WHERE user = %s"
    valores = (user,)
    cursor.execute(consulta, valores)
    resultado = cursor.fetchone()

    if resultado:
        error1= "Nome de usuario ja cadastrado em sistema!"
        return render_template('cadastro.html', error1=error1)
    
    else:
        insercao = "INSERT INTO `cadastro` (`user`, `password`) VALUES (%s, %s)"
        valores = (user, password)
        cursor.execute(insercao, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        ok = "Cadastro efetuado com sucesso!"

    
        return render_template('cadastro.html', ok=ok)



@app.route('/login', methods=['GET', 'POST'])
def login():
        user = request.form['user']
        password = request.form['password']

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        consulta = "SELECT * FROM `cadastro` WHERE `user` = %s AND `password` = %s"
        valores = (user, password)
        cursor.execute(consulta, valores)
        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        if resultado:
            return redirect('/posicao')
        else:
            error2 = 'Usuário ou senha incorretos'
        
            return render_template("login.html", error2=error2)
        


@app.route('/posicao', methods=['GET', 'POST'])
def posi():
    with open('position.json') as file:
        data = json.load(file)

    latitudes = [float(item['latitude']) for item in data['data']]
    longitudes = [float(item['longitude']) for item in data['data']]

    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], zoom=12)
    
    for item in data['data']:
        ignition_state = item['ignition_state']
        ignition_text = "Desligada" if ignition_state == 0 else "Ligada"
        date_time_utc = item['date_time']
        date_time_obj = datetime.datetime.fromisoformat(date_time_utc)
        time_brasilia = datetime.timezone(datetime.timedelta(hours=-3))
        date_time_brasilia = date_time_obj.astimezone(time_brasilia)
        formato_date_vehicle_brasilia = date_time_brasilia.strftime("%d/%m/%Y - %H:%M:%S")
        latitude = float(item['latitude'])
        longitude = float(item['longitude'])
        info_box = "<dl><dt style='text-align: center;'><strong>Placa</strong></dt><dd><dt style='text-align: center;'>{}</dt></dd><dt><dt style='text-align: center;'><strong>Ignicao</strong></dt><dd><dt style='text-align: center;'>{}</dt></dd><dt><dt style='text-align: center;'><strong>Velocidade</strong></dt><dd><dt style='text-align: center;'>{} km </dt></dd><dt><dt style='text-align: center;'><strong>Data</strong></dt><dd><dt style='text-align: center;'>{}</dd></dl>".format(item['vehicle']['plate'], ignition_text,item['speed'], formato_date_vehicle_brasilia )
        gmap.marker(latitude, longitude, title=item['vehicle']['plate'], info_window=info_box)

    gmap.plot(latitudes, longitudes, 'blue', edge_width=2.5)
    

    output_file = 'map.html'
    gmap.draw(output_file)

    destination_folder = 'templates/'
    shutil.move(output_file, destination_folder + output_file)
    return render_template("posicao.html")





@app.route('/search', methods=['GET', 'POST'])
def search():
    placa = request.form['placa']

    data = {"username":loginwr, "password": passwordwr, "realm": "G"}
    session = requests.Session()
    result = session.post('https://api.webrota.com.br/auth/login/', data=data)
    session.cookies['wrauth-access'] = result.json()['access_token']
    wr_result = session.get('https://api.webrota.com.br/vehicle/?visible=2&plate='+ placa +'&includes=customer,device,vehicle_model,vehicle_model.vehicle_model_manufacturer,fuel_category,fleet,vehicle_color,vehicle_category,licenses')
    wr_result = wr_result.json()['data']

    

    if wr_result:
        id = wr_result[0]['id']
        return redirect('/posicao/' + str(id))
    else:
        novehicle = 'Veículo não encontrado.'
        return render_template("posicao.html", novehicle=novehicle)





class InfoSchema(Schema):
    vehicle = fields.Str()
    speed = fields.Int()
    date_time = fields.DateTime()
    ignition = fields.Int()
    latitude = fields.Float()
    longitude = fields.Float()



def search2(id):
    data = {"username": loginwr, "password": passwordwr, "realm": "G"}
    session = requests.Session()
    result = session.post('https://api.webrota.com.br/auth/login/', data=data)
    session.cookies['wrauth-access'] = result.json()['access_token']
    wr_result = session.get('https://api.webrota.com.br/position/?begin_date=2023-07-03T03:00:00.000Z&end_date=2023-07-04T02:59:00.000Z&vehicles_id=%5B'+ id +'%5D&includes=vehicle,point_of_interest,virtual_area,packet_reason,driver')
    wr_result = wr_result.json()['data']
    
    results = []
    
    for result in wr_result:
        vehicle = result['vehicle']['plate']
        speed = result['speed']
        date_time = datetime.datetime.strptime(result['date_time'], "%Y-%m-%dT%H:%M:%S+00:00")
        ignition = result['ignition_state']
        latitudefe = result['latitude']
        longitudefe = result['longitude']
        
        results.append({
            "vehicle": vehicle,
            "speed": speed,
            "date_time": date_time,
            "ignition": ignition,
            "latitude": latitudefe,
            "longitude": longitudefe
        })
        
    return results


def create_json(id, results):
    results=search2(id)
    schema = InfoSchema(many=True)
    json_output = schema.dumps(results)
    with open('positionsearch.json', 'w') as f:
        f.write(json_output)

    return posis()
    




@app.route('/posicao/<id>', methods=['GET', 'POST'])
def posi3(id):
    results = search2(id)
    return create_json(id, results)







def posis():
    with open('positionsearch.json') as file:
        data = json.load(file)

    latitudes = [float(item['latitude']) for item in data]
    longitudes = [float(item['longitude']) for item in data]

   

    if not latitudes or not longitudes:
        noresult = "Não existe rastro para este veículo!"
        return render_template("posicao.html", noresult=noresult)
    
   

    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], zoom=12)
    
    for item in data:
        ignition_state = item['ignition']
        ignition_text = "Desligada" if ignition_state == 0 else "Ligada"
        date_time_utc = item['date_time']
        date_time_obj = datetime.datetime.fromisoformat(date_time_utc)
        time_brasilia = datetime.timezone(datetime.timedelta(hours=-3))
        date_time_brasilia = date_time_obj.astimezone(time_brasilia)
        formato_date_vehicle_brasilia = date_time_brasilia.strftime("%d/%m/%Y - %H:%M:%S")
        latitude = float(item['latitude'])
        longitude = float(item['longitude'])
        info_box = "<dl><dt style='text-align: center;'><strong>Placa</strong></dt><dd><dt style='text-align: center;'>{}</dt></dd><dt><dt style='text-align: center;'><strong>Ignicao</strong></dt><dd><dt style='text-align: center;'>{}</dt></dd><dt><dt style='text-align: center;'><strong>Velocidade</strong></dt><dd><dt style='text-align: center;'>{} km </dt></dd><dt><dt style='text-align: center;'><strong>Data</strong></dt><dd><dt style='text-align: center;'>{}</dd></dl>".format(item['vehicle'], ignition_text, item['speed'], formato_date_vehicle_brasilia)
        gmap.marker(latitude, longitude, title=item['vehicle'], info_window=info_box)

    gmap.plot(latitudes, longitudes, 'blue', edge_width=2.5)
    

    output_file = 'map.html'
    gmap.draw(output_file)

    destination_folder = 'templates/'
    shutil.move(output_file, destination_folder + output_file)
    
    


    return render_template("posicao.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    

        



