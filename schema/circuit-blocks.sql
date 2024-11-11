CREATE DATABASE "circuit-blocks";


-- object: public.credit_card | type: TABLE --
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
ALTER TABLE public.credit_card OWNER TO postgres;

-- object: public.warranty | type: TABLE --
CREATE TABLE public.warranty (
	id serial NOT NULL,
	expiration_date date,
	is_under boolean,
	CONSTRAINT warranty_pk PRIMARY KEY (id)
);
ALTER TABLE public.warranty OWNER TO postgres;

-- object: public.member | type: TABLE --
CREATE TABLE public.member (
	join_date date,
	expiration_date date,
	status_tier varchar(10),
	id smallint NOT NULL,
	CONSTRAINT member_pk PRIMARY KEY (id)
);
ALTER TABLE public.member OWNER TO postgres;

-- object: public.product | type: TABLE --
CREATE TABLE public.product (
	id serial NOT NULL,
	type varchar(10),
	cost integer,
	id_order integer,
	CONSTRAINT product_pk PRIMARY KEY (id)
);
ALTER TABLE public.product OWNER TO postgres;

-- object: public."order" | type: TABLE --
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
ALTER TABLE public."order" OWNER TO postgres;

-- object: public.customer | type: TABLE --
CREATE TABLE public.customer (
	id serial NOT NULL,
	name varchar(50),
	email varchar(50),
	phone numeric(10),
	number_credit_card numeric(16),
	id_member smallint,
	CONSTRAINT customer_pk PRIMARY KEY (id)
);
ALTER TABLE public.customer OWNER TO postgres;

-- object: customer_fk | type: CONSTRAINT --
ALTER TABLE public."order" ADD CONSTRAINT customer_fk FOREIGN KEY (id_customer)
REFERENCES public.customer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: credit_card_fk | type: CONSTRAINT --
ALTER TABLE public.customer ADD CONSTRAINT credit_card_fk FOREIGN KEY (number_credit_card)
REFERENCES public.credit_card (number) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: customer_uq | type: CONSTRAINT --
ALTER TABLE public.customer ADD CONSTRAINT customer_uq UNIQUE (number_credit_card);

-- object: order_fk | type: CONSTRAINT --
ALTER TABLE public.product ADD CONSTRAINT order_fk FOREIGN KEY (id_order)
REFERENCES public."order" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: warranty_fk | type: CONSTRAINT --
ALTER TABLE public."order" ADD CONSTRAINT warranty_fk FOREIGN KEY (id_warranty)
REFERENCES public.warranty (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: order_uq | type: CONSTRAINT --
ALTER TABLE public."order" ADD CONSTRAINT order_uq UNIQUE (id_warranty);

-- object: public.backorder | type: TABLE --
CREATE TABLE public.backorder (
	id serial NOT NULL,
	manufacturer varchar(20),
	quantity integer,
	cost smallint,
	CONSTRAINT backorder_pk PRIMARY KEY (id)
);
ALTER TABLE public.backorder OWNER TO postgres;

-- object: public.inventory | type: TABLE --
CREATE TABLE public.inventory (
	location varchar(20) NOT NULL,
	quantity integer,
	is_backordered boolean,
	id_product integer,
	id_backorder integer,
	CONSTRAINT inventory_pk PRIMARY KEY (location)
);
ALTER TABLE public.inventory OWNER TO postgres;

-- object: product_fk | type: CONSTRAINT --
ALTER TABLE public.inventory ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: backorder_fk | type: CONSTRAINT --
ALTER TABLE public.inventory ADD CONSTRAINT backorder_fk FOREIGN KEY (id_backorder)
REFERENCES public.backorder (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: inventory_uq | type: CONSTRAINT --
ALTER TABLE public.inventory ADD CONSTRAINT inventory_uq UNIQUE (id_backorder);

-- object: public.prospect | type: TABLE --
CREATE TABLE public.prospect (
	name varchar(50),
	email varchar(50) NOT NULL,
	id_customer integer,
	CONSTRAINT prospect_pk PRIMARY KEY (email)
);
ALTER TABLE public.prospect OWNER TO postgres;

-- object: customer_fk | type: CONSTRAINT --
ALTER TABLE public.prospect ADD CONSTRAINT customer_fk FOREIGN KEY (id_customer)
REFERENCES public.customer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: prospect_uq | type: CONSTRAINT --
ALTER TABLE public.prospect ADD CONSTRAINT prospect_uq UNIQUE (id_customer);

-- object: public.mailing_list | type: TABLE --
CREATE TABLE public.mailing_list (
	type varchar(20) NOT NULL,
	last_sent_date date,
	total_emails integer,
	is_subscribed smallint,
	email_prospect varchar(50),
	CONSTRAINT mailing_list_pk PRIMARY KEY (type)
);
ALTER TABLE public.mailing_list OWNER TO postgres;

-- object: prospect_fk | type: CONSTRAINT --
ALTER TABLE public.mailing_list ADD CONSTRAINT prospect_fk FOREIGN KEY (email_prospect)
REFERENCES public.prospect (email) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: member_fk | type: CONSTRAINT --
ALTER TABLE public.customer ADD CONSTRAINT member_fk FOREIGN KEY (id_member)
REFERENCES public.member (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: customer_uq1 | type: CONSTRAINT --
ALTER TABLE public.customer ADD CONSTRAINT customer_uq1 UNIQUE (id_member);

-- object: public.email | type: TABLE --
CREATE TABLE public.email (
	title varchar(50),
	description varchar(200),
	markup_html varchar(1000),
	id serial NOT NULL,
	CONSTRAINT email_pk PRIMARY KEY (id)
);
ALTER TABLE public.email OWNER TO postgres;

-- object: public.many_mailing_list_has_many_email | type: TABLE --
CREATE TABLE public.many_mailing_list_has_many_email (
	type_mailing_list varchar(20) NOT NULL,
	id_email integer NOT NULL,
	CONSTRAINT many_mailing_list_has_many_email_pk PRIMARY KEY (type_mailing_list,id_email)
);

-- object: mailing_list_fk | type: CONSTRAINT --
ALTER TABLE public.many_mailing_list_has_many_email ADD CONSTRAINT mailing_list_fk FOREIGN KEY (type_mailing_list)
REFERENCES public.mailing_list (type) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

-- object: email_fk | type: CONSTRAINT --
ALTER TABLE public.many_mailing_list_has_many_email ADD CONSTRAINT email_fk FOREIGN KEY (id_email)
REFERENCES public.email (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

-- object: public.designer | type: TABLE --
CREATE TABLE public.designer (
	id serial NOT NULL,
	name varchar(50),
	id_product integer,
	salary integer,
	id_department integer,
	CONSTRAINT designer_pk PRIMARY KEY (id)
);
ALTER TABLE public.designer OWNER TO postgres;

-- object: product_fk | type: CONSTRAINT --
ALTER TABLE public.designer ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: public.programmer | type: TABLE --
CREATE TABLE public.programmer (
	name varchar(50),
	id serial NOT NULL,
	salary integer,
	id_department integer,
	CONSTRAINT programmer_pk PRIMARY KEY (id)
);
ALTER TABLE public.programmer OWNER TO postgres;

-- object: public.department | type: TABLE --
CREATE TABLE public.department (
	id serial NOT NULL,
	name varchar(50),
	CONSTRAINT department_pk PRIMARY KEY (id)
);
ALTER TABLE public.department OWNER TO postgres;

-- object: department_fk | type: CONSTRAINT --
ALTER TABLE public.programmer ADD CONSTRAINT department_fk FOREIGN KEY (id_department)
REFERENCES public.department (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: department_fk | type: CONSTRAINT --
ALTER TABLE public.designer ADD CONSTRAINT department_fk FOREIGN KEY (id_department)
REFERENCES public.department (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: public.payroll | type: TABLE --
CREATE TABLE public.payroll (
	id serial NOT NULL,
	amount integer,
	id_designer integer,
	id_programmer integer,
	CONSTRAINT payroll_pk PRIMARY KEY (id)
);
ALTER TABLE public.payroll OWNER TO postgres;

-- object: designer_fk | type: CONSTRAINT --
ALTER TABLE public.payroll ADD CONSTRAINT designer_fk FOREIGN KEY (id_designer)
REFERENCES public.designer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: payroll_uq | type: CONSTRAINT --
ALTER TABLE public.payroll ADD CONSTRAINT payroll_uq UNIQUE (id_designer);

-- object: programmer_fk | type: CONSTRAINT --
ALTER TABLE public.payroll ADD CONSTRAINT programmer_fk FOREIGN KEY (id_programmer)
REFERENCES public.programmer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: payroll_uq1 | type: CONSTRAINT --
ALTER TABLE public.payroll ADD CONSTRAINT payroll_uq1 UNIQUE (id_programmer);

-- object: public.files | type: TABLE --
CREATE TABLE public.files (
	id serial NOT NULL,
	name varchar(50),
	content varchar(10000),
	id_programmer integer,
	CONSTRAINT files_pk PRIMARY KEY (id)
);
ALTER TABLE public.files OWNER TO postgres;

-- object: programmer_fk | type: CONSTRAINT --
ALTER TABLE public.files ADD CONSTRAINT programmer_fk FOREIGN KEY (id_programmer)
REFERENCES public.programmer (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
