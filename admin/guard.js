/**
 * KLAIZ DESIGNS — ADMIN GUARD
 * Protects admin pages from unauthorized access.
 * Add this to the top of every admin HTML file.
 */
(function() {
    const adminSession = localStorage.getItem('klaiz_admin_session');
    
    // If no session found and we are not already on the login page
    if (!adminSession && !window.location.pathname.includes('login.html')) {
        console.warn('[Guard] Unauthorized access. Redirecting to login...');
        window.location.href = 'login.html';
    }

    // Global Logout Function
    window.adminLogout = function(e) {
        if (e) e.preventDefault();
        if (confirm('Are you sure you want to logout from admin panel?')) {
            localStorage.removeItem('klaiz_admin_session');
            window.location.href = 'login.html';
        }
    };
})();
