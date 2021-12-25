CREATE TABLE public.products (
	id integer not null default nextval('products_id_seq'::regclass),
    code varchar(8) not null,
    name varchar(50) not null,
    spec varchar(50) not null,
    base_unit varchar(6) not null,
    base_weight decimal(10,2) not null default 0,
    base_price decimal(12,2) not null default 0,
    is_active bool not null default true,
    first_stock decimal(12,2) not null default 0,
    unit_in_stock decimal(12,2) not null default 0,
    category_id smallint not null
);

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);

create unique index uq_product_code
    on products (code);

create unique index uq_product_name
    on products (name);

create index ix_product_category_id
    on products (category_id);

alter table public.products
    add constraint fk_product_category
    foreign key (category_id)
    references public.categories(id)
    on delete cascade;
