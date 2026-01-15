from sqlmodel import SQLModel, Field

class Commune(SQLModel, table=True):
    """Table représentant les communes associées à un département."""
    
    __tablename__ = "t_communes"
    
    id: int | None = Field(default=None, primary_key=True)
    dep: str = Field(foreign_key="t_dept.code_dept", max_length=2, nullable=False)
    cp: str | None = Field(default=None, max_length=5, nullable=True)
    ville: str | None = Field(default=None, max_length=50, nullable=True)
