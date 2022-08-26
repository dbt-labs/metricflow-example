{{ config(materialized='table') }}
select * from transform.mf_demo_countries