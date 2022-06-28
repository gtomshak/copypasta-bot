CREATE TABLE IF NOT EXISTS guilds(
	GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "-"
);

CREATE TABLE IF NOT EXISTS copypasta (
	CopyPastaID text,
	GuildID integer,
	Content text NOT NULL,
	PRIMARY KEY(CopyPastaID, GuildID)
);

