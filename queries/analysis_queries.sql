-- Competitions by category
SELECT c.category_name, COUNT(*) AS total_competitions
FROM Competitions cp
JOIN Categories c ON c.category_id = cp.category_id
GROUP BY c.category_name;

-- Top 10 competitors by ranking
SELECT co.name, r.rank, r.points
FROM Competitor_Rankings r
JOIN Competitors co ON r.competitor_id = co.competitor_id
ORDER BY r.rank ASC LIMIT 10;
