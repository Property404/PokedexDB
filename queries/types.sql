SELECT pkm.pkm_code AS `#`, pkm.pkm_name AS Name,GROUP_CONCAT(`type`.type_name) AS `Type`,pkm_category AS Species,pkm_weight AS Weight
	FROM poketype, pkm, `type`
		WHERE pkm.pkm_code=poketype.pkm_code
			AND poketype.type_code=`type`.type_code
	GROUP BY pkm.pkm_code;
