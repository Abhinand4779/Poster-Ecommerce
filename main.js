/**
 * KLAIZ DESIGNS — MAIN UI SCRIPT
 * Handles UI interactions, scrolling, and animations.
 * Product rendering is handled separately by cms.js.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (window.lucide) lucide.createIcons();

    // 2. STICKY NAVBAR
    const navbar = document.getElementById('main-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 3. MOBILE MENU DRAWER
    const drawer = document.getElementById('mobile-drawer');
    const drawerOpen = document.getElementById('mobile-menu-open');
    const drawerClose = document.getElementById('mobile-menu-close');

    // Create overlay
    let overlay = document.querySelector('.drawer-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'drawer-overlay';
        document.body.appendChild(overlay);
    }

    if (drawerOpen && drawer) {
        drawerOpen.addEventListener('click', () => {
            drawer.classList.add('active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    const closeMenu = () => {
        if (drawer) drawer.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    };

    if (drawerClose) drawerClose.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);

    // 4. COLLECTION SIDEBAR FILTERING (for collection.html)
    const priceSlider = document.getElementById('price-slider');
    const priceVal = document.getElementById('price-val');
    const catLinks = document.querySelectorAll('.cat-link');
    const productGrid = document.getElementById('product-grid');
    const filterSidebar = document.getElementById('filters-sidebar');
    const filterOpen = document.getElementById('open-filters');
    const filterClose = document.getElementById('close-filters');

    if (filterOpen && filterSidebar) {
        filterOpen.addEventListener('click', () => {
            filterSidebar.classList.add('active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    const closeAllModals = () => {
        if (drawer) drawer.classList.remove('active');
        if (filterSidebar) filterSidebar.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    };

    if (drawerClose) drawerClose.addEventListener('click', closeAllModals);
    if (filterClose) filterClose.addEventListener('click', closeAllModals);
    if (overlay) overlay.addEventListener('click', closeAllModals);


    if (priceSlider && priceVal) {
        priceSlider.addEventListener('input', (e) => {
            priceVal.textContent = `₹${e.target.value}`;
            applyFilters();
        });
    }

    catLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            catLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            applyFilters();
        });
    });

    function applyFilters() {
        if (!productGrid || !window.KlaizCMS) return;

        const activeCat = document.querySelector('.cat-link.active');
        const category = activeCat ? activeCat.getAttribute('data-category') : 'all';
        const maxPrice = priceSlider ? parseFloat(priceSlider.value) : 99999;

        const allProducts = KlaizCMS.getAll();
        let filtered = (category === 'all') 
            ? allProducts 
            : allProducts.filter(p => p.category && p.category.toLowerCase() === category.toLowerCase());
        
        filtered = filtered.filter(p => parseFloat(p.price) <= maxPrice);

        KlaizCMS.renderGrid(productGrid, filtered);
    }

    window.resetFilters = () => {
        if (priceSlider) priceSlider.value = 2000;
        if (priceVal) priceVal.textContent = '₹2000';
        catLinks.forEach(l => l.classList.remove('active'));
        const allBtn = document.querySelector('[data-category="all"]');
        if (allBtn) allBtn.classList.add('active');
        applyFilters();
    };

    // 5. CART BADGE UPDATE
    window.updateCartBadge = () => {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const count = cart.reduce((acc, item) => acc + (item.quantity || 1), 0);
        document.querySelectorAll('.cart-count').forEach(el => el.textContent = count);
    };

    window.updateCartBadge();

    // 6. QUICK ADD TO CART
    window.quickAddToCart = (productId) => {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existing = cart.find(item => String(item.id) === String(productId));
        
        if (existing) {
            existing.quantity = (existing.quantity || 1) + 1;
        } else {
            cart.push({ id: productId, quantity: 1, addedAt: new Date().toISOString() });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        window.updateCartBadge();
        showToast("Added to cart!");
    };

    // 8. AUTHENTICATION LOGIC (Login/Signup)
    const authTabs = document.querySelectorAll('.auth-tab');
    const authForms = document.querySelectorAll('.auth-form');

    if (authTabs.length > 0) {
        authTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                authTabs.forEach(t => t.classList.remove('active'));
                authForms.forEach(f => f.classList.remove('active'));
                tab.classList.add('active');
                const target = document.getElementById(tab.getAttribute('data-tab') + '-form');
                if (target) target.classList.add('active');
            });
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = loginForm.querySelector('input[type="email"]').value;
            const btn = loginForm.querySelector('button[type="submit"]');
            btn.textContent = 'LOGGING IN...';
            btn.disabled = true;

            setTimeout(() => {
                // Simulate success
                const user = { email: email, name: email.split('@')[0], loggedInAt: new Date().toISOString() };
                localStorage.setItem('klaiz_user', JSON.stringify(user));
                
                // Redirect back if needed
                const params = new URLSearchParams(window.location.search);
                const redirect = params.get('redirect') || 'account.html';
                window.location.href = redirect;
            }, 1000);
        });
    }

    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = signupForm.querySelector('input[type="email"]').value;
            const name = signupForm.querySelector('input[type="text"]').value;
            const btn = signupForm.querySelector('button[type="submit"]');
            btn.textContent = 'CREATING ACCOUNT...';
            btn.disabled = true;

            setTimeout(() => {
                const user = { email: email, name: name, loggedInAt: new Date().toISOString() };
                localStorage.setItem('klaiz_user', JSON.stringify(user));
                
                const params = new URLSearchParams(window.location.search);
                const redirect = params.get('redirect') || 'account.html';
                window.location.href = redirect;
            }, 1500);
        });
    }

    function showToast(message) {
        let toast = document.getElementById('klaiz-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'klaiz-toast';
            toast.style = `
                position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
                background: #2EA7D7; color: white; padding: 12px 24px; border-radius: 50px;
                font-weight: 700; font-size: 0.9rem; z-index: 10000;
                box-shadow: 0 10px 30px rgba(46, 167, 215, 0.4);
                transition: all 0.3s ease; opacity: 0; pointer-events: none;
            `;
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        toast.style.opacity = '1';
        toast.style.bottom = '40px';
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.bottom = '30px';
        }, 3000);
    }
});
