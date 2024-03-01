from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from sqlalchemy.sql import func
import serial
import time


app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust accordingly for security


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coins.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Replace 'COM3' with the correct port name where your Arduino is connected
arduino = serial.Serial('/dev/tty.usbmodem149589401', 9600)
time.sleep(2) # Wait for the serial connection to initialize

def withdraw10Yen():
    arduino.write(b'a')

def withdraw100Yen():
    arduino.write(b'b')

def pickUp10Yen():
    arduino.write(b'c')

def pickUp100Yen():
    arduino.write(b'd')






class CoinEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CoinEntry {self.value} yen, {self.timestamp}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/add_10_yen', methods=['POST'])
def add_10_yen():
    pickUp10Yen();
    time.sleep(1);
    entry = CoinEntry(value=10)
    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'Added 10 yen successfully'}), 200

@app.route('/add_100_yen', methods=['POST'])
def add_100_yen():
    pickUp100Yen();
    time.sleep(1);
    entry = CoinEntry(value=100)
    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'Added 100 yen successfully'}), 200

@app.route('/subtract_10_yen', methods=['POST'])
def subtract_10_yen():
            
    total_tens = CoinEntry.query.filter(CoinEntry.value == 10).count() - CoinEntry.query.filter(CoinEntry.value == -10).count()
    if total_tens > 0:  # Check if there's at least one 10 yen to subtract
        entry = CoinEntry(value=-10)
        db.session.add(entry)
        db.session.commit()
        withdraw10Yen()
        time.sleep(1) # Delay to allow Arduino to process the command

        return jsonify({'message': 'Subtracted 10 yen successfully'}), 200
    else:
        return jsonify({'message': 'Insufficient 10 yen to subtract'}), 400


@app.route('/subtract_100_yen', methods=['POST'])
def subtract_100_yen():
    total_hundreds = CoinEntry.query.filter(CoinEntry.value == 100).count() - CoinEntry.query.filter(CoinEntry.value == -100).count()
    if total_hundreds > 0:  # Check if there's at least one 100 yen to subtract
        entry = CoinEntry(value=-100)
        db.session.add(entry)
        db.session.commit()
        withdraw100Yen()
        time.sleep(1) # Delay to allow Arduino to process the command

        return jsonify({'message': 'Subtracted 100 yen successfully'}), 200
    else:
        return jsonify({'message': 'Insufficient 100 yen to subtract'}), 400



@app.route('/add_coin', methods=['GET'])
def add_coin():
    coin_value = request.args.get('value', default=0, type=int)
    if coin_value not in [10, 100]:
        return jsonify({'error': 'Invalid coin value. Accepts only 10 or 100 yen.'}), 400
    new_coin = CoinEntry(value=coin_value)
    db.session.add(new_coin)
    db.session.commit()
    return jsonify({'message': 'Coin added successfully.', 'coin': {'value': new_coin.value, 'timestamp': new_coin.timestamp}}), 201




@app.route('/withdraw_coin', methods=['GET'])
def withdraw_coin():
    withdraw_amount = request.args.get('amount', default=0, type=int)

    print(withdraw_amount)

    # Check if the withdrawal amount is valid (must be a multiple of 10)
    if withdraw_amount <= 0 or withdraw_amount % 10 != 0:
        return jsonify({'error': 'Invalid withdrawal amount. Must be a positive multiple of 10.'}), 400

    # Calculate available coins
    coins_10_available = sum(1 for entry in CoinEntry.query.filter_by(value=10)) - sum(1 for entry in CoinEntry.query.filter_by(value=-10))
    coins_100_available = sum(1 for entry in CoinEntry.query.filter_by(value=100)) - sum(1 for entry in CoinEntry.query.filter_by(value=-100))
    
    # Calculate if the withdrawal can be fulfilled
    amount_remaining = withdraw_amount
    coins_100_needed = min(amount_remaining // 100, coins_100_available)
    amount_remaining -= coins_100_needed * 100
    coins_10_needed = amount_remaining // 10

    if amount_remaining % 10 != 0 or coins_10_needed > coins_10_available:
        return jsonify({'error': 'Cannot fulfill withdrawal with available coins.'}), 400

    for _ in range(coins_100_needed):
        new_coin = CoinEntry(value=-100)
        db.session.add(new_coin)

    for _ in range(coins_10_needed):
        new_coin = CoinEntry(value=-10)
        db.session.add(new_coin)
    
    db.session.commit()

    return jsonify({'message': f'Withdrawn {withdraw_amount} yen successfully.', 'details': {'100_yen_coins': coins_100_needed, '10_yen_coins': coins_10_needed}}), 201

@app.route('/total', methods=['GET'])
def get_totals():
    # Calculate the total amount by summing all values, including negatives for withdrawals
    total_amount = sum(entry.value for entry in CoinEntry.query)
    
    # Count the occurrences of each coin type, considering both additions and withdrawals
    coins_10_count = CoinEntry.query.filter(CoinEntry.value.in_([10, -10])).count()
    coins_100_count = CoinEntry.query.filter(CoinEntry.value.in_([100, -100])).count()

    # Calculate the net count for each coin type (this accounts for withdrawals as negative)
    net_coins_10 = sum(1 for entry in CoinEntry.query.filter_by(value=10)) - sum(1 for entry in CoinEntry.query.filter_by(value=-10))
    net_coins_100 = sum(1 for entry in CoinEntry.query.filter_by(value=100)) - sum(1 for entry in CoinEntry.query.filter_by(value=-100))

    return jsonify({
        'total_amount': total_amount,
        'coins': {
            '10_yen': {
                'count': net_coins_10,
                'total': net_coins_10 * 10
            },
            '100_yen': {
                'count': net_coins_100,
                'total': net_coins_100 * 100
            }
        }
    }), 200


@app.route('/total_over_time', methods=['GET'])
def total_over_time():
    # This assumes `CoinEntry` has `value` (10 or -10 for withdrawals, and 100 or -100) and `timestamp`
    results = db.session.query(
        CoinEntry.timestamp,
        func.sum(CoinEntry.value).over(order_by=CoinEntry.timestamp).label('cumulative_total')
    ).order_by(CoinEntry.timestamp).all()

    data = [
        {'timestamp': result.timestamp.strftime('%Y-%m-%dT%H:%M:%S'), 'totalAmount': result.cumulative_total}
        for result in results
    ]

    return jsonify(data)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='192.168.0.150', port=5001, debug=True)
    #change here
