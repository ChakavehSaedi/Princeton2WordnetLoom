INSERT INTO text(text) VALUES('comment');
INSERT INTO text(text) VALUES('definition');
INSERT INTO text(text) VALUES('isabstract');
INSERT INTO text(text) VALUES('princetonId');
INSERT INTO text(text) VALUES('owner');
INSERT INTO text(text) VALUES('Sumo');

INSERT INTO text(text) VALUES('source');
INSERT INTO text(text) VALUES('project');
INSERT INTO text(text) VALUES('register');
INSERT INTO text(text) VALUES('use_cases');
INSERT INTO text(text) VALUES('link');
INSERT INTO text(text) VALUES('a1_markedness');
INSERT INTO text(text) VALUES('a1_emotions');
INSERT INTO text(text) VALUES('a1_emotions_values');
INSERT INTO text(text) VALUES('a1_emotional_markedness');
INSERT INTO text(text) VALUES('a1_examples');
INSERT INTO text(text) VALUES('a2_markedness');
INSERT INTO text(text) VALUES('a2_emotions');
INSERT INTO text(text) VALUES('a2_emotions_values');
INSERT INTO text(text) VALUES('a2_emotional_markedness');
INSERT INTO text(text) VALUES('a2_examples');
INSERT INTO text(text) VALUES('a3_markedness');
INSERT INTO text(text) VALUES('a3_emotions');
INSERT INTO text(text) VALUES('a3_emotions_values');
INSERT INTO text(text) VALUES('a3_emotional_markedness');
INSERT INTO text(text) VALUES('a3_examples');

INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",(select id from text where text="comment"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="comment"));

INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",(select id from text where text="Sumo"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",(select id from text where text="definition"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",(select id from text where text="princetonId"));

INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",(select id from text where text="isabstract"));

INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",(select id from text where text="owner"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("synset",0);  -- this will return NULL

INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="definition"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="source"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="project"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="register"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="use_cases"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="link"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a1_markedness"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a1_emotions"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a1_emotions_values"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a1_emotional_markedness"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a1_examples"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a2_markedness"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a2_emotions"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a2_emotions_values"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a2_emotions_values"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a2_emotional_markedness"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a2_examples"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a3_markedness"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a3_emotions"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a3_emotions_values"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a3_emotional_markedness"));
INSERT INTO attribute_type(table_name, type_name) VALUES ("sense",(select id from text where text="a3_examples"));
