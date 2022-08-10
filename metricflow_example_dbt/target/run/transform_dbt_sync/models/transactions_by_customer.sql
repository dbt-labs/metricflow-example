

  create  table "metricflow"."dbt_meta"."transactions_by_customer__dbt_tmp"
  as (
    
with total_customer_transactions as 
(select id_customer, sum(transaction_amount_usd) as total_transaction_amount_usd
from "metricflow"."dbt_meta"."demo_transactions_base" 
group by id_customer)
select 
customers.id_customer, total_customer_transactions.total_transaction_amount_usd, customers.country
from "metricflow"."dbt_meta"."demo_customers_base" customers 
left join total_customer_transactions on customers.id_customer = total_customer_transactions.id_customer
  );