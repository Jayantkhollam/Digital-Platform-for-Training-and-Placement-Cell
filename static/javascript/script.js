// Function to show the subscribe success alert
function showSubscribeAlert() {
    var alert = document.getElementById("subscribe-success-alert");
    alert.style.display = "flex";
    setTimeout(function() {
        alert.style.display = "none";
    }, 3000); // Hide the alert after 3 seconds
}

// Function to show the unsubscribe success alert
function showUnsubscribeAlert() {
    var alert = document.getElementById("unsubscribe-success-alert");
    alert.style.display = "flex";
    setTimeout(function() {
        alert.style.display = "none";
    }, 3000); // Hide the alert after 3 seconds
}

// Function to handle the subscribe button click event
document.getElementById("subscribe-btn").addEventListener("click", function() {
    // Call the showSubscribeAlert function
    showSubscribeAlert();
});

// Function to handle the unsubscribe button click event
document.getElementById("unsubscribe-btn").addEventListener("click", function() {
    // Call the showUnsubscribeAlert function
    showUnsubscribeAlert();
});







