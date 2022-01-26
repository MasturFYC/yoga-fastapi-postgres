UPDATE stocks SET
	total = total + :total - ,
	price = (:base_price + (:base_price * (margin/100.0))) * content
WHERE product_id = :id;