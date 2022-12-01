function sendData(){
    // Отправка данных из формы на сервер

    $('form.appeal-form').submit(function (e) {
        e.preventDefault();
        let jsondata = {};
        let formdata = $('form.appeal-form').serializeArray();
        $.map(formdata, function (el) {
            jsondata[el['name']] = el['value'];            
        });
        console.log(jsondata);
    });
}

$(function () {
    // Запустить после загрузки страницы страницы

    sendData();
});