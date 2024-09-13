-- Create a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE total_point FLOAT;
    DECLARE average_score FLOAT;

    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_point, total_weight
    FROM corrections AS c
    INNER JOIN projects AS p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    IF total_weight > 0 THEN
        SET average_score = total_point / total_weight;
    ELSE
        SET average_score = 0;
    END IF;

    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;

END //

DELIMITER ;
