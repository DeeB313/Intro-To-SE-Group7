function getInput() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("pwd").value;
    var verifyPassword = document.getElementById("verifypwd").value;
    var email = document.getElementById("email").value;
    var address = document.getElementById("address").value;
    var cardNumber = document.getElementById("cardNum").value;
    return [username, password, verifyPassword, email, address, cardNumber]
}

function verifyPassword(password, verifyPassword) {
    if (password == verifyPassword) {
        return true;
    }
    else {
        return false;
    }
}

function navigateHome() {
    location.href = "home.html";
}

function register() {
    var information = getInput();
    verifyPassword(information[1], information[2]);
    // do something with information

    location.href = "login.html"
}
