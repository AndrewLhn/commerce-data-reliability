-- Тест: все сегменты не должны быть пустыми
select segment, count(*) as cnt
from {{ ref('rfm_segments') }}
group by segment
having count(*) = 0
