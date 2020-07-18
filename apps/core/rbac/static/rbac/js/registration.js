class Registration {
    constructor() {
        this._helper = new Helper();
        this._api_v1 = '/api/v1/';
    }
    
    registration(data){ 
        let url = this._api_v1+'Registration/';
        var promise = this._helper.httpRequest(url, 'POST', JSON.stringify(data));
        promise.done(function (response) {
            // redirect to dashboard
            window.location.replace("/");
        });
        promise.fail(function (response) {
            // send back to registration page with an error notification
            $.growl(response.responseJSON.detail, { type: 'danger' });
        });
    }
}

let registration = new Registration();

$(document).on('click', '#registration', function(e){
    let first_name = $('#first_name').val();
    let last_name = $('#last_name').val();
    let username = $('#username').val();
    let email = $('#email').val();
    let password = $('#password').val();
    if (first_name==='' || last_name==='' || username==='' || email==='' || password===''){
        $.growl('Fill up all fields.', { type: 'danger' });
    } else {
        registration.registration(
            {'username': username, 'password': password}
        );
    }
});