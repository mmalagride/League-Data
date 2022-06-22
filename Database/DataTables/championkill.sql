CREATE TABLE "data.championkill" (
	"event_gameid"	TEXT,
	"event_type"	TEXT,
	"event_timestamp"	INTEGER,
	"event_killerid"	TEXT,
	"event_victimid"	TEXT,
	"event_assist1"	TEXT,
	"event_assist2"	TEXT,
	"event_assist3"	TEXT,
	"event_assist4"	TEXT,
	"event_killedby"	TEXT,
	"event_posx"	INTEGER,
	"event_posy"	INTEGER,
	PRIMARY KEY("event_gameid","event_type","event_timestamp")
);