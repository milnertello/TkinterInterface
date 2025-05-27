from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Menu data for the Peruvian restaurant
MENU = {
    "Ceviche": 25.00,
    "Lomo Saltado": 28.00,
    "Aji de Gallina": 22.00,
    "Anticuchos": 20.00,
    "Papa a la Huancaina": 10.00,
    "Pollo a la Brasa": 24.00,
    "Causa Limeña": 15.00,
    "Rocoto Relleno": 18.00
}

# Store orders in memory (in production, use a database)
orders = {}
order_counter = 1

@app.route('/')
def index():
    """Main page displaying the restaurant ordering system"""
    return render_template('index.html', menu=MENU)

@app.route('/api/menu')
def get_menu():
    """API endpoint to get menu items"""
    return jsonify(MENU)

@app.route('/api/add-to-order', methods=['POST'])
def add_to_order():
    """Add items to the current order"""
    try:
        data = request.get_json()
        dish = data.get('dish')
        quantity = int(data.get('quantity', 1))
        
        if dish not in MENU:
            return jsonify({'error': 'Plato no encontrado en el menú'}), 400
        
        if quantity <= 0:
            return jsonify({'error': 'La cantidad debe ser mayor a 0'}), 400
        
        # Use session ID or create a simple order system
        session_id = request.headers.get('X-Session-ID', 'default')
        
        if session_id not in orders:
            orders[session_id] = {}
        
        if dish in orders[session_id]:
            orders[session_id][dish] += quantity
        else:
            orders[session_id][dish] = quantity
        
        return jsonify({
            'success': True,
            'message': f'{dish} agregado al pedido',
            'order': orders[session_id]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-order')
def get_order():
    """Get current order details"""
    try:
        session_id = request.headers.get('X-Session-ID', 'default')
        current_order = orders.get(session_id, {})
        
        order_details = []
        subtotal = 0
        
        for dish, quantity in current_order.items():
            price = MENU[dish]
            total_price = price * quantity
            subtotal += total_price
            
            order_details.append({
                'dish': dish,
                'quantity': quantity,
                'unit_price': price,
                'total_price': total_price
            })
        
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return jsonify({
            'items': order_details,
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/finalize-order', methods=['POST'])
def finalize_order():
    """Finalize the current order"""
    try:
        session_id = request.headers.get('X-Session-ID', 'default')
        
        if session_id not in orders or not orders[session_id]:
            return jsonify({'error': 'No hay productos en el pedido'}), 400
        
        global order_counter
        order_number = order_counter
        order_counter += 1
        
        # Clear the order after finalizing
        orders[session_id] = {}
        
        return jsonify({
            'success': True,
            'message': f'¡Pedido #{order_number} finalizado! Gracias por su compra en Wasi de Sabor Peruano!',
            'order_number': order_number
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cancel-order', methods=['POST'])
def cancel_order():
    """Cancel the current order"""
    try:
        session_id = request.headers.get('X-Session-ID', 'default')
        orders[session_id] = {}
        
        return jsonify({
            'success': True,
            'message': 'Pedido cancelado exitosamente'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/remove-item', methods=['POST'])
def remove_item():
    """Remove an item from the order"""
    try:
        data = request.get_json()
        dish = data.get('dish')
        session_id = request.headers.get('X-Session-ID', 'default')
        
        if session_id in orders and dish in orders[session_id]:
            del orders[session_id][dish]
            return jsonify({
                'success': True,
                'message': f'{dish} removido del pedido'
            })
        else:
            return jsonify({'error': 'Producto no encontrado en el pedido'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
