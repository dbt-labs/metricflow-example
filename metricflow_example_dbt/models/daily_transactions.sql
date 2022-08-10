{{ config(materialized='table') }}
select 
extract(day from ds) as day, sum(transaction_amount_usd) as total_transaction_amount_usd
from {{ref('demo_transactions_base')}}
group by day
order by day