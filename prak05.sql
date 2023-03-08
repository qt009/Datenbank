/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     28/11/2022 23:54:57                          */
/*==============================================================*/


drop index ASSOCIATION_5_FK;

drop index ASSOCIATION_4_FK;

drop index ABFLUG_PK;

drop table Abflug;

drop index BUCHT_FK;

drop index GEBUCHT_FK;

drop index BUCHUNG_PK;

drop table Buchung;

drop index ZIEL_FK;

drop index START_FK;

drop index FLUG_PK;

drop table Flug;

drop index FLUGHAFEN_PK;

drop table Flughafen;

drop index FLUGZEUG_PK;

drop table Flugzeug;

drop index PASSAGIER_PK;

drop table Passagier;

drop index WARTET_FK;

drop index GEWARTET_FK;

drop index WARTUNG_PK;

drop table Wartung;

drop index WARTUNGSTECHNIKER_PK;

drop table Wartungstechniker;

/*==============================================================*/
/* Table: Abflug                                                */
/*==============================================================*/
create table Abflug (
   flugNr               VARCHAR(254)         not null,
   datum                DATE                 not null,
   kennzeichen          VARCHAR(254)         not null,
   constraint PK_ABFLUG primary key (flugNr, datum)
);

/*==============================================================*/
/* Index: ABFLUG_PK                                             */
/*==============================================================*/
create unique index ABFLUG_PK on Abflug (
flugNr,
datum
);

/*==============================================================*/
/* Index: ASSOCIATION_4_FK                                      */
/*==============================================================*/
create  index ASSOCIATION_4_FK on Abflug (
kennzeichen
);

/*==============================================================*/
/* Index: ASSOCIATION_5_FK                                      */
/*==============================================================*/
create  index ASSOCIATION_5_FK on Abflug (
flugNr
);

/*==============================================================*/
/* Table: Buchung                                               */
/*==============================================================*/
create table Buchung (
   kundennummer         INT4                 not null,
   flugNr               VARCHAR(254)         not null,
   datum                DATE                 not null,
   ticket_preis         NUMERIC              null,
   constraint PK_BUCHUNG primary key (flugNr, kundennummer, datum)
);

/*==============================================================*/
/* Index: BUCHUNG_PK                                            */
/*==============================================================*/
create unique index BUCHUNG_PK on Buchung (
flugNr,
kundennummer,
datum
);

/*==============================================================*/
/* Index: GEBUCHT_FK                                            */
/*==============================================================*/
create  index GEBUCHT_FK on Buchung (
kundennummer
);

/*==============================================================*/
/* Index: BUCHT_FK                                              */
/*==============================================================*/
create  index BUCHT_FK on Buchung (
flugNr,
datum
);

/*==============================================================*/
/* Table: Flug                                                  */
/*==============================================================*/
create table Flug (
   flugNr               VARCHAR(254)         not null,
   start                VARCHAR(254)         null,
   ziel                 VARCHAR(254)         null,
   constraint PK_FLUG primary key (flugNr)
);

/*==============================================================*/
/* Index: FLUG_PK                                               */
/*==============================================================*/
create unique index FLUG_PK on Flug (
flugNr
);

/*==============================================================*/
/* Index: START_FK                                              */
/*==============================================================*/
create  index START_FK on Flug (
start
);

/*==============================================================*/
/* Index: ZIEL_FK                                               */
/*==============================================================*/
create  index ZIEL_FK on Flug (
ziel
);

/*==============================================================*/
/* Table: Flughafen                                             */
/*==============================================================*/
create table Flughafen (
   IATA                 VARCHAR(254)         not null,
   name                 VARCHAR(254)         null,
   laengengrad          NUMERIC              null,
   breitengrad          NUMERIC              null,
   constraint PK_FLUGHAFEN primary key (IATA)
);

/*==============================================================*/
/* Index: FLUGHAFEN_PK                                          */
/*==============================================================*/
create unique index FLUGHAFEN_PK on Flughafen (
IATA
);

/*==============================================================*/
/* Table: Flugzeug                                              */
/*==============================================================*/
create table Flugzeug (
   sitze                INT4                 null,
   kennzeichen          VARCHAR(254)         not null,
   typ                  VARCHAR(254)         null,
   constraint PK_FLUGZEUG primary key (kennzeichen)
);

/*==============================================================*/
/* Index: FLUGZEUG_PK                                           */
/*==============================================================*/
create unique index FLUGZEUG_PK on Flugzeug (
kennzeichen
);

/*==============================================================*/
/* Table: Passagier                                             */
/*==============================================================*/
create table Passagier (
   kundennummer         INT4                 not null,
   vorname              VARCHAR(254)         null,
   nachname             VARCHAR(254)         null,
   bonusmeilen          INT4                 null,
   constraint PK_PASSAGIER primary key (kundennummer)
);

/*==============================================================*/
/* Index: PASSAGIER_PK                                          */
/*==============================================================*/
create unique index PASSAGIER_PK on Passagier (
kundennummer
);

/*==============================================================*/
/* Table: Wartung                                               */
/*==============================================================*/
create table Wartung (
   WNR                  INT4                 not null,
   kennzeichen          VARCHAR(254)         not null,
   datum                DATE                 not null,
   constraint PK_WARTUNG primary key (WNR, kennzeichen, datum)
);

/*==============================================================*/
/* Index: WARTUNG_PK                                            */
/*==============================================================*/
create unique index WARTUNG_PK on Wartung (
WNR,
kennzeichen,
datum
);

/*==============================================================*/
/* Index: GEWARTET_FK                                           */
/*==============================================================*/
create  index GEWARTET_FK on Wartung (
WNR
);

/*==============================================================*/
/* Index: WARTET_FK                                             */
/*==============================================================*/
create  index WARTET_FK on Wartung (
kennzeichen
);

/*==============================================================*/
/* Table: Wartungstechniker                                     */
/*==============================================================*/
create table Wartungstechniker (
   vorname              VARCHAR(254)         null,
   nachname             VARCHAR(254)         null,
   WNR                  INT4                 not null,
   constraint PK_WARTUNGSTECHNIKER primary key (WNR)
);

/*==============================================================*/
/* Index: WARTUNGSTECHNIKER_PK                                  */
/*==============================================================*/
create unique index WARTUNGSTECHNIKER_PK on Wartungstechniker (
WNR
);

alter table Abflug
   add constraint FK_ABFLUG_ASSOCIATI_FLUGZEUG foreign key (kennzeichen)
      references Flugzeug (kennzeichen)
      on delete restrict on update restrict;

alter table Abflug
   add constraint FK_ABFLUG_ASSOCIATI_FLUG foreign key (flugNr)
      references Flug (flugNr)
      on delete restrict on update restrict;

alter table Buchung
   add constraint FK_BUCHUNG_BUCHT_ABFLUG foreign key (flugNr, datum)
      references Abflug (flugNr, datum)
      on delete restrict on update restrict;

alter table Buchung
   add constraint FK_BUCHUNG_GEBUCHT_PASSAGIE foreign key (kundennummer)
      references Passagier (kundennummer)
      on delete restrict on update restrict;

alter table Flug
   add constraint FK_FLUG_START_FLUGHAFE foreign key (start)
      references Flughafen (IATA)
      on delete restrict on update restrict;

alter table Flug
   add constraint FK_FLUG_ZIEL_FLUGHAFE foreign key (ziel)
      references Flughafen (IATA)
      on delete restrict on update restrict;

alter table Wartung
   add constraint FK_WARTUNG_GEWARTET_WARTUNGS foreign key (WNR)
      references Wartungstechniker (WNR)
      on delete restrict on update restrict;

alter table Wartung
   add constraint FK_WARTUNG_WARTET_FLUGZEUG foreign key (kennzeichen)
      references Flugzeug (kennzeichen)
      on delete restrict on update restrict;

