UPDATE units SET
	is_default = :val
WHERE id = :id;