function getInput() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("pwd").value;
    var verifyPassword = document.getElementById("verifypwd").value;
    // verifyPassword(password, verifyPassword);  will be used before accepting input
    var email = document.getElementById("email").value;
    var address = document.getElementById("address").value;
    var cardNumber = document.getElementById("cardNum").value;
    return [username,password, email, address, cardNumber]
}

function verifyPassword(password, verifyPassword) {
    if (password == verifyPassword) {
        return true;
    }
    else {
        return false;
    }
}
