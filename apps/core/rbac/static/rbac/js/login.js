class Login {
    constructor() {
        this._helper = new Helper();
        this._api_v1 = '/api/v1/';
    }
    
    login(data){ 
        let url = this._api_v1+'login/';
        var promise = this._helper.httpRequest(url, 'POST', JSON.stringify(data));
            console.log(this._helper.storage);
            console.log(promise);
        promise.done(function (response) {
            // store token in browser session
            this._helper = new Helper();
            this._helper.storage.saveStorage('local', 'token', response)
            // redirect to dashboard
            window.location.replace("/");
        });
        promise.fail(function (response) {
            // send back to login page with an error notification
            alert(response.responseJSON.detail);
        });
    }
}

let login = new Login();
// removing token if available
let helper = new Helper();
helper.storage.removeStorage('local', 'token');

$(document).on('click', '#login', function(e){
    let username = $('#username').val();
    let password = $('#password').val();
    if (username==='' || password===''){
        alert('Fill up both fields.');
    } else {
        login.login(
            {'username': username, 'password': password}
        );
    }
});