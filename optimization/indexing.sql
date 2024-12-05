-- Indexes for foreign keys used in joins
create index on personal_information (id_customer);
create index on public.order (id_customer);
create index on public.order (id_product);
create index on public.order (id_customer, id_product);
create index on warranty (id_order);
create index on inventory (id_product);
create index on inventory_backorder (location_inventory);
create index on inventory_backorder (id_product_inventory);
create index on inventory_backorder (id_backorder);
create index on inventory_backorder (location_inventory, id_product_inventory, id_backorder);
