LIBNAME proiect '/home/u64501251/Proiect';

DATA proiect.ore_studiu_sim;
    SET proiect.studenti2;

    IF MISSING(Nota_Finala) THEN Nota_Finala = 0;
    IF MISSING(Ore_Studiu) THEN Ore_Studiu = 0;

    IF Nota_Finala < 10;

    Ore_Curente = Ore_Studiu;
    Nota_Estimata = Nota_Finala;
    Ore_Suplimentare = 0;

    DO UNTIL (Nota_Estimata >= 10);
        Ore_Curente + 1;
        Nota_Estimata + 0.5;
        Ore_Suplimentare + 1;
    END;

    LABEL Ore_Suplimentare = 'Ore suplimentare necesare'
          Nota_Estimata    = 'Nota estimata dupa studiu suplimentar'
          Nota_Finala      = 'Nota finala actuala'
          Ore_Studiu       = 'Ore studiu actuale';

    DROP Ore_Curente;

RUN;

TITLE "Ore suplimentare necesare pentru promovare";
PROC PRINT DATA=proiect.ore_studiu_sim (OBS=20) LABEL;
    VAR Nota_Finala Ore_Studiu
        Ore_Suplimentare Nota_Estimata;
RUN;

DATA proiect.comportament;
    SET proiect.studenti2;

    length Profil_Student $ 35
           Nivel_Comportament $ 15;

    ARRAY comportament(3) Alcool_Saptamana Alcool_Weekend Iesiri;
    Scor_Comportament = 0;

    DO i = 1 TO 3;
        IF comportament(i) > 3 THEN Scor_Comportament + 1;
    END;

    IF Scor_Comportament = 0      THEN Nivel_Comportament = 'Bun';
    ELSE IF Scor_Comportament = 1 THEN Nivel_Comportament = 'Mediu';
    ELSE                               Nivel_Comportament = 'Riscant';

    IF Scor_Comportament >= 2 AND Nota_Finala < 10 THEN
        Profil_Student = 'Impact negativ confirmat';
    ELSE IF Scor_Comportament >= 2 AND Nota_Finala >= 10 THEN
        Profil_Student = 'Rezistent la factori externi';
    ELSE IF Scor_Comportament < 2 AND Nota_Finala < 10 THEN
        Profil_Student = 'Alta cauza de esec';
    ELSE
        Profil_Student = 'Profil echilibrat';

    LABEL Scor_Comportament    = 'Scor comportamental'
          Nivel_Comportament   = 'Categoria comportament'
          Profil_Student       = 'Profil student'
          Alcool_Saptamana     = 'Consum alcool saptamana'
          Alcool_Weekend       = 'Consum alcool weekend'
          Iesiri               = 'Frecventa iesiri'
          Nota_Finala          = 'Nota finala';

    DROP i;

RUN;

PROC SORT DATA=proiect.comportament;
    BY DESCENDING Scor_Comportament;
RUN;

TITLE "Analiza profil comportamental si impact asupra notelor";
PROC PRINT DATA=proiect.comportament (OBS=20) LABEL;
    VAR Alcool_Saptamana Alcool_Weekend Iesiri 
        Scor_Comportament Nivel_Comportament
        Nota_Finala Profil_Student;
RUN;

TITLE "Distributia studentilor pe profile comportamentale";
PROC FREQ DATA=proiect.comportament;
    TABLES Profil_Student / NOCUM;
RUN;