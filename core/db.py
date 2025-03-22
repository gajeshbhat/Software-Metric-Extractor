import os
from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, create_engine
from sqlalchemy.dialects.mysql import LONGTEXT  # 🔥 Use LONGTEXT for descriptions
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Load environment variables from .env file
load_dotenv()

# Database connection string from .env
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://metrics_user:metrics_password@localhost/software_metrics")

Base = declarative_base()

# Repository Table
class Repository(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    github_id = Column(Integer, unique=True, nullable=False)  # GitHub Repo ID
    name = Column(String(255), nullable=False)
    full_name = Column(String(255), unique=True, nullable=False)
    clone_url = Column(String(512), nullable=False)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    language = Column(String(100))
    description = Column(LONGTEXT)  # 🔥 FIX: LONGTEXT for large descriptions
    is_fork = Column(Boolean, default=False)
    created_at = Column(String(50))
    updated_at = Column(String(50))

    project = relationship("Project", uselist=False, back_populates="repository")


# Project Table (Linked to Repositories)
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), unique=True)
    path = Column(String(512), nullable=False)
    total_files = Column(Integer, nullable=False)
    total_lines_of_code = Column(Integer, nullable=False)
    avg_cyclomatic_complexity = Column(Float)
    created_at = Column(String(50))

    repository = relationship("Repository", back_populates="project")
    directories = relationship("Directory", back_populates="project")


# Directory Table
class Directory(Base):
    __tablename__ = 'directories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    path = Column(String(512), nullable=False)

    project = relationship("Project", back_populates="directories")
    files = relationship("File", back_populates="directory")


# File Table
class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    directory_id = Column(Integer, ForeignKey('directories.id'))
    name = Column(String(255), nullable=False)
    path = Column(String(512), nullable=False)
    lines_of_code = Column(Integer)
    cyclomatic_complexity = Column(Float)

    directory = relationship("Directory", back_populates="files")
    metrics = relationship("Metric", back_populates="file")


# Metric Table
class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    metric_name = Column(String(255), nullable=False)
    metric_value = Column(Float, nullable=False)

    file = relationship("File", back_populates="metrics")


# Database Session Setup
def get_session():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)  # Creates tables if they don’t exist
    Session = sessionmaker(bind=engine)
    return Session()
