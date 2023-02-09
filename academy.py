from sqlalchemy import create_engine, Column, Integer, Text, Float, Date, String, select, desc, Connection, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, relationship, Mapped
 
class Base(DeclarativeBase):
    pass
 
class Department(Base):
    __tablename__ = 'Departments'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_faculty = Column(Integer, ForeignKey("Faculties.id"))
    Name = Column(Text, unique=True, nullable=False) 
    Financing = Column(Float, default=0, nullable=False) 

    faculty = relationship("Facultie", back_populates="departments")

    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, name={self.Name!r}, financing={self.Financing!r})"
    
class Facultie(Base): 
    __tablename__ = 'Faculties' 
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_group = Column(Integer, ForeignKey("Groups.id")) 
    Name = Column(Text, unique=True, nullable=False) 
    Dean = Column(Text, nullable=False)

    departments = relationship("Department", back_populates="faculty")
    group = relationship("Group", back_populates="facultie")

    def __repr__(self) -> str:
        return f"Facultie(id={self.id!r}, name={self.Name!r}, dean={self.Dean!r})"

class Group(Base): 
    __tablename__ = 'Groups' 
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) 
    Name = Column(Text, unique=True, nullable=False)             
    Year = Column(Integer, nullable=False)   
    Rating = Column(Integer)

    facultie = relationship("Facultie", back_populates="group")
    grop = relationship("Group_Teacher", back_populates="group_teacher")

    def __repr__(self) -> str:
        return f"Group (id={self.id!r}, name={self.Name!r}, rating={self.Rating!r}, rating={self.Year!r})"

class Group_Teacher(Base):
    __tablename__ = "Groups_Teachers"
    id=Column(Integer, primary_key=True, autoincrement=True)

    id_group=Column(Integer, ForeignKey("Groups.id"))
    id_teacher=Column(Integer, ForeignKey("Teachers.id"))

    group_teacher = relationship("Group", back_populates="grop")
    teacher_grop = relationship("Teacher", back_populates="teach")

class Teacher(Base):   
    __tablename__ = 'Teachers'   
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)   
    Name = Column(Text, nullable=False)   
    Surname = Column(Text, nullable=False)   
    Position =Column (Text, nullable=False)   
    Salary=Column (Float, nullable=False)   
    EmploymentDate=Column (String, nullable=False )   
    Premium=Column (Float ,default=0, nullable=False) 
    IsAssistant=Column (Integer ,default = 0, nullable=False) 
    IsProfessor=Column (Integer ,default = 0, nullable=False)

    teach = relationship("Group_Teacher", back_populates="teacher_grop")
    
    def __repr__(self) -> str:
        return f"Teacher (id={self.id!r}, first_name={self.Name!r}, last_name={self.Surname!r}, position={self.Position!r}, employmentDate={self.EmploymentDate!r}, salary={self.Salary!r}, premium={self.Premium!r})"



engine = create_engine('sqlite:///academy.db')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Создаем сессию
with Session(engine) as session:
#добавляем 3 строки в таблицу Teacher     
    teacher1 = Teacher(Name="James", Surname="Smith", Position="Lecturer", Salary=3000.00, EmploymentDate="2020-05-01", Premium=500.00, IsAssistant=0, IsProfessor=0 )    
    teacher2 = Teacher(Name="Michael", Surname="Johnson", Position="Associate Professor", Salary=5000.00, EmploymentDate="2020-06-01", Premium=1000.00 , IsAssistant=0 , IsProfessor=1 )     
    teacher3 = Teacher ( Name="David" , Surname="Anderson" , Position="Assistant" , Salary = 2500.00 , EmploymentDate="2020-07-01" , Premium = 100.00, IsAssistant = 1, IsProfessor=1 )
    session.add_all([teacher1, teacher2, teacher3])  
    session.commit() 

# Добавляем данные в таблицу Group 
    group_1 = Group(Name="Group 1", Year=2020, Rating=4)  
    group_2 = Group(Name="Group 2", Year=2021, Rating=5)  
    group_3 = Group(Name="Group 3", Year=2020, Rating=4)               
    session.add_all([group_1, group_2, group_3])  
    session.commit() 

# Добавляем данные в таблицу Group_Teacher

    group_teacher1 = Group_Teacher(id_group = group_1.id, id_teacher = teacher1.id)
    group_teacher2 = Group_Teacher(id_group = group_1.id, id_teacher = teacher1.id)
    group_teacher3 = Group_Teacher(id_group = group_1.id, id_teacher = teacher1.id)   
    session.add_all([ group_teacher1,  group_teacher2,  group_teacher3])  
    session.commit() 

# Добавляем данные в таблицу Facultie
    faculty_1 = Facultie(Name='Mathematics Faculty', Dean='John Smith')
    faculty_2 = Facultie(Name='Computer Science Faculty', Dean='Michael Johnson')
    faculty_3 = Facultie(Name='Physics Faculty', Dean='David Anderson')
    session.add_all([faculty_1, faculty_2, faculty_3])
    session.commit()

# Добавляем данные в таблицу Department
    department_1 = Department(id_faculty = faculty_1.id,Name='Mathematics', Financing=1000)
    department_2 = Department(id_faculty = faculty_3.id,Name='Computer Science', Financing=2000)
    department_3 = Department(id_faculty = faculty_2.id,Name='Physics', Financing=3000)
    session.add_all([department_1, department_2, department_3])
    session.commit()  # сохраняем изменения в БД
# with Session(engine) as session:
#     session.query(Department).order_by(desc(Department.Name)).all()
#     session.commit()

    # print(s)
    # result = Connection.execute(stmt)
    # s = select([Group.c.group_name, Group.c.rating])
    # s = select([Teacher.c.teacher_last_name, (Teacher.c.allowance/Teacher.c.salary)*100].label("allowance_percentage"), (Teacher.c.rate/Teacher.c salary)*100).label("rate_percentage"))
    # s = select([Teacher]).where(and_(Teacher .c .professor == 1, Teacher .c .rate > 1050))
    # s = select([Department]).where(or_(Department .c .funding < 11000, Department .c .funding > 25000))