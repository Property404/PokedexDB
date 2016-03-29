SELECT pkm.pkm_code AS `#`, pkm.pkm_name AS Name, GROUP_CONCAT(move.move_name) AS Moves
	FROM pokemove, pkm, move
	WHERE pkm.pkm_code = pokemove.pkm_code
		AND pokemove.move_code = move.move_code
		AND pkm.pkm_code<5
	GROUP BY pkm.pkm_code;
