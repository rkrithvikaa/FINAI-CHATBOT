// ========================================
// FINAI - PROFILE
// ========================================


// Load profile
async function loadProfile() {

    checkAuthentication();

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/profile",
            {
                headers: {
                    "Authorization":
                        `Bearer ${getToken()}`
                }
            }
        );

        const data = await response.json();

        document.getElementById("name").value =
            data.name || "";

        document.getElementById("email").value =
            data.email || "";

    } catch (error) {

        console.error(error);

    }
}


// Update profile
async function updateProfile(event) {

    event.preventDefault();

    const name =
        document.getElementById("name")?.value;

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/profile",
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${getToken()}`
                },

                body: JSON.stringify({
                    name: name
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Profile updated successfully!");

        } else {

            alert(
                data.message ||
                "Unable to update profile."
            );
        }

    } catch (error) {

        console.error(error);

        alert("Server connection failed.");
    }
}