import os
import re

perfect_header = """<body class="dark-theme">
    <!-- 1. MOBILE MENU DRAWER -->
    <div class="mobile-drawer" id="mobile-drawer">
        <div class="drawer-header">
            <a href="index.html" class="logo"><img src="photos/white blue.png" alt="Klaiz Designs" class="nav-logo-img"></a>
            <button class="nav-icon-btn" id="mobile-menu-close"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>
        </div>
        <ul class="mobile-nav-links">
            <!-- Dynamic Links via cms.js -->
        </ul>
        <div class="drawer-footer" style="margin-top:auto; padding: 2rem 0; border-top: 1px solid #222;">
            <div class="drawer-help-links" style="display:flex; gap:15px; margin-bottom:1rem; font-size:0.8rem; color:#666;">
                <a href="policies.html">Shipping</a>
                <a href="policies.html">Returns</a>
                <a href="about.html">About</a>
            </div>
        </div>
    </div>

    <!-- 2. BOTTOM NAVIGATION BAR (Mobile Only) -->
    <nav class="bottom-nav">
        <a href="index.html" class="bottom-nav-item">
            <i data-lucide="home"></i>
            <span>Home</span>
        </a>
        <a href="collection.html" class="bottom-nav-item">
            <i data-lucide="grid"></i>
            <span>Shop</span>
        </a>
        <a href="custom-builder.html" class="bottom-nav-item custom">
            <i data-lucide="palette"></i>
            <span>Custom</span>
        </a>
        <a href="login.html" class="bottom-nav-item">
            <i data-lucide="heart"></i>
            <span>Wishlist</span>
        </a>
        <a href="login.html" class="bottom-nav-item">
            <i data-lucide="user"></i>
            <span>Account</span>
        </a>
    </nav>

    <div class="sheet-overlay" id="sheet-overlay"></div>

    <!-- 1. ANNOUNCEMENT BAR -->
    <div class="announcement-bar">
        <div class="marquee-wrapper">
            <div class="marquee">
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
            </div>
            <div class="marquee" aria-hidden="true">
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
            </div>
        </div>
    </div>

    <!-- 2. STICKY NAVBAR -->
    <nav class="navbar" id="main-nav">
        <div class="container navbar-inner">
            <div class="nav-left">
                <button class="mobile-menu-btn" id="mobile-menu-open">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
                </button>
                <a href="index.html" class="logo"><img src="photos/white blue.png" alt="Klaiz Designs" class="nav-logo-img"></a>
            </div>

            <div class="nav-center desktop-only">
                <ul class="nav-links">
                    <!-- Dynamic Navbar Links are loaded here via cms.js -->
                </ul>
            </div>

            <div class="nav-right">
                <a href="search.html" class="nav-icon-btn"><i data-lucide="search"></i></a>
                <a href="login.html" class="nav-icon-btn"><i data-lucide="user"></i></a>
                <a href="cart.html" class="nav-icon-btn cart-btn">
                    <i data-lucide="shopping-bag"></i>
                    <span class="cart-count">0</span>
                </a>
            </div>
        </div>
    </nav>"""

# List of HTML files to skip (admin files)
skip_files = ['settings.html', 'products.html', 'orders.html', 'customers.html']

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in skip_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # This regex matches EVERYTHING from the body tag (including the typo <<body)
        # all the way until it sees a <main> tag or the start of the hero section.
        # This is guaranteed to wipe out all duplicate navbars.
        new_content = re.sub(r'<+body.*?<main>', perfect_header + '\n    <main>', content, flags=re.DOTALL)
        
        # If no <main> tag, try to find the start of a section
        if new_content == content:
             new_content = re.sub(r'<+body.*?<section', perfect_header + '\n    <section', content, flags=re.DOTALL)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"SURGICAL CLEANUP in {filename}")
