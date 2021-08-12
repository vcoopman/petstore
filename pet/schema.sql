DROP TABLE IF EXISTS pet;
DROP TABLE IF EXISTS transaction;

CREATE TABLE `pet` (
  `pet_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_family` varchar(255) NOT NULL,
  `pet_species` varchar(255) NOT NULL,
  `available` int(11) NOT NULL,
  `price` int(11) NOT NULL,

  `age` int(11),
  `size` varchar(20),
  `weight` int(11),
  `color` varchar(20),
  `diet` varchar(50),
  `comment` varchar(255),

  PRIMARY KEY (`pet_id`)
 );

CREATE TABLE `transaction` (
  `transaction_id` varchar(255) NOT NULL,
  `pet_id` int(11) NOT NULL,
  `total_price` int(11) NOT NULL,
  `pet_amount` int(11) NOT NULL,

  PRIMARY KEY (`transaction_id`)
 );


-- DUMMY VALUES --

INSERT INTO pet(pet_id, pet_family, pet_species, available, price, age, size, weight, color, diet, comment) 
VALUES (1, "dog", "kiltrox", 5, 40000, 1, "medium", 10, "grey", "omnivore", "cool specie");

INSERT INTO pet(pet_id, pet_family, pet_species, available, price, age, size, weight, color, diet, comment) 
VALUES (2, "cat", "persian", 2, 60000, 1, "small", 5, "white", "carnivorous", "they have a lot of hair");
