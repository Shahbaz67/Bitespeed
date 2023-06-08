# Bitespeed
Bitespeed Backend Task: Identity Reconciliation 
- Bitespeed needs a way to identify and keep track of a customer's identity across multiple purchases.

API service hosted on AWS EC2: http://50.17.158.118/identify/

Go to the above url to test the functionality of the "/identify" endpoint.

My Resume link: https://bit.ly/3INyy4X 

# Stack Used
Database: PostgreSQL on AWS RDS instance
Backend Framework: Python Django Rest Framework

# Testing the endpoint:
Request: 
{
	"email"?: string,
	"phone_number"?: number
}
'?' indicated optional field.

Three conditions arise based on requests(dealing each request separately):
1. Only email is present.
    - Email may already exist
    - create new contact
2. Only phone_number is present.
    - Phone_number may already exist
    - create new contact
3. Both are present.
    Here again 3 poosibilities can happen:
    - both email and phone_number may be already existing (either in contacts of one customer or from two different customers)
    - One of them existing 
    - None exist (create new contact)

Based on these requests we either create a new contact and return the serialized data,
OR if contact already exists, we return the consolidated contact.

