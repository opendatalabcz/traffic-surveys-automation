from sqlalchemy import ARRAY, Column, Enum, ForeignKey, Integer, JSON, MetaData, Table, TEXT

from tsa import enums

metadata = MetaData()


LineModel = Table(
    "lines",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="Auto-incremented primary key of a single lines definition.",
    ),
    Column(
        "task_id", ForeignKey("tasks.id"), nullable=False, index=True, doc="Reference the task the lines belong to."
    ),
    Column("lines", JSON, nullable=False, server_default="{}", doc="JSON data describing the lines."),
)


SourceFileModel = Table(
    "source_files",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, doc="Auto-incremented primary key of a source file."),
    Column("name", TEXT, nullable=False, doc="Name of the source file assigned by a user."),
    Column("path", TEXT, unique=True, nullable=False, doc="Relative path to the source file. It has to be unique."),
    Column(
        "status",
        Enum(enums.SourceFileStatus, name="source_file_status"),
        server_default="new",
        nullable=False,
        doc="Status of the source file.",
    ),
)

TaskModel = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, doc="Auto-incremented primary key of a task."),
    Column("name", TEXT, nullable=False, doc="Name of the task."),
    Column(
        "models",
        ARRAY(TEXT),
        nullable=False,
        default="{}",
        doc="List of models to use when processing the task. Usually, it's one detector and one tracker.",
    ),
    Column("output_path", TEXT, unique=True, nullable=False, doc="Output file generated as a result of a task."),
    Column(
        "parameters",
        JSON,
        server_default="{}",
        nullable=False,
        doc="Parameters of the models. These override the default parameters of the app.",
    ),
    Column(
        "status",
        Enum(enums.TaskStatus, name="task_status"),
        server_default="created",
        nullable=False,
        doc="Status of the a task.",
    ),
    Column("source_file_id", ForeignKey("source_files.id"), nullable=False, index=True),
)
