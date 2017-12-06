from flask import jsonify, request, abort
from flask import Blueprint, render_template, abort
from factory import db
from models import Ticket, Comment
from ticketbyrd import schema
from ticketbyrd.utils import token_required, generate_jwt

tickets_blueprint = Blueprint('tickets', __name__)

@tickets_blueprint.route('/api/login', methods=['POST'])
def login():
    """Return a jwt if the user is valid."""
    if not request.json:
        abort(400)

    data, err = schema.User().load(request.json)
    if err:
        return jsonify({'message': err}), 400

    token = generate_jwt(user_id=1)

    message = {'user': {"token": token}}
    return jsonify(message), 200


@tickets_blueprint.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create a new ticket, return its id. 400 Otherwise"""
    if not request.json:
        abort(400)

    data, err = schema.Ticket().load(request.json)
    if err:
        return jsonify({'message': err}), 400

    ticket = Ticket(**data)
    db.session.add(ticket)
    db.session.commit()

    message = {'ticket': {"id": ticket.id}}
    return jsonify(message), 200



@tickets_blueprint.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
@token_required
def update_ticket(ticket_id):
    """Create a new ticket, return its id. 400 Otherwise"""
    if not request.json:
        abort(400)

    query = Ticket.query.filter_by(id=ticket_id)
    ticket = query.first_or_404()

    data, err = schema.Ticket(partial=True).load(request.json)
    if err:
        print(err)
        return jsonify({'message': err}), 400

    query.update(data)
    db.session.commit()

    message = {'ticket': {"id": ticket.id}}
    return jsonify(message), 200

@tickets_blueprint.route('/api/tickets', methods=['GET'])
@token_required
def get_tickets():
    """Get a ticket if exists. 404 Otherwise."""
    tickets = Ticket.query.all()

    result = schema.Ticket(many=True).dump(tickets)
    return jsonify({'tickets': result.data}), 200

@tickets_blueprint.route('/api/tickets/<int:ticket_id>', methods=['GET'])
@token_required
def get_ticket(ticket_id):
    """Get a ticket if exists. 404 Otherwise."""
    ticket = Ticket.query.filter_by(id=ticket_id).first_or_404()

    result = schema.Ticket().dump(ticket)
    return jsonify({'ticket': result.data}), 200

@tickets_blueprint.route('/api/tickets/<int:ticket_id>/comments', methods=['POST'])
@token_required
def add_comment(ticket_id):
    if not request.json:
        abort(400)

    ticket = Ticket.query.filter_by(id=ticket_id).first_or_404()

    comment, err = schema.Comment().load(request.json)
    if err:
        return jsonify({'message': err}), 400
    comment = Comment(**comment)

    ticket.comments.append(comment)
    db.session.add(ticket)
    db.session.commit()
    message = {'comment': {"id": comment.id}}
    return jsonify(message), 200

@tickets_blueprint.route('/api/tickets/<int:ticket_id>/comments', methods=['GET'])
@token_required
def get_comments(ticket_id):
    """Get ticket's comments.

    If the ticket does not exist raise 404.
    """
    ticket = Ticket.query.filter_by(id=ticket_id).first_or_404()

    comments = schema.Comment(many=True).dump(ticket.comments)

    return jsonify({'comments': comments.data}), 200
