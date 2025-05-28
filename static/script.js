// Global variables
let currentOrder = {};
let sessionId = generateSessionId();

// Generate a unique session ID
function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    refreshOrder();
    
    // Set up event listeners for quantity inputs
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            if (this.value > 20) this.value = 20;
        });
    });
});

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    const toastMessage = document.getElementById('toastMessage');
    const toastHeader = toast.querySelector('.toast-header');
    
    // Set message
    toastMessage.textContent = message;
    
    // Set color based on type
    toastHeader.className = 'toast-header';
    switch(type) {
        case 'success':
            toastHeader.style.backgroundColor = '#28a745';
            break;
        case 'error':
            toastHeader.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            toastHeader.style.backgroundColor = '#ffc107';
            break;
        default:
            toastHeader.style.backgroundColor = '#17a2b8';
    }
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Update total price when quantity changes
function updateTotalPrice(dish, unitPrice) {
    const input = document.getElementById(`quantity-${dish}`);
    const totalSpan = document.getElementById(`total-${dish}`);
    const quantity = parseInt(input.value) || 1;
    const total = (unitPrice * quantity).toFixed(2);
    totalSpan.textContent = total;
}

// Increase quantity
function increaseQuantity(dish) {
    const input = document.getElementById(`quantity-${dish}`);
    const currentValue = parseInt(input.value);
    if (currentValue < 20) {
        input.value = currentValue + 1;
        // Get unit price from menu item data
        const menuItem = input.closest('.menu-item');
        const unitPrice = parseFloat(menuItem.dataset.price);
        updateTotalPrice(dish, unitPrice);
    }
}

// Decrease quantity
function decreaseQuantity(dish) {
    const input = document.getElementById(`quantity-${dish}`);
    const currentValue = parseInt(input.value);
    if (currentValue > 1) {
        input.value = currentValue - 1;
        // Get unit price from menu item data
        const menuItem = input.closest('.menu-item');
        const unitPrice = parseFloat(menuItem.dataset.price);
        updateTotalPrice(dish, unitPrice);
    }
}

// Add item to order
async function addToOrder(dish) {
    const quantityInput = document.getElementById(`quantity-${dish}`);
    const quantity = parseInt(quantityInput.value);
    const button = event.target;
    
    if (quantity <= 0) {
        showToast('La cantidad debe ser mayor a 0', 'warning');
        return;
    }
    
    // Add loading state
    button.classList.add('loading');
    button.disabled = true;
    
    try {
        const response = await fetch('/api/add-to-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': sessionId
            },
            body: JSON.stringify({
                dish: dish,
                quantity: quantity
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'success');
            // Add animation
            button.classList.add('add-animation');
            setTimeout(() => button.classList.remove('add-animation'), 300);
            
            // Reset quantity to 1
            quantityInput.value = 1;
            
            // Refresh order display
            refreshOrder();
        } else {
            showToast(data.error || 'Error al agregar el producto', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión. Inténtelo de nuevo.', 'error');
    } finally {
        // Remove loading state
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Refresh order display
async function refreshOrder() {
    try {
        const response = await fetch('/api/get-order', {
            headers: {
                'X-Session-ID': sessionId
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayOrder(data);
        } else {
            console.error('Error fetching order:', data.error);
            showToast('Error al cargar el pedido', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión al cargar el pedido', 'error');
    }
}

// Display order in the UI
function displayOrder(orderData) {
    const orderSummary = document.getElementById('orderSummary');
    const finalizeBtn = document.getElementById('finalizeBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    
    if (!orderData.items || orderData.items.length === 0) {
        // Show empty order state
        orderSummary.innerHTML = `
            <div class="empty-order text-center py-4">
                <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                <p class="text-muted">No hay productos en el pedido</p>
            </div>
        `;
        finalizeBtn.disabled = true;
        cancelBtn.disabled = true;
        
        // Disable print button when empty
        const printBtn = document.getElementById('printBtn');
        if (printBtn) {
            printBtn.disabled = true;
        }
        return;
    }
    
    // Build order items HTML
    let orderHTML = '';
    orderData.items.forEach(item => {
        orderHTML += `
            <div class="order-item">
                <div class="order-item-header">
                    <span class="order-item-name">${item.dish}</span>
                    <button class="remove-item-btn" onclick="removeItem('${item.dish}')" title="Eliminar producto">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="order-item-details">
                    <div>Cantidad: ${item.quantity}</div>
                    <div>Precio unitario: S/. ${item.unit_price.toFixed(2)}</div>
                    <div><strong>Total: S/. ${item.total_price.toFixed(2)}</strong></div>
                </div>
            </div>
        `;
    });
    
    // Add totals
    orderHTML += `
        <div class="order-totals">
            <div class="row">
                <div class="col-6">Subtotal:</div>
                <div class="col-6 text-end">S/. ${orderData.subtotal.toFixed(2)}</div>
            </div>
            <div class="row">
                <div class="col-6">IGV (18%):</div>
                <div class="col-6 text-end">S/. ${orderData.igv.toFixed(2)}</div>
            </div>
            <div class="row total-row">
                <div class="col-6">TOTAL:</div>
                <div class="col-6 text-end">S/. ${orderData.total.toFixed(2)}</div>
            </div>
        </div>
    `;
    
    orderSummary.innerHTML = orderHTML;
    finalizeBtn.disabled = false;
    cancelBtn.disabled = false;
    
    // Enable print button when there are items
    const printBtn = document.getElementById('printBtn');
    if (printBtn) {
        printBtn.disabled = false;
    }
}

// Remove item from order
async function removeItem(dish) {
    if (!confirm(`¿Está seguro de que desea eliminar ${dish} del pedido?`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/remove-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': sessionId
            },
            body: JSON.stringify({
                dish: dish
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'success');
            refreshOrder();
        } else {
            showToast(data.error || 'Error al eliminar el producto', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión. Inténtelo de nuevo.', 'error');
    }
}

// Finalize order
async function finalizeOrder() {
    if (!confirm('¿Confirma que desea finalizar este pedido?')) {
        return;
    }
    
    const button = document.getElementById('finalizeBtn');
    button.classList.add('loading');
    button.disabled = true;
    
    try {
        const response = await fetch('/api/finalize-order', {
            method: 'POST',
            headers: {
                'X-Session-ID': sessionId
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'success');
            refreshOrder();
            
            // Show celebration effect
            celebrateOrder();
        } else {
            showToast(data.error || 'Error al finalizar el pedido', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión. Inténtelo de nuevo.', 'error');
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Cancel order
async function cancelOrder() {
    if (!confirm('¿Está seguro de que desea cancelar todo el pedido?')) {
        return;
    }
    
    const button = document.getElementById('cancelBtn');
    button.classList.add('loading');
    button.disabled = true;
    
    try {
        const response = await fetch('/api/cancel-order', {
            method: 'POST',
            headers: {
                'X-Session-ID': sessionId
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'warning');
            refreshOrder();
        } else {
            showToast(data.error || 'Error al cancelar el pedido', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión. Inténtelo de nuevo.', 'error');
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Celebration effect for successful order
function celebrateOrder() {
    // Create confetti effect
    const colors = ['#ff704d', '#ff8533', '#ffa366', '#28a745', '#17a2b8'];
    
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            createConfetti(colors[Math.floor(Math.random() * colors.length)]);
        }, i * 50);
    }
}

// Create confetti particle
function createConfetti(color) {
    const confetti = document.createElement('div');
    confetti.style.position = 'fixed';
    confetti.style.left = Math.random() * 100 + 'vw';
    confetti.style.top = '-10px';
    confetti.style.width = '10px';
    confetti.style.height = '10px';
    confetti.style.backgroundColor = color;
    confetti.style.zIndex = '9999';
    confetti.style.pointerEvents = 'none';
    confetti.style.borderRadius = '50%';
    
    document.body.appendChild(confetti);
    
    // Animate confetti falling
    let position = -10;
    const animation = setInterval(() => {
        position += 5;
        confetti.style.top = position + 'px';
        
        if (position > window.innerHeight) {
            clearInterval(animation);
            document.body.removeChild(confetti);
        }
    }, 50);
}

// Handle connection errors gracefully
window.addEventListener('online', function() {
    showToast('Conexión restaurada', 'success');
});

window.addEventListener('offline', function() {
    showToast('Sin conexión a internet', 'warning');
});

// Print order function
function printOrder() {
    // Get current order data
    fetch('/api/get-order', {
        headers: {
            'X-Session-ID': sessionId
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.items && data.items.length > 0) {
            generatePrintableReceipt(data);
        } else {
            showToast('No hay productos en el pedido para imprimir', 'warning');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al generar el recibo', 'error');
    });
}

// Generate printable receipt
function generatePrintableReceipt(orderData) {
    const printWindow = window.open('', '_blank', 'width=800,height=600');
    const currentDate = new Date().toLocaleString('es-PE');
    
    let receiptHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Recibo - Restaurante Wasi</title>
            <style>
                body {
                    font-family: 'Courier New', monospace;
                    margin: 20px;
                    line-height: 1.4;
                    color: #333;
                }
                .header {
                    text-align: center;
                    border-bottom: 2px solid #333;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .restaurant-name {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .subtitle {
                    font-size: 14px;
                    color: #666;
                }
                .order-info {
                    margin-bottom: 20px;
                    border-bottom: 1px dashed #333;
                    padding-bottom: 10px;
                }
                .item-row {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px;
                    padding: 2px 0;
                }
                .item-name {
                    flex: 1;
                }
                .item-qty {
                    width: 60px;
                    text-align: center;
                }
                .item-price {
                    width: 80px;
                    text-align: right;
                }
                .totals {
                    border-top: 1px solid #333;
                    padding-top: 10px;
                    margin-top: 15px;
                }
                .total-row {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px;
                }
                .total-final {
                    font-weight: bold;
                    font-size: 18px;
                    border-top: 2px solid #333;
                    padding-top: 8px;
                    margin-top: 8px;
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 1px dashed #333;
                    font-size: 12px;
                    color: #666;
                }
                @media print {
                    body { margin: 0; }
                    .no-print { display: none; }
                }
                .print-btn {
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin: 10px 5px;
                }
                .download-btn {
                    background: #28a745;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin: 10px 5px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="restaurant-name">RESTAURANTE WASI</div>
                <div class="restaurant-name">DE SABOR PERUANO</div>
                <div class="subtitle">Auténtica cocina peruana</div>
            </div>
            
            <div class="order-info">
                <div><strong>Fecha:</strong> ${currentDate}</div>
                <div><strong>Pedido #:</strong> ${Math.floor(Math.random() * 1000) + 1}</div>
            </div>
            
            <div class="no-print" style="text-align: center; margin-bottom: 20px;">
                <button class="print-btn" onclick="window.print()">🖨️ Imprimir</button>
                <button class="download-btn" onclick="downloadReceipt()">📄 Descargar PDF</button>
            </div>
            
            <div class="items">
                <div class="item-row" style="font-weight: bold; border-bottom: 1px solid #333; padding-bottom: 5px;">
                    <div class="item-name">PRODUCTO</div>
                    <div class="item-qty">CANT.</div>
                    <div class="item-price">PRECIO</div>
                </div>
    `;
    
    // Add items
    orderData.items.forEach(item => {
        receiptHTML += `
                <div class="item-row">
                    <div class="item-name">${item.dish}</div>
                    <div class="item-qty">${item.quantity}</div>
                    <div class="item-price">S/. ${item.total_price.toFixed(2)}</div>
                </div>
        `;
    });
    
    // Add totals
    receiptHTML += `
            </div>
            
            <div class="totals">
                <div class="total-row">
                    <span>Subtotal:</span>
                    <span>S/. ${orderData.subtotal.toFixed(2)}</span>
                </div>
                <div class="total-row">
                    <span>IGV (18%):</span>
                    <span>S/. ${orderData.igv.toFixed(2)}</span>
                </div>
                <div class="total-row total-final">
                    <span>TOTAL:</span>
                    <span>S/. ${orderData.total.toFixed(2)}</span>
                </div>
            </div>
            
            <div class="footer">
                <p>¡Gracias por su preferencia!</p>
                <p>Wasi de Sabor Peruano</p>
                <p>www.wasirestaurante.com</p>
            </div>
            
            <script>
                function downloadReceipt() {
                    // Create downloadable content
                    const content = document.documentElement.outerHTML;
                    const blob = new Blob([content], { type: 'text/html' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'recibo-wasi-' + new Date().getTime() + '.html';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                }
            </script>
        </body>
        </html>
    `;
    
    printWindow.document.write(receiptHTML);
    printWindow.document.close();
    
    // Auto focus the print window
    printWindow.focus();
    
    showToast('Recibo generado exitosamente', 'success');
}
