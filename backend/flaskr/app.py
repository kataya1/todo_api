from logging import debug
from flask import Flask, render_template, request, json, jsonify, abort, redirect, url_for
from flask_cors import CORS
from flask_restful import Resource, Api



def session_error(db, e):
    db.session.rollback()
    print(e) 

def main():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from models import db, Todo
    db.app = app
    db.init_app(app)
    api=Api(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    class TodoRUD(Resource):
        def get(self, todo_id):
            task = Todo.query.filter(Todo.id == todo_id).one_or_none()
            if task:
                return (task, 200)
            else: 
                abort(404)

        def delete(self, todo_id):
            task = Todo.query.filter(Todo.id == todo_id).one_or_none()
            if task:
                try:
                    task.delete()
                    return {'success': True}
                except Exception as e:
                    session_error(db, e)
                    abort(500)
            else:
                abort(404)
                
        def patch(self, todo_id):
            # doesn't work
            task = Todo.query.filter(Todo.id == todo_id).one_or_none()
            if task:
                try:
                    print(request.get_json())
                    for key,value in request.get_json().items():
                        task[key] = value

                    task.update()
                    # return jsonify(repr(task))
                    return {'success': 'success'}
                except Exception as e:
                    session_error(db, e)
                    abort(500)
            else:
                abort(404)
            
        def put(self):
            pass

    
    class TodoLC(Resource):
        def post(self):
            try:
                descripiton = request.get_json().get('description')
                todo = Todo(description=descripiton)
                todo.insert()
                # return str(todo)
                return {'happynow': 'fu'}
            except Exception as e:
                session_error(db,e)
                abort(400)

            
        def get(self):
            todolist = Todo.query.order_by(Todo.id).all()
            my_new_list = []
            limit = request.args.get('limit')

            for task in todolist:
                data = {
                    'id': task.id,
                    'name': task.description,
                    'finished': task.completed,
                    'created at': task.created_at
                }

                my_new_list.append(data)

            if limit:
                print(type(limit))
                my_new_list = my_new_list[:int(limit)]

            return jsonify(my_new_list)


   

    api.add_resource(TodoRUD, '/todos/<int:todo_id>')
    api.add_resource(TodoLC, '/todos/')
    


    @app.route('/hello', methods=['GET'])
    def welcome_back():
        return "welcomeback friend"



    @app.route('/')
    def index():
        return 'works'

    @app.before_first_request
    def create_table ():
        db.create_all()

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    
    return app


if __name__ == "__main__":
    main().run(debug=True)

            # print(f"request.get_json() -> {request.get_json()}")
            # print(f"request.form -> {request.form}")
            # print(f"request.args -> {request.args}")
