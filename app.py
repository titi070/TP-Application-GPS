from flask import Flask, request, jsonify, send_from_directory
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Point central (Paris, pour cet exemple)
central_latitude = 48.8566
central_longitude = 2.3522

# Types de véhicules disponibles
vehicle_types = ['car', 'bike', 'motorcycle']

# Simuler 50 parkings avec des coordonnées aléatoires autour de Paris
def generate_parkings(n):
    parkings = []
    types_per_vehicle = n // len(vehicle_types)  # Nombre de parkings par type de véhicule
    
    # Pré-remplir pour chaque type de véhicule
    for vehicle_type in vehicle_types:
        for i in range(types_per_vehicle):
            parking = {
                'id': len(parkings) + 1,
                'name': f'Parking {chr(65 + len(parkings) % 26)}',  # Parking A, B, C, etc.
                'address': f'{random.randint(1, 100)} Rue {chr(65 + len(parkings) % 26)}, Paris',
                'latitude': central_latitude + random.uniform(-0.02, 0.02),
                'longitude': central_longitude + random.uniform(-0.02, 0.02),
                'type': vehicle_type,
                'tariff': f'{random.randint(1, 5)}€/heure'
            }
            parkings.append(parking)
    
    # Ajouter des parkings restants aléatoires pour atteindre n total
    while len(parkings) < n:
        parking = {
            'id': len(parkings) + 1,
            'name': f'Parking {chr(65 + len(parkings) % 26)}',
            'address': f'{random.randint(1, 100)} Rue {chr(65 + len(parkings) % 26)}, Paris',
            'latitude': central_latitude + random.uniform(-0.02, 0.02),
            'longitude': central_longitude + random.uniform(-0.02, 0.02),
            'type': random.choice(vehicle_types),  # Type aléatoire parmi 'car', 'bike', 'motorcycle'
            'tariff': f'{random.randint(1, 5)}€/heure'
        }
        parkings.append(parking)

    return parkings

# Liste de 250 parkings simulés
parkings_data = generate_parkings(250)

# Endpoint pour servir les fichiers statiques (HTML, CSS, JS)
@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')

# Endpoint pour obtenir les données de parking
@app.route('/api/parkings', methods=['GET'])
def get_parkings():
    vehicle_type = request.args.get('vehicle_type', 'car')  # Par défaut, type de véhicule 'car'
    arriving = request.args.get('arriving')
    leaving = request.args.get('leaving')

    # Convertir les dates d'arrivée et de départ en objets datetime
    try:
        arriving_datetime = datetime.strptime(arriving, '%Y-%m-%dT%H:%M')
        leaving_datetime = datetime.strptime(leaving, '%Y-%m-%dT%H:%M')
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM'}), 400

    # Filtrer les parkings en fonction du type de véhicule (et dates si nécessaire)
    filtered_parkings = [parking for parking in parkings_data if parking['type'] == vehicle_type]

    return jsonify({
        'locations': filtered_parkings,
        'arriving': arriving_datetime.isoformat(),
        'leaving': leaving_datetime.isoformat()
    })

# Endpoint pour gérer les réservations
@app.route('/api/reserve', methods=['POST'])
def reserve_parking():
    reservation_details = request.json
    parking_id = reservation_details.get('parking_id')
    vehicle_type = reservation_details.get('vehicle_type')
    arriving = reservation_details.get('arriving')
    leaving = reservation_details.get('leaving')

    # Convertir les dates d'arrivée et de départ en objets datetime
    try:
        arriving_datetime = datetime.strptime(arriving, '%Y-%m-%dT%H:%M')
        leaving_datetime = datetime.strptime(leaving, '%Y-%m-%dT%H:%M')
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM'}), 400

    # Simuler une réservation réussie
    return jsonify({
        'status': 'success',
        'message': f'Réservation effectuée pour le parking {parking_id} avec un {vehicle_type}',
        'arriving': arriving_datetime.isoformat(),
        'leaving': leaving_datetime.isoformat()
    }), 201

# Démarre le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
