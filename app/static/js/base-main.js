/**
 * BASE MAIN - JavaScript extraído do template base
 * Funções principais para carrinho e navegação
 */

// Atualizar badge do carrinho ao carregar a página
function atualizarBadgeCarrinho() {
    fetch('/api/carrinho/total')
        .then(response => response.json())
        .then(data => {
            const badgeDesktop = document.getElementById('cart-badge');
            const badgeMobile = document.getElementById('cart-badge-mobile');
            const total = data.total_itens || '0';

            if (badgeDesktop) {
                badgeDesktop.textContent = total;
            }
            if (badgeMobile) {
                badgeMobile.textContent = total;
            }
        })
        .catch(error => console.error('Erro ao atualizar badge do carrinho:', error));
}

// Atualizar ao carregar a página
document.addEventListener('DOMContentLoaded', atualizarBadgeCarrinho);

// Header Sticky - Adicionar classe ao scrollar
window.addEventListener('scroll', function() {
    const header = document.getElementById('templatemo_main_nav_container');
    if (header) {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
});
