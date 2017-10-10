DELIMITER $$
-- SET FOREIGN_KEY_CHECKS = 0$$

-- trackers schema

-- ----------------------------------------------------------------------------
-- Table tracker
-- ----------------------------------------------------------------------------
CREATE TABLE `tracker` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `inserted` tinyint(1) NOT NULL DEFAULT '0',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `data_before_change` bigint(20) DEFAULT NULL COMMENT 'identyfikator wiersza z wartosciami pól przed zmiana',
  `table` varchar(64) NOT NULL,
  `tid` bigint(20) DEFAULT NULL,
  `user` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tid` (`tid`),
  KEY `table` (`table`),
  KEY `data_before_change` (`data_before_change`),
  KEY `table_2` (`table`),
  KEY `data_before_change_2` (`data_before_change`)
) DEFAULT CHARSET=utf8$$

-- ----------------------------------------------------------------------------
-- Table tracker_lexicalrelation
-- ----------------------------------------------------------------------------
CREATE TABLE `tracker_lexicalrelation` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `PARENT_ID` bigint(20) NOT NULL,
  `CHILD_ID` bigint(20) NOT NULL,
  `REL_ID` bigint(20) NOT NULL,
  `valid` int(11) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) DEFAULT CHARSET=utf8$$

-- ----------------------------------------------------------------------------
-- Table tracker_lexicalunit
-- ----------------------------------------------------------------------------
CREATE TABLE `tracker_lexicalunit` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `ID` bigint(20) NOT NULL,
  `lemma` varchar(255) CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `domain` int(11) DEFAULT NULL,
  `pos` int(11) DEFAULT NULL,
  `tagcount` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `comment` varchar(2048) DEFAULT NULL,
  `variant` int(11) DEFAULT NULL,
  `owner` varchar(255) NOT NULL,
  `project` int(11) NOT NULL,
  PRIMARY KEY (`tid`),
  KEY `ID` (`ID`),
  KEY `ID_2` (`ID`)
) DEFAULT CHARSET=utf8$$

-- ----------------------------------------------------------------------------
-- Table tracker_synset
-- ----------------------------------------------------------------------------
CREATE TABLE `tracker_synset` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `ID` bigint(20) NOT NULL,
  `split` int(11) DEFAULT NULL,
  `definition` varchar(255) DEFAULT NULL,
  `isabstract` int(1) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `comment` varchar(2048) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  `unitsstr` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) CHARSET=utf8$$

-- ----------------------------------------------------------------------------
-- Table tracker_synsetrelation
-- ----------------------------------------------------------------------------
CREATE TABLE `tracker_synsetrelation` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `PARENT_ID` bigint(20) NOT NULL,
  `CHILD_ID` bigint(20) NOT NULL,
  `REL_ID` bigint(20) NOT NULL,
  `valid` int(11) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) DEFAULT CHARSET=utf8$$

-- ----------------------------------------------------------------------------
-- Table tracker_unitandsynset
-- ----------------------------------------------------------------------------
CREATE TABLE `tracker_unitandsynset` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `LEX_ID` bigint(20) NOT NULL,
  `SYN_ID` bigint(20) NOT NULL,
  PRIMARY KEY (`tid`)
) DEFAULT CHARSET=utf8$$

-- trackers data migration

INSERT INTO tracker SELECT * from db_name.tracker$$
INSERT INTO tracker_lexicalrelation SELECT * from db_name.tracker_lexicalrelation$$
INSERT INTO tracker_lexicalunit SELECT * from db_name.tracker_lexicalunit$$
INSERT INTO tracker_synset SELECT * from db_name.tracker_synset$$
INSERT INTO tracker_synsetrelation SELECT * from db_name.tracker_synsetrelation$$
INSERT INTO tracker_unitandsynset SELECT * from db_name.tracker_unitandsynset$$

-- triggers for trackers

CREATE TRIGGER `tracker_unitrelation_delete` AFTER DELETE ON `sense_relation` FOR EACH ROW BEGIN
    INSERT INTO tracker_lexicalrelation 
      SET 
        `PARENT_ID` = OLD.sense_from,
        `CHILD_ID` = OLD.sense_to,
        `REL_ID` = OLD.relation,
        `valid` = null,
        `owner` = null;
    INSERT INTO tracker
      SET
      `deleted` = 1,
        `datetime` = NOW(),
        `table` = 'lexicalrelation',
        `user` = @owner,
        `tid` = LAST_INSERT_ID();
END$$

CREATE TRIGGER `tracker_unitrelation_insert` AFTER INSERT ON `sense_relation` FOR EACH ROW BEGIN
    INSERT INTO tracker_lexicalrelation 
      SET 
        `PARENT_ID` = NEW.sense_from,
        `CHILD_ID` = NEW.sense_to,
        `REL_ID` = NEW.relation,
        `valid` = null,
        `owner` = null;
    INSERT INTO tracker
      SET
      `inserted` = 1,
        `datetime` = NOW(),
        `table` = 'lexicalrelation',
        `user` = @owner,
        `tid` = LAST_INSERT_ID();
END$$

CREATE TRIGGER `tracker_unitrelation_update` AFTER UPDATE ON `sense_relation` FOR EACH ROW BEGIN
	    INSERT INTO tracker_lexicalrelation SET `PARENT_ID` = NEW.sense_from, `CHILD_ID` = NEW.sense_to, `REL_ID` = NEW.relation;
	    SET @before_id := LAST_INSERT_ID();
	    INSERT INTO tracker_lexicalrelation SET `PARENT_ID` = NEW.sense_from, `CHILD_ID` = NEW.sense_to, `REL_ID` = NEW.relation;
	    SET @after_id := LAST_INSERT_ID();
	    
	    INSERT INTO tracker SET `datetime` = NOW(), `table` = 'lexicalrelation', `tid` = @before_id, `user` = @owner;
	    INSERT INTO tracker SET `datetime` = NOW(), `table` = 'lexicalrelation', `tid` = @after_id, `data_before_change` = LAST_INSERT_ID(), `user` = @owner;
END$$

CREATE TRIGGER `tracker_unitandsynset_delete` AFTER DELETE ON `sense_to_synset` FOR EACH ROW BEGIN
    INSERT INTO tracker_unitandsynset SET `LEX_ID` = OLD.id_sense, `SYN_ID` = OLD.id_synset;
    INSERT INTO tracker SET `deleted` = 1, `datetime` = NOW(), `table` = 'unitandsynset', `tid` = LAST_INSERT_ID(), `user` = @owner;
END$$

CREATE TRIGGER `tracker_unitandsynset_insert` AFTER INSERT ON `sense_to_synset` FOR EACH ROW BEGIN
    INSERT INTO tracker_unitandsynset SET `LEX_ID` = NEW.id_sense, `SYN_ID` = NEW.id_synset;
    INSERT INTO tracker SET `inserted` = 1, `datetime` = NOW(), `table` = 'unitandsynset', `tid` = LAST_INSERT_ID(), `user` = @owner;
END$$

CREATE TRIGGER `tracker_synsetrelation_delete` AFTER DELETE ON `synset_relation` FOR EACH ROW BEGIN
    INSERT INTO tracker_synsetrelation 
      SET 
        `PARENT_ID` = OLD.synset_from,
        `CHILD_ID` = OLD.synset_to,
        `REL_ID` = OLD.relation,
        `valid` = null,
        `owner` = null;
    INSERT INTO tracker
      SET
      `deleted` = 1,
        `datetime` = NOW(),
        `table` = 'synsetrelation',
        `user` = @owner,
        `tid` = LAST_INSERT_ID();
END$$

CREATE TRIGGER `tracker_synsetrelation_insert` AFTER INSERT ON `synset_relation` FOR EACH ROW BEGIN
    INSERT INTO tracker_synsetrelation 
      SET 
        `PARENT_ID` = NEW.synset_from,
        `CHILD_ID` = NEW.synset_to,
        `REL_ID` = NEW.relation,
        `valid` = null,
        `owner` = null;
    INSERT INTO tracker
      SET
      `inserted` = 1,
        `datetime` = NOW(),
        `table` = 'synsetrelation',
        `user` = @owner,
        `tid` = LAST_INSERT_ID();
END$$

CREATE TRIGGER `tracker_synsetrelation_update` AFTER UPDATE ON `synset_relation` FOR EACH ROW BEGIN
	    INSERT INTO tracker_synsetrelation SET `PARENT_ID` = NEW.synset_from, `CHILD_ID` = NEW.synset_to, `REL_ID` = NEW.relation;
	    SET @before_id := LAST_INSERT_ID();
	    INSERT INTO tracker_synsetrelation SET `PARENT_ID` = NEW.synset_from, `CHILD_ID` = NEW.synset_to, `REL_ID` = NEW.relation;
	    SET @after_id := LAST_INSERT_ID();
	    
	    INSERT INTO tracker SET `datetime` = NOW(), `table` = 'synsetrelation', `tid` = @before_id, `user` = @owner;
	    INSERT INTO tracker SET `datetime` = NOW(), `table` = 'synsetrelation', `tid` = @after_id, `data_before_change` = LAST_INSERT_ID(), `user` = @owner;
END$$

-- SET FOREIGN_KEY_CHECKS = 1$$
