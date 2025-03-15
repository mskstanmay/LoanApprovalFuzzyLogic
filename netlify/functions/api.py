from http.server import BaseHTTPRequestHandler
import json
from backend.main import loan_simulation, jsonify

def handler(event, context):
    # Handle health check for GET requests
    if event['httpMethod'] == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Loan Approval Fuzzy Logic API is running!'})
        }
        
    # For POST requests, continue with existing loan calculation logic
    try:
        # Parse the incoming JSON data
        body = json.loads(event['body'])
        
        # Extract data from request
        user_income = float(body['income'])
        user_credit_score = float(body['credit_score'])
        user_age = int(body['age'])
        user_employment_status = int(body['employment_status'])
        user_loan_amount = float(body['loan_amount'])

        # Set inputs
        loan_simulation.input['income'] = user_income
        loan_simulation.input['credit_score'] = user_credit_score
        loan_simulation.input['age'] = user_age
        loan_simulation.input['employment_status'] = user_employment_status
        loan_simulation.input['loan_amount'] = user_loan_amount

        # Compute results
        loan_simulation.compute()
        loan_approval_value = loan_simulation.output['loan_approval']

        return {
            'statusCode': 200,
            'body': json.dumps({
                'approval_score': round(loan_approval_value, 2),
                'is_approved': loan_approval_value >= 5,
                'status': "Approved" if loan_approval_value >= 5 else "Rejected"
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
