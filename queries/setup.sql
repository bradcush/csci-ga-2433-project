-- Setup required to query inventory backorders
insert into product (id, type, price) values (1, 'bundle', 2499);
insert into product (id, type, price) values (2, 'battery', 499);
insert into product (id, type, price) values (3, 'block', 199);

insert into backorder (id, manufacturer, quantity, cost, status) values (1, 'somewhere', 100, 30000, 'open');
insert into backorder (id, manufacturer, quantity, cost, status) values (2, 'elsewhere', 1000, 200000, 'filled');

insert into inventory (location, quantity, id_product) values ('poughkeepsie', 500, 1);
insert into inventory (location, quantity, id_product) values ('poughkeepsie', 250, 2);
insert into inventory (location, quantity, id_product) values ('poughkeepsie', 1000, 3);
insert into inventory (location, quantity, id_product) values ('berkeley', 200, 1);
insert into inventory (location, quantity, id_product) values ('berkeley', 100, 2);
insert into inventory (location, quantity, id_product) values ('berkeley', 500, 3);

insert into inventory_backorder (location_inventory, id_product_inventory, id_backorder) values ('berkeley', 2, 1);
insert into inventory_backorder (location_inventory, id_product_inventory, id_backorder) values ('berkeley', 3, 2);

-- Setup required for adding personal information and warranty
insert into prospect (name, email) values ('bradley', 'bradley@whatit.be');
insert into prospect (name, email) values ('laura', 'laura@whatit.be');
insert into prospect (name, email) values ('oodie', 'oodie@whatit.be');

insert into customer (id, name, email, phone, email_prospect) values (1, 'bradley', 'bradley@whatit.be', 1234567890, 'bradley@whatit.be');
insert into customer (id, name, email, phone, email_prospect) values (2, 'laura', 'laura@whatit.be', 1234567890, 'laura@whatit.be');
insert into customer (id, name, email, phone, email_prospect) values (3, 'oodie', 'oodie@whatit.be', 1234567890, 'oodie@whatit.be');

insert into personal_information (age, kids_count, pets_count, siblings_count, income, has_risk, id_customer) values (37, 2, 1, 3, 900000, 1, 2);

-- We need to prefix order with the public schema because order is a keyword
insert into public.order (id, status, date, quantity, total_amt, id_customer, id_product) values (1, 'filled', '2024-10-24', 1, 2499, 1, 1);
insert into public.order (id, status, date, quantity, total_amt, id_customer, id_product) values (2, 'filled', '2024-11-19', 1, 2499, 1, 1);
insert into public.order (id, status, date, quantity, total_amt, id_customer, id_product) values (3, 'filled', '2024-11-20', 2, 398, 1, 3);
insert into public.order (id, status, date, quantity, total_amt, id_customer, id_product) values (4, 'filled', '2024-12-02', 1, 499, 1, 2);
insert into public.order (id, status, date, quantity, total_amt, id_customer, id_product) values (5, 'filled', '2024-12-03', 1, 199, 1, 3);

insert into warranty (id, expiration_date, price, percentage, id_order, date_order) values (1, '2025-12-01', 98, 20, 1, '2024-10-24');
