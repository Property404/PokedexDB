SET @pokemon=359;

SELECT pkm.pkm_code AS `#`, pkm.pkm_name AS Name, GROUP_CONCAT(`type`.type_name) AS `Type`, pkm.pkm_category AS Category, pkm.pkm_weight AS Weight
	FROM pkm, poketype, `type`
		WHERE poketype.pkm_code=pkm.pkm_code
			AND poketype.type_code=`type`.type_code
			AND pkm.pkm_code=@pokemon
	GROUP BY pkm.pkm_code;
 
SELECT pokemove.pokemove_level AS `Level`, move.move_name AS `Move`, move.move_condition AS `Condition`, move.move_category AS `Category`, `type`.type_name AS `Type`
	FROM pokemove, pkm, move, `type`
		WHERE pkm.pkm_code=pokemove.pkm_code
			AND move.move_code=pokemove.move_code
			AND move.type_code=`type`.type_code
			AND pkm.pkm_code=@pokemon
	ORDER BY pokemove.pokemove_level, move.move_name;
