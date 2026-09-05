// ========================================
// FINAI - BUDGET
// ========================================

const BUDGET_API =
    "http://127.0.0.1:5000/api/budget";


// Add budget
async function addBudget(event) {

    event.preventDefault();

    const category =
        document.getElementById("category")?.value;

    const amount =
        document.getElementById("amount")?.value;

    if (!category || !amount) {

        alert("Please enter category and amount.");

        return;
    }

    try {

        const response = await fetch(
            BUDGET_API,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${getToken()}`
                },

                body: JSON.stringify({
                    category: category,
                    amount: Number(amount)
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Budget saved successfully!");

            document
                .getElementById("budgetForm")
                ?.reset();

            loadBudgets();

        } else {

            alert(
                data.message ||
                "Unable to save budget."
            );
        }

    } catch (error) {

        console.error(error);

        alert("Server connection failed.");
    }
}


// Load budgets
async function loadBudgets() {

    try {

        const response = await fetch(
            BUDGET_API,
            {
                headers: {
                    "Authorization":
                        `Bearer ${getToken()}`
                }
            }
        );

        const data = await response.json();

        displayBudgets(data);

    } catch (error) {

        console.error(error);
    }
}


// Display budgets
function displayBudgets(data) {

    const container =
        document.getElementById("budgetList");

    if (!container) return;

    container.innerHTML = "";

    data.forEach(item => {

        container.innerHTML += `
            <div class="content-card">
                <h5>${item.category}</h5>
                <p>Budget: ₹${item.amount}</p>

                <div class="progress">
                    <div
                        class="progress-bar"
                        style="width:${item.percentage || 0}%">
                    </div>
                </div>
            </div>
        `;

    });
}