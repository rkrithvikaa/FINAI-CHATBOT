// ========================================
// FINAI - SAVINGS GOALS
// ========================================

const SAVINGS_API =
    "http://127.0.0.1:5000/api/savings";


// Add savings goal
async function addSavingsGoal(event) {

    event.preventDefault();

    const name =
        document.getElementById("goalName")?.value;

    const target =
        document.getElementById("targetAmount")?.value;

    if (!name || !target) {

        alert("Please enter goal name and target amount.");

        return;
    }

    try {

        const response = await fetch(
            SAVINGS_API,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${getToken()}`
                },

                body: JSON.stringify({
                    name: name,
                    target_amount: Number(target)
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Savings goal created!");

            document
                .getElementById("savingsForm")
                ?.reset();

            loadSavingsGoals();

        } else {

            alert(
                data.message ||
                "Unable to create goal."
            );
        }

    } catch (error) {

        console.error(error);

        alert("Server connection failed.");
    }
}


// Load goals
async function loadSavingsGoals() {

    try {

        const response = await fetch(
            SAVINGS_API,
            {
                headers: {
                    "Authorization":
                        `Bearer ${getToken()}`
                }
            }
        );

        const data = await response.json();

        displaySavingsGoals(data);

    } catch (error) {

        console.error(error);
    }
}


// Display goals
function displaySavingsGoals(data) {

    const container =
        document.getElementById("savingsList");

    if (!container) return;

    container.innerHTML = "";

    data.forEach(goal => {

        const percentage =
            goal.target_amount > 0
                ? (goal.saved_amount /
                    goal.target_amount) * 100
                : 0;

        container.innerHTML += `
            <div class="goal-card">

                <h5>${goal.name}</h5>

                <p>
                    ₹${goal.saved_amount || 0}
                    /
                    ₹${goal.target_amount}
                </p>

                <div class="progress">
                    <div
                        class="progress-bar"
                        style="width:${Math.min(percentage, 100)}%">
                    </div>
                </div>

                <small>
                    ${Math.round(percentage)}% completed
                </small>

            </div>
        `;

    });
}