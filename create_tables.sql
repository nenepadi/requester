CREATE TABLE "users" (
	"userid" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"fname" TEXT NOT NULL,
	"lname" TEXT NOT NULL,
	"email" TEXT NOT NULL UNIQUE,
	"phonenumber" TEXT NOT NULL UNIQUE,
	"password" TEXT NOT NULL,
	"role" TEXT NOT NULL DEFAULT 'user'
)