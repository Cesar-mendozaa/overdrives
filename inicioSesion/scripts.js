// Espera a que la página cargue completamente
window.addEventListener('load', function() {
    // Selecciona el contenedor del formulario
    const loginContainer = document.querySelector('.login-container');
    
    // Después de 500ms, añade la clase 'show' para mostrar la animación
    setTimeout(function() {
        loginContainer.classList.add('show');
    }, 500);
});
