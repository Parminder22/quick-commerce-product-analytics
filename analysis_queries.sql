-- 1. AOV and Repeat Purchase Rate 
WITH UserOrders AS (
    SELECT 
        user_id, 
        COUNT(transaction_id) AS total_orders, 
        SUM(order_value) AS total_spend
    FROM transactions 
    GROUP BY user_id
)
SELECT 
    AVG(total_spend / total_orders) AS average_order_value_AOV,
    CAST(COUNT(CASE WHEN total_orders > 1 THEN 1 END) AS FLOAT) / COUNT(user_id) AS repeat_purchase_rate
FROM UserOrders;



-- 2. Revenue Segmentation 
WITH SegmentRevenue AS (
    SELECT 
        customer_segment, 
        SUM(order_value) AS segment_revenue
    FROM transactions 
    GROUP BY customer_segment
)
SELECT 
    customer_segment, 
    segment_revenue,
    (segment_revenue / (SELECT SUM(order_value) FROM transactions)) * 100 AS percentage_of_total_revenue
FROM SegmentRevenue;




-- 3. A/B Testing
SELECT 
    ab_test_group,
    COUNT(DISTINCT user_id) AS total_users,
    COUNT(transaction_id) AS total_orders,
    CAST(COUNT(transaction_id) AS FLOAT) / COUNT(DISTINCT user_id) AS avg_orders_per_user
FROM transactions
GROUP BY ab_test_group;