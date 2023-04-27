from marshmallow import Schema, fields
from models import ChangeStatus, PersonRole


class PlainBankAccountSchema(Schema):
    id = fields.Int(dump_only=True)
    balance = fields.Float(required=True)


class PlainPersonSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    gender = fields.Str(required=True)
    password = fields.Str(load_only=True)


class PersonSchema(PlainPersonSchema):
    role = fields.Enum(PersonRole, required=True)


class BankAccountSchema(PlainBankAccountSchema):
    customers = fields.List(fields.Nested(PlainPersonSchema), dump_only=True)


class CustomerSchema(PlainPersonSchema):
    bank_accounts = fields.List(fields.Nested(PlainBankAccountSchema), dump_only=True)


class BankAccountAndCustomerSchema(Schema):
    message = fields.Str()
    bank_account = fields.Nested(BankAccountSchema)
    customer = fields.Nested(CustomerSchema)


class AmountSchema(Schema):
    amount = fields.Float(required=True)


class PlainPersonChangeSchema(Schema):
    email = fields.Email()
    name = fields.Str()
    age = fields.Int()
    gender = fields.Str()


class PlainChangeSchema(Schema):
    old = fields.Nested(PlainPersonChangeSchema)
    new = fields.Nested(PlainPersonChangeSchema)


class CommentSchema(Schema):
    comment = fields.Str(required=True)


class ChangeSchema(CommentSchema):
    id = fields.Int(dump_only=True)
    status = fields.Enum(ChangeStatus, dump_only=True)
    customer_id = fields.Int(dump_only=True)
    change = fields.Nested(PlainChangeSchema)


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    bank_account_id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    balance = fields.Float(required=True)


class LoginSchema(Schema):
    role = fields.Enum(PersonRole, required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
