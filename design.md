#feature

- user reg
- user login
- user logout
- create task
- view task
- update task
- delete task
- mark done
- filter tasks
- task summary

#user table

- id(auto incremented primary key)
- email
- password

#task table
- id
- title
- desc
- priority
- status
- due date
- owner_email

#user API end points                                        auth

- POST(register)                                            No
- POST(Login)                                               No
- GET(get email and id)                                     Yes 

#task API end points
- POST(create task)                                         Yes
- GET(get all tasks)                                        Yes
- GET(get task by task_id)                                  Yes
- PUT(UPDATE ALL ASPECTS OF A TASK by task_id)              Yes
- PATCH(update a specific attribute of a specific task)     Yes
- DELETE(remove a task by task_id)                          Yes
- GET(get summary of all tasks)                             Yes

#streamlit structure

- Login page
- Dashboard
- Add Task Page
- View Task Page

#security
- users see only their tasks
- passwords are hashed
- All tasks endpint require tokens

#Project structure

task_manager
|--backend
|  |--main.py
|  |--db.py
|  |--auth.py
|  |--schemas.py
|  |--router
|  |  |--auth_router.py
|  |  |--task_router.py
|--frontend
|  |--app.py
|--.env
|--.gitignore
|--design.md
|--README.md
|--requirements.txt