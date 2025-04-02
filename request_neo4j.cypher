// 1. Afficher 10 films et les acteurs ayant joué dedans
MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
RETURN a.name AS Acteur, f.title AS Film
LIMIT 10;


// 2. Films réalisés par un réalisateur particulier (tous réalisateurs)
MATCH (f:Film)-[:DIRECTED_BY]->(d:Director)
RETURN f.title AS Film, d.name AS Réalisateur
LIMIT 5;


// 3. Films dans lesquels Matt Damon a joué
MATCH (a:Actor {name: "Matt Damon"})-[:ACTED_IN]->(f:Film)
RETURN f.title AS Film, f.year AS Année
ORDER BY f.year DESC;


// 4. Nombre de films par réalisateur (top 10)
MATCH (f:Film)-[:DIRECTED_BY]->(d:Director)
RETURN d.name AS Réalisateur, COUNT(f) AS NbFilms
ORDER BY NbFilms DESC
LIMIT 10;


// 5. Tous les acteurs ayant joué dans "The Departed"
MATCH (a:Actor)-[:ACTED_IN]->(f:Film {title: "The Departed"})
RETURN a.name AS Acteur;


// 6. Genres associés au film "Inception"
MATCH (f:Film {title: "Inception"})-[:BELONGS_TO]->(g:Genre)
RETURN g.name AS Genre;


// 7. Top 10 des acteurs avec le plus de films
MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
RETURN a.name AS Acteur, COUNT(f) AS NbFilms
ORDER BY NbFilms DESC
LIMIT 10;


// 8. Films appartenant au genre "Drama"
MATCH (f:Film)-[:BELONGS_TO]->(g:Genre {name: "Drama"})
RETURN f.title AS Film, f.year AS Année
ORDER BY f.year DESC
LIMIT 10;
