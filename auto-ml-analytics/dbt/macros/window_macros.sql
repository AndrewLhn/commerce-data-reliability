{% macro rfm_scores(customer_id, order_date, amount) %}
    ntile(5) over (partition by customer_id order by max({{ order_date }}) desc) as recency,
    ntile(5) over (partition by customer_id order by count(1) asc) as frequency,
    ntile(5) over (partition by customer_id order by sum({{ amount }}) asc) as monetary
{% endmacro %}
