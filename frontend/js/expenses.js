// ========================================
// FINAI - EXPENSES
// ========================================

const EXPENSE_API =
    "http://127.0.0.1:5000/api/expenses";


// Add expense
async function addExpense(event) {

    event.preventDefault();

    const amount =
        document.getElementById("amount")?.value;

    const category =
        document.getElementById("category")?.value;

    const description =
        document.getElementById("description")?.value;

    const date =
        document.getElementById("date")?.value;

    if (!amount || !category || !date) {

        alert("Please fill required fields.");

        return;
    }

    try {

        const response = await fetch(EXPENSE_API, {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },

            body: JSON.stringify({
                amount: Number(amount),
                category: category,
                description: description,
                date: date
            })
        });

        const data = await response.json();

        if (response.ok) {

            alert("Expense added successfully!");

            document
                .getElementById("expenseForm")
                ?.reset();

            loadExpenses();

        } else {

            alert(
                data.message ||
                "Failed to add expense."
            );
        }

    } catch (error) {

        console.error(error);

        alert("Server connection failed.");
    }
}


// Load expenses
async function loadExpenses() {

    try {

        const response = await fetch(
            EXPENSE_API,
            {
                headers: {
                    "Authorization":
                        `Bearer ${getToken()}`
                }
            }
        );

        const data = await response.json();

        displayExpenses(data);

    } catch (error) {

        console.error(error);
    }
}


// Display expenses
function displayExpenses(data) {

    const table =
        document.getElementById("expenseTable");

    if (!table) return;

    table.innerHTML = "";

    data.forEach(item => {

        table.innerHTML += `
            <tr>
                <td>${item.category}</td>
                <td>₹${item.amount}</td>
                <td>${item.description || "-"}</td>
                <td>${item.date}</td>
            </tr>
        `;

    });
}