UPDATE units SET
	is_default = :val
WHERE product_id = :product_id AND id <> :id;