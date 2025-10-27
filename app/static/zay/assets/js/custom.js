/**
 * Custom JavaScript - Xodó da Preta
 */

// ========================================
// CARRINHO DE COMPRAS (localStorage)
// ========================================

let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Atualizar badge do carrinho
function updateCartBadge() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        badge.textContent = totalItems;
        badge.style.display = totalItems > 0 ? 'block' : 'none';
    }
}

// Adicionar produto ao carrinho
function addToCart(productId, productName, productPrice, productImage, productSize = null) {
    const existingItem = cart.find(item => 
        item.id === productId && item.size === productSize
    );

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: parseFloat(productPrice),
            image: productImage,
            size: productSize,
            quantity: 1
        });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
    showAlert('Produto adicionado ao carrinho!', 'success');
}

// Mostrar alerta
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-custom alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    updateCartBadge();
    
    // Animação de fade-in nos produtos
    const products = document.querySelectorAll('.product-wap');
    products.forEach((product, index) => {
        setTimeout(() => {
            product.classList.add('fade-in');
        }, index * 100);
    });
});