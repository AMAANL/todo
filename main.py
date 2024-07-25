from flask import Flask, render_template, request

app = Flask(__name__)


def get_todos():
    with open('todos.txt', 'r') as file:
        todos = file.readlines()
    return todos


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_action = request.form['user_action'].lower().strip()

        if user_action.startswith('add'):
            todo = user_action[4:]
            todos = get_todos()
            todos.append(todo + '\n')
            with open('todos.txt', 'w') as file_w:
                file_w.writelines(todos)

        elif user_action.startswith('show'):
            todos = get_todos()
            todos_list = [f"{index + 1}-{item.strip()}" for index, item in enumerate(todos)]

            return render_template('index.html', todos=todos_list)

        elif user_action.startswith('edit'):
            try:
                number = int(user_action[5:])
                number -= 1
                todos = get_todos()
                new_todo = request.form['new_todo']
                todos[number] = new_todo + '\n'
                with open('todos.txt', 'w') as file_w:
                    file_w.writelines(todos)
            except ValueError:

                return render_template('index.html', todos=get_todos(), error="Invalid input for edit command.")

        elif user_action.startswith('complete'):
            try:
                number = int(user_action[9:])
                todos = get_todos()
                index = number - 1
                todo_to_remove = todos[index].strip('\n')
                todos.pop(index)
                with open('todos.txt', 'w') as file_w:
                    file_w.writelines(todos)

                return render_template('index.html', todos=todos, message=f"Todo {todo_to_remove} removed.")
            except (IndexError, ValueError):

                return render_template('index.html', todos=get_todos(), error="No item with that number.")

        elif user_action.startswith('exit'):

            return render_template('index.html', todos=get_todos(), message="Goodbye!")

        else:
            return render_template('index.html', todos=get_todos(), error="Invalid command.")


    todos = get_todos()
    return render_template('index.html', todos=[item.strip() for item in todos])


if __name__ == '__main__':
    app.run(debug=True)

