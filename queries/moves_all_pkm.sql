SELECT pkm.pkm_code as '#', pkm.pkm_name as Name,GROUP_CONCAT(move.move_name) AS Moves FROM pokemove 
	JOIN pkm ON pkm.pkm_code=pokemove.pkm_code
	JOIN move ON pokemove.move_code=move.move_code
	WHERE pkm.pkm_code<5
	GROUP BY pkm.pkm_code;
