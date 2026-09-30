const filterButtons = document.querySelectorAll('.filter-button');
const productCards = document.querySelectorAll('.product-card');
const addButtons = document.querySelectorAll('.add-button');
const cartBar = document.querySelector('#cart-bar');
const cartSummary = document.querySelector('#cart-summary');
const cartDialog = document.querySelector('#cart-dialog');
const cartItems = document.querySelector('#cart-items');
const cartTotal = document.querySelector('#cart-total');
const checkoutButton = document.querySelector('#checkout-button');
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-nav');
const cart = new Map();

function formatPrice(cents) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(cents / 100);
}

filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const selectedFilter = button.dataset.filter;
        filterButtons.forEach((filterButton) => {
            const isActive = filterButton === button;
            filterButton.classList.toggle('is-active', isActive);
            filterButton.setAttribute('aria-pressed', String(isActive));
        });
        productCards.forEach((card) => {
            card.hidden = selectedFilter !== 'todos' && card.dataset.category !== selectedFilter;
        });
    });
});

function renderCart() {
    const entries = Array.from(cart.entries());
    const itemCount = entries.reduce((count, [, item]) => count + item.quantity, 0);
    const totalCents = entries.reduce((total, [, item]) => total + item.price * item.quantity, 0);

    cartSummary.textContent = `${itemCount} ${itemCount === 1 ? 'item' : 'itens'} no pedido`;
    cartBar.hidden = itemCount === 0;
    document.body.classList.toggle('has-cart', itemCount > 0);
    cartItems.replaceChildren();
    cartTotal.textContent = formatPrice(totalCents);

    entries.forEach(([name, item]) => {
        const row = document.createElement('div');
        row.className = 'cart-line';

        const title = document.createElement('span');
        title.textContent = name;
        const unitPrice = document.createElement('strong');
        unitPrice.textContent = formatPrice(item.price);

        const controls = document.createElement('div');
        controls.className = 'quantity-controls';
        const decrease = document.createElement('button');
        decrease.type = 'button';
        decrease.textContent = '-';
        decrease.setAttribute('aria-label', `Remover uma unidade de ${name}`);
        decrease.addEventListener('click', () => {
            if (item.quantity === 1) cart.delete(name);
            else item.quantity -= 1;
            renderCart();
        });
        const quantity = document.createElement('span');
        quantity.textContent = String(item.quantity);
        const increase = document.createElement('button');
        increase.type = 'button';
        increase.textContent = '+';
        increase.setAttribute('aria-label', `Adicionar uma unidade de ${name}`);
        increase.addEventListener('click', () => {
            item.quantity += 1;
            renderCart();
        });
        controls.append(decrease, quantity, increase);

        const lineTotal = document.createElement('span');
        lineTotal.className = 'line-total';
        lineTotal.textContent = formatPrice(item.price * item.quantity);
        row.append(title, unitPrice, controls, lineTotal);
        cartItems.append(row);
    });

    const message = entries.map(([name, item]) => `${item.quantity}x ${name} - ${formatPrice(item.price * item.quantity)}`);
    message.push(`Total: ${formatPrice(totalCents)}`);
    checkoutButton.href = `https://wa.me/?text=${encodeURIComponent(`Oi! Quero fazer este pedido:\n${message.join('\n')}`)}`;
}

addButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const { name, price } = button.dataset;
        const item = cart.get(name);
        if (item) item.quantity += 1;
        else cart.set(name, { price: Number(price), quantity: 1 });
        renderCart();
        button.innerHTML = 'Adicionado <span aria-hidden="true">&#10003;</span>';
        window.setTimeout(() => {
            button.innerHTML = 'Adicionar <span aria-hidden="true">+</span>';
        }, 900);
    });
});

cartBar.addEventListener('click', () => cartDialog.showModal());
document.querySelector('.dialog-close').addEventListener('click', () => cartDialog.close());
cartDialog.addEventListener('click', (event) => {
    if (event.target === cartDialog) cartDialog.close();
});

menuToggle.addEventListener('click', () => {
    const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!isOpen));
    mainNav.classList.toggle('is-open', !isOpen);
});

mainNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
        menuToggle.setAttribute('aria-expanded', 'false');
        mainNav.classList.remove('is-open');
    });
});