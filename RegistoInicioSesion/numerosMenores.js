// Función para calcular la edad en base a la fecha de nacimiento
function calcularEdad() {
    const fechaNacimiento = document.getElementById('fecha_nacimiento').value;
    const fechaNacimientoObj = new Date(fechaNacimiento);
    const fechaActual = new Date();
    
    let edad = fechaActual.getFullYear() - fechaNacimientoObj.getFullYear();
    const mes = fechaActual.getMonth() - fechaNacimientoObj.getMonth();

    // Si el mes actual es anterior al mes de nacimiento o si es el mismo mes pero el día actual es anterior, resta 1 a la edad
    if (mes < 0 || (mes === 0 && fechaActual.getDate() < fechaNacimientoObj.getDate())) {
        edad--;
    }

    // Si la edad es válida, se asigna al input, de lo contrario se borra
    if (edad >= 0) {
        document.getElementById('edad').value = edad;
    } else {
        document.getElementById('edad').value = '';
        alert('La fecha de nacimiento es incorrecta.');
    }
}

// Función para validar el formulario y asegurarse de que no haya números negativos
function validarFormulario() {
    const estatura = document.getElementById('estatura').value;
    const peso = document.getElementById('peso').value;
    const telefono = document.getElementById('telefono').value;

    // Validar estatura y peso
    if (estatura < 0 || peso < 0) {
        alert('La estatura y el peso no pueden ser números negativos.');
        return false; // Detiene el envío del formulario
    }

    // Validar que el número de teléfono tenga exactamente 10 dígitos
    if (telefono.length !== 10) {
        alert('El número de teléfono debe tener exactamente 10 dígitos.');
        return false;
    }

    return true; // Envía el formulario si todo es correcto
}
