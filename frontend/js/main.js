function successQuery(){
    //Выполняется в случае успешного отправления json
    $('form.appeal-form')[0].reset();
    alert('Ваше сообщение успешно отправлено')
}

function failQuery(){
    //Выполняется в случае ошибки отправления json
    alert('Сообщение не удалось отправить')
}

function sendData(){
    // Отправка данных из формы на сервер
    $('form.appeal-form').submit(function (e) {
        e.preventDefault();

        //формирование json файла
        let jsondata = {};
        let formdata = $('form.appeal-form').serializeArray();
        $.map(formdata, function (el) {
            jsondata[el['name']] = el['value'];            
        });
        
        //отправка json на сервер
        $.ajax({
            url: 'http://localhost:8080/',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(jsondata),
            success: () => {
                //Выполняется в случае успешного отправления json
                $('form.appeal-form')[0].reset();
                alert('Ваше сообщение успешно отправлено')
            },
            error: () =>{
                //Выполняется в случае ошибки отправления json
                alert('Сообщение не удалось отправить')
            }
        });

    });
}

$(function () {
    // Запустить после загрузки страницы страницы
    sendData();
});