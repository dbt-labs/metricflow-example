

  create  table "metricflow"."dbt_meta"."demo_customers_base__dbt_tmp"
  as (
    
select * from transform.mf_demo_customers
  );