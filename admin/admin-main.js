document.addEventListener('DOMContentLoaded', () => {
    // 1. Sidebar Toggle Logic
    const sidebar = document.querySelector('.admin-sidebar');
    const toggleBtn = document.querySelector('.mobile-menu-trigger');
    
    // Create and add overlay if it doesn't exist
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
    }

    if (toggleBtn && sidebar) {
        const icon = toggleBtn.querySelector('i');
        
        const updateUI = () => {
            const isActive = sidebar.classList.contains('active');
            overlay.classList.toggle('active', isActive);
            
            // Toggle Icon
            if (icon) {
                icon.setAttribute('data-lucide', isActive ? 'x' : 'menu');
                if (window.lucide) lucide.createIcons();
            }

            // Prevent Scroll when menu is open
            document.body.style.overflow = isActive ? 'hidden' : '';
        };

        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            updateUI();
        });

        // Close sidebar when clicking overlay
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            updateUI();
        });

        // Close sidebar when clicking nav items on mobile
        sidebar.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('active');
                    updateUI();
                }
            });
        });
    }

    // 2. Lucide Icons Initialization
    if (window.lucide) {
        lucide.createIcons();
    }
});
