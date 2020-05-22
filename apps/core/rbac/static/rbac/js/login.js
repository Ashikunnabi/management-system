class Login {
    constructor() {
        this._helper = new Helper();
        this._api_v1 = '/api/v1/';
    }
    
    login(data){ 
        let url = this._api_v1+'login/';
        var promise = this._helper.httpRequest(url, 'POST', JSON.stringify(data));
        promise.done(function (response) {
            // store token in browser session
            // redirect to dashboard            
        });
        promise.fail(function (response) {
            // send back to login page with error notification
        });
    }
}

let login = new Login();

$(document).on('click', '#login', function(e){
    let username = $('#username').val();
    let password = $('#password').val();
    if (username==='' || password===''){
        alert('fill up both fields.');
    } else {
        login.login(
            {'username': username, 'password': password}
        );
    }
});