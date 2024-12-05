-- Partitioning order table by date
create table public.order (
  id serial not null,
  status varchar(10),
  date date,
  quantity integer,
  total_amt integer,
  id_customer integer,
  id_product integer,
  constraint order_pk primary key (id, date)
) partition by range (date);
alter table public.order owner to postgres;

create table order_y2024m10 partition of public.order
    for values from ('2024-10-01') to ('2024-11-01');
alter TABLE public.order_y2024m10 OWNER TO postgres;

create table order_y2024m11 partition of public.order
    for values from ('2024-11-01') to ('2024-12-01');
alter TABLE public.order_y2024m11 OWNER TO postgres;

create table order_y2024m12 partition of public.order
    for values from ('2024-12-01') to ('2025-01-01');
alter TABLE public.order_y2024m12 OWNER TO postgres;

create index on public.order (date);
