UPDATE units SET
	buy_price = :base_price * content,
	price = (:base_price + (:base_price * (margin/100.0))) * content
WHERE product_id = :id;