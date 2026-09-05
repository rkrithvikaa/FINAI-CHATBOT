// ========================================
// FINAI - INCOME PAGE
// ========================================

const INCOME_API = "http://127.0.0.1:5000/api/income";


// ========================================
// CHECK LOGIN
// ========================================

function checkLogin() {

    const token = localStorage.getItem("token");

    console.log(
        "LOGIN CHECK:",
        token ? "TOKEN FOUND" : "NO TOKEN"
    );

    if (!token) {

        alert("Please login first.");

        window.location.href = "login.html";

        return false;
    }

    return true;
}


// ========================================
// ADD INCOME
// ========================================

async function addIncome(event) {

    event.preventDefault();

    console.log("================================");
    console.log("ADD INCOME STARTED");
    console.log("================================");


    // ----------------------------------------
    // CHECK LOGIN
    // ----------------------------------------

    if (!checkLogin()) {
        return;
    }


    const token = localStorage.getItem("token");


    // ----------------------------------------
    // GET FORM VALUES
    // ----------------------------------------

    const amountElement =
        document.getElementById("amount");

    const sourceElement =
        document.getElementById("source");

    const dateElement =
        document.getElementById("date");

    const notesElement =
        document.getElementById("notes");


    if (!amountElement ||
        !sourceElement ||
        !dateElement ||
        !notesElement) {

        console.error(
            "One or more form elements were not found."
        );

        alert("Income form error.");

        return;
    }


    const amount =
        amountElement.value;

    const source =
        sourceElement.value.trim();

    const date =
        dateElement.value;

    const notes =
        notesElement.value.trim();


    console.log("FORM VALUES:", {
        amount: amount,
        source: source,
        date: date,
        notes: notes
    });


    // ----------------------------------------
    // VALIDATION
    // ----------------------------------------

    if (!amount || !source || !date) {

        alert(
            "Please fill Amount, Source and Date."
        );

        return;
    }


    const numericAmount =
        Number(amount);


    if (isNaN(numericAmount) ||
        numericAmount <= 0) {

        alert(
            "Please enter a valid amount."
        );

        return;
    }


    // ----------------------------------------
    // SEND TO FLASK
    // ----------------------------------------

    try {

        console.log(
            "Sending income to:",
            INCOME_API
        );


        const response = await fetch(
            INCOME_API,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({

                    amount: numericAmount,

                    source: source,

                    date: date,

                    notes: notes

                })
            }
        );


        console.log(
            "POST STATUS:",
            response.status
        );


        const data =
            await response.json();


        console.log(
            "POST RESPONSE:",
            data
        );


        // ----------------------------------------
        // TOKEN EXPIRED
        // ----------------------------------------

        if (response.status === 401) {

            alert(
                "Your login session has expired. Please login again."
            );


            localStorage.removeItem(
                "token"
            );

            localStorage.removeItem(
                "user"
            );


            window.location.href =
                "login.html";


            return;
        }


        // ----------------------------------------
        // SUCCESS
        // ----------------------------------------

        if (response.ok) {

            alert(
                data.message ||
                "Income added successfully!"
            );


            // Clear form

            document
                .getElementById("incomeForm")
                .reset();


            // IMPORTANT:
            // Reload income from database

            await loadIncome();


            console.log(
                "INCOME ADDED AND TABLE RELOADED"
            );


        } else {

            console.error(
                "ADD INCOME FAILED:",
                data
            );


            alert(
                data.message ||
                data.error ||
                "Failed to add income."
            );
        }


    } catch (error) {

        console.error(
            "ADD INCOME ERROR:",
            error
        );


        alert(
            "Unable to connect to the server."
        );
    }


    console.log("================================");
    console.log("ADD INCOME FINISHED");
    console.log("================================");
}


// ========================================
// LOAD INCOME FROM DATABASE
// ========================================

async function loadIncome() {

    console.log("");
    console.log("================================");
    console.log("LOADING INCOME");
    console.log("================================");


    // ----------------------------------------
    // CHECK LOGIN
    // ----------------------------------------

    if (!checkLogin()) {
        return;
    }


    const token =
        localStorage.getItem("token");


    // ----------------------------------------
    // FIND TABLE
    // ----------------------------------------

    const table =
        document.getElementById(
            "incomeTable"
        );


    console.log(
        "TABLE ELEMENT:",
        table
    );


    if (!table) {

        console.error(
            "ERROR: #incomeTable was not found!"
        );

        return;
    }


    // ----------------------------------------
    // REQUEST DATABASE RECORDS
    // ----------------------------------------

    try {

        console.log(
            "GET:",
            INCOME_API
        );


        const response =
            await fetch(
                INCOME_API,
                {
                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${token}`,

                        "Content-Type":
                            "application/json"
                    }
                }
            );


        console.log(
            "GET STATUS:",
            response.status
        );


        const data =
            await response.json();


        console.log(
            "FULL GET RESPONSE:",
            data
        );


        console.log(
            "data.income:",
            data.income
        );


        console.log(
            "data.income is array:",
            Array.isArray(data.income)
        );


        // ----------------------------------------
        // TOKEN EXPIRED
        // ----------------------------------------

        if (response.status === 401) {

            console.error(
                "TOKEN INVALID OR EXPIRED"
            );


            localStorage.removeItem(
                "token"
            );

            localStorage.removeItem(
                "user"
            );


            window.location.href =
                "login.html";


            return;
        }


        // ----------------------------------------
        // SERVER ERROR
        // ----------------------------------------

        if (!response.ok) {

            console.error(
                "GET INCOME FAILED:",
                data
            );


            table.innerHTML = `
                <tr>
                    <td
                        colspan="4"
                        class="text-center text-danger">

                        ${escapeHTML(
                            data.message ||
                            "Failed to load income records."
                        )}

                    </td>
                </tr>
            `;


            return;
        }


        // ========================================
        // GET INCOME ARRAY
        // ========================================

        let incomes = [];


        // Your Flask backend returns:
        //
        // {
        //     success: true,
        //     income: [...]
        // }

        if (Array.isArray(data.income)) {

            incomes =
                data.income;

        }

        // Backup support

        else if (Array.isArray(data.incomes)) {

            incomes =
                data.incomes;

        }

        else if (Array.isArray(data.data)) {

            incomes =
                data.data;
        }


        console.log(
            "FINAL INCOME ARRAY:",
            incomes
        );


        console.log(
            "NUMBER OF INCOME RECORDS:",
            incomes.length
        );


        // ========================================
        // NO RECORDS
        // ========================================

        if (incomes.length === 0) {

            table.innerHTML = `
                <tr>
                    <td
                        colspan="4"
                        class="text-center text-muted">

                        No income records yet.

                    </td>
                </tr>
            `;


            console.log(
                "NO INCOME RECORDS"
            );


            return;
        }


        // ========================================
        // CLEAR TABLE
        // ========================================

        table.innerHTML = "";


        // ========================================
        // DISPLAY EACH INCOME
        // ========================================

        incomes.forEach(
            function(income) {

                console.log(
                    "DISPLAYING INCOME:",
                    income
                );


                const row =
                    document.createElement("tr");


                // Source

                const sourceCell =
                    document.createElement("td");

                sourceCell.textContent =
                    income.source || "-";


                // Amount

                const amountCell =
                    document.createElement("td");

                amountCell.textContent =
                    "₹" +
                    Number(
                        income.amount || 0
                    ).toFixed(2);


                // Date

                const dateCell =
                    document.createElement("td");

                dateCell.textContent =
                    formatDate(
                        income.date
                    );


                // Notes

                const notesCell =
                    document.createElement("td");

                notesCell.textContent =
                    income.notes || "-";


                // Add cells to row

                row.appendChild(
                    sourceCell
                );

                row.appendChild(
                    amountCell
                );

                row.appendChild(
                    dateCell
                );

                row.appendChild(
                    notesCell
                );


                // Add row to table

                table.appendChild(
                    row
                );

            }
        );


        console.log(
            "TABLE UPDATED SUCCESSFULLY"
        );


        console.log(
            "ROWS IN TABLE:",
            table.children.length
        );


    } catch (error) {

        console.error(
            "LOAD INCOME ERROR:",
            error
        );


        table.innerHTML = `
            <tr>
                <td
                    colspan="4"
                    class="text-center text-danger">

                    Unable to load income records.

                </td>
            </tr>
        `;
    }


    console.log("================================");
    console.log("LOADING INCOME FINISHED");
    console.log("================================");
}


// ========================================
// FORMAT DATE
// ========================================

function formatDate(dateValue) {

    if (!dateValue) {
        return "-";
    }


    // Backend normally returns:
    // 2026-08-05

    const parts =
        String(dateValue).split("-");


    if (parts.length === 3) {

        return (
            parts[2] +
            "-" +
            parts[1] +
            "-" +
            parts[0]
        );
    }


    return dateValue;
}


// ========================================
// ESCAPE HTML
// ========================================

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }


    const div =
        document.createElement("div");


    div.textContent =
        String(value);


    return div.innerHTML;
}


// ========================================
// PAGE LOAD
// ========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        console.log(
            "================================"
        );

        console.log(
            "INCOME PAGE LOADED"
        );

        console.log(
            "================================"
        );


        loadIncome();

    }
);