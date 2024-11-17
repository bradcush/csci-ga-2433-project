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
