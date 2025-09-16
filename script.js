class DarkModeToggle {
    constructor() {
        this.settingsBtn = document.getElementById('settingsBtn');
        this.settingsMenu = document.getElementById('settingsMenu');
        this.darkModeToggle = document.getElementById('darkModeToggle');
        this.storageKey = 'cognition-task-theme';
        
        this.init();
    }
    
    init() {
        this.loadTheme();
        this.bindEvents();
        this.handleClickOutside();
    }
    
    loadTheme() {
        const savedTheme = localStorage.getItem(this.storageKey);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        const isDarkMode = savedTheme === 'dark' || (!savedTheme && prefersDark);
        
        if (isDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            this.darkModeToggle.checked = true;
        } else {
            document.documentElement.removeAttribute('data-theme');
            this.darkModeToggle.checked = false;
        }
    }
    
    toggleTheme() {
        const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
        
        if (isDarkMode) {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem(this.storageKey, 'light');
            this.darkModeToggle.checked = false;
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem(this.storageKey, 'dark');
            this.darkModeToggle.checked = true;
        }
    }
    
    toggleSettingsMenu() {
        this.settingsMenu.classList.toggle('active');
    }
    
    closeSettingsMenu() {
        this.settingsMenu.classList.remove('active');
    }
    
    bindEvents() {
        this.settingsBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleSettingsMenu();
        });
        
        this.darkModeToggle.addEventListener('change', () => {
            this.toggleTheme();
        });
        
        this.settingsMenu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
    
    handleClickOutside() {
        document.addEventListener('click', (e) => {
            if (!this.settingsMenu.contains(e.target) && !this.settingsBtn.contains(e.target)) {
                this.closeSettingsMenu();
            }
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeSettingsMenu();
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new DarkModeToggle();
    
    console.log('Cognition Task Dashboard initialized');
    console.log('Dark mode toggle ready');
});
