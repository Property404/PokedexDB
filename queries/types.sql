SELECT pkm.pkm_code as '#', pkm.pkm_name as Name,GROUP_CONCAT(type.type_name) AS Type,pkm_category AS Species,pkm_weight as Weight FROM poketype
	JOIN pkm ON pkm.pkm_code=poketype.pkm_code
	JOIN type ON poketype.type_code=type.type_code
	WHERE pkm.pkm_code>700
	GROUP BY pkm.pkm_code;
