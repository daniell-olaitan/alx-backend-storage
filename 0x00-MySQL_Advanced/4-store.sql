-- create a trigger that decreases the quantity of an item
-- after adding a new order

CREATE TRIGGER decrease_quantity_after_order
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
