(function($) {

    function onFormSubmit(event) {
        var data = $(event.target).serializeArray();

        var thesis = {};
        for (var i = 0; i < data.length; i++) {
            var key = data[i].name;
            var value = data[i].value;
            thesis[key] = value
        }

        var list_element = $('<li>');

        list_element.html(thesis.thesis_year + ' ' + thesis.thesis_title + ' - by ' + thesis.thesis_createdby + thesis.thesis_createdby + ' ' + '<br><a href=\"/delete/' + thesis.id + '\"><button id=\"delete\" type=\"submit\">Delete</button></a>' + ' ' + '<a href=\"/edit/' + thesis.id + '\"><button id=\"edit\" type=\"submit\">Edit</button></a><br>');

        var thesis_entry_api = '/api/thesis'
        $.post(thesis_entry_api, thesis, function(response){
            if (response.status = 'OK'){
                var full_detail = response.data.thesis_year + ' ' + response.data.thesis_title + ' - by ' + response.data.thesis_createdby + ' ' + '<br><a href=\"/delete/' + response.data.id + '\"><button id=\"delete\" type=\"submit\">Delete</button></a>' + ' ' + '<a href=\"/edit/' + response.data.id + '\"><button id=\"edit\" type=\"submit\">Edit</button></a><br>'

                $('.thesis-list').prepend('<li>' + full_detail + '</li>');
                $('.create-form').trigger("reset");
            }else {

            }
        });

        // $('a').click(function(){        
        //     $(this).parent().remove();      
        // });

        return false;
    }

    function loadAllThesis(){
        var thesis_entry_api = '/api/thesis';
        $.get(thesis_entry_api, {}, function(response){
            console.log('Thesis list', response)
            response.data.forEach(function(thesis){
                var full_detail = thesis.thesis_year + ' ' + thesis.thesis_title + ' - by ' + thesis.thesis_createdby + ' ' + '<br><a href=\"/delete/' + thesis.id + '\"><button id=\"delete\" type=\"submit\">Delete</button></a>' + ' ' + '<a href=\"/edit/' + thesis.id + '\"><button id=\"edit\" type=\"submit\">Edit</button></a><br>';
                $('.thesis-list').append('<li>' +  full_detail + '</li>')
            });
        });
    }

    function onRegistrationForm(event) {
        var data = $(event.target).serializeArray();

        var user = {};
        for (var i = 0; i < data.length; i++) {
            var key = data[i].name;
            var value = data[i].value;
            user[key] = value
        }

        var api_register = '/api/user';
        $.post(api_register, user, function(response){
            if (response.status = 'OK'){
                $(location).attr('href', '/home');
                console.log();
                return false;
            }
        })

        return false;
    }

    $('.registration-form').submit(onRegistrationForm)
    $('.create-form').submit(onFormSubmit)
    loadAllThesis()
})(jQuery)