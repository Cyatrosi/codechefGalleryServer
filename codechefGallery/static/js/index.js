function show_hide(show_id, hide_id) {
    document.getElementById(hide_id).style.display = 'none';
    document.getElementById(show_id).style.display = 'block';
}

// =========== Cookie Functions =======
function setCookie(data) {
    document.cookie = JSON.stringify(data);
}
function clearCookie(data) {
    document.cookie = "";
}
function getCookie() {
    var cookies = document.cookie.split(";");
    if (cookies.length > 1) {
        return JSON.parse(cookies[1]);
    }
    return "";
}

// ============ AUTH Functions ========
function validate(username, password) {
    if (!username) {
        alert("Username is required");
        return false;
    }
    if (!password) {
        alert("Password is required");
        return false;
    }
    return true;
}
function login() {
    username = document.getElementById('login-username').value;
    password = document.getElementById('login-password').value;
    if (!validate(username, password)) {
        return false;
    }
    params = {
        "username": username,
        "password": password
    }
    params = JSON.stringify(params);
    var request = httpRequest('POST', 'http://127.0.0.1:8000/users/login/', params);
    request.onload = function () {
        if (this.status == '200') {
            var resp = JSON.parse(this.response);
            if (resp.status == 200) {
                var data = resp.data;
                setCookie(data);
                window.location.href = "/photos";
            } else {
                alert(resp.message);
            }
        } else {
            alert("An error Occured !");
        }
    };
}
function validateSignup() {
    if (!document.getElementById('signup-username').value) {
        alert("Enter Username");
        return false;
    }
    if (!document.getElementById('signup-gender').value) {
        alert("Enter Gender");
        return false;
    }
    if (!document.getElementById('signup-first-name').value) {
        alert("Enter First Name");
        return false;
    }
    if (!document.getElementById('signup-last-name').value) {
        alert("Enter Last Name");
        return false;
    }
    if (!document.getElementById('signup-email').value) {
        alert("Enter Email");
        return false;
    }
    if (!document.getElementById('signup-password').value) {
        alert("Enter Password");
        return false;
    }
    if (!document.querySelector('#upload-file').files[0]) {
        alert("Select Photo");
        return false;
    }
    return true;
}
function signup() {
    if (!validateSignup())
        return false;

    var data = new FormData();
    var request = new XMLHttpRequest();

    data.append('username', document.getElementById('signup-username').value);
    data.append('gender', document.getElementById('signup-gender').value);
    data.append('first_name', document.getElementById('signup-first-name').value);
    data.append('last_name', document.getElementById('signup-last-name').value);
    data.append('email', document.getElementById('signup-email').value);
    data.append('password', document.getElementById('signup-password').value);
    data.append('file', document.querySelector('#upload-file').files[0]);

    request.addEventListener('load', function (e) {
        if (this.status == '200') {
            var resp = this.response
            if (resp.status == 200) {
                alert("Signup Successful !!");
                location.reload();
            } else {
                alert(resp.message);
            }
        } else {
            alert("FAILED!! An error Occured !");
        }

    });

    request.responseType = 'json';
    request.open('POST', 'http://127.0.0.1:8000/users/');
    request.send(data);
}

// ===== FILE Upload Function =====
document.querySelector('#choose-button').addEventListener('click', function () {
    document.querySelector('#upload-file').click();
});
document.querySelector('#upload-file').addEventListener('change', function () {
    var file = this.files[0];
    var mime_types = ['image/jpeg', 'image/png'];

    if (mime_types.indexOf(file.type) == -1) {
        alert('Error : Incorrect file type');
        return;
    }

    // Max 2 Mb allowed
    if (file.size > 2 * 1024 * 1024) {
        alert('Error : Exceeded size 2MB');
        return;
    }

    alert('You have chosen the file ' + file.name);

});
// =====================================
function httpRequest(method, url, params) {
    var request = new XMLHttpRequest();
    request.open(method, url, true);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    if (params == null) {
        request.send();
    } else {
        request.send(params);
    }
    return request;
}