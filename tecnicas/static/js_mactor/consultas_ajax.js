
// Obtiene la descripcion del actorY seleccionado

$('#id_actorY').on('change', DescripcionY);
        function  DescripcionY()
        {
            var id = $(this).val()
            $.ajax({
                data : {'id' : id},
                url : 'actor-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Descripción:' + "</p><p>" + object.
                            descripcion + "</p>";
                    $('#info').html(html)
                }
            });
        }

// Obtiene la descripcion del actorX seleccionado

$('#id_actorX').on('change', DescripcionX);
        function  DescripcionX()
        {
            var id = $(this).val()
            $.ajax({
                data : {'id' : id},
                url : 'actor-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Descripción:' + "</p><p>" + object.
                            descripcion + "</p>";
                    $('#info2').html(html)
                }
            });
        }


// Obtiene la descripcion del objetivoX seleccionado

$('#id_objetivoX').on('change', Descripcion);
        function  Descripcion()
        {
            var id = $(this).val()
            $.ajax({
                data : {'id' : id},
                url : 'objetivo-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Descripción:' + "</p><p>" + object.
                            descripcion + "</p>";
                    $('#info2').html(html)
                }
            });
        }

// Obtiene el registro de la ficha de estrategias de los actores seleccionados

function  Consultar_ficha()
        {
            var id = $(id_actorX).val()
            var id2 = $(id_actorY).val()
            $.ajax({
                data : {'id' : id, 'id2' : id2},
                url : 'actor-ajax2',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Estrategias:' + "</p><p>" + object.
                            info + "</p>";
                    $('#mod_body').html(html)
                }
            });
        }
