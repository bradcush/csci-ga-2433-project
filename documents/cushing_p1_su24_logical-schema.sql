-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.2.0-alpha1
-- PostgreSQL version: 17.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file.
-- These commands were put in this file only as a convenience.
--
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE new_database;
-- ddl-end --


-- object: public.credit_card | type: TABLE --
-- DROP TABLE IF EXISTS public.credit_card CASCADE;
CREATE TABLE public.credit_card (
	fname varchar(20),
	minit varchar(10),
	lname varchar(10),
	number numeric(16) NOT NULL,
	expiration_date date,
	security_code numeric(3),
	zip_code numeric(5),
	CONSTRAINT credit_card_pk PRIMARY KEY (number)
);
-- ddl-end --
ALTER TABLE public.credit_card OWNER TO postgres;
-- ddl-end --

-- object: public.warranty | type: TABLE --
-- DROP TABLE IF EXISTS public.warranty CASCADE;
CREATE TABLE public.warranty (
	id serial NOT NULL,
	expiration_date date,
	is_under boolean,
	CONSTRAINT warranty_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.warranty OWNER TO postgres;
-- ddl-end --

-- object: public.member | type: TABLE --
-- DROP TABLE IF EXISTS public.member CASCADE;
CREATE TABLE public.member (
	join_date date,
	expiration_date date,
	status_tier varchar(10),
	id smallint NOT NULL,
	CONSTRAINT member_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.member OWNER TO postgres;
-- ddl-end --

-- object: public.product | type: TABLE --
-- DROP TABLE IF EXISTS public.product CASCADE;
CREATE TABLE public.product (
	id serial NOT NULL,
	type varchar(10),
	cost integer,
	id_order integer,
	CONSTRAINT product_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.product OWNER TO postgres;
-- ddl-end --

-- object: public."order" | type: TABLE --
-- DROP TABLE IF EXISTS public."order" CASCADE;
CREATE TABLE public."order" (
	id serial NOT NULL,
	status varchar(10),
	date date,
	quantity integer,
	total_amt integer,
	id_customer integer,
	id_warranty integer,
	CONSTRAINT order_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public."order" OWNER TO postgres;
-- ddl-end --

-- object: public.customer | type: TABLE --
-- DROP TABLE IF EXISTS public.customer CASCADE;
CREATE TABLE public.customer (
	id serial NOT NULL,
	name varchar(50),
	email varchar(50),
	phone numeric(10),
	number_credit_card numeric(16),
	id_member smallint,
	CONSTRAINT customer_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.customer OWNER TO postgres;
-- ddl-end --

-- object: customer_fk | type: CONSTRAINT --
-- ALTER TABLE public."order" DROP CONSTRAINT IF EXISTS customer_fk CASCADE;
ALTER TABLE public."order" ADD CONSTRAINT customer_fk FOREIGN KEY (id_customer)
REFERENCES public.customer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: credit_card_fk | type: CONSTRAINT --
-- ALTER TABLE public.customer DROP CONSTRAINT IF EXISTS credit_card_fk CASCADE;
ALTER TABLE public.customer ADD CONSTRAINT credit_card_fk FOREIGN KEY (number_credit_card)
REFERENCES public.credit_card (number) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: customer_uq | type: CONSTRAINT --
-- ALTER TABLE public.customer DROP CONSTRAINT IF EXISTS customer_uq CASCADE;
ALTER TABLE public.customer ADD CONSTRAINT customer_uq UNIQUE (number_credit_card);
-- ddl-end --

-- object: order_fk | type: CONSTRAINT --
-- ALTER TABLE public.product DROP CONSTRAINT IF EXISTS order_fk CASCADE;
ALTER TABLE public.product ADD CONSTRAINT order_fk FOREIGN KEY (id_order)
REFERENCES public."order" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: warranty_fk | type: CONSTRAINT --
-- ALTER TABLE public."order" DROP CONSTRAINT IF EXISTS warranty_fk CASCADE;
ALTER TABLE public."order" ADD CONSTRAINT warranty_fk FOREIGN KEY (id_warranty)
REFERENCES public.warranty (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: order_uq | type: CONSTRAINT --
-- ALTER TABLE public."order" DROP CONSTRAINT IF EXISTS order_uq CASCADE;
ALTER TABLE public."order" ADD CONSTRAINT order_uq UNIQUE (id_warranty);
-- ddl-end --

-- object: public.backorder | type: TABLE --
-- DROP TABLE IF EXISTS public.backorder CASCADE;
CREATE TABLE public.backorder (
	id serial NOT NULL,
	manufacturer varchar(20),
	quantity integer,
	cost smallint,
	CONSTRAINT backorder_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.backorder OWNER TO postgres;
-- ddl-end --

-- object: public.inventory | type: TABLE --
-- DROP TABLE IF EXISTS public.inventory CASCADE;
CREATE TABLE public.inventory (
	location varchar(20) NOT NULL,
	quantity integer,
	is_backordered boolean,
	id_product integer,
	id_backorder integer,
	CONSTRAINT inventory_pk PRIMARY KEY (location)
);
-- ddl-end --
ALTER TABLE public.inventory OWNER TO postgres;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.inventory DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.inventory ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: backorder_fk | type: CONSTRAINT --
-- ALTER TABLE public.inventory DROP CONSTRAINT IF EXISTS backorder_fk CASCADE;
ALTER TABLE public.inventory ADD CONSTRAINT backorder_fk FOREIGN KEY (id_backorder)
REFERENCES public.backorder (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: inventory_uq | type: CONSTRAINT --
-- ALTER TABLE public.inventory DROP CONSTRAINT IF EXISTS inventory_uq CASCADE;
ALTER TABLE public.inventory ADD CONSTRAINT inventory_uq UNIQUE (id_backorder);
-- ddl-end --

-- object: public.prospect | type: TABLE --
-- DROP TABLE IF EXISTS public.prospect CASCADE;
CREATE TABLE public.prospect (
	name varchar(50),
	email varchar(50) NOT NULL,
	id_customer integer,
	CONSTRAINT prospect_pk PRIMARY KEY (email)
);
-- ddl-end --
ALTER TABLE public.prospect OWNER TO postgres;
-- ddl-end --

-- object: customer_fk | type: CONSTRAINT --
-- ALTER TABLE public.prospect DROP CONSTRAINT IF EXISTS customer_fk CASCADE;
ALTER TABLE public.prospect ADD CONSTRAINT customer_fk FOREIGN KEY (id_customer)
REFERENCES public.customer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: prospect_uq | type: CONSTRAINT --
-- ALTER TABLE public.prospect DROP CONSTRAINT IF EXISTS prospect_uq CASCADE;
ALTER TABLE public.prospect ADD CONSTRAINT prospect_uq UNIQUE (id_customer);
-- ddl-end --

-- object: public.mailing_list | type: TABLE --
-- DROP TABLE IF EXISTS public.mailing_list CASCADE;
CREATE TABLE public.mailing_list (
	type varchar(20) NOT NULL,
	last_sent_date date,
	total_emails integer,
	is_subscribed smallint,
	email_prospect varchar(50),
	CONSTRAINT mailing_list_pk PRIMARY KEY (type)
);
-- ddl-end --
ALTER TABLE public.mailing_list OWNER TO postgres;
-- ddl-end --

-- object: prospect_fk | type: CONSTRAINT --
-- ALTER TABLE public.mailing_list DROP CONSTRAINT IF EXISTS prospect_fk CASCADE;
ALTER TABLE public.mailing_list ADD CONSTRAINT prospect_fk FOREIGN KEY (email_prospect)
REFERENCES public.prospect (email) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: member_fk | type: CONSTRAINT --
-- ALTER TABLE public.customer DROP CONSTRAINT IF EXISTS member_fk CASCADE;
ALTER TABLE public.customer ADD CONSTRAINT member_fk FOREIGN KEY (id_member)
REFERENCES public.member (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: customer_uq1 | type: CONSTRAINT --
-- ALTER TABLE public.customer DROP CONSTRAINT IF EXISTS customer_uq1 CASCADE;
ALTER TABLE public.customer ADD CONSTRAINT customer_uq1 UNIQUE (id_member);
-- ddl-end --

-- object: public.email | type: TABLE --
-- DROP TABLE IF EXISTS public.email CASCADE;
CREATE TABLE public.email (
	title varchar(50),
	description varchar(200),
	markup_html varchar(1000),
	id serial NOT NULL,
	CONSTRAINT email_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.email OWNER TO postgres;
-- ddl-end --

-- object: public.many_mailing_list_has_many_email | type: TABLE --
-- DROP TABLE IF EXISTS public.many_mailing_list_has_many_email CASCADE;
CREATE TABLE public.many_mailing_list_has_many_email (
	type_mailing_list varchar(20) NOT NULL,
	id_email integer NOT NULL,
	CONSTRAINT many_mailing_list_has_many_email_pk PRIMARY KEY (type_mailing_list,id_email)
);
-- ddl-end --

-- object: mailing_list_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_mailing_list_has_many_email DROP CONSTRAINT IF EXISTS mailing_list_fk CASCADE;
ALTER TABLE public.many_mailing_list_has_many_email ADD CONSTRAINT mailing_list_fk FOREIGN KEY (type_mailing_list)
REFERENCES public.mailing_list (type) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: email_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_mailing_list_has_many_email DROP CONSTRAINT IF EXISTS email_fk CASCADE;
ALTER TABLE public.many_mailing_list_has_many_email ADD CONSTRAINT email_fk FOREIGN KEY (id_email)
REFERENCES public.email (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.designer | type: TABLE --
-- DROP TABLE IF EXISTS public.designer CASCADE;
CREATE TABLE public.designer (
	id serial NOT NULL,
	name varchar(50),
	id_product integer,
	salary integer,
	id_department integer,
	CONSTRAINT designer_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.designer OWNER TO postgres;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.designer DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.designer ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.programmer | type: TABLE --
-- DROP TABLE IF EXISTS public.programmer CASCADE;
CREATE TABLE public.programmer (
	name varchar(50),
	id serial NOT NULL,
	salary integer,
	id_department integer,
	CONSTRAINT programmer_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.programmer OWNER TO postgres;
-- ddl-end --

-- object: public.department | type: TABLE --
-- DROP TABLE IF EXISTS public.department CASCADE;
CREATE TABLE public.department (
	id serial NOT NULL,
	name varchar(50),
	CONSTRAINT department_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.department OWNER TO postgres;
-- ddl-end --

-- object: department_fk | type: CONSTRAINT --
-- ALTER TABLE public.programmer DROP CONSTRAINT IF EXISTS department_fk CASCADE;
ALTER TABLE public.programmer ADD CONSTRAINT department_fk FOREIGN KEY (id_department)
REFERENCES public.department (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: department_fk | type: CONSTRAINT --
-- ALTER TABLE public.designer DROP CONSTRAINT IF EXISTS department_fk CASCADE;
ALTER TABLE public.designer ADD CONSTRAINT department_fk FOREIGN KEY (id_department)
REFERENCES public.department (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.payroll | type: TABLE --
-- DROP TABLE IF EXISTS public.payroll CASCADE;
CREATE TABLE public.payroll (
	id serial NOT NULL,
	amount integer,
	id_designer integer,
	id_programmer integer,
	CONSTRAINT payroll_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.payroll OWNER TO postgres;
-- ddl-end --

-- object: designer_fk | type: CONSTRAINT --
-- ALTER TABLE public.payroll DROP CONSTRAINT IF EXISTS designer_fk CASCADE;
ALTER TABLE public.payroll ADD CONSTRAINT designer_fk FOREIGN KEY (id_designer)
REFERENCES public.designer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: payroll_uq | type: CONSTRAINT --
-- ALTER TABLE public.payroll DROP CONSTRAINT IF EXISTS payroll_uq CASCADE;
ALTER TABLE public.payroll ADD CONSTRAINT payroll_uq UNIQUE (id_designer);
-- ddl-end --

-- object: programmer_fk | type: CONSTRAINT --
-- ALTER TABLE public.payroll DROP CONSTRAINT IF EXISTS programmer_fk CASCADE;
ALTER TABLE public.payroll ADD CONSTRAINT programmer_fk FOREIGN KEY (id_programmer)
REFERENCES public.programmer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: payroll_uq1 | type: CONSTRAINT --
-- ALTER TABLE public.payroll DROP CONSTRAINT IF EXISTS payroll_uq1 CASCADE;
ALTER TABLE public.payroll ADD CONSTRAINT payroll_uq1 UNIQUE (id_programmer);
-- ddl-end --

-- object: public.files | type: TABLE --
-- DROP TABLE IF EXISTS public.files CASCADE;
CREATE TABLE public.files (
	id serial NOT NULL,
	name varchar(50),
	content varchar(10000),
	id_programmer integer,
	CONSTRAINT files_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.files OWNER TO postgres;
-- ddl-end --

-- object: programmer_fk | type: CONSTRAINT --
-- ALTER TABLE public.files DROP CONSTRAINT IF EXISTS programmer_fk CASCADE;
ALTER TABLE public.files ADD CONSTRAINT programmer_fk FOREIGN KEY (id_programmer)
REFERENCES public.programmer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --


