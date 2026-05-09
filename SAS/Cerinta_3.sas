LIBNAME proiect '/home/u64501251/Proiect';

DATA proiect.consum_alcool;
    SET proiect.studenti2;

    length Nivel_Consum $ 15;

    Scor_Consum = SUM(Alcool_Saptamana, Alcool_Weekend);
    IF Scor_Consum <= 2      THEN Nivel_Consum = 'Consum scazut';
    ELSE IF Scor_Consum <= 5 THEN Nivel_Consum = 'Consum moderat';
    ELSE                          Nivel_Consum = 'Consum ridicat';

    LABEL Scor_Consum      = 'Scor total consum alcool'
          Nivel_Consum     = 'Nivel consum alcool'
          Alcool_Saptamana = 'Consum alcool saptamana'
          Alcool_Weekend   = 'Consum alcool weekend';

RUN;

TITLE "Analiza consum alcool studenti";
PROC PRINT DATA=proiect.consum_alcool LABEL;
    VAR Alcool_Saptamana Alcool_Weekend 
        Scor_Consum Nivel_Consum;
RUN;

TITLE "Distributia studentilor dupa nivelul de consum alcool";
PROC FREQ DATA=proiect.consum_alcool;
    TABLES Nivel_Consum / NOCUM;
RUN;

DATA proiect.analiza_note;
    SET proiect.studenti2;

    Nota_Min  = MIN(Nota_T1, Nota_T2, Nota_Finala);
    Nota_Max  = MAX(Nota_T1, Nota_T2, Nota_Finala);
    Progres   = Nota_T2 - Nota_T1;

    length Tip_Progres $ 25;
    IF Progres > 2                        THEN Tip_Progres = 'Progres cu peste 2 puncte';
    ELSE IF Progres >= 1 AND Progres <= 2 THEN Tip_Progres = 'Progres cu 1-2 puncte';
    ELSE IF Progres = 0                   THEN Tip_Progres = 'Stabil';
    ELSE IF Progres >= -2 AND Progres < 0 THEN Tip_Progres = 'Regres cu 1-2 puncte';
    ELSE                                       Tip_Progres = 'Regres cu peste 2 puncte';

    LABEL Nota_Min    = 'Nota minima'
          Nota_Max    = 'Nota maxima'
          Progres     = 'Progres intre teste'
          Tip_Progres = 'Nivel progres'
          Nota_T1     = 'Nota primul test'
          Nota_T2     = 'Nota al doilea test'
          Nota_Finala = 'Nota finala';

RUN;

PROC SORT DATA=proiect.analiza_note;
    BY DESCENDING Progres;
RUN;

TITLE "Analiza progres note studenti";
PROC PRINT DATA=proiect.analiza_note LABEL;
    VAR Nota_T1 Nota_T2 Nota_Finala
        Nota_Min Nota_Max 
        Progres Tip_Progres;
RUN;

TITLE "Distributia studentilor dupa nivelul de progres";
PROC FREQ DATA=proiect.analiza_note;
    TABLES Tip_Progres / NOCUM;
RUN;