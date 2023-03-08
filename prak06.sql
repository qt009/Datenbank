CREATE OR REPLACE FUNCTION getAvailableSeats(flightNumber varchar, flighDate date) RETURNS INTEGER AS $$
DECLARE
    this_kennzeichen varchar;
    typ INTEGER;
    sitze INTEGER;
    gebuchte_sitze INTEGER;
BEGIN
    SELECT a.kennzeichen INTO this_kennzeichen FROM Abflug a WHERE a.flugnr = flightNumber AND a.datum = flighDate;
    SELECT f.sitze INTO sitze FROM Flugzeug f WHERE f.kennzeichen = this_kennzeichen;
    SELECT COUNT(*) INTO gebuchte_sitze FROM Buchung b WHERE b.flugnr = flightNumber AND b.datum = flighDate;
    RETURN sitze - gebuchte_sitze;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION checkAvailableSeats()
RETURNS TRIGGER AS $$
DECLARE
  availableSeats INTEGER;
BEGIN
  SELECT getAvailableSeats(NEW.flugnr, NEW.datum) INTO availableSeats;
  IF availableSeats <= 0 THEN
    RAISE EXCEPTION 'All seats are occupied on this flight.';
  END IF;
  RETURN NEW;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER checkAvailableSeats
BEFORE INSERT ON Buchung
FOR EACH ROW
EXECUTE FUNCTION checkAvailableSeats();

CREATE OR REPLACE VIEW gebuchte_passagieren AS
    SELECT nachname, vorname, flugNr
    FROM Passagier NATURAL JOIN Buchung
	  ORDER BY nachname ASC