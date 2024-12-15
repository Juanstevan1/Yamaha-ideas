// global.js
document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('[data-scroll]');
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        },
        { threshold: 0.1 }
    );
    elements.forEach((el) => observer.observe(el));
});
