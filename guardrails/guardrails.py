from langchain.tools import tool
from langchain_groq import ChatGroq 
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware


from dotenv import load_dotenv
load_dotenv()

# Sample customer data
customers = {
    "Satish": {
        "customer_id": "CUST1001",
        "name": "Satish",
        "email": "satish_001@abc.com",
        "phone": "+91-9876543210",
        "address": "Bangalore, Karnataka, India",
        "credit_card": "4111-1111-1111-1111",
        "loyalty_status": "Gold",
        "orders": [
            {"order_id": "ORD12345", "status": "Shipped", "amount": 2499},
            {"order_id": "ORD12346", "status": "Delivered", "amount": 999}
        ]
    },

    "Shiva": {
        "customer_id": "CUST1002",
        "name": "Shiva",
        "email": "shiva_002@abc.com",
        "phone": "+91-9123456789",
        "address": "Hyderabad, Telangana, India",
        "credit_card": "5500-0000-0000-0004",
        "loyalty_status": "Silver",
        "orders": [
            {"order_id": "ORD22345", "status": "Delivered", "amount": 1599}
        ]
    },

    "Teja": {
        "customer_id": "CUST1003",
        "name": "Teja",
        "email": "teja2009@xyz.com",
        "phone": "+91-9012345678",
        "address": "Vijayawada, Andhra Pradesh, India",
        "credit_card": "6011-1111-1111-1117",
        "loyalty_status": "Bronze",
        "orders": [
            {"order_id": "ORD32345", "status": "Processing", "amount": 499}
        ]
    },

    "Bhavishya": {
        "customer_id": "CUST1004",
        "name": "Bhavishya",
        "email": "bhavishya.k@abc.com",
        "phone": "+91-9234567890",
        "address": "Chennai, Tamil Nadu, India",
        "credit_card": "3530-1113-3330-0000",
        "loyalty_status": "Gold",
        "orders": [
            {"order_id": "ORD42345", "status": "Cancelled", "amount": 799}
        ]
    },

    "Ramya": {
        "customer_id": "CUST1005",
        "name": "Ramya",
        "email": "ramya_dev@xyz.com",
        "phone": "+91-9988776655",
        "address": "Pune, Maharashtra, India",
        "credit_card": "3400-0000-0000-009",
        "loyalty_status": "Platinum",
        "orders": [
            {"order_id": "ORD52345", "status": "Shipped", "amount": 3499}
        ]
    }
}

# Tool 
@tool
def get_customer_details_tool(cust_name: str) -> str:
    """
    Fetch customer details using customer name.
    """
    return customers.get(cust_name, "Customer not found.")

# Create Agent
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)
customer_service_agent = create_agent(
    system_prompt="""
    You are a customer service assistant.

    Your responsibilities:
    1. Help customers with account related queries.
    2. Use tools when customer information is required.
    3. Never reveal:
        - Full credit card numbers
        - Full phone numbers
        - Internal customer IDs
    4. Always provide polite responses.

    IMPORTANT RULES:
    1. Return all data fields EXACTLY as received from the tool 'get_customer_info_tool' — do NOT reformat, 
       abbreviate, paraphrase, or restructure any field values (especially numbers and emails).
    2. Credit card numbers must always be returned in their original format with dashes 
       e.g., XXXX-XXXX-XXXX-XXXX — never remove dashes or spaces.
    3. Do not handle PII directly. Middleware will automatically redact/mask sensitive 
       fields — your job is only to pass the raw values through unchanged.
    4. Return information as plain text, not JSON.    
        """,
    model=llm,
    tools=[get_customer_details_tool],
    middleware= [       # Mask credit cards in user input
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_tool_results=True
        ),
        # Redact emails in user input before sending to model
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_tool_results=True,  
            apply_to_output=True
        ),
        
    ]

)

response = customer_service_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Show me Satish customer details"
            }
        ]
    }
)


print(response["messages"][-1].content)
