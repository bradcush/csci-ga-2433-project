-- List products and inventory
select id, type, price, location, quantity
from product as p, inventory as i
where p.id = i.id_product;

-- List backordered products which are low on inventory
select p.id, type, price, location, i.quantity, manufacturer, b.quantity
from product as p, inventory as i, inventory_backorder as ib, backorder as b
where p.id = i.id_product and i.location = ib.location_inventory
  and i.id_product = ib.id_product_inventory and ib.id_backorder = b.id;
