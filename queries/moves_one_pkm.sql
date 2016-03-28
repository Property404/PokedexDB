SET @pokemon=21;
SELECT pkm.pkm_code AS "#", pkm.pkm_name as Name, group_concat(type.type_name) as Type, pkm.pkm_category as Category, pkm.pkm_weight as Weight  from pkm 
	JOIN poketype ON poketype.pkm_code=pkm.pkm_code
	JOIN type ON poketype.type_code = type.type_code
	where pkm.pkm_code=@pokemon
	GROUP BY pkm.pkm_code;
SELECT pokemove.pokemove_level, move.move_name, move.move_condition, move.move_category, type.type_name FROM pokemove
	JOIN pkm ON pkm.pkm_code=pokemove.pkm_code
	JOIN move ON move.move_code=pokemove.move_code
	JOIN type ON move.type_code = type.type_code
	WHERE pkm.pkm_code = @pokemon
	ORDER BY pokemove.pokemove_level;
