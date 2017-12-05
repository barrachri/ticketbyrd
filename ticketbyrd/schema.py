from marshmallow import Schema, fields
from marshmallow.validate import OneOf

ticket_type = ("Bug", "Report", "Feature", "Request", "Other")
ticket_urgency = ("Low", "Mid", "High")
ticket_status = ("In Progress", "Completed", "Rejected")

class Ticket(Schema):
    name = fields.Str(required=True, )
    email = fields.Email(required=True)
    subject = fields.Str(required=True)
    type = fields.Str(required=True, validate=OneOf(ticket_type))
    message = fields.Str(required=True)
    urgency = fields.Str(required=True, validate=OneOf(ticket_urgency))

class Comment(Schema):
    message = fields.Str(required=True)

