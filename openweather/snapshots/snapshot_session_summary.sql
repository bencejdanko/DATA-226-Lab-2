{% snapshot snapshot_session_summary %}

{{
  config(
    target_schema='snapshot',
    unique_key= "CITY_NAME || '-' || DATE",
    strategy='timestamp',
    updated_at='DATE',
    invalidate_hard_deletes=True
  )
}}

SELECT * FROM {{ ref('session_summary') }}

{% endsnapshot %}
