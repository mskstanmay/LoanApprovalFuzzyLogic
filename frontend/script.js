function calculateLoanApproval() {
    const income = parseFloat(document.getElementById('income').value);
    const creditScore = parseFloat(document.getElementById('credit_score').value);
    const age = parseInt(document.getElementById('age').value);
    const employmentStatus = parseInt(document.getElementById('employment_status').value);
    const loanAmount = parseFloat(document.getElementById('loan_amount').value);

    // Input validation
    if (isNaN(income) || isNaN(creditScore) || isNaN(age) || isNaN(employmentStatus) || isNaN(loanAmount)) {
        document.getElementById('result').innerHTML = 'Please fill in all fields with valid numbers';
        return;
    }

    // Validate ranges
    if (income < 0 || income > 2500000) {
        document.getElementById('result').innerHTML = 'Income must be between ₹0 and ₹25,00,000';
        return;
    }

    if (creditScore < 0 || creditScore > 850) {
        document.getElementById('result').innerHTML = 'Credit score must be between 0 and 850';
        return;
    }

    if (age < 18 || age > 70) {
        document.getElementById('result').innerHTML = 'Age must be between 18 and 70';
        return;
    }

    if (![0, 1, 2].includes(employmentStatus)) {
        document.getElementById('result').innerHTML = 'Employment status must be 0 (Unemployed), 1 (Employed), or 2 (Self-employed)';
        return;
    }

    if (loanAmount < 0 || loanAmount > 3500000) {
        document.getElementById('result').innerHTML = 'Loan amount must be between ₹0 and ₹35,00,000';
        return;
    }

    // Make API call to backend
    fetch('/api/calculate-loan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            income,
            credit_score: creditScore,
            age,
            employment_status: employmentStatus,
            loan_amount: loanAmount
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `Data Error: ${data.error}`;
            return;
        }
        
        let result = `Approval Score: ${data.approval_score}<br>`;
        result += `Status: <span class="${data.is_approved ? 'text-green-600' : 'text-red-600'}">${data.status}</span>`;
        
        document.getElementById('result').innerHTML = result;
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `Promise Error: ${error.message} ${error.stack}`;
    });
}
