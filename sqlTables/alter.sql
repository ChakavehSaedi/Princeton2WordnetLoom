#  --------------------  from 4_Collation.sql file  -------------------------------
ALTER TABLE db_name.word CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;

ALTER TABLE db_name.extgraph ADD INDEX idx_pos_and_packageno (packageno, pos);

#  --------------------  from 5_Laxicons.sql file  --------------------------------

# Lexicon table  -------------------------------------------
#?????
#INSERT INTO lexicon(id,name,lexicon_identifier) VALUES(0,100,100);
#?????
#UPDATE lexicon SET id=0 WHERE id=3;

ALTER TABLE lexicon 
ADD CONSTRAINT fk_lexicon_to_text
FOREIGN KEY (lexicon_identifier)
REFERENCES text(id);
# -----------------------------------------------------------

# Word table -----------------------------------------------
ALTER TABLE word
DROP FOREIGN KEY FK37C70A9567D038;

ALTER TABLE word
DROP COLUMN id_lexicon;
# -------------------------------------------------------------

# Pos table ------------------------------------------------

ALTER TABLE part_of_speech
ADD CONSTRAINT fk_lexicon_to_pos
FOREIGN KEY (id_lexicon)
REFERENCES lexicon(id);

# ------------------------------------------------------------
# Sense table ------------------------------------------------
ALTER TABLE sense
ADD CONSTRAINT fk_lexicon_to_sense
FOREIGN KEY (id_lexicon)
REFERENCES lexicon(id);
ALTER TABLE `sense` ADD COLUMN `status_id` BIGINT(20) NULL;
update sense set status_id = 1;

# Synset table ------------------------------------------------
ALTER TABLE `synset` ADD COLUMN `status_id` BIGINT(20) NULL;
update synset set status_id = 1;
#---------------------------------------------------------------

#Relation_type table -----------------------------------------
#?????
#UPDATE relation_type SET id_lexicon=0;

ALTER TABLE relation_type
ADD CONSTRAINT fk_lexicon_to_relation_type
FOREIGN KEY (id_lexicon)
REFERENCES lexicon(id);

#---------------------------------------------------------------
# Domain table -----------------------------------------
#?????
#UPDATE domain SET id_lexicon=0;

ALTER TABLE domain
ADD CONSTRAINT fk_lexicon_to_domain
FOREIGN KEY (id_lexicon)
REFERENCES lexicon(id);

#  --------------------  from 6_Split_Comment.sql file  --------------------------------

ALTER TABLE db_name.tracker_lexicalunit CHANGE COLUMN comment comment VARCHAR(2048) NULL DEFAULT NULL;
ALTER TABLE db_name.tracker_synset CHANGE COLUMN comment comment VARCHAR(2048) NULL DEFAULT NULL;

#  --------------------  from 7_UbyLmf.sql file  --------------------------------

ALTER TABLE relation_type ADD multilingual bool default 0;
update db_name.relation_type set multilingual=true;

# --------------------- later additions to the database
# --------------------- Dictionary tabel
CREATE TABLE `dictionaries` (
  `dtype` varchar(31) NOT NULL,
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
INSERT INTO dictionaries VALUES ('StatusDictionary',1,'default','Status Not Set'),('LanguageVariantDictionary',2,'default','Common');
