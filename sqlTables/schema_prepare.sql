-- SET FOREIGN_KEY_CHECKS = 0;
-- ----------------------------------------------------------------------------
-- Table attribute_type
-- ----------------------------------------------------------------------------

SET SESSION SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

CREATE TABLE IF NOT EXISTS attribute_type (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  table_name ENUM('sense','synset','proposedconnatr') CHARACTER SET utf8 NOT NULL,
  type_name BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FK8B17DEFDC342D3F1 (type_name ASC),
  CONSTRAINT FK8B17DEFDC342D3F1
    FOREIGN KEY (type_name)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table text
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS text (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  text VARCHAR(2048) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_text_text (text(255) ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table corpus_example
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corpus_example (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  text TEXT CHARACTER SET utf8 NULL DEFAULT NULL,
  word BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FKD2C1EBF3A48A0468 (word ASC),
  CONSTRAINT FKD2C1EBF3A48A0468
    FOREIGN KEY (word)
    REFERENCES word (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table word
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS word (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  word VARCHAR(255) CHARACTER SET utf8 NOT NULL,
  id_lexicon BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FK37C70A9567D038 (id_lexicon ASC),
  INDEX idx_word_word (word ASC),
  CONSTRAINT FK37C70A9567D038
    FOREIGN KEY (id_lexicon)
    REFERENCES lexicon (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table domain
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS domain (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  description BIGINT(20) NULL DEFAULT NULL,
  name BIGINT(20) NOT NULL,
  id_lexicon bigint(20),
  PRIMARY KEY (id),
  INDEX FKB0F3D4C4A484360C (name ASC),
  INDEX FKB0F3D4C43D863F7D (description ASC),
  CONSTRAINT FKB0F3D4C43D863F7D
    FOREIGN KEY (description)
    REFERENCES text (id),
  CONSTRAINT FKB0F3D4C4A484360C
    FOREIGN KEY (name)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table domain_allowed_posses
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS domain_allowed_posses (
  id_pos BIGINT(20) NOT NULL,
  id_domain BIGINT(20) NOT NULL,
  PRIMARY KEY (id_pos, id_domain),
  INDEX FKCCE940DF4ADEF630 (id_pos ASC),
  INDEX FKCCE940DF6EB4E680 (id_domain ASC),
  CONSTRAINT FKCCE940DF4ADEF630
    FOREIGN KEY (id_pos)
    REFERENCES part_of_speech (id),
  CONSTRAINT FKCCE940DF6EB4E680
    FOREIGN KEY (id_domain)
    REFERENCES domain (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table part_of_speech
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS part_of_speech (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  name BIGINT(20) NOT NULL,
  id_lexicon bigint(20),
  uby_lmf_type varchar(255) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (id),
  INDEX FKD61652FEA484360C (name ASC),
  CONSTRAINT FKD61652FEA484360C
    FOREIGN KEY (name)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

ALTER TABLE part_of_speech AUTO_INCREMENT=0;

-- ----------------------------------------------------------------------------
-- Table extgraph
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS extgraph (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  packageno BIGINT(20) NULL DEFAULT NULL,
  score1 DOUBLE NULL DEFAULT NULL,
  score2 DOUBLE NULL DEFAULT NULL,
  weak BIT(1) NULL DEFAULT NULL,
  word VARCHAR(255) CHARACTER SET utf8 NULL DEFAULT NULL,
  pos BIGINT(20) NULL DEFAULT NULL,
  synid BIGINT(20) NULL DEFAULT NULL,
  PRIMARY KEY (id),
  INDEX FK939563CDD8FD93D1 (synid ASC),
  INDEX FK939563CD9205BF54 (pos ASC),
  INDEX idx_extgraph_packageno (packageno ASC),
  CONSTRAINT FK939563CD9205BF54
    FOREIGN KEY (pos)
    REFERENCES part_of_speech (id),
  CONSTRAINT FK939563CDD8FD93D1
    FOREIGN KEY (synid)
    REFERENCES synset (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table synset
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS synset (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  split INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table extgraphextension
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS extgraphextension (
  base BIT(1) NULL DEFAULT NULL,
  rank DOUBLE NULL DEFAULT NULL,
  REL_ID BIGINT(20) NOT NULL,
  UNIT_ID BIGINT(20) NOT NULL,
  EXTGRAPH_ID BIGINT(20) NOT NULL,
  PRIMARY KEY (REL_ID, UNIT_ID, EXTGRAPH_ID),
  INDEX FK8516AF12D459C82B (REL_ID ASC),
  INDEX FK8516AF12920BFECE (EXTGRAPH_ID ASC),
  INDEX FK8516AF12D4A47190 (UNIT_ID ASC),
  CONSTRAINT FK8516AF12D4A47190
    FOREIGN KEY (UNIT_ID)
    REFERENCES sense (id),
  CONSTRAINT FK8516AF12920BFECE
    FOREIGN KEY (EXTGRAPH_ID)
    REFERENCES extgraph (id),
  CONSTRAINT FK8516AF12D459C82B
    FOREIGN KEY (REL_ID)
    REFERENCES relation_type (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table sense
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sense (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  sense_number INT(11) NOT NULL DEFAULT '-1',
  domain BIGINT(20) NOT NULL,
  lemma BIGINT(20) NOT NULL,
  part_of_speech BIGINT(20) NOT NULL,
  id_lexicon bigint(20),
  PRIMARY KEY (id),
  INDEX FK68423AE681A5FFE (part_of_speech ASC),
  INDEX FK68423AEAA73B806 (lemma ASC),
  INDEX FK68423AE693DDADC (domain ASC),
  CONSTRAINT FK68423AE693DDADC
    FOREIGN KEY (domain)
    REFERENCES domain (id),
  CONSTRAINT FK68423AE681A5FFE
    FOREIGN KEY (part_of_speech)
    REFERENCES part_of_speech (id),
  CONSTRAINT FK68423AEAA73B806
    FOREIGN KEY (lemma)
    REFERENCES word (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table relation_type
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS relation_type (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  auto_reverse BIT(1) NOT NULL,
  argument_type BIGINT(20) NOT NULL,
  description BIGINT(20) NULL DEFAULT NULL,
  display_text BIGINT(20) NOT NULL,
  name BIGINT(20) NOT NULL,
  parent BIGINT(20) NULL DEFAULT NULL,
  reverse BIGINT(20) NULL DEFAULT NULL,
  short_display_text BIGINT(20) NOT NULL,
  id_lexicon bigint(20),
  PRIMARY KEY (id),
  INDEX FK1B162B9DC435D8EE (short_display_text ASC),
  INDEX FK1B162B9DA484360C (name ASC),
  INDEX FK1B162B9D3D863F7D (description ASC),
  INDEX FK1B162B9D497CA0B (display_text ASC),
  INDEX FK1B162B9D4D9DD48C (reverse ASC),
  INDEX FK1B162B9DD0BA8A54 (parent ASC),
  INDEX FK1B162B9D571A30A9 (argument_type ASC),
  CONSTRAINT FK1B162B9D571A30A9
    FOREIGN KEY (argument_type)
    REFERENCES relation_argument (id),
  CONSTRAINT FK1B162B9D3D863F7D
    FOREIGN KEY (description)
    REFERENCES text (id),
  CONSTRAINT FK1B162B9D497CA0B
    FOREIGN KEY (display_text)
    REFERENCES text (id),
  CONSTRAINT FK1B162B9D4D9DD48C
    FOREIGN KEY (reverse)
    REFERENCES relation_type (id),
  CONSTRAINT FK1B162B9DA484360C
    FOREIGN KEY (name)
    REFERENCES text (id),
  CONSTRAINT FK1B162B9DC435D8EE
    FOREIGN KEY (short_display_text)
    REFERENCES text (id),
  CONSTRAINT FK1B162B9DD0BA8A54
    FOREIGN KEY (parent)
    REFERENCES relation_type (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table lexicon
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lexicon (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  name BIGINT(20) NOT NULL,
  lexicon_identifier bigint(20),
  language VARCHAR(4) NULL,
  PRIMARY KEY (id),
  INDEX FK446B718A484360C (name ASC),
  CONSTRAINT FK446B718A484360C
    FOREIGN KEY (name)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table relation_argument
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS relation_argument (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  name BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FKD06411A0A484360C (name ASC),
  CONSTRAINT FKD06411A0A484360C
    FOREIGN KEY (name)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table relation_test
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS relation_test (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  pos BIGINT(20) NOT NULL,
  relation_type BIGINT(20) NOT NULL,
  text BIGINT(20) NOT NULL,
  position INT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  INDEX FK1B15E0F5A48700AE (text ASC),
  INDEX FK1B15E0F59205BF54 (pos ASC),
  INDEX FK1B15E0F52725AD47 (relation_type ASC),
  CONSTRAINT FK1B15E0F52725AD47
    FOREIGN KEY (relation_type)
    REFERENCES relation_type (id),
  CONSTRAINT FK1B15E0F59205BF54
    FOREIGN KEY (pos)
    REFERENCES part_of_speech (id),
  CONSTRAINT FK1B15E0F5A48700AE
    FOREIGN KEY (text)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table sense_attribute
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sense_attribute (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  sense BIGINT(20) NOT NULL,
  type BIGINT(20) NOT NULL,
  value BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FKD16E874BAAFD4CF2 (value ASC),
  INDEX FKD16E874B53AF75C (type ASC),
  INDEX FKD16E874BEC3C9B88 (sense ASC),
  CONSTRAINT FKD16E874BEC3C9B88
    FOREIGN KEY (sense)
    REFERENCES sense (id),
  CONSTRAINT FKD16E874B53AF75C
    FOREIGN KEY (type)
    REFERENCES attribute_type (id),
  CONSTRAINT FKD16E874BAAFD4CF2
    FOREIGN KEY (value)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table sense_relation
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sense_relation (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  sense_from BIGINT(20) NULL DEFAULT NULL,
  sense_to BIGINT(20) NULL DEFAULT NULL,
  relation BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FK6B74B6DEB037BA6 (relation ASC),
  INDEX FK6B74B6D39A84175 (sense_from ASC),
  INDEX FK6B74B6D30EE0086 (sense_to ASC),
  CONSTRAINT FK6B74B6D30EE0086
    FOREIGN KEY (sense_to)
    REFERENCES sense (id),
  CONSTRAINT FK6B74B6D39A84175
    FOREIGN KEY (sense_from)
    REFERENCES sense (id),
  CONSTRAINT FK6B74B6DEB037BA6
    FOREIGN KEY (relation)
    REFERENCES relation_type (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table sense_to_synset
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sense_to_synset (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  id_sense BIGINT(20) NOT NULL,
  id_synset BIGINT(20) NOT NULL,
  sense_index INT(11) NOT NULL,
  PRIMARY KEY (id),
  INDEX FK76D5C38DA3018E2C (id_synset ASC),
  INDEX FK76D5C38DD3A38B64 (id_sense ASC),
  CONSTRAINT FK76D5C38DD3A38B64
    FOREIGN KEY (id_sense)
    REFERENCES sense (id),
  CONSTRAINT FK76D5C38DA3018E2C
    FOREIGN KEY (id_synset)
    REFERENCES synset (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table synset_attribute
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS synset_attribute (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  synset BIGINT(20) NOT NULL,
  type BIGINT(20) NOT NULL,
  value BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FK28245537AAFD4CF2 (value ASC),
  INDEX FK282455379D8A8288 (synset ASC),
  INDEX FK2824553753AF75C (type ASC),
  CONSTRAINT FK2824553753AF75C
    FOREIGN KEY (type)
    REFERENCES attribute_type (id),
  CONSTRAINT FK282455379D8A8288
    FOREIGN KEY (synset)
    REFERENCES synset (id),
  CONSTRAINT FK28245537AAFD4CF2
    FOREIGN KEY (value)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table synset_relation
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS synset_relation (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  relation BIGINT(20) NOT NULL,
  synset_from BIGINT(20) NOT NULL,
  synset_to BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FK645A1001EB037BA6 (relation ASC),
  INDEX FK645A1001B8CA62E (synset_to ASC),
  INDEX FK645A100135A4521D (synset_from ASC),
  CONSTRAINT FK645A100135A4521D
    FOREIGN KEY (synset_from)
    REFERENCES synset (id),
  CONSTRAINT FK645A1001B8CA62E
    FOREIGN KEY (synset_to)
    REFERENCES synset (id),
  CONSTRAINT FK645A1001EB037BA6
    FOREIGN KEY (relation)
    REFERENCES relation_type (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table text_translation
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS text_translation (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  language_code VARCHAR(5) CHARACTER SET utf8 NOT NULL,
  translation VARCHAR(2048) CHARACTER SET utf8 NOT NULL,
  id_text BIGINT(20) NOT NULL,
  PRIMARY KEY (id),
  INDEX FKA353A9F6D4A552 (id_text ASC),
  CONSTRAINT FKA353A9F6D4A552
    FOREIGN KEY (id_text)
    REFERENCES text (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Table wordforms
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS word_form (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  word VARCHAR(255) CHARACTER SET utf8 NULL DEFAULT NULL,
  tag VARCHAR(255) CHARACTER SET utf8 NULL DEFAULT NULL,
  form VARCHAR(255) CHARACTER SET utf8 NULL DEFAULT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- SET FOREIGN_KEY_CHECKS = 1;
