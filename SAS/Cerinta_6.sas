LIBNAME proiect '/home/u64505510/Proiect';

GOPTIONS RESET=ALL;

TITLE "Distributia profilului comportamental per scoala";
PATTERN1 value=solid color=blue;
PATTERN2 value=solid color=cornflowerblue;
PATTERN3 value=solid color=navy;
PATTERN4 value=solid color=lightblue;
PROC GCHART DATA=proiect.comportament;
    VBAR Scoala / subgroup=Profil_Student
                  type=freq;
RUN;
QUIT;

TITLE "Distributia promovabilitatii per scoala";
PATTERN1 value=solid color=green;
PATTERN2 value=solid color=red;
PROC GCHART DATA=proiect.studenti2;
    VBAR Scoala / subgroup=Promovabilitate
                  type=freq;
RUN;
QUIT;

TITLE "Distributia riscului de abandon - Urban";
PATTERN1 value=solid color=blue;
PATTERN2 value=solid color=cornflowerblue;
PATTERN3 value=solid color=navy;
PROC GCHART DATA=proiect.studenti_Urban;
    HBAR Risc_Abandon / type=freq;
RUN;
QUIT;

TITLE "Distributia riscului de abandon - Rural";
PATTERN1 value=solid color=blue;
PATTERN2 value=solid color=cornflowerblue;
PATTERN3 value=solid color=navy;
PROC GCHART DATA=proiect.studenti_Rural;
    HBAR Risc_Abandon / type=freq;
RUN;
QUIT;

TITLE "Distributia suportului educational - Urban";
PATTERN1 value=solid color=red;
PATTERN2 value=solid color=salmon;
PATTERN3 value=solid color=crimson;
PROC GCHART DATA=proiect.studenti_Urban;
    PIE Suport_Educational /
        percent=outside
        value=outside
        slice=outside;
RUN;
QUIT;

TITLE "Distributia suportului educational - Rural";
PATTERN1 value=solid color=red;
PATTERN2 value=solid color=salmon;
PATTERN3 value=solid color=crimson;
PROC GCHART DATA=proiect.studenti_Rural;
    PIE Suport_Educational /
        percent=outside
        value=outside
        slice=outside;
RUN;
QUIT;
