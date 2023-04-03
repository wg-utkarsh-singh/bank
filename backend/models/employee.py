from db import db
from models.person import PersonModel, PersonRole


class EmployeeModel(PersonModel):
    __tablename__ = "employees"
    role = db.Column(db.Enum(PersonRole, create_constraint=True), nullable=False)
