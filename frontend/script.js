async function calculateLoanApproval() {
    const income = parseFloat(document.getElementById('income').value);
    const creditScore = parseFloat(document.getElementById('credit_score').value);
    const age = parseInt(document.getElementById('age').value);
    const employmentStatus = parseInt(document.getElementById('employment_status').value);
    const loanAmount = parseFloat(document.getElementById('loan_amount').value);
    const resultElement = document.getElementById('result');

    // Input validation
    if ([income, creditScore, age, employmentStatus, loanAmount].some(isNaN)) {
        resultElement.innerHTML = 'Please fill in all fields with valid numbers';
        return;
    }

    // Validate ranges
    const validationErrors = [];
    if (income < 0 || income > 2500000) validationErrors.push('Income must be between ₹0 and ₹25,00,000');
    if (creditScore < 0 || creditScore > 850) validationErrors.push('Credit score must be between 0 and 850');
    if (age < 18 || age > 70) validationErrors.push('Age must be between 18 and 70');
    if (![0, 1, 2].includes(employmentStatus)) 
        validationErrors.push('Employment status must be 0 (Unemployed), 1 (Employed), or 2 (Self-employed)');
    if (loanAmount < 0 || loanAmount > 3500000) 
        validationErrors.push('Loan amount must be between ₹0 and ₹35,00,000');

    if (validationErrors.length > 0) {
        resultElement.innerHTML = validationErrors.join('<br>');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/calculate-loan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ income, credit_score: creditScore, age, employment_status: employmentStatus, loan_amount: loanAmount })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            resultElement.innerHTML = `Data Error: ${data.error}`;
            return;
        }

        resultElement.innerHTML = `
            <strong>Approval Score:</strong> ${data.approval_score}<br>
            <strong>Status:</strong> <span class="${data.is_approved ? 'text-green-600' : 'text-red-600'}">
                ${data.status}
            </span>
        `;
    } catch (error) {
        resultElement.innerHTML = `Error: ${error.message}`;
        console.error("Fetch error:", error);
    }
}
