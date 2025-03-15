# Install required package if not already installed
try:
    import skfuzzy as fuzz
    import skfuzzy.control as ctrl
except ImportError:
    import os
    os.system('pip install -q scikit-fuzzy')
    import skfuzzy as fuzz
    import skfuzzy.control as ctrl

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://fuzzylogicloanapprovalsystem.netlify.app/",
    "http://localhost:3000"
]}})

# **1. Define Input Variables**
income = ctrl.Antecedent(np.arange(0, 2500001, 1000), 'income')  # ₹0 to ₹25,00,000
credit_score = ctrl.Antecedent(np.arange(0, 851, 1), 'credit_score')  # 0 to 850
age = ctrl.Antecedent(np.arange(18, 71, 1), 'age')  # 18 to 70 years
employment_status = ctrl.Antecedent(np.arange(0, 3, 1), 'employment_status')  # 0: Unemployed, 1: Employed, 2: Self-employed
loan_amount = ctrl.Antecedent(np.arange(0, 3500001, 1000), 'loan_amount')  # ₹0 to ₹35,00,000
loan_approval = ctrl.Consequent(np.arange(0, 11, 1), 'loan_approval')  # 0 (Rejected) to 10 (Fully Approved)

# **2. Define Membership Functions**
# Income Membership
income['very_low'] = fuzz.trimf(income.universe, [0, 0, 200000])
income['low'] = fuzz.trimf(income.universe, [0, 200000, 500000])
income['medium'] = fuzz.trimf(income.universe, [200000, 500000, 1000000])
income['high'] = fuzz.trimf(income.universe, [500000, 1000000, 2000000])
income['very_high'] = fuzz.trimf(income.universe, [1000000, 2000000, 2500000])

# Credit Score Membership
credit_score['very_poor'] = fuzz.trimf(credit_score.universe, [0, 0, 300])
credit_score['poor'] = fuzz.trimf(credit_score.universe, [0, 300, 500])
credit_score['fair'] = fuzz.trimf(credit_score.universe, [300, 500, 650])
credit_score['good'] = fuzz.trimf(credit_score.universe, [500, 650, 750])
credit_score['excellent'] = fuzz.trimf(credit_score.universe, [650, 750, 850])

# Age Membership
age['young'] = fuzz.trimf(age.universe, [18, 18, 30])
age['middle_aged'] = fuzz.trimf(age.universe, [30, 40, 50])
age['senior'] = fuzz.trimf(age.universe, [50, 60, 70])

# Employment Status Membership (Fixed Overlaps)
employment_status['unemployed'] = fuzz.trimf(employment_status.universe, [0, 0, 0.5])
employment_status['employed'] = fuzz.trimf(employment_status.universe, [0.5, 1, 1.5])
employment_status['self_employed'] = fuzz.trimf(employment_status.universe, [1.5, 2, 2])

# Loan Amount Membership
loan_amount['very_small'] = fuzz.trimf(loan_amount.universe, [0, 0, 100000])
loan_amount['small'] = fuzz.trimf(loan_amount.universe, [0, 100000, 500000])
loan_amount['medium'] = fuzz.trimf(loan_amount.universe, [100000, 500000, 1500000])
loan_amount['large'] = fuzz.trimf(loan_amount.universe, [500000, 1500000, 3000000])
loan_amount['very_large'] = fuzz.trimf(loan_amount.universe, [1500000, 3000000, 3500000])

# Loan Approval Membership (Fixed Gap at 5)
loan_approval['rejected'] = fuzz.trimf(loan_approval.universe, [0, 2.5, 5])
loan_approval['accepted'] = fuzz.trimf(loan_approval.universe, [5, 7.5, 10])

# **3. Define Rules** (Fixed OR conditions)
rules = [
    ctrl.Rule((income['very_low'] & credit_score['very_poor']) | (employment_status['unemployed']), loan_approval['rejected']),
    ctrl.Rule((income['low'] & credit_score['poor'] & loan_amount['very_large']), loan_approval['rejected']),
    ctrl.Rule((income['medium'] & credit_score['fair'] & employment_status['employed']), loan_approval['accepted']),
    ctrl.Rule((income['high'] & credit_score['good'] & employment_status['self_employed']), loan_approval['accepted']),
    ctrl.Rule((income['very_high'] & credit_score['excellent'] & loan_amount['large']), loan_approval['accepted']),
    ctrl.Rule((age['senior'] & loan_amount['very_large']), loan_approval['rejected']),
    ctrl.Rule((employment_status['unemployed'] & loan_amount['medium']), loan_approval['rejected']),
]

# **4. Create Control System**
loan_ctrl = ctrl.ControlSystem(rules)
loan_simulation = ctrl.ControlSystemSimulation(loan_ctrl)

@app.route('/')
def home():
    return "Loan Approval Fuzzy Logic API is running!"

@app.route('/calculate-loan', methods=['POST'])
def calculate_loan():
    try:
        data = request.json
        
        # Extract data from request
        user_income = float(data['income'])
        user_credit_score = float(data['credit_score'])
        user_age = int(data['age'])
        user_employment_status = int(data['employment_status'])
        user_loan_amount = float(data['loan_amount'])

        # Validate input ranges
        if not (0 <= user_income <= 2500000):
            return jsonify({"error": "Income should be between ₹0 and ₹25,00,000."}), 400
        if not (0 <= user_credit_score <= 850):
            return jsonify({"error": "Credit Score should be between 0 and 850."}), 400
        if not (18 <= user_age <= 70):
            return jsonify({"error": "Age should be between 18 and 70."}), 400
        if user_employment_status not in [0, 1, 2]:
            return jsonify({"error": "Employment status should be 0 (Unemployed), 1 (Employed), or 2 (Self-Employed)."}), 400
        if not (0 <= user_loan_amount <= 3500000):
            return jsonify({"error": "Loan Amount should be between ₹0 and ₹35,00,000."}), 400

        # Set inputs
        loan_simulation.input['income'] = user_income
        loan_simulation.input['credit_score'] = user_credit_score
        loan_simulation.input['age'] = user_age
        loan_simulation.input['employment_status'] = user_employment_status
        loan_simulation.input['loan_amount'] = user_loan_amount

        # Compute results
        loan_simulation.compute()
        loan_approval_value = loan_simulation.output['loan_approval']

        return jsonify({
            'approval_score': round(loan_approval_value, 2),
            'is_approved': loan_approval_value >= 5,
            'status': "Approved" if loan_approval_value >= 5 else "Rejected"
        })

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)