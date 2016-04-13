SELECT pkm.pkm_code, pkm.pkm_name AS `Name`,`type`.type_name as `Primary Type`, COUNT(pokemove.move_code) AS `Moves of Same Type`
	FROM pkm,poketype,type,pokemove,move
	WHERE pkm.pkm_code=poketype.pkm_code
		AND pkm.pkm_code=pokemove.pkm_code
		AND `poketype`.poketype_is_primary=true
		AND pkm.pkm_code<722
		AND `type`.type_code=poketype.type_code
		AND move.move_code=pokemove.move_code
		AND move.type_code=poketype.type_code
	GROUP BY pkm.pkm_code
	ORDER BY COUNT(pokemove.move_code), pkm.pkm_code,pkm.pkm_name;
