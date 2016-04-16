SELECT base.pkm_name as `Base`, btype.type_name as `Type`,  next.pkm_name as `Evolution`, ntype.type_name as `Type`, next.evolution_condition as `Evolution Condtion`
	from pkm AS base, pkm AS next, poketype AS bpt, poketype npt,
		type as btype, type as ntype 
	WHERE base.pkm_code=next.evolution_code
		AND bpt.pkm_code=base.pkm_code
		AND npt.pkm_code=next.pkm_code
		AND bpt.type_code=btype.type_code
		AND npt.type_code=ntype.type_code
		AND bpt.poketype_is_primary=true
		AND npt.poketype_is_primary=true
		and bpt.type_code<>npt.type_code
	ORDER BY base.pkm_code DESC;
