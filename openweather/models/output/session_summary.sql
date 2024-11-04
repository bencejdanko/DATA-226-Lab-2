WITH w AS (
    SELECT * FROM {{ ref("temperature_timestamp") }}
), c AS (
    SELECT * FROM {{ source('raw_data', 'city_dimension_table') }}
)
SELECT w.*, c."Name" as city_name
FROM w
JOIN c ON w.city_id = c.city_id
