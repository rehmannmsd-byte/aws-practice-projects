const API_URL = "https://qusdou5f5a.execute-api.ap-south-1.amazonaws.com/contact";

const form = document.getElementById("contactForm");
const status = document.getElementById("status");
const button = document.getElementById("sendBtn");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    button.disabled = true;
    button.innerText = "Sending...";

    status.style.color = "black";
    status.innerText = "Sending your message...";

    const payload = {
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        subject: document.getElementById("subject").value.trim(),
        message: document.getElementById("message").value.trim()
    };

    console.log("Payload:", payload);

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        console.log("Response:", result);

        if (response.ok) {

            status.style.color = "green";
            status.innerHTML = "✅ Thank you! Your message has been sent successfully.";

            form.reset();

        } else {

            status.style.color = "red";
            status.innerHTML = "❌ " + result.message;

        }

    } catch (error) {

        console.error(error);

        status.style.color = "red";
        status.innerHTML = "❌ Unable to connect to the API.";

    }

    button.disabled = false;
    button.innerText = "Send Message";

});