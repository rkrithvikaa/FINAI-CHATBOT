// ========================================
// FINAI - DASHBOARD
// ========================================

const DASHBOARD_API = "http://127.0.0.1:5000/api";


// Load dashboard
async function loadDashboard() {

    checkAuthentication();

    try {

        const token = getToken();

        const response = await fetch(
            `${DASHBOARD_API}/dashboard`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to load dashboard");
        }

        const data = await response.json();

        updateDashboard(data);

    } catch (error) {

        console.error(error);

        console.log("Dashboard data will load after backend connection.");
    }
}


// Update dashboard cards
function updateDashboard(data) {

    const income = document.getElementById("totalIncome");
    const expense = document.getElementById("totalExpense");
    const balance = document.getElementById("balance");
    const budget = document.getElementById("budget");

    if (income) {
        income.textContent = `₹${data.total_income || 0}`;
    }

    if (expense) {
        expense.textContent = `₹${data.total_expense || 0}`;
    }

    if (balance) {
        balance.textContent = `₹${data.balance || 0}`;
    }

    if (budget) {
        budget.textContent = `₹${data.budget || 0}`;
    }
}


// Load when page opens
document.addEventListener("DOMContentLoaded", () => {

    if (document.body.dataset.page === "dashboard") {
        loadDashboard();
    }

});