-- Consulta principal para el dashboard 
with unique_users_projects as (
select distinct 
    project_id
    ,user_id 
from tasks t
),
unique_users_tasks as (
select distinct 
    id as task_id
    ,user_id 
from tasks t
)
,activities_users as (
select 
    a.*
    ,coalesce(up.user_id, ut.user_id) as user_id
from activities a
left join unique_users_tasks ut 
    on a.object_type = 'task' 
    and a.object_id = ut.task_id
left join unique_users_projects up 
    on a.object_type = 'project' 
    and a.object_id = up.project_id
)
,activities_data as (
select 
    *
    ,date_trunc('day', event_date)::date as event_day
    ,date_trunc('month', event_date)::date as event_month
    ,date_part('days', DATE_TRUNC('month', event_date) + interval '1 month' - interval '1 day') as days_in_month
from activities_users au 
where au.event_date >= now() - interval '3 months'
)
select *
from activities_data


-- Consulta secundaria para el dashboard 
with task_activity as (
select
    object_id as task_id
    ,date_trunc('day', event_date) as activity_day
    ,date_trunc('month', event_date) as activity_month
    ,case 
        when event_type = 'added' then 'Abierta'
        when event_type = 'updated' then 'Abierta'
        when event_type = 'uncompleted' then 'Abierta'
        when event_type = 'deleted' then 'Eliminada'
        when event_type = 'completed' then 'Cerrada'
    end as task_status
    ,row_number() over (partition by object_id, date_trunc('day', event_date) order by event_date desc) as rn_day
    ,row_number() over (partition by object_id, date_trunc('month', event_date) order by event_date desc) as rn_month
from activities
where object_type = 'task' 
    and event_date >= current_date - interval '3 months'
)
,task_data as (
select 
    t.project_id
    ,p."name" as project_name
    ,ta.*
from task_activity ta
left join tasks t 
    on t.id = ta.task_id
left join projects p 
    on p.id = t.project_id
)
select *
from task_data


