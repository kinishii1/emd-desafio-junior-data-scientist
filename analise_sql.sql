-- 1 
SELECT COUNT(*) AS total_ocorrencias 
FROM `datario.adm_central_atendimento_1746.chamado` 
WHERE DATE(data_inicio) = "2023-04-01";

-- 2
SELECT tipo, COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = "2023-04-01"
GROUP BY tipo
ORDER BY total_chamados DESC
LIMIT 1;

-- 3
SELECT b.nome AS nome_bairro, COUNT(c.id_bairro) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = "2023-04-01"
GROUP BY b.nome
ORDER BY total_chamados DESC
LIMIT 3;

-- 4
SELECT b.subprefeitura, COUNT(c.id_bairro) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = "2023-04-01"
GROUP BY b.subprefeitura
ORDER BY total_chamados DESC
LIMIT 1;

-- 5
SELECT c.*
FROM `datario.adm_central_atendimento_1746.chamado` c
LEFT JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = "2023-04-01" AND b.id_bairro IS NULL;
