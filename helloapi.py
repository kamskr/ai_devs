from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer

token = authenticate('helloapi')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

answerData = {
    'answer': task['cookie']
}
answer(token, answerData)
