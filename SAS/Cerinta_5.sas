LIBNAME proiect '/home/u64505510/Proiect';

TITLE "Statistici descriptive - Scoala GP";
PROC MEANS DATA=proiect.studenti_GP 
    N MEAN MEDIAN STD MIN MAX CLM;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

TITLE "Analiza distributie note - Scoala GP";
PROC UNIVARIATE DATA=proiect.studenti_GP;
    VAR Nota_Finala;
RUN;

TITLE "Statistici descriptive - Scoala MS";
PROC MEANS DATA=proiect.studenti_MS 
    N MEAN MEDIAN STD MIN MAX CLM ALPHA=0.05;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

TITLE "Analiza distributie note - Scoala MS";
PROC UNIVARIATE DATA=proiect.studenti_MS;
    VAR Nota_Finala;
RUN;

TITLE "Statistici descriptive - Mediul Rural";
PROC MEANS DATA=proiect.studenti_Rural 
    N MEAN MEDIAN STD MIN MAX CLM;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

TITLE "Analiza distributie note - Mediul Rural";
PROC UNIVARIATE DATA=proiect.studenti_Rural;
    VAR Nota_Finala;
RUN;

TITLE "Statistici descriptive - Mediul Urban";
PROC MEANS DATA=proiect.studenti_Urban 
    N MEAN MEDIAN STD MIN MAX CLM ALPHA=0.05;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

TITLE "Analiza distributie note - Mediul Urban";
PROC UNIVARIATE DATA=proiect.studenti_Urban;
    VAR Nota_Finala;
RUN;

TITLE "Statistici descriptive - Suport Educational Complet";
PROC MEANS DATA=proiect.studenti_SuportComplet 
    N MEAN MEDIAN STD MIN MAX CLM ALPHA=0.05;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

TITLE "Statistici descriptive - Suport Educational Partial";
PROC MEANS DATA=proiect.studenti_SuportPartial 
    N MEAN MEDIAN STD MIN MAX CLM ALPHA=0.05;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

/* statistici Fara Suport */
TITLE "Statistici descriptive - Fara Suport Educational";
PROC MEANS DATA=proiect.studenti_FaraSuport 
    N MEAN MEDIAN STD MIN MAX CLM;
    VAR Varsta Ore_Studiu Materii_Picate 
        Absente Nota_T1 Nota_T2 Nota_Finala Medie_Note;
RUN;

TITLE "Corelatia dintre factori si absentism - Spearman";
PROC CORR DATA=proiect.studenti2 SPEARMAN NOSIMPLE;
    VAR Varsta Ore_Studiu Materii_Picate 
        Alcool_Saptamana Alcool_Weekend
        Timp_Liber Iesiri Nota_T1 Nota_T2 Nota_Finala;
    WITH Absente;
RUN;


TITLE "Distributia promovabilitatii per scoala";
PROC FREQ DATA=proiect.studenti2;
    TABLES Scoala * Promovabilitate / NOCOL NOROW;
RUN;

TITLE "Distributia riscului de abandon per mediu";
PROC FREQ DATA=proiect.studenti2;
    TABLES Mediu * Risc_Abandon / NOCOL NOROW;
RUN;

TITLE "Distributia suportului educational per scoala";
PROC FREQ DATA=proiect.studenti2;
    TABLES Scoala * Suport_Educational / NOCOL NOROW;
RUN;
