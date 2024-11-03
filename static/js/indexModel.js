
$(document).ready(function () {
    // Diccionario de características físicas
    const caracteristicas_fisicas = {
        "Género": ['hombre', 'mujer'],
        "Tono de piel": ["blanco","trigueño","moreno","oscuro","negro","blanca","trigueña","morena","oscura","negra"],
        "Forma del rostro": ["redondo", "ovalado", "cuadrado","rectangular","corazón","alargado","diamante",],
        "Contextura física": ["delgado","normal", "atlético","corpulento","gordo"],
        "Longitud del cuello": ["corto", "medio", "largo"],
        "Ancho de muñeca": ["delgada", "media", "ancha"],
        "Estatura": ["baja", "alta"],
        "Altura": ["baja", "media", "alta"],
        "Textura de piel": ["suave", "áspera", "mixta", "grasosa", "seca"],
        "Color de ojos": ["azules","verdes","marrón","avellana","gris", "negros"],
        "Color de cabello": ["castaño", "negro", "canoso", "rubio", "pelirrojo"],
        "Estilo de cabello": ["corto","medio","largo","rizado","liso","ondulado"],
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
        $("#btnSendReaction").attr("hidden",true);
        $("#reacciones").attr("hidden",true);
        
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



const itemsPerPage = 3;
let currentPage = 0; 
let allImages = [];

// Lógica del botón de sugerencias
$("#toggle-suggestions").on("click", function (event) {
  event.preventDefault();

  let nameInput = $("#name").val();
  const genero = $(this).val();
  nameInput += "," + genero;

  $("#spinner").removeClass("hidden");
  $(".container").addClass("opacity-50");
  $(".container").addClass("disabled");
  
  
  $("#recommended-images").attr("hidden",true);
  $("#btnSendReaction").attr("hidden",true);
  $("#reacciones").attr("hidden",true);
  $("#reacionContainer").attr("hidden",true);

  $.ajax({
    url: "/predict",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ texto: nameInput }),
    success: function (data) {
      console.log(data);
      allImages = []; // Reiniciar el array de imágenes

      // Recorrer todas las propiedades del objeto data
      Object.keys(data).forEach(function (key) {
        if (key.startsWith("images") && data[key] && data[key].length > 0) {
          data[key].forEach(function (imageUrl) {
            allImages.push(imageUrl);
          });
        }
      });

      displayImages();
    },
    error: function (error) {
      console.error("Error:", error);
    },
    complete: function () {
      $("#spinner").addClass("hidden");
      $(".container").removeClass("opacity-50");
      $(".container").removeClass("disabled");
      
      $("#reacionContainer").removeAttr("hidden");
      $("#recommended-images").attr("hidden",false);
      
      setTimeout(()=>{
        $("#btnSendReaction").removeAttr("hidden");
        $("#reacciones").removeAttr("hidden");
        
      },4000)

    },
  });
});

// Función para mostrar imágenes en el carrusel
function displayImages() {
  const imagesContainer = $("#recommended-images");
  imagesContainer.empty(); // Limpiar contenedor

  // Añadir imágenes al contenedor
  allImages.forEach((imageUrl) => {
    const imageElement = `
      <div class="w-1/3 p-2 flex-shrink-0">
        <img src="${imageUrl}" class="w-full h-auto rounded-lg shadow-md" alt="Image">
      </div>
    `;
    imagesContainer.append(imageElement);
  });

  updateSlidePosition();
  updateNavigationButtons();
}

// Función para actualizar la posición del carrusel
function updateSlidePosition() {
  const imagesContainer = $("#recommended-images");
  const translateXValue = -(currentPage * 100);
  imagesContainer.css("transform", `translateX(${translateXValue}%)`);
}

// Función para actualizar los botones de navegación
function updateNavigationButtons() {
  const totalPages = Math.ceil(allImages.length / itemsPerPage);
 // $("#prevButton").toggle(currentPage > 0);
 // $("#nextButton").toggle(currentPage < totalPages - 1);
}

// Manejo de eventos para los botones de navegación
$("#prevButton").on("click", function () {
  if (currentPage > 0) {
    currentPage--;
    updateSlidePosition();
    updateNavigationButtons();
  }
});

$("#nextButton").on("click", function () {
  const totalPages = Math.ceil(allImages.length / itemsPerPage);
  if (currentPage < totalPages - 1) {
    currentPage++;
    updateSlidePosition();
    updateNavigationButtons();
  }
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