
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

    function autoResize(textarea) {
        textarea.style.height = 'auto'; // Reset height to calculate new height
        textarea.style.height = (textarea.scrollHeight) + 'px'; // Set height based on scroll height
      }

    // Manejar cambios en el campo de texto
    $("#name").on("input", function () {
        const campo = $(this).val();
        const caracteristicasDetectadas = contarCaracteristicas(campo);

        // Habilitar el botón si hay al menos 2 características detectadas
        if (caracteristicasDetectadas >= 2) {
            $("#toggle-suggestions").prop("disabled", false);
            $("#toggle-suggestions").css("background-color", "#a8845c");
        } else {
            $("#toggle-suggestions").prop("disabled", true);
            $("#toggle-suggestions").css("background-color", "#bca484");
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

$("#select").on("change", function (event) {
   const valor = $(this).val();
   $('.hombre, .mujer').attr('hidden', true); // Ocultar todos los elementos al principio

   $('#name').val('');
   if(valor == 'hombre'){
      $('.hombre').removeAttr('hidden'); // Mostrar solo los elementos de hombre
   } else if(valor == 'mujer'){
      $('.mujer').removeAttr('hidden'); // Mostrar solo los elementos de mujer
   }
})


const enviarReaccion = () =>{
      // Obtener la reacción seleccionada
      const selectedReaction = $('input[name="reaction"]:checked').val();
    
      // Verificar si hay una reacción seleccionada
  
      if (selectedReaction) {
        // Enviar la reacción al endpoint /send
        $("#reacionContainer").attr("hidden",true);
        $.ajax({
          url: '/send',
          method: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({ 
              mensaje: "El usuario presiono el boton: "+selectedReaction ,
              edad:"Desconodido los"
          
          }),
          success: function(response) {
            console.log('Reacción enviada:', response);
            //alert('Tu reacción ha sido enviada: ' + selectedReaction);
          },
          error: function(error) {
            console.error('Error al enviar la reacción:', error);
          }
        });
      } else {
        alert('Por favor, selecciona una reacción antes de enviar.');
      }
}

// Delegación de eventos para el botón enviado dinámicamente
$(document).on('click', '#send-btn', function() {
    enviarReaccion();
});



    // Handle form submit
    // Start of Selection
    $("#toggle-suggestions").on("click", function (event) {
        event.preventDefault();

        let nameInput = $("#name").val();
        const imagesContainer = $("#recommended-images");
        imagesContainer.empty(); // Limpiar imágenes previas
        const genero = $(this).val();

        nameInput += ","+genero;

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
        
        // Limpiar imágenes previas
        imagesContainer.empty(); 

        $("#reacionContainer").removeAttr("hidden",false);
        $('#reacionContainer').html(`
        
        <legend class="card-title mb-3">¿Te gustó la recomendación?</legend>

        <!-- Me gusta -->
        <label for="me-gusta" class="d-flex align-items-center mb-3 p-2 border rounded hover-shadow">
        <span class="me-2">👍</span> Me gusta
        <input type="radio" name="reaction" class="form-check-input ms-auto" id="me-gusta" value="Me gusta" />
        </label>

        <!-- No me gusta -->
        <label for="no-me-gusta" class="d-flex align-items-center mb-3 p-2 border rounded hover-shadow">
        <span class="me-2">👎</span> No me gusta
        <input type="radio" name="reaction" class="form-check-input ms-auto" id="no-me-gusta" value="No me gusta" />
        </label>

        <!-- Indiferente -->
        <label for="indiferente" class="d-flex align-items-center mb-3 p-2 border rounded hover-shadow">
        <span class="me-2">😐</span> Indiferente
        <input type="radio" name="reaction" class="form-check-input ms-auto" id="indiferente" value="Indiferente" />
        </label>

        <!-- Normal -->
        <label for="normal" class="d-flex align-items-center mb-3 p-2 border rounded hover-shadow">
        <span class="me-2">🙂</span> Normal
        <input type="radio" name="reaction" class="form-check-input ms-auto" id="normal" value="Normal" />
        </label>
        <button id="send-btn" class="btn btn-success">Enviar</button>

            `)
        // Recorrer todas las propiedades del objeto data
        Object.keys(data).forEach(function (key) {
            // Verificar si la propiedad comienza con "images"
            if (key.startsWith("images") && data[key] && data[key].length > 0) {
                // Recorrer cada array de imágenes dentro de la propiedad
                data[key].forEach(function (imageUrl, index) {
                    const imageElement = `
                        <div class="image-thumb card cursor-pointer w-auto">
                            <img src="${imageUrl}" class="w-full h-auto rounded-lg shadow-md" alt="Image ${index + 1}" data-index="${index}">
                        </div>
                    `;
                    imagesContainer.append(imageElement);
                });
            }
        });





    },
    error: function (error) {
        console.error("Error:", error);
    },
    complete: function () {
        $("#spinner").addClass("hidden");
        $(".container").removeClass("opacity-50");
    },
});

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