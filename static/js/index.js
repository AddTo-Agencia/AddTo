
$(document).ready(function () {
    // Diccionario de características físicas
    const caracteristicas_fisicas = {
        "Género": ['hombre', 'mujer'],
        "Tono de piel": [
            "blanco",
            "trigueño",
            "moreno",
            "oscuro",
            "negro",
            "blanca",
            "trigueña",
            "morena",
            "oscura",
            "negra",
        ],
        "Forma del rostro": [
            "redondo",
            "ovalado",
            "cuadrado",
            "rectangular",
            "corazón",
            "alargado",
            "diamante",
        ],
        "Contextura física": [
            "delgado",
            "normal",
            "atlético",
            "corpulento",
            "gordo",
        ],
        "Longitud del cuello": ["corto", "medio", "largo"],
        "Ancho de muñeca": ["delgada", "media", "ancha"],
        Estatura: ["baja", "alta"],
        Altura: ["baja", "media", "alta"],
        "Textura de piel": ["suave", "áspera", "mixta", "grasosa", "seca"],
        "Color de ojos": [
            "azules",
            "verdes",
            "marrón",
            "avellana",
            "gris",
            "negros",
        ],
        "Color de cabello": ["castaño", "negro", "canoso", "rubio", "pelirrojo"],
        "Estilo de cabello": [
            "corto",
            "medio",
            "largo",
            "rizado",
            "liso",
            "ondulado",
        ],
        "Personalidad": ['tranquilo', 'introvertido', 'cauteloso', 'convencional',
            'sociable', 'reservado', 'conformista', 'pragmático', 'rígido',
            'humilde', 'paciente', 'resiliente', 'negativo', 'conservador',
            'extrovertido', 'optimista', 'seguro', 'aventurero', 'ambicioso',
            'idealista', 'adaptable', 'curioso', 'emocional', 'innovador',
            'creativo', 'decidido', 'racional', 'minucioso', 'descuidado',
            'indeciso', 'apático', 'impaciente', 'tranquila', 'introvertida',
            'cautelosa', 'decidida', 'pragmática', 'rígida', 'intolerante',
            'descuidada', 'conservadora.', 'extrovertida', 'segura',
            'aventurera', 'creativa', 'tolerante', 'empática', 'curiosa',
            'arrogante', 'innovadora.', 'indecisa', 'planificadora', 'frágil',
            'minuciosa', 'innovadora', 'reservada', 'conservadora', 'empático',
            'mionuciosa', 'innovador.', 'descudiada.', 'conservador.',
            'planificador', 'perseverante', 'disciplinado', 'espontáneo',
            'fragil', 'emocional descuidada', 'mininuciosa', 'convenciona',
            'organizada', 'ambiciosa','descuidada.', 'extrovetido',
            'conservardor.', 'pragmático tolerante', 'rígifo', 'convecional',
            'minucioso descuidado', 'organizado'],

        "Evento": ['boda', 'matrimonio', 'pre-nupcial', 'propuesta', 'compromiso',
            'cena de empresa', 'almuerzos ejecutivos', 'fiesta de cumpleaños',
            'reunion familiar', 'comer con amigos', 'evento deportivo',
            'concierto', 'navidad y año nuevo', 'día de la madre',
            'día del padre.', 'quinceañera', 'quince años',
            'eventos de caridad', 'aniversario', 'almuerzo ejecutivo',
            'comida con amigos', 'eventos de cariudad', 'graduaciones',
            'aniversarios', 'fiestas de cumpleaños', 'reuniones familiares',
            'gala', 'evento de caridad', 'graduación',
            'ceremonia de premiación', 'exposición de arte', 'inauguración.',
            'comida con amgios', 'reunión familiar', 'quinceaños',
            'san valentín', 'evento de networking', 'cena con amigos',
            'navidad', 'año nuevo.', 'bodas', 'recepción dimplomática',
            'reunión de negocios', 'inauguruación.']
    };



    // Función para verificar cuántas características físicas están presentes en la descripción
    function contarCaracteristicas(text) {
        let count = 0;

        Object.values(caracteristicas_fisicas).forEach((suggestions) => {
            suggestions.forEach((item) => {
                const regex = new RegExp(`\\b${item}\\b`, "i"); // Buscar coincidencias exactas, no parciales
                if (regex.test(text)) {
                    count++;
                }
            });
        });

        return count;
    }

    // Manejar cambios en el campo de texto
    $("#name").on("input", function () {
        const campo = $(this).val();
        const caracteristicasDetectadas = contarCaracteristicas(campo);

        // Habilitar el botón si hay al menos 2 características detectadas
        if (caracteristicasDetectadas >= 2) {
            $("#toggle-suggestions").prop("disabled", false);
        } else {
            $("#toggle-suggestions").prop("disabled", true);
        }
    });

    $("#characteristics-list").on("click", function() {
        $("#suggestions").prop("hidden", false);
    })


 // Manejar clics en los elementos <li> de sugerencias usando delegación de eventos
document.getElementById("characteristics-list").addEventListener("click", (event) => {
    if (event.target.tagName === "LI") {
        const category = event.target.getAttribute("data-category");
        const suggestions = caracteristicas_fisicas[category] || ["No hay sugerencias para esta categoría."];

        // Mostrar sugerencias en el div correspondiente
        const suggestionsHTML = `
        <strong>Sugerencias para ${category}:</strong> 
        <a href="#model" id="quitar-rec" class="btn btn-danger">
            <i class="fa-solid fa-trash"></i>
        </a>
            <ul class="list-disc pl-5">
                ${suggestions.map((item) => `<li>${item}</li>`).join("")}
            </ul>
        `;

        document.getElementById("suggestions").innerHTML = suggestionsHTML;
        $('#suggestions').prop("hidden", false);
    }
});

// Delegar el evento 'click' en el documento para el botón de quitar sugerencias
document.addEventListener("click", (event) => {
    if (event.target.matches("#quitar-rec, #quitar-rec *")) {
        $("#suggestions").empty(); // Limpiar sugerencias
    }
    if (event.target.matches("#quitar-images, #quitar-images *")) {
        $("#recommended-images").empty(); // Limpiar sugerencias
    }
});


    // Handle form submit
    // Start of Selection
    $("#toggle-suggestions").on("click", function (event) {
        event.preventDefault();

        const nameInput = $("#name").val();
        const imagesContainer = $("#recommended-images");
        imagesContainer.empty(); // Limpiar imágenes previas

        $("#spinner").removeClass("hidden");
        $(".container").addClass("opacity-50");

        // Simulación de petición AJAX
        $.ajax({
            url: "/predict",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ texto: nameInput }),
            success: function (data) {
                console.log(data);
                
                    // Si `data.images` es un array de URLs de imágenes
                if (data.images && data.images.length > 0) {
                    imagesContainer.empty(); // Limpiar imágenes previas
                  
                    data.images.forEach(function (imageUrl, index) {
                        const imageElement = `

                <div class="image-thumb card cursor-pointer">
                    <img src="${imageUrl}" class="rounded-full cursor-pointer" alt="Image ${index + 1}" data-index="${index}">
                </div>

                `;
                        imagesContainer.append(imageElement);
                    });
                    
                  
                }
            },
            error: function (error) {
                console.error("Error:", error);
            },
            complete: function () {
                $("#spinner").addClass("hidden");
                $(".container").removeClass("opacity-50");
            },
        });

        // Agregar botón de eliminar al contenedor
        
    });

    // Al hacer clic en una miniatura, abrir el modal y mostrar la imagen seleccionada en el carrusel
    $(document).on("click", ".image-thumb img", function () {
        const imageIndex = $(this).data("index");
        $("#carouselInner").empty(); // Limpiar el carrusel

        // Añadir imágenes al carrusel
        $("#recommended-images img").each(function (index) {
            const isActive = index === imageIndex ? "active" : "";
            const carouselItem = `
        <div class="carousel-item ${isActive}">
          <img src="${$(this).attr("src")}" class="d-block w-100" alt="Image ${index + 1
                }">
        </div>
      `;
            $("#carouselInner").append(carouselItem);
        });

        $("#imageCarouselModal").modal("show");
    });

    // Mostrar/Ocultar sugerencias
    $("#toggle-suggestions").on("click", function () {
        $("#suggestions-container").toggleClass("hidden");
    });

    $("#hide-suggestions").on("click", function () {
        $("#suggestions-container").addClass("hidden");
    });



   
});