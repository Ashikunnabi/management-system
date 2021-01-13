
class Login {
    constructor() {
        this._helper = new Helper();
        this._api_v1 = '/api/v1/';

        this.Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })
    }

    login(data) {
        let object = this;
        let url = this._api_v1 + 'login/';
        var promise = this._helper.httpRequestWithoutHeaders(url, 'POST', JSON.stringify(data));
        promise.done(function (response) {
            // store token in browser session
            object._helper.storage.saveStorage('local', 'token', response)
            // redirect to dashboard
            window.location.replace("/");
        });
        promise.fail(function (response) {
            // send back to login page with an error notification
            object.Toast.fire({
                icon: 'error',
                title: "<p style='color: dark;'>" + response.responseJSON.detail + "<p>",
                background: '#ffabab',
            });
            // $.growl(response.responseJSON.detail, {type: 'danger'});
        });
    }
}

let login = new Login();
// removing token if available
let helper = new Helper();
helper.storage.removeStorage('local', 'token');

function do_login() {
    let username = $('#username').val();
    let password = $('#password').val();
    if (username === '' || password === '') {
        login.Toast.fire({
                icon: 'error',
                title: "<p style='color: dark;'>Fill up both fields.<p>",
                background: '#ffabab',
            });
        // $.growl('Fill up both fields.', {type: 'danger'});
    } else {
        login.login(
            {'username': username, 'password': password}
        );
    }
}

$(document).on('click', '#login', function (e) {
    do_login();
});

$(document).on('keypress', function (e) {
    if (e.which === 13) {
        do_login();
    }
});

