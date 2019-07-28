CREATE TABLE "complains" (
	"complain_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"userid"	INTEGER NOT NULL,
	"complain_type"	TEXT NOT NULL,
	"complain_desc"	TEXT NOT NULL,
	"timestamp"	INTEGER NOT NULL,
	"assignee"	INTEGER,
	"is_solved"	INTEGER NOT NULL DEFAULT 0,
	"deleted"	INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE "departments" (
	"deptid" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name" TEXT NOT NULL
);

CREATE TABLE "users" (
	"userid"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"fname"	TEXT NOT NULL,
	"lname"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"phonenumber"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"role"	TEXT NOT NULL DEFAULT 'user',
	"department"	INTEGER
);

CREATE TABLE "projector_request" (
	"request_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"userid"	INTEGER NOT NULL,
	"start_datetime"	NUMERIC NOT NULL,
	"end_datetime"	NUMERIC NOT NULL,
	"purpose"	TEXT NOT NULL,
	"status"	INTEGER NOT NULL DEFAULT 0,
	"deleted"	INTEGER NOT NULL DEFAULT 0
);

INSERT INTO "main"."departments" ("deptid", "name") VALUES ('1', 'Statistics');
INSERT INTO "main"."departments" ("deptid", "name") VALUES ('2', 'Grading and Inspection');
INSERT INTO "main"."departments" ("deptid", "name") VALUES ('3', 'Area Office');
INSERT INTO "main"."departments" ("deptid", "name") VALUES ('4', 'Final Inspection');