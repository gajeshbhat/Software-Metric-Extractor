from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProjectMetric(Base):
    __tablename__ = 'ProjectMetric'

    # Relationships
    files = relationship("FileCodeMetric",back_populates='project')

    # Tables
    id = Column(Integer, primary_key=True)

    project_name = Column(String)
    comment_ratio = Column(Float)
    cyclomatic_complexity = Column(Integer)

    fanout_external = Column(Integer)
    fanout_internal = Column(Integer)

    halstead_bugprop = Column(Float)
    halstead_difficulty = Column(Float)
    halstead_effort = Column(Float)
    halstead_timerequired = Column(Float)
    halstead_volume = Column(Float)

    programming_lang = Column(String)

    lines_of_code = Column(Integer)
    maintainability_index = Column(Float)

    operands_sum = Column(Integer)
    operands_uniq = Column(Integer)
    operators_sum = Column(Integer)
    operators_uniq = Column(Integer)

    tiobe = Column(Float)
    tiobe_compiler = Column(Float)
    tiobe_complexity = Column(Float)
    tiobe_coverage = Column(Float)
    tiobe_duplication = Column(Float)
    tiobe_fanout = Column(Float)
    tiobe_functional = Column(Float)
    tiobe_security = Column(Float)
    tiobe_standard = Column(Float)


class FileCodeMetric(Base):
    __tablename__ = 'FileCodeMetric'

    # Relationships
    project = relationship("ProjectMetric", back_populates='files')

    # Table Columns
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('ProjectMetric.id'))

    comment_ratio = Column(Float)

    cyclomatic_complexity = Column(Integer)
    fanout_external = Column(Integer)
    fanout_internal = Column(Integer)

    halstead_bugprop = Column(Float)
    halstead_difficulty = Column(Float)
    halstead_effort = Column(Float)
    halstead_timerequired = Column(Float)
    halstead_volume = Column(Float)

    programming_lang = Column(String)

    lines_of_code = Column(Integer)
    maintainability_index = Column(Float)

    operands_sum = Column(Integer)
    operands_uniq = Column(Integer)
    operators_sum = Column(Integer)
    operators_uniq = Column(Integer)

    tiobe = Column(Float)
    tiobe_compiler = Column(Float)
    tiobe_complexity = Column(Float)
    tiobe_coverage = Column(Float)
    tiobe_duplication = Column(Float)
    tiobe_fanout = Column(Float)
    tiobe_functional = Column(Float)
    tiobe_security = Column(Float)
    tiobe_standard = Column(Float)


# Create overall db object
def get_overall_obj(metric_obj, project_name):
    overall_metric = ProjectMetric \
            (
            project_name=str(project_name),
            comment_ratio=float(metric_obj['comment_ratio']),
            cyclomatic_complexity=int(metric_obj['cyclomatic_complexity']),
            fanout_external=int(metric_obj['fanout_external']),
            fanout_internal=int(metric_obj['fanout_internal']),
            halstead_bugprop=float(metric_obj['halstead_bugprop']),
            halstead_difficulty=float(metric_obj['halstead_difficulty']),
            halstead_effort=float(metric_obj['halstead_effort']),
            halstead_timerequired=float(metric_obj['halstead_timerequired']),
            halstead_volume=float(metric_obj['halstead_volume']),
            programming_lang=str(metric_obj['lang']),
            lines_of_code=int(metric_obj['loc']),
            maintainability_index=float(metric_obj['maintainability_index']),
            operands_sum=int(metric_obj['operands_sum']),
            operands_uniq=int(metric_obj['operands_uniq']),
            operators_sum=int(metric_obj['operators_sum']),
            operators_uniq=int(metric_obj['operators_uniq']),
            tiobe=float(metric_obj['tiobe']),
            tiobe_compiler=float(metric_obj['tiobe_compiler']),
            tiobe_complexity=float(metric_obj['tiobe_complexity']),
            tiobe_coverage=float(metric_obj['tiobe_coverage']),
            tiobe_duplication=float(metric_obj['tiobe_duplication']),
            tiobe_fanout=float(metric_obj['tiobe_fanout']),
            tiobe_functional=float(metric_obj['tiobe_functional']),
            tiobe_security=float(metric_obj['tiobe_security']),
            tiobe_standard=float(metric_obj['tiobe_standard'])
        )
    return overall_metric


def get_each_file_obj(metric_obj,project_inst):
    file_metric_obj = FileCodeMetric(
        comment_ratio=float(metric_obj['comment_ratio']),
        cyclomatic_complexity=int(metric_obj['cyclomatic_complexity']),
        fanout_external=int(metric_obj['fanout_external']),
        fanout_internal=int(metric_obj['fanout_internal']),
        halstead_bugprop=float(metric_obj['halstead_bugprop']),
        halstead_difficulty=float(metric_obj['halstead_difficulty']),
        halstead_effort=float(metric_obj['halstead_effort']),
        halstead_timerequired=float(metric_obj['halstead_timerequired']),
        halstead_volume=float(metric_obj['halstead_volume']),
        programming_lang=str(metric_obj['lang']),
        lines_of_code=int(metric_obj['loc']),
        maintainability_index=float(metric_obj['maintainability_index']),
        operands_sum=int(metric_obj['operands_sum']),
        operands_uniq=int(metric_obj['operands_uniq']),
        operators_sum=int(metric_obj['operators_sum']),
        operators_uniq=int(metric_obj['operators_uniq']),
        tiobe=float(metric_obj['tiobe']),
        tiobe_compiler=float(metric_obj['tiobe_compiler']),
        tiobe_complexity=float(metric_obj['tiobe_complexity']),
        tiobe_coverage=float(metric_obj['tiobe_coverage']),
        tiobe_duplication=float(metric_obj['tiobe_duplication']),
        tiobe_fanout=float(metric_obj['tiobe_fanout']),
        tiobe_functional=float(metric_obj['tiobe_functional']),
        tiobe_security=float(metric_obj['tiobe_security']),
        tiobe_standard=float(metric_obj['tiobe_standard']),
        project=project_inst
    )
    return file_metric_obj


def get_session():
    engine = create_engine(f"sqlite:///test.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    metric_db_session = sessionmaker(bind=engine)
    metric_db_session = metric_db_session()  # sessionmaker returns a class for some fu**ing reason so instansiate again. Raise a pull request
    return metric_db_session
