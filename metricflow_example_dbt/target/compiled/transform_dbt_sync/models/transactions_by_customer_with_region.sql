
select 
ds, customer_transactions.id_customer, customer_transactions.total_transaction_amount_usd, customer_transactions.country, countries.region
from "metricflow"."dbt_meta"."transactions_by_customer" customer_transactions left join "metricflow"."dbt_meta"."demo_countries_base" countries on customer_transactions.country = countries.country