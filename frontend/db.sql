--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Debian 13.5-1.pgdg100+1)
-- Dumped by pg_dump version 13.5 (Debian 13.5-1.pgdg100+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.category_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id smallint DEFAULT nextval('public.category_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_id_seq OWNER TO postgres;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id smallint DEFAULT nextval('public.customer_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    street character varying(128) NOT NULL,
    city character varying(50) NOT NULL,
    phone character varying(25) NOT NULL,
    cell character varying(25),
    zip character varying(8),
    email character varying(128)
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_id_seq OWNER TO postgres;

--
-- Name: fackturers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fackturers (
    id integer DEFAULT nextval('public.order_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    descriptions character varying(128),
    instructions character varying(512),
    total numeric(12,2) NOT NULL,
    qty numeric(12,2) NOT NULL,
    price numeric(12,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.fackturers OWNER TO postgres;

--
-- Name: orderdetail_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orderdetail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orderdetail_id_seq OWNER TO postgres;

--
-- Name: facturer_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facturer_details (
    id integer DEFAULT nextval('public.orderdetail_id_seq'::regclass) NOT NULL,
    qty numeric(10,2) NOT NULL,
    content numeric(8,2) NOT NULL,
    unit_name character varying(6) NOT NULL,
    real_qty numeric(10,2) NOT NULL,
    price numeric(12,2) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    fackturer_id integer NOT NULL,
    product_id integer NOT NULL,
    unit_id integer NOT NULL
);


ALTER TABLE public.facturer_details OWNER TO postgres;

--
-- Name: first_stocks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.first_stocks (
    qty numeric(10,2) NOT NULL,
    unit_name character varying(6) NOT NULL,
    content numeric(8,2) NOT NULL,
    product_id integer NOT NULL,
    unit_id integer NOT NULL
);


ALTER TABLE public.first_stocks OWNER TO postgres;

--
-- Name: order_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_details (
    id integer DEFAULT nextval('public.orderdetail_id_seq'::regclass) NOT NULL,
    qty numeric(10,2) NOT NULL,
    content numeric(8,2) NOT NULL,
    unit_name character varying(6) NOT NULL,
    real_qty numeric(10,2) NOT NULL,
    price numeric(12,2) NOT NULL,
    buy_price numeric(12,2) NOT NULL,
    discount numeric(12,2) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    unit_id integer NOT NULL
);


ALTER TABLE public.order_details OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer DEFAULT nextval('public.order_id_seq'::regclass) NOT NULL,
    total numeric(12,2) NOT NULL,
    cash numeric(12,2) NOT NULL,
    payment numeric(12,2) NOT NULL,
    remain_payment numeric(12,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    customer_id smallint NOT NULL,
    sales_id smallint NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_id_seq OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer DEFAULT nextval('public.product_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    spec character varying(128),
    base_unit character varying(6) NOT NULL,
    base_weight numeric(10,2) NOT NULL,
    base_price numeric(12,2) NOT NULL,
    first_stock numeric(10,2) NOT NULL,
    stock numeric(10,2) NOT NULL,
    is_active boolean NOT NULL,
    is_sale boolean NOT NULL,
    category_id smallint NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: salesman_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.salesman_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.salesman_id_seq OWNER TO postgres;

--
-- Name: salesmans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.salesmans (
    id smallint DEFAULT nextval('public.salesman_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    street character varying(128) NOT NULL,
    city character varying(50) NOT NULL,
    phone character varying(25) NOT NULL,
    cell character varying(25),
    zip character varying(8),
    email character varying(128)
);


ALTER TABLE public.salesmans OWNER TO postgres;

--
-- Name: stock_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_details (
    id integer DEFAULT nextval('public.orderdetail_id_seq'::regclass) NOT NULL,
    qty numeric(10,2) NOT NULL,
    content numeric(8,2) NOT NULL,
    unit_name character varying(6) NOT NULL,
    real_qty numeric(10,2) NOT NULL,
    price numeric(12,2) NOT NULL,
    discount numeric(12,2) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    stock_id integer NOT NULL,
    product_id integer NOT NULL,
    unit_id integer NOT NULL
);


ALTER TABLE public.stock_details OWNER TO postgres;

--
-- Name: stocks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stocks (
    id integer DEFAULT nextval('public.order_id_seq'::regclass) NOT NULL,
    invoice_number character varying(50) NOT NULL,
    total numeric(12,2) NOT NULL,
    cash numeric(12,2) NOT NULL,
    payment numeric(12,2) NOT NULL,
    remain_payment numeric(12,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    supplier_id smallint NOT NULL
);


ALTER TABLE public.stocks OWNER TO postgres;

--
-- Name: supplier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.supplier_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_id_seq OWNER TO postgres;

--
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suppliers (
    id smallint DEFAULT nextval('public.supplier_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    sales_name character varying(50) NOT NULL,
    street character varying(128) NOT NULL,
    city character varying(50) NOT NULL,
    phone character varying(25) NOT NULL,
    cell character varying(25),
    zip character varying(8),
    email character varying(128)
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- Name: unit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.unit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.unit_id_seq OWNER TO postgres;

--
-- Name: units; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.units (
    id integer DEFAULT nextval('public.unit_id_seq'::regclass) NOT NULL,
    name character varying(6) NOT NULL,
    barcode character varying(25) NOT NULL,
    content numeric(8,2) NOT NULL,
    buy_price numeric(12,2) NOT NULL,
    margin numeric(8,4) NOT NULL,
    price numeric(12,2) NOT NULL,
    is_default boolean NOT NULL,
    product_id integer NOT NULL
);


ALTER TABLE public.units OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id smallint DEFAULT nextval('public.user_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    email character varying(128) NOT NULL,
    password character varying(50) NOT NULL,
    role character varying(25) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name) FROM stdin;
1	Produk Jadi
2	Bahan Baku
3	Tenaga Kerja
4	Bahan Pendukung
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (id, name, street, city, phone, cell, zip, email) FROM stdin;
\.


--
-- Data for Name: fackturers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fackturers (id, name, descriptions, instructions, total, qty, price, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: facturer_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facturer_details (id, qty, content, unit_name, real_qty, price, subtotal, fackturer_id, product_id, unit_id) FROM stdin;
\.


--
-- Data for Name: first_stocks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.first_stocks (qty, unit_name, content, product_id, unit_id) FROM stdin;
\.


--
-- Data for Name: order_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_details (id, qty, content, unit_name, real_qty, price, buy_price, discount, subtotal, order_id, product_id, unit_id) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, total, cash, payment, remain_payment, created_at, updated_at, customer_id, sales_id) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, name, spec, base_unit, base_weight, base_price, first_stock, stock, is_active, is_sale, category_id) FROM stdin;
3	Plastik PP Bal	35 x 65	pcs	0.10	776.00	0.00	0.00	t	f	4
4	Lakban	48 x 80	pcs	0.20	12000.00	0.00	0.00	t	f	4
5	Plastik Roll 1 kg	320 x 10000	roll	10.00	405000.00	0.00	0.00	t	f	4
1	Gula Pasir	1 zak 50 kg	gr	0.00	524.00	0.00	0.00	t	f	2
6	Tenaga Kerja	Ongkos Borongan	Org	0.00	2000.00	0.00	0.00	t	f	3
2	Gula Pasir Kemasan 1 kg	1 pcs @ 1 kg	kg	1.00	10000.00	0.00	0.00	t	t	1
\.


--
-- Data for Name: salesmans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.salesmans (id, name, street, city, phone, cell, zip, email) FROM stdin;
\.


--
-- Data for Name: stock_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock_details (id, qty, content, unit_name, real_qty, price, discount, subtotal, stock_id, product_id, unit_id) FROM stdin;
\.


--
-- Data for Name: stocks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stocks (id, invoice_number, total, cash, payment, remain_payment, created_at, updated_at, supplier_id) FROM stdin;
\.


--
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.suppliers (id, name, sales_name, street, city, phone, cell, zip, email) FROM stdin;
\.


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.units (id, name, barcode, content, buy_price, margin, price, is_default, product_id) FROM stdin;
7	pcs	001	1.00	776.00	0.0000	776.00	f	3
8	pcs	002	1.00	12000.00	0.0000	12000.00	f	4
9	roll	004	1.00	405000.00	0.0000	405000.00	f	5
3	40g	0123456789	1.00	131000.00	0.0000	524.00	t	1
15	zak	9999	1250.00	524.00	0.0000	655000.00	f	1
14	besar	8888s	25.00	524.00	0.0000	13100.00	f	1
11	sedang	7777	12.50	524000.00	0.0000	6550.00	f	1
10	kecil	6666	6.25	262000.00	0.0000	3275.00	f	1
16	tk	5555	1.00	2000.00	0.0000	2000.00	f	6
4	kg	987654321	1.00	10000.00	10.0000	11000.00	f	2
5	ls	987654320	12.00	120000.00	7.0000	128400.00	t	2
6	bal	987654300	120.00	1200000.00	5.0000	1260000.00	f	2
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role) FROM stdin;
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 4, true);


--
-- Name: customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_id_seq', 1, false);


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_id_seq', 1, false);


--
-- Name: orderdetail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orderdetail_id_seq', 1, false);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_id_seq', 6, true);


--
-- Name: salesman_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.salesman_id_seq', 1, false);


--
-- Name: supplier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.supplier_id_seq', 1, false);


--
-- Name: unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.unit_id_seq', 16, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: customers customers_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_name_key UNIQUE (name);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: fackturers fackturers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fackturers
    ADD CONSTRAINT fackturers_pkey PRIMARY KEY (id);


--
-- Name: facturer_details facturer_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturer_details
    ADD CONSTRAINT facturer_details_pkey PRIMARY KEY (id);


--
-- Name: first_stocks first_stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.first_stocks
    ADD CONSTRAINT first_stocks_pkey PRIMARY KEY (product_id);


--
-- Name: order_details order_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_name_key UNIQUE (name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: salesmans salesmans_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salesmans
    ADD CONSTRAINT salesmans_name_key UNIQUE (name);


--
-- Name: salesmans salesmans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salesmans
    ADD CONSTRAINT salesmans_pkey PRIMARY KEY (id);


--
-- Name: stock_details stock_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_details
    ADD CONSTRAINT stock_details_pkey PRIMARY KEY (id);


--
-- Name: stocks stocks_invoice_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_invoice_number_key UNIQUE (invoice_number);


--
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (id);


--
-- Name: suppliers suppliers_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_name_key UNIQUE (name);


--
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- Name: units units_barcode_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_barcode_key UNIQUE (barcode);


--
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- Name: units uq_unit_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT uq_unit_name UNIQUE (product_id, name);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_facturer_details_fackturer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_facturer_details_fackturer_id ON public.facturer_details USING btree (fackturer_id);


--
-- Name: ix_facturer_details_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_facturer_details_product_id ON public.facturer_details USING btree (product_id);


--
-- Name: ix_facturer_details_unit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_facturer_details_unit_id ON public.facturer_details USING btree (unit_id);


--
-- Name: ix_first_stocks_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_first_stocks_product_id ON public.first_stocks USING btree (product_id);


--
-- Name: ix_first_stocks_unit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_first_stocks_unit_id ON public.first_stocks USING btree (unit_id);


--
-- Name: ix_order_details_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_details_order_id ON public.order_details USING btree (order_id);


--
-- Name: ix_order_details_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_details_product_id ON public.order_details USING btree (product_id);


--
-- Name: ix_order_details_unit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_details_unit_id ON public.order_details USING btree (unit_id);


--
-- Name: ix_orders_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_customer_id ON public.orders USING btree (customer_id);


--
-- Name: ix_orders_sales_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_sales_id ON public.orders USING btree (sales_id);


--
-- Name: ix_stock_details_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stock_details_product_id ON public.stock_details USING btree (product_id);


--
-- Name: ix_stock_details_stock_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stock_details_stock_id ON public.stock_details USING btree (stock_id);


--
-- Name: ix_stock_details_unit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stock_details_unit_id ON public.stock_details USING btree (unit_id);


--
-- Name: ix_stocks_supplier_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stocks_supplier_id ON public.stocks USING btree (supplier_id);


--
-- Name: ix_units_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_units_name ON public.units USING btree (name);


--
-- Name: ix_units_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_units_product_id ON public.units USING btree (product_id);


--
-- Name: facturer_details facturer_details_fackturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturer_details
    ADD CONSTRAINT facturer_details_fackturer_id_fkey FOREIGN KEY (fackturer_id) REFERENCES public.fackturers(id) ON DELETE CASCADE;


--
-- Name: facturer_details facturer_details_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturer_details
    ADD CONSTRAINT facturer_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: facturer_details facturer_details_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturer_details
    ADD CONSTRAINT facturer_details_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- Name: first_stocks first_stocks_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.first_stocks
    ADD CONSTRAINT first_stocks_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: first_stocks first_stocks_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.first_stocks
    ADD CONSTRAINT first_stocks_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- Name: order_details order_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_details order_details_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: order_details order_details_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: orders orders_sales_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_sales_id_fkey FOREIGN KEY (sales_id) REFERENCES public.salesmans(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: stock_details stock_details_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_details
    ADD CONSTRAINT stock_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: stock_details stock_details_stock_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_details
    ADD CONSTRAINT stock_details_stock_id_fkey FOREIGN KEY (stock_id) REFERENCES public.stocks(id) ON DELETE CASCADE;


--
-- Name: stock_details stock_details_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_details
    ADD CONSTRAINT stock_details_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- Name: stocks stocks_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id);


--
-- Name: units units_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

