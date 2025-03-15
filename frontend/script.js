function calculateLoanApproval() {
    const income = parseFloat(document.getElementById('income').value);
    const creditScore = parseFloat(document.getElementById('credit_score').value);
    const debtRatio = parseFloat(document.getElementById('debt_ratio').value);

    // Input validation
    if (isNaN(income) || isNaN(creditScore) || isNaN(debtRatio)) {
        document.getElementById('result').innerHTML = 'Please fill in all fields with valid numbers';
        return;
    }

    if (creditScore < 300 || creditScore > 850) {
        document.getElementById('result').innerHTML = 'Credit score must be between 300 and 850';
        return;
    }

    if (debtRatio < 0 || debtRatio > 100) {
        document.getElementById('result').innerHTML = 'Debt ratio must be between 0 and 100';
        return;
    }

    // TODO: Add actual fuzzy logic calculation here
    // For now, using a simple weighted average
    const incomeScore = Math.min(income / 100, 1);
    const creditScoreNormalized = (creditScore - 300) / 550;
    const debtRatioScore = 1 - (debtRatio / 100);

    const approvalScore = (incomeScore * 0.4 + creditScoreNormalized * 0.35 + debtRatioScore * 0.25) * 100;
    
    let result = `Approval Score: ${approvalScore.toFixed(2)}%<br>`;
    if (approvalScore >= 70) {
        result += '<span class="text-green-600">Loan Approved</span>';
    } else if (approvalScore >= 50) {
        result += '<span class="text-yellow-600">Conditional Approval</span>';
    } else {
        result += '<span class="text-red-600">Loan Denied</span>';
    }

    document.getElementById('result').innerHTML = result;
}
