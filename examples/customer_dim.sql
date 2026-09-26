INSERT INTO dwh.customer_dim (
    customer_id,
    customer_name
)
SELECT
    c.customer_id,
    c.customer_name
FROM crm.customers c
JOIN crm.customer_status s
    ON s.customer_id = c.customer_id
WHERE s.active_flag = 'Y';
