class Registration {
    constructor() {
        this._helper = new Helper();
        this._api_v1 = '/api/v1/';
    }
    
    registration(data){ 
        let url = this._api_v1+'Registration/';
        var promise = this._helper.httpRequest(url, 'POST', JSON.stringify(data));
            console.log(this._helper.storage);
            console.log(promise);
        promise.done(function (response) {
            // redirect to dashboard
            window.location.replace("/");
        });
        promise.fail(function (response) {
            // send back to registration page with an error notification
            alert(response.responseJSON.detail);
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
        alert('Fill all fields.');
    } else {
        registration.registration(
            {'username': username, 'password': password}
        );
    }
});