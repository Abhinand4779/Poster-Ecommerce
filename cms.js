/**
 * KLAIZ DESIGNS — CMS ENGINE
 * Single source of truth for product management.
 * All pages (admin + user) import this file.
 * Data is stored in localStorage under key: 'klaiz_products'
 */

const KlaizCMS = {
    STORAGE_KEY: 'klaiz_products',

    // ── Read ─────────────────────────────────────────────────────────────────
    getAll() {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY) || '[]');
        } catch (e) {
            console.error('[CMS] Failed to read products:', e);
            return [];
        }
    },

    getById(id) {
        return this.getAll().find(p => String(p.id) === String(id)) || null;
    },

    getByCategory(category) {
        const all = this.getAll();
        if (!category || category === 'all') return all;
        return all.filter(p => p.category && p.category.toLowerCase() === category.toLowerCase());
    },

    // ── Write ────────────────────────────────────────────────────────────────
    save(productsArray) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(productsArray));
            return true;
        } catch (e) {
            console.error('[CMS] Failed to save products (storage full?):', e);
            return false;
        }
    },

    add(product) {
        const products = this.getAll();
        const newProduct = {
            id: Date.now(),
            name: product.name,
            category: product.category,
            price: parseFloat(product.price),
            image: product.image,
            createdAt: new Date().toISOString()
        };
        products.unshift(newProduct);
        this.save(products);
        return newProduct;
    },

    update(id, updates) {
        const products = this.getAll();
        const idx = products.findIndex(p => String(p.id) === String(id));
        if (idx === -1) return false;
        products[idx] = { ...products[idx], ...updates, updatedAt: new Date().toISOString() };
        this.save(products);
        return true;
    },

    delete(id) {
        const products = this.getAll().filter(p => String(p.id) !== String(id));
        this.save(products);
    },

    // ── Image Processing ─────────────────────────────────────────────────────
    compressImage(file) {
        return new Promise((resolve, reject) => {
            const name = file.name.toLowerCase();
            const type = (file.type || '').toLowerCase();
            if (name.endsWith('.heic') || name.endsWith('.heif') || type === 'image/heic' || type === 'image/heif') {
                reject(new Error('HEIC_NOT_SUPPORTED'));
                return;
            }
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                const img = new Image();
                img.src = e.target.result;
                img.onload = () => {
                    try {
                        const canvas = document.createElement('canvas');
                        const MAX = 900;
                        const ratio = Math.min(1, MAX / Math.max(img.width, img.height));
                        canvas.width = Math.round(img.width * ratio);
                        canvas.height = Math.round(img.height * ratio);
                        canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
                        resolve(canvas.toDataURL('image/jpeg', 0.80));
                    } catch (canvasErr) {
                        resolve(e.target.result); // fallback: raw base64
                    }
                };
                img.onerror = () => reject(new Error('IMAGE_LOAD_FAILED'));
            };
            reader.onerror = () => reject(new Error('FILE_READ_FAILED'));
        });
    },

    // ── Render to a grid element ─────────────────────────────────────────────
    renderGrid(gridElement, products, options = {}) {
        if (!gridElement) return;

        const {
            linkPrefix = '',     // e.g. '' for root, '../' for admin subfolder
            emptyMessage = 'No products found.',
            badgeText = 'NEW'
        } = options;

        if (!products || products.length === 0) {
            gridElement.innerHTML = `
                <div style="grid-column:1/-1; padding:3rem 1rem; color:#aaa; text-align:center; font-size:1rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2EA7D7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block;margin:0 auto 1rem;"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                    ${emptyMessage}
                </div>`;
            return;
        }

        gridElement.innerHTML = products.map(p => `
            <div class="product-card" data-product-id="${p.id}">
                <a href="${linkPrefix}product.html?id=${p.id}" style="text-decoration:none; color:inherit; display:block;">
                    <div class="product-img">
                        <span class="badge-new">${badgeText}</span>
                        <button class="wishlist-btn" onclick="event.preventDefault()"><i data-lucide="heart"></i></button>
                        <img src="${p.image}" alt="${p.name}" class="primary" style="object-fit:cover;">
                        <img src="${p.image}" alt="${p.name}" class="secondary" style="object-fit:cover;">
                    </div>
                    <div class="product-info">
                        <span class="piece-label">${p.category || '1 Piece'}</span>
                        <h3>${p.name}</h3>
                        <div class="price-row">
                            <span class="price-sale">₹${p.price}</span>
                        </div>
                    </div>
                </a>
            </div>
        `).join('');

        // Re-init icons
        if (window.lucide) lucide.createIcons();
    },

    // --- GLOBAL SETTINGS ---
    getSettings() {
        const defaults = {
            marquee: "FREE SHIPPING on orders above â‚¹499 | COD Available | 10,000+ Happy Customers",
            contactEmail: "support@klaizdesigns.com",
            contactPhone: "+91 98765 43210",
            contactAddress: "Kochi, Kerala, India",
            instagram: "klaiz_designs",
            heroTitle: "PREMIUM WALL ART FOR YOUR SPACE",
            heroSubtitle: "Elevate your room with high-quality posters",
            // About Page
            aboutHeroImg: "photos/hero_slide_1_1777291339894.png",
            aboutMission: "At Klaiz Designs, we believe in the power of creativity to transform ideas into impactful visual experiences. Founded by Adhil Muhammed S, Klaiz Designs has grown into a hub for innovative and modern design solutions.",
            aboutStoryTitle: "How It All Started",
            aboutStoryText: "Guided by our founderâ€™s vision, Klaiz Designs is supported by the expertise of our managing partners... Together, we form a dynamic team dedicated to crafting designs that are aesthetically captivating.",
            aboutStoryImg: "photos/design_your_own_custom_1777291662169.png",
            // Team
            team: [
                { name: "Adhil Muhammed S", role: "CEO", img: "photos/adhil.png" },
                { name: "Akshay Mohan", role: "Co-Founder", img: "photos/akshay.png" },
                { name: "Abhinand Binu", role: "Co-Founder", img: "photos/abhinand.png" },
                { name: "Giri Shankar", role: "Managing Partner", img: "photos/giri.png" },
                { name: "Al Ameen Noushad", role: "Managing Partner", img: "photos/Alameen.png" },
                { name: "Nabeel N Rasool", role: "Managing Partner", img: "photos/nabeel.png" }
            ],
            // Categories
            categories: [
                { name: "Superhero", img: "photos/category_superhero_1777291640908.png", url: "collection-superhero.html" },
                { name: "Cars", img: "photos/hero_slide_1_1777291339894.png", url: "collection-cars.html" },
                { name: "Movies", img: "photos/product_poster_1_1777291679013.png", url: "collection-movies.html" },
                { name: "Music", img: "photos/design_your_own_custom_1777291662169.png", url: "collection.html?cat=Music" }
            ],
            // Navbar Links
            navbar: [
                { label: "Home", url: "index.html" },
                { label: "Best Sellers", url: "collection.html" },
                { label: "New Arrivals", url: "collection.html" },
                { label: "Design Your Own", url: "custom-builder.html" },
                { label: "Bulk Posters", url: "bulk-posters.html" },
                { label: "Our Services", url: "services.html" },
                { label: "About", url: "about.html" },
                { label: "Contact", url: "contact.html" }
            ],
            // Hero Marquee Images
            heroMarqueeRow1: [
                "photos/product_poster_1_1777291679013.png", "photos/category_superhero_1777291640908.png", "photos/design_your_own_custom_1777291662169.png",
                "photos/hero_slide_1_1777291339894.png", "photos/hero_slide_2_1777291568402.png", "photos/hero_slide_3_1777291582739.png"
            ],
            heroMarqueeRow2: [
                "photos/customized baleno 1.jpeg", "photos/customized baleno 2.jpeg", "photos/customized domi.jpeg",
                "photos/hero_slide_1_1777291339894.png", "photos/hero_slide_2_1777291568402.png", "photos/hero_slide_3_1777291582739.png"
            ],
            // Customer Review Videos
            customerVideos: [
                { url: "https://www.w3schools.com/html/mov_bbb.mp4" },
                { url: "https://www.w3schools.com/html/mov_bbb.mp4" },
                { url: "https://www.w3schools.com/html/mov_bbb.mp4" }
            ]
        };
        const saved = JSON.parse(localStorage.getItem('klaiz_settings') || '{}');
        return { ...defaults, ...saved };
    },

    updateSettings(newSettings) {
        const current = this.getSettings();
        const updated = { ...current, ...newSettings };
        localStorage.setItem('klaiz_settings', JSON.stringify(updated));

        // Sync to UI immediately
        this.applySettingsToUI();
        return updated;
    },

    applySettingsToUI() {
        const s = this.getSettings();

        // Announcement Bar
        const marquee = document.querySelector('.announcement-bar marquee, .promo-text');
        if (marquee) marquee.textContent = s.marquee;

        // Navbar Rendering (Dynamic Header)
        const navLinksList = document.querySelector('.nav-links');
        const mobileLinksList = document.querySelector('.mobile-nav-links');
        if (navLinksList && s.navbar) {
            // Find "Home" in the navbar array if it exists, otherwise we'll prepend it
            const homeLink = s.navbar.find(l => l.label.toLowerCase() === 'home');
            const otherLinks = s.navbar.filter(l => l.label.toLowerCase() !== 'home');

            const otherHtml = otherLinks.map(link => `<li><a href="${link.url}">${link.label}</a></li>`).join('');

            navLinksList.innerHTML = `
                <li><a href="${homeLink ? homeLink.url : 'index.html'}">Home</a></li>
                <li class="has-mega-menu">
                    <a href="collection.html">Shop By Category <i data-lucide="chevron-down"></i></a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h3>Popular</h3>
                                ${s.categories.slice(0, 4).map(c => `<a href="collection.html?cat=${c.name}">${c.name}</a>`).join('')}
                            </div>
                            <div class="mega-col">
                                <h3>Featured</h3>
                                <a href="collection.html">Best Sellers</a>
                                <a href="collection.html">New Arrivals</a>
                                <a href="custom-builder.html">Custom Posters</a>
                            </div>
                            <div class="mega-col featured-card">
                                <div class="card-img"><img src="photos/hero_slide_2_1777291568402.png" alt="Custom"></div>
                                <div class="card-content">
                                    <h4>Custom Posters</h4>
                                    <a href="custom-builder.html" class="btn-text">Design Now â†’</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            ` + otherHtml;
            if (window.lucide) lucide.createIcons();
        }
        if (mobileLinksList && s.navbar) {
            mobileLinksList.innerHTML = s.navbar.map(link => `<li><a href="${link.url}">${link.label}</a></li>`).join('');
        }

        // Hero Section (Home)
        const hTitle = document.querySelector('.hero-content h1');
        const hSub = document.querySelector('.hero-content p');
        if (hTitle && s.heroTitle) hTitle.textContent = s.heroTitle;
        if (hSub && s.heroSubtitle) hSub.textContent = s.heroSubtitle;

        // Hero Marquee Dynamic Injection
        const marqueeRows = document.querySelectorAll('.marquee-row');
        if (marqueeRows.length >= 2 && s.heroMarqueeRow1 && s.heroMarqueeRow2) {
            marqueeRows[0].innerHTML = s.heroMarqueeRow1.map(img => `<div class="marquee-item"><img src="${img}" alt="Gallery Image"></div>`).join('') + 
                                       s.heroMarqueeRow1.map(img => `<div class="marquee-item"><img src="${img}" alt="Gallery Image"></div>`).join('');
            marqueeRows[1].innerHTML = s.heroMarqueeRow2.map(img => `<div class="marquee-item"><img src="${img}" alt="Gallery Image"></div>`).join('') + 
                                       s.heroMarqueeRow2.map(img => `<div class="marquee-item"><img src="${img}" alt="Gallery Image"></div>`).join('');
        }

        // Category Circles (Home)
        const catScroll = document.getElementById('category-scroll');
        if (catScroll && s.categories) {
            catScroll.innerHTML = s.categories.map(c => `
                <a href="collection.html?cat=${c.name}" class="category-item">
                    <div class="circle-img"><img src="${c.img}" alt="${c.name}"></div>
                    <span>${c.name}</span>
                </a>
            `).join('') + `
                <a href="collection.html" class="category-item">
                    <div class="circle-img"><div class="explore-more-icon"><i data-lucide="plus"></i></div></div>
                    <span>Explore More</span>
                </a>
            `;
        }

        // Customer Videos (Home)
        const videoCarousel = document.getElementById('video-reviews-container');
        if (videoCarousel && s.customerVideos) {
            videoCarousel.innerHTML = s.customerVideos.map(v => `
                <div class="custom-card" style="width: 250px; flex-shrink: 0;">
                    <video src="${v.url}" controls style="width: 100%; height: 350px; object-fit: cover; border-radius: 15px;"></video>
                </div>
            `).join('');
        }

        // About Page
        const aboutHeroImg = document.querySelector('.about-hero .hero-bg-img');
        const aboutMission = document.querySelector('.mission-text');
        const storyTitle = document.querySelector('.about-story h2');
        const storyText = document.querySelector('.about-story p');
        const storyImg = document.querySelector('.story-img img');

        if (aboutHeroImg) aboutHeroImg.src = s.aboutHeroImg;
        if (aboutMission) aboutMission.textContent = s.aboutMission;
        if (storyTitle) storyTitle.textContent = s.aboutStoryTitle;
        if (storyText) storyText.textContent = s.aboutStoryText;
        if (storyImg) storyImg.src = s.aboutStoryImg;

        // Team Rendering
        const teamCarousel = document.querySelector('.team-carousel');
        if (teamCarousel && s.team) {
            teamCarousel.innerHTML = s.team.map(m => `
                <div class="team-card">
                    <img src="${m.img}" alt="${m.name}" class="team-img">
                    <h3>${m.name}</h3>
                    <span>${m.role}</span>
                </div>
            `).join('');
        }

        // Contact Info (Global)
        document.querySelectorAll('.contact-email').forEach(el => el.textContent = s.contactEmail);
        document.querySelectorAll('.contact-phone').forEach(el => el.textContent = s.contactPhone);
        document.querySelectorAll('.contact-address').forEach(el => el.textContent = s.contactAddress);
    },

    // ── Main init: auto-render any page that has .product-grid ──────────────
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            // Apply settings first
            this.applySettingsToUI();

            // Seed initial custom products if missing
            const currentProducts = this.getAll();
            if (!currentProducts.find(p => p.name === 'Customized Baleno 1')) {
                this.add({
                    name: 'Customized Baleno 1',
                    category: 'Cars',
                    price: 1499,
                    image: 'photos/customized baleno 1.jpeg'
                });
            }
            if (!currentProducts.find(p => p.name === 'Customized Baleno 2')) {
                this.add({
                    name: 'Customized Baleno 2',
                    category: 'Cars',
                    price: 1499,
                    image: 'photos/customized baleno 2.jpeg'
                });
            }

            // --- SMART CATEGORY DETECTION ---
            const urlParams = new URLSearchParams(window.location.search);
            const urlCat = urlParams.get('cat');
            const s = this.getSettings();

            // Update Page Titles & Breadcrumbs if on collection page
            const pageTitle = document.querySelector('.page-title');
            const breadcrumb = document.querySelector('.breadcrumb span');
            if (urlCat) {
                if (pageTitle) pageTitle.textContent = urlCat + ' Collection';
                if (breadcrumb) breadcrumb.textContent = urlCat;
                document.body.setAttribute('data-category', urlCat);
            } else {
                if (pageTitle) pageTitle.textContent = 'Our Full Collection';
                if (breadcrumb) breadcrumb.textContent = 'All Products';
            }


            // Sync Sidebar Category List
            const sidebarCats = document.querySelector('.category-links');
            if (sidebarCats && s.categories) {
                sidebarCats.innerHTML = `<a href="collection.html" class="cat-link ${!urlCat ? 'active' : ''}" data-category="all">All Products</a>` +
                    s.categories.map(c => `<a href="collection.html?cat=${c.name}" class="cat-link ${urlCat === c.name ? 'active' : ''}" data-category="${c.name}">${c.name}</a>`).join('');
            }

            // Support both Homepage (.product-grid) and Collections (.product-listing-grid)
            const grids = document.querySelectorAll('.product-grid, .product-listing-grid');
            if (grids.length === 0) return;

            const allProducts = this.getAll();
            const bodyCategory = document.body.getAttribute('data-category') || 'all';

            grids.forEach(grid => {
                // If grid has its own category (like on home page), use it. Else use body's category.
                const gridCategory = grid.getAttribute('data-category') || bodyCategory;

                let products = (gridCategory !== 'all')
                    ? allProducts.filter(p => p.category && p.category.toLowerCase() === gridCategory.toLowerCase())
                    : allProducts;

                // Update product count if element exists
                const countEl = document.querySelector('.product-count');
                if (countEl) countEl.textContent = `${products.length} products`;

                this.renderGrid(grid, products);
            });
        });
    }
};

KlaizCMS.init();


