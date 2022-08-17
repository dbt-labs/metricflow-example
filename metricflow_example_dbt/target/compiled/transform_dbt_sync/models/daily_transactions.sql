
select 
ds, sum(transaction_amount_usd) as total_transaction_amount_usd
from "metricflow"."dbt_meta"."demo_transactions_base"
group by ds
order by ds