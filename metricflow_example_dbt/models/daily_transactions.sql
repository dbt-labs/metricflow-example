{{ config(materialized='table') }}
select 
ds, sum(transaction_amount_usd) as total_transaction_amount_usd
from {{ref('demo_transactions_base')}}
group by ds
order by ds