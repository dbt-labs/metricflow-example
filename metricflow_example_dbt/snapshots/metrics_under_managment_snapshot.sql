{% snapshot metrics_under_management_snapshot %}

    {{
        config(
          target_schema='snapshots',
          strategy='check',
          unique_key='organization_id',
          check_cols=['metrics'],
        )
    }}

 select
    m.organization_id
    ,o.name
    ,count(mm.metric_version_id) as metrics
from prod_public.models m
join prod_public.model_metrics mm on m.id = mm.model_id
join prod_public.organizations o on o.id = m.organization_id
where
      m.is_current = TRUE
      and m.organization_id IN (17,140,137,20,21, 170)
      group by 1,2
{% endsnapshot %}