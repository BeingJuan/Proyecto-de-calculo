from flask import Flask, render_template, request, jsonify, session
import json
import os
import base64
from datetime import datetime
import uuid

app = Flask(__name__, template_folder='templates')
app.secret_key = 'ecoapp_secret_key_2024'


@app.context_processor
def inject_user():
    return dict(user=users_db['demo_user'])


reports_db = []
users_db = {
    'demo_user': {
        'name': 'Alejandro Alzate',
        'points': 2340,
        'level': 'Eco Guardián',
        'avatar': '🌿',
        'joined': '2024-01-15',
        'recycled_kg': 47.5,
        'reports': 12
    }
}

recycling_points = [

    {'id': 1,  'name': 'EcoPunto Boyacá',        'lat': 3.4800, 'lng': -76.5200, 'address': 'Barrio Boyacá, Cali',
        'hours': 'Lun-Sab 7am-6pm',  'types': ['Orgánicos', 'Aprovechables']},
    {'id': 2,  'name': 'Punto Verde Calimío',     'lat': 3.4720, 'lng': -76.5350, 'address': 'Barrio Calimío, Cali',
        'hours': 'Lun-Vie 8am-5pm',  'types': ['Industriales', 'Aprovechables']},
    {'id': 3,  'name': 'EcoReciclaje Chipichape', 'lat': 3.4650, 'lng': -76.5120,
        'address': 'Sector Chipichape, Cali',      'hours': 'Mar-Dom 9am-7pm',  'types': ['Aprovechables', 'Peligrosos']},

    {'id': 4,  'name': 'Punto Limpio Salomia',    'lat': 3.4700, 'lng': -76.5050, 'address': 'Barrio Salomia, Cali',
        'hours': 'Lun-Dom 7am-8pm',  'types': ['Orgánicos', 'Aprovechables']},
    {'id': 5,  'name': 'EcoPunto Quintas',        'lat': 3.4580, 'lng': -76.4980,
        'address': 'Quintas de Don Simón, Cali',   'hours': 'Lun-Sab 8am-6pm',  'types': ['Industriales', 'Peligrosos']},

    {'id': 6,  'name': 'Centro Verde Petecuy',    'lat': 3.4760, 'lng': -76.5480, 'address': 'Barrio Petecuy, Cali',
        'hours': 'Lun-Vie 7am-5pm',  'types': ['Orgánicos', 'Aprovechables']},
    {'id': 7,  'name': 'EcoPunto Unidad Dep.',    'lat': 3.4630, 'lng': -76.5550, 'address': 'Unidad Deportiva, Cali',
        'hours': 'Mar-Dom 8am-6pm',  'types': ['Aprovechables', 'Industriales']},

    {'id': 8,  'name': 'Punto Verde Granada',     'lat': 3.4480, 'lng': -76.5290,
        'address': 'Barrio Granada, Cali',         'hours': 'Lun-Dom 7am-8pm',  'types': ['Todos los residuos']},
    {'id': 9,  'name': 'EcoCenter San Antonio',   'lat': 3.4430, 'lng': -76.5370,
        'address': 'Barrio San Antonio, Cali',     'hours': 'Lun-Sab 8am-6pm',  'types': ['Aprovechables', 'Peligrosos']},
    {'id': 10, 'name': 'Punto Limpio El Peñón',   'lat': 3.4390, 'lng': -76.5430, 'address': 'Barrio El Peñón, Cali',
        'hours': 'Mar-Dom 9am-7pm',  'types': ['Orgánicos', 'Aprovechables']},

    {'id': 11, 'name': 'EcoPunto Laureles',       'lat': 3.4600, 'lng': -76.5620,
        'address': 'Barrio Laureles, Cali',        'hours': 'Lun-Dom 7am-8pm',  'types': ['Todos los residuos']},
    {'id': 12, 'name': 'Punto Verde Normandía',   'lat': 3.4520, 'lng': -76.5700, 'address': 'Barrio Normandía, Cali',
        'hours': 'Lun-Sab 8am-5pm',  'types': ['Industriales', 'Aprovechables']},
    {'id': 13, 'name': 'EcoReciclaje La Flora',   'lat': 3.4350, 'lng': -76.5580,
        'address': 'Barrio La Flora, Cali',        'hours': 'Mar-Dom 9am-6pm',  'types': ['Orgánicos', 'Peligrosos']},

    {'id': 14, 'name': 'EcoPunto El Ingenio',     'lat': 3.3850, 'lng': -76.5380, 'address': 'Barrio El Ingenio, Cali',
        'hours': 'Lun-Sab 7am-6pm',  'types': ['Aprovechables', 'Industriales']},
    {'id': 15, 'name': 'Punto Verde Ciudad Jard.', 'lat': 3.3950, 'lng': -76.5450, 'address': 'Ciudad Jardín, Cali',
        'hours': 'Lun-Dom 8am-7pm',  'types': ['Orgánicos', 'Aprovechables']},
    {'id': 16, 'name': 'EcoCenter Pance',         'lat': 3.3700, 'lng': -76.5500, 'address': 'Sector Pance, Cali',
        'hours': 'Lun-Vie 7am-5pm',  'types': ['Peligrosos', 'Industriales']},

    {'id': 17, 'name': 'Punto Limpio Meléndez',   'lat': 3.3780, 'lng': -76.5600, 'address': 'Barrio Meléndez, Cali',
        'hours': 'Mar-Dom 8am-6pm',  'types': ['Aprovechables', 'Orgánicos']},
    {'id': 18, 'name': 'EcoPunto Univalle',       'lat': 3.3760, 'lng': -76.5350,
        'address': 'Sector Univalle, Cali',        'hours': 'Lun-Sab 9am-7pm',  'types': ['Todos los residuos']},

    {'id': 19, 'name': 'Centro Verde Aguablanca', 'lat': 3.4000, 'lng': -76.4900,
        'address': 'Distrito Aguablanca, Cali',    'hours': 'Lun-Dom 7am-6pm',  'types': ['Aprovechables', 'Orgánicos']},
    {'id': 20, 'name': 'EcoPunto Marroquín',      'lat': 3.3900, 'lng': -76.4980,
        'address': 'Barrio Marroquín, Cali',       'hours': 'Lun-Sab 8am-5pm',  'types': ['Industriales', 'Peligrosos']},
    {'id': 21, 'name': 'Punto Verde Alfonso L.',  'lat': 3.4080, 'lng': -76.4850, 'address': 'Alfonso López, Cali',
        'hours': 'Mar-Dom 9am-6pm',  'types': ['Aprovechables', 'Orgánicos']},

    {'id': 22, 'name': 'EcoPunto Villacolombia',  'lat': 3.4300, 'lng': -76.4950,
        'address': 'Barrio Villacolombia, Cali',   'hours': 'Lun-Dom 7am-7pm',  'types': ['Orgánicos', 'Aprovechables']},
    {'id': 23, 'name': 'Punto Verde Calipso',     'lat': 3.4200, 'lng': -76.5000, 'address': 'Barrio Calipso, Cali',
        'hours': 'Lun-Sab 8am-6pm',  'types': ['Industriales', 'Aprovechables']},
]

companies = [
    {'name': 'EcoMarket',    'logo': '🛒', 'discount': '15% descuento',
        'min_points': 500,  'color': '#a8d5a2'},
    {'name': 'Verde Café',   'logo': '☕', 'discount': 'Café gratis',
        'min_points': 200,  'color': '#c8b5e8'},
    {'name': 'BiciEco',      'logo': '🚲', 'discount': '1 hora gratis',
        'min_points': 300,  'color': '#b8e0b0'},
    {'name': 'NaturalStore', 'logo': '🌱', 'discount': '20% en productos',
        'min_points': 800,  'color': '#d4c5f0'},
    {'name': 'GreenGym',     'logo': '💪', 'discount': '3 días gratis',
        'min_points': 1000, 'color': '#a0d4a0'},
    {'name': 'EcoFarm',      'logo': '🥦', 'discount': 'Cesta orgánica',
        'min_points': 600,  'color': '#c0b0e8'},
]

waste_types = ['Orgánicos', 'Aprovechables', 'Industriales', 'Peligrosos']
zones = ['Norte', 'Sur', 'Este', 'Oeste',
         'SurEste', 'SurOeste', 'NorEste', 'NorOeste']


@app.route('/')
def home():
    user = users_db['demo_user']
    return render_template('home.html', waste_types=waste_types, zones=zones, reports=reports_db[:5])


@app.route('/mis-puntos')
def mis_puntos():
    user = users_db['demo_user']
    return render_template('mis_puntos.html', user=user, companies=companies, recycling_points=json.dumps(recycling_points))


@app.route('/servicios')
def servicios():
    user = users_db['demo_user']
    return render_template('servicios.html')


@app.route('/api/reports', methods=['POST'])
def create_report():
    data = request.json
    report = {
        'id': str(uuid.uuid4())[:8].upper(),
        'waste_type': data.get('waste_type'),
        'zone': data.get('zone'),
        'address': data.get('address'),
        'description': data.get('description'),
        'urgency': data.get('urgency', 'media'),
        'photo': data.get('photo'),
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'status': 'Recibido',
        'user': 'Alejandro Alzate',
        'points_earned': 15
    }
    reports_db.insert(0, report)
    users_db['demo_user']['points'] += 15
    users_db['demo_user']['reports'] += 1
    return jsonify({'success': True, 'report': report, 'new_points': users_db['demo_user']['points']
                    })


@app.route('/api/reports', methods=['GET'])
def get_reports():
    return jsonify(reports_db)


@app.route('/api/user-points')
def get_user_points():
    return jsonify(users_db['demo_user'])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
