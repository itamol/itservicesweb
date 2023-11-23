// funcionalidad "Menu Hamburguesa"
const menu = document.querySelector(".menu-conteiner");
const openMenuBtn = document.querySelector(".open-menu");
const closeMenuBtn = document.querySelector(".close-menu");

window.addEventListener("load", (e) => {
    e.preventDefault();

    function toggleMenu() {
        menu.classList.toggle("menu_abierto");


        openMenuBtn.addEventListener("click", toggleMenu);
        closeMenuBtn.addEventListener("click", toggleMenu);

        const enlaces = document.querySelectorAll(".menu-conteiner a");

        enlaces.forEach(enlace => {
            enlace.addEventListener("click", function () {
                menu.classList.remove("menu_abierto");
            })
        })


        // Funcionalidad "Selector"
        let menuItem = document.querySelectorAll(".menu-item");
        menuItem.forEach(function (item) {
            item.addEventListener("click", function (e) {
                const currentItem = document.querySelector(".active");
                currentItem.classList.remove("active");
                e.target.classList.add("active");
            });
        });

        // Funcionalidad Dark-Mode 
        const lightMode = document.querySelector(".light-mode");
        const darkMode = document.querySelector(".dark-mode");

        lightMode.addEventListener("click", setDarkMode);
        darkMode.addEventListener("click", setlightMode);

        function setDarkMode() {
            setUserTheme("dark");
        }

        function setlightMode() {
            setUserTheme("light");
        }

        function setUserTheme(newTheme) {
            document.documentElement.setAttribute("data-theme", newTheme);
        }
        }
    })

    //MENU PRINCIPAL
const cerrarMenuBtn = document.getElementById('cerrar-menu');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

// Agrega un evento de clic al botón de cerrar el menú
cerrarMenuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('nav-menu_visible');
    });

    // Muestra el menú desplegable al hacer clic en los items
navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('nav-menu_visible');

    if (navMenu.classList.contains("nav-menu_visible")) {
        navToggle.setAttribute("aria-label", "Cerrar Menú");
      } else {
        navToggle.setAttribute("aria-label", "Abrir Menú");
      }
    });



     //EFECTO AL DAR CLIC A LOS ENLACES DEL MENU
     $(document).ready(function() {
        $('a[href^="#"]').on('click', function(event) {
            event.preventDefault();
    
            var target = this.hash;
            var $target = $(target);
    
            $('html, body').animate({
                'scrollTop': $target.offset().top
            }, 500, 'linear', function() {
                $target.fadeIn(500);
                window.location.hash = target;
            });
        });
    });
    
     // MENSAJE DE REGISTRO
    document.addEventListener('DOMContentLoaded', function () {
        // Obtén el mensaje flash desde el elemento HTML
        var flashDataElement = document.getElementById('flash-data');
        var successMessage = flashDataElement ? flashDataElement.getAttribute('data-success-message') : null;
    
        // Muestra la alerta de SweetAlert si hay un mensaje
        if (successMessage) {
            Swal.fire({
                title: 'Registro exitoso',
                text: successMessage,
                icon: 'success',
                position: 'center', // Centrar la alerta en la pantalla
                showConfirmButton: false, // No mostrar el botón de confirmación
                timer: 2500, // Cerrar automáticamente después de 2 segundos
                customClass: {
                    container: 'small-alert' // Aplica la clase personalizada a la ventana modal
                },
            });
        }
    });
    
    //RESPONDER CORREO ELECTRONICO AL CLIENTE
    function abrirCorreo(direccionCorreo) {
        // Abre el cliente de correo electrónico predeterminado
        window.location.href = 'mailto:' + direccionCorreo;
    }