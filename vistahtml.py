def vistaHtml(mensaje, edad):    
    return f"""
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .card {{
                width: 190px;
                background: white;
                padding: .4em;
                border-radius: 6px;
                margin-bottom: 20px;
            }}
            .card-image {{
                background-color: rgb(236, 236, 236);
                width: 100%;
                height: 130px;
                border-radius: 6px 6px 0 0;
                transition: transform 0.3s;
            }}
            .card-image:hover {{
                transform: scale(0.98);
            }}
            .category {{
                text-transform: uppercase;
                font-size: 0.7em;
                font-weight: 600;
                color: rgb(63, 121, 230);
                padding: 10px 7px 0;
            }}
            .category:hover {{
                cursor: pointer;
            }}
            .heading {{
                font-weight: 600;
                color: rgb(88, 87, 87);
                padding: 7px;
            }}
            .heading:hover {{
                cursor: pointer;
            }}
            .author {{
                color: gray;
                font-weight: 400;
                font-size: 11px;
                padding-top: 20px;
            }}
            .name {{
                font-weight: 600;
            }}
            .name:hover {{
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Información del Usuario</h5>
                <p class="card-text user-age"><strong>{edad}</strong> años de edad</p>
                <hr>
                <div class="message">
                    {mensaje}
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image"></div>
            <div class="category">Ilustración</div>
            <div class="heading">
                Un encabezado que debe ocupar más de dos líneas
                <div class="author">Por <span class="name">Abi</span> hace 4 días</div>
            </div>
        </div>
    </body>
    </html>
    """