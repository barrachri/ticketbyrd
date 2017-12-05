from flask import Flask, jsonify, request, abort

from ticketbyrd import schema

app = Flask(__name__)

tickets = []
comments = []

@app.route('/tickets', methods=['POST'])
def create_ticket():
    if not request.json:
        abort(400)

    ticket, err = schema.Ticket().load(request.json)

    if err:
        return jsonify({'message': err}), 400
    tickets.append(ticket)
    print(tickets)
    return jsonify({'task': "created"}), 200

@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_tickets(ticket_id):
    #ticket, err = schema.Ticket().load(request.json)

    return jsonify({'task': tickets[ticket_id]}), 200

@app.route('/comments/<int:ticket_id>', methods=['GET'])
def add_comment(ticket_id):
    #ticket, err = schema.Ticket().load(request.json)

    return jsonify({'task': tickets[ticket_id]}), 200

@app.route('/comments/<int:ticket_id>', methods=['POST'])
def get_comments(ticket_id):
    #ticket, err = schema.Ticket().load(request.json)
    if not request.json:
        abort(400)

    comment, err = schema.Comment().load(request.json)
    if err:
        print(err)
        return jsonify({'message': err}), 400
    comments.append(comment)
    return jsonify({'task': "created"}), 200

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080)
