function navigateToHome() {
    location.href = "home.html";
}

function navigateToPayment() {
    location.href = "payment.html";
}

function setTotal(total) {
    document.getElementById("total").value = total;
}

function checkout() {
    // temp for navigation
    navigateToPayment();
}