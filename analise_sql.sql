-- 1
SELECT COUNT(*) AS total_ocorrencias
FROM
    `datario.adm_central_atendimento_1746.chamado`
WHERE
    DATE(data_inicio) = "2023-04-01";

-- 2
SELECT tipo, COUNT(*) AS total_chamados
FROM
    `datario.adm_central_atendimento_1746.chamado`
WHERE
    DATE(data_inicio) = "2023-04-01"
GROUP BY
    tipo
ORDER BY total_chamados DESC
LIMIT 1;

-- 3
SELECT b.nome AS nome_bairro, COUNT(c.id_bairro) AS total_chamados
FROM
    `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE
    DATE(c.data_inicio) = "2023-04-01"
GROUP BY
    b.nome
ORDER BY total_chamados DESC
LIMIT 3;

-- 4
SELECT b.subprefeitura, COUNT(c.id_bairro) AS total_chamados
FROM
    `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE
    DATE(c.data_inicio) = "2023-04-01"
GROUP BY
    b.subprefeitura
ORDER BY total_chamados DESC
LIMIT 1;

-- 5
SELECT c.*
FROM
    `datario.adm_central_atendimento_1746.chamado` c
    LEFT JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE
    DATE(c.data_inicio) = "2023-04-01"
    AND b.id_bairro IS NULL;
-- 73 chamados sem bairro associado
-- verificando outros dias do mesmo mes podemos concluir que há uma predominância de chamados tipo "Onibus" e "Atendimento ao cidadão". Podemos assumir que esses chamados os campos nao sejam requeridos. Caso contrario haja algum erro no momento da inserção dos dados especificamente para esses tipos.

-- 6
SELECT count(*) as chamados
FROM
    `datario.adm_central_atendimento_1746.chamado`
WHERE
    subtipo = "Perturbação do sossego"
    AND (
        DATE(data_inicio) BETWEEN "2022-01-01" AND "2023-12-31"
    );

-- utilizando a função DISTINCT para retornar as datas unicas verificasse que não há nenhuma chamada no intervalo pedido
SELECT DISTINCT
    DATE(data_inicio)
FROM
    `datario.adm_central_atendimento_1746.chamado`
WHERE
    subtipo = "Perturbação do sossego"
    -- 7
SELECT COUNT(*) AS total_chamados
FROM
    `datario.adm_central_atendimento_1746.chamado` c
    INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e ON (
        DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    )
WHERE
    c.subtipo = "Perturbação do sossego";

-- 8 Quantos chamados desse subtipo foram abertos em cada evento?

SELECT e.evento, COUNT(c.id_chamado) AS total_chamados
FROM
    `datario.adm_central_atendimento_1746.chamado` c
    INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e ON (
        DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    )
WHERE
    c.subtipo = "Perturbação do sossego"
GROUP BY
    e.evento
ORDER BY total_chamados DESC;

-- 9 Qual evento teve a maior média diária de chamados abertos desse subtipo?

SELECT subquery.evento, SUM(subquery.total_chamados) / (
        DATE_DIFF (
            MAX(subquery.data_fim), MIN(subquery.data_inicio), DAY
        ) + 1
    ) AS media_diaria
FROM (
        SELECT
            e.evento, DATE(c.data_inicio) AS data_inicio, DATE(c.data_fim) AS data_fim, COUNT(c.id_chamado) AS total_chamados
        FROM
            `datario.adm_central_atendimento_1746.chamado` c
            INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e ON (
                DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
            )
        WHERE
            c.subtipo = "Perturbação do sossego"
        GROUP BY
            e.evento, data_inicio, data_fim
    ) AS subquery
GROUP BY
    subquery.evento
ORDER BY media_diaria DESC
LIMIT 1;

-- 10 Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

WITH
    media_eventos AS (
        SELECT subquery.evento, SUM(subquery.total_chamados) / (
                DATE_DIFF (
                    MAX(subquery.data_fim), MIN(subquery.data_inicio), DAY
                ) + 1
            ) AS media_diaria
        FROM (
                SELECT
                    e.evento, DATE(c.data_inicio) AS data_inicio, DATE(c.data_fim) AS data_fim, COUNT(c.id_chamado) AS total_chamados
                FROM
                    `datario.adm_central_atendimento_1746.chamado` c
                    INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e ON (
                        DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
                    )
                WHERE
                    c.subtipo = "Perturbação do sossego"
                GROUP BY
                    e.evento, data_inicio, data_fim
            ) AS subquery
        GROUP BY
            subquery.evento
    ),
    media_total AS (
        SELECT COUNT(*) / (
                DATE_DIFF (
                    DATE '2023-12-31', DATE '2022-01-01', DAY
                ) + 1
            ) AS media_diaria
        FROM datario.adm_central_atendimento_1746.chamado
        WHERE
            subtipo = 'Perturbação do sossego'
            AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
    )
SELECT
    media_eventos.evento AS evento,
    media_eventos.media_diaria AS media_diaria_evento,
    media_total.media_diaria AS media_diaria_total
FROM media_eventos, media_total;