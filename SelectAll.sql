SELECT
    game_name as Spiel,
    steam_reviews as Steam,
    rift_reviews as Rift,
    quest_reviews as Quest,
    (steam_reviews + rift_reviews + quest_reviews) AS Gesamt
FROM
    vr_games
ORDER BY
	Gesamt DESC;