(002,'Niharika','Verma',80000,'2019-06-02','Admin'),
(003,'Vishal','Singhal',300000,'2019-06-03','HR'),
(004,'Amithab','Singh',500000,'2019-06-04','Admin'),
(005,'Vivek','Bhati',500000,'2019-06-05','Admin'),
(006,'Vipul','Diwan',200000,'2019-06-05','Account'),
(007,'Satish','Kumar',75000,'2019-06-14','Account'),
(008,'Deepika','Chauhan',90000,'2019-06-21','Admin')



(1,'2020-06-02',5000),
(2,'2020-06-03',3000),
(3,'2020-06-04',4000),
(1,'2020-06-05',4500),
(2,'2020-06-05',3500)


(1,'Manager','2019-06-08'),
(2,'Executive','2019-06-02'),
(8,'Executive','2019-06-03'),
(5,'Manager','2019-06-08'),
(4,'Asst. Manager','2019-06-02'),
(7,'Executive','2019-06-03') 




(1,1,'2020-06-01',1,10),   
(2,1,'2020-06-08',2,10),
(3,2,'2020-06-02',1,5),
(4,3,'2020-06-03',3,5),
(5,4,'2020-06-04',4,1),
(6,4,'2020-06-05',5,5),
(7,5,'2020-06-05',1,10),
(8,5,'2020-06-14',4,5),
(9,5,'2020-06-21',3,5)



(1,'LC Alg. Book','Book'),  
(2,'LC DB. Book','Book'),  
(3,'LC SmartPhone','Phone'),
(4,'LC Phone 2020','Phone'),
(5,'LC SmartGlass','Glasses'),
(6,'LC T-Shirt XL','T-Shirt' ) 



(1,'Joe',85000,1),
(2,'Henry',80000,2),
(3,'Sam',60000,2),
(4,'Max',90000,1),
(5,'Janet',69000,1),
(6,'Randy',85000,1),
(7,'Will',70000,1)



, SUM(IF(dayname(orders.order_date)='Tuesday', orders.quantity, 0)) AS Tuesday, SUM(IF(dayname(orders.order_date)='Wednesday', orders.quantity, 0)) AS Wednesday, SUM(IF(dayname(orders.order_date)='Thursday', orders.quantity, 0)) AS Thursday, SUM(IF(dayname(orders.order_date)='Friday', orders.quantity, 0)) AS Friday, SUM(IF(dayname(orders.order_date)='Saturday', orders.quantity, 0)) AS Saturday, SUM(IF(dayname(orders.order_date)='Sunday', orders.quantity, 0)) AS Sunday




[
{
	EmpId : 1,
	EmpFname : 'Karan',
	EmpLname : 'mehta',
	Department : 'HR',
	Salary : 300000
},
{
	EmpId : 2,
	EmpFname : 'Rohit',
	EmpLname : 'Sharma',
	Department : 'Admin',
	Salary : 75000
},
{
	EmpId : 3,
	EmpFname :'Ankush',
	EmpLname :'Rajput',
	Department :'Account',
	Salary : 60000
},
{
	EmpId : 4,
	EmpFname :'Priyadershini',
	EmpLname :'Sharma',
	Department : 'HR',
	Salary : 500000
},
{
	EmpId : 5,
	EmpFname :'Sanket',
	EmpLname :'Gupta',
	Department :'Developer',
	Salary : 100000
},
{
	EmpId : 6,
	EmpFname :'Shruthi',
	EmpLname :'Varyar',
	Department :'Admin',
	Salary : 80000
},
{
	EmpId : 2,
	EmpFname : 'Rohit',
	EmpLname :'Sharma',
	Department :'Admin',
	Salary : 75000
}
]









([{title : "Fight Club",
writer : "Chuck Palahniuk",
year : 1999,
actors : [
  "Brad Pitt",
  "Edward Norton"
]},
{title : "Pulp Fiction",
writer : "Quentin Tarantino",
year : 1994,
actors : [
  "John Travolta",
  "Uma Thurman"
]},
{title : "Inglorious Basterds",
writer : "Quentin Tarantino",
year : 2009,
actors : [
  "Brad Pitt",
  "Diane Kruger",
  "Eli Roth"
]},
{title : "The Hobbit: An Unexpected Journey",
writer : "J.R.R. Tolkein",
year : 2012,
franchise : "The Hobbit"},
{title : "The Hobbit: The Desolation of Smaug",
writer : "J.R.R. Tolkein",
year : 2013,
franchise : "The Hobbit"},
{title : "The Hobbit: The Battle of the Five Armies",
writer : "J.R.R. Tolkein",
year : 2012,
franchise : "The Hobbit",
synopsis : "Bilbo and Company are forced to engage in a war against an array of combatants and keep the Lonely Mountain from falling into the hands of a rising darkness."},
{title : "Pee Wee Herman's Big Adventure"},
{title : "Avatar"}])











{username : "GoodGuyGreg",
first_name : "Good Guy",
last_name : "Greg"},
{username : "ScumbagSteve",
full_name :
  first : "Scumbag",
  last : "Steve"}