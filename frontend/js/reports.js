// ========================================
// FINAI - REPORTS & CHARTS
// ========================================

const REPORT_API =
    "http://127.0.0.1:5000/api/reports";


// Load reports
async function loadReports() {

    try {

        const response = await fetch(
            REPORT_API,
            {
                headers: {
                    "Authorization":
                        `Bearer ${getToken()}`
                }
            }
        );

        const data = await response.json();

        createExpenseChart(data);

        createIncomeExpenseChart(data);

    } catch (error) {

        console.error(error);
    }
}


// Expense category chart
function createExpenseChart(data) {

    const canvas =
        document.getElementById("expenseChart");

    if (!canvas) return;

    new Chart(canvas, {

        type: "pie",

        data: {

            labels: data.categories || [],

            datasets: [{
                data: data.category_values || []
            }]
        },

        options: {

            responsive: true,

            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}


// Income vs expense
function createIncomeExpenseChart(data) {

    const canvas =
        document.getElementById("incomeExpenseChart");

    if (!canvas) return;

    new Chart(canvas, {

        type: "bar",

        data: {

            labels: data.months || [],

            datasets: [

                {
                    label: "Income",
                    data: data.income || []
                },

                {
                    label: "Expenses",
                    data: data.expenses || []
                }

            ]
        },

        options: {

            responsive: true,

            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}