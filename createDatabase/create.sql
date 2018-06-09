DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS CourseGrades;

CREATE TABLE Courses (
	Subject TEXT,
	CourseID INTEGER,
	SectionID INTEGER,
	AverageGPA REAL,
	PercentageA REAL, 
	PercentageAB REAL,
	PercentageB REAL,
	PercentageBC REAL,
	PercentageC REAL,
	PercentageD REAL,
	PercentageF REAL,
	PRIMARY KEY(Subject, CourseID)
);

