CREATE OR REPLACE FUNCTION clean_answer_duplicates() 
RETURNS TRIGGER 
AS $stamp$
DECLARE 
	var_survey_id INTEGER;
BEGIN
	SELECT s.id INTO var_survey_id FROM surveys_survey s
 	INNER JOIN surveys_possibleanswer pa ON pa.survey_id = s.id
 	WHERE pa.id = NEW.possibleanswer_id
 	GROUP BY s.id;
	
	DELETE FROM surveys_possibleanswer_voters pav
	WHERE pav.user_id = NEW.user_id 
	AND pav.possibleanswer_id IN (
 		SELECT pa.id FROM surveys_possibleanswer pa
 		WHERE pa.survey_id = var_survey_id
 		GROUP BY pa.id
 		);
	RETURN NEW;
END;
$stamp$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS unique_answers ON surveys_possibleanswer_voters;

CREATE TRIGGER unique_answers 
BEFORE INSERT 
ON surveys_possibleanswer_voters
FOR EACH ROW
EXECUTE PROCEDURE clean_answer_duplicates();

