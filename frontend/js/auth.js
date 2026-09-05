// ========================================
// FINAI - AUTHENTICATION
// ========================================

const API_URL = "http://127.0.0.1:5000/api";


// ========================================
// REGISTER
// ========================================

async function registerUser(event) {

    event.preventDefault();

    const name = document.getElementById("name")?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const password = document.getElementById("password")?.value;

    if (!name || !email || !password) {
        alert("Please fill all fields.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/auth/register`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Registration successful!");

            window.location.href = "login.html";

        } else {

            alert(
                data.message ||
                "Registration failed."
            );
        }

    } catch (error) {

        console.error("Register error:", error);

        alert("Unable to connect to server.");
    }
}


// ========================================
// LOGIN
// ========================================

async function loginUser(event) {

    event.preventDefault();

    const email =
        document.getElementById("email")?.value.trim();

    const password =
        document.getElementById("password")?.value;

    if (!email || !password) {

        alert("Please enter email and password.");

        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        console.log("Login response:", data);

        if (response.ok) {

            // Save JWT token
            localStorage.setItem(
                "token",
                data.token
            );

            // Save user
            if (data.user) {

                localStorage.setItem(
                    "user",
                    JSON.stringify(data.user)
                );
            }

            alert("Login successful!");

            window.location.href =
                "dashboard.html";

        } else {

            alert(
                data.message ||
                "Invalid email or password."
            );
        }

    } catch (error) {

        console.error("Login error:", error);

        alert("Unable to connect to server.");
    }
}


// ========================================
// LOGOUT
// ========================================

function logoutUser() {

    localStorage.removeItem("token");

    localStorage.removeItem("user");

    window.location.href = "login.html";
}


// ========================================
// CHECK LOGIN
// ========================================

function checkAuthentication() {

    const token =
        localStorage.getItem("token");

    if (!token) {

        window.location.href =
            "login.html";

        return false;
    }

    return true;
}


// ========================================
// GET TOKEN
// ========================================

function getToken() {

    return localStorage.getItem("token");
}