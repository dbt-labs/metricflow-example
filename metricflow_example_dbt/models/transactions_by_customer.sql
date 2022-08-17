{{ config(materialized='table') }}
with total_customer_transactions as 
(select max(ds) as ds, id_customer, sum(transaction_amount_usd) as total_transaction_amount_usd
from {{ref('demo_transactions_base')}} 
group by id_customer)
select 
total_customer_transactions.ds, customers.id_customer, total_customer_transactions.total_transaction_amount_usd, customers.country
from {{ref('demo_customers_base')}} customers 
left join total_customer_transactions on customers.id_customer = total_customer_transactions.id_customer