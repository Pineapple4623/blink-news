// main.js

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuToggle.contains(event.target)) {
                mobileMenu.classList.remove('active');
            }
        });
    }
    
    // Add fade-in animation to article cards
    const articleCards = document.querySelectorAll('.article-card');
    articleCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Smooth scroll to top for pagination links
    const paginationLinks = document.querySelectorAll('.pagination-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't scroll to top if it's navigating away from the page
            if (this.getAttribute('href').includes(window.location.pathname)) {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Handle broken images
    const images = document.querySelectorAll('.article-image');
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Replace broken image with placeholder
            if (this.tagName === 'IMG') {
                const container = document.createElement('div');
                container.className = 'article-image';
                container.style.backgroundColor = '#f5f5f7';
                container.style.display = 'flex';
                container.style.alignItems = 'center';
                container.style.justifyContent = 'center';
                
                const icon = document.createElement('i');
                icon.className = 'fas fa-newspaper';
                icon.style.fontSize = '48px';
                icon.style.color = '#d2d2d7';
                
                container.appendChild(icon);
                this.parentNode.replaceChild(container, this);
            }
        });
    });
    
    // Handle search form submission
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.focus();
                
                // Add shake animation if empty search
                searchInput.classList.add('shake');
                setTimeout(() => {
                    searchInput.classList.remove('shake');
                }, 500);
            }
        });
    }
    
    // Add keyframes for shake animation
    if (!document.querySelector('#shake-keyframes')) {
        const style = document.createElement('style');
        style.id = 'shake-keyframes';
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
            .shake {
                animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add current year to footer
    const yearElements = document.querySelectorAll('.current-year');
    const currentYear = new Date().getFullYear();
    yearElements.forEach(el => {
        el.textContent = currentYear;
    });
});