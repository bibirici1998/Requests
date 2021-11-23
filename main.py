import requests
import objects
class APIrequests:
    responses = [] #contains operation statuses
    operations = [] #contains id of object and type of object of all succeeded operations
    def __init__(self, URL, token):
        self._URL = URL
        self._token = token

    def getObject(self, obj):
        if obj == 'all':
            api_url = self._URL
            for e in objects.APIobjects.objects.keys():
                response = requests.get(api_url + e)
                print(response.json())
                print(f'GET status: {response.status_code}')
                APIrequests.responses.append(response.status_code)
                APIrequests.checkResponse(self, response.status_code)
        else:
            api_url = f'{self._URL}{obj}'
            response = requests.get(api_url)
            print(response.json())
            print(f'GET status: {response.status_code}')
            APIrequests.checkResponse(self, response.status_code)
            APIrequests.responses.append(response.status_code)

    def deleteObject(self, obj, id):
        api_url = f"{self._URL}{obj}/{id}?access-token={self._token}"
        response = requests.delete(api_url)
        print(f'DELETE status: {response.status_code}')
        APIrequests.responses.append(response.status_code)
        APIrequests.checkResponse(self, response.status_code)

    def postObject(self, obj, values):
        k = objects.APIobjects.objects[obj]
        d = dict.fromkeys(k)
        for i in range(len(k)):
            d[k[i]] = values[i]
        api_url = f"{self._URL}{obj}?access-token={self._token}"
        response = requests.post(api_url, json=d)
        print(response.json())
        print(f'POST status: {response.status_code}')
        APIrequests.responses.append(response.status_code)
        if APIrequests.checkResponse(self, response.status_code):
            APIrequests.operations.append({'object': obj, 'id': response.json()['data']['id']})

    def checkResponse(self, response):
        if response >= 200 and response < 300:
            print('Status OK\n')
            return True
        else:
            print('Status Failed\n')
            return False

    def cleanup(self, objects): #objects is a list containing length 2 lists: [type of object, id]
        nr = 0
        print("Cleanup started")
        print(f'{len(objects)} items to be deleted')
        print(APIrequests.operations)
        for obj in objects:
            api_url = f"{self._URL}{obj['object']}/{obj['id']}?access-token={self._token}"
            response = requests.delete(api_url)
            print(f'Deleting item {objects.index(obj)+1}')
            if APIrequests.checkResponse(self, response.status_code):
                nr += 1
        if nr == len(objects): #if all items have been deleted
            print("Cleanup successful")
            print(f'{nr}/{len(objects)} items deleted')
        else:
            print("Cleanup failed")
            print(f'{nr}/{len(objects)} items deleted')


a1 = APIrequests("https://gorest.co.in/public/v1/", '3d987e4a7c44200d76deca198fbef4b2b269c3b052afb6489591a6af7ecc6bb1')

values_users = ['abcde', 'abcde@yahoo.com', 'male', 'active']
values_posts = [14, 'asd1', 'asd1']
values_comments = [14, 'asd123', 'asd123@yahoo.com', 'body']
values_todos = [14, 'title', '2021-12-15T00:00:00.000+05:30', 'pending']
a1.getObject("users")
a1.getObject("posts")
a1.getObject("comments")
a1.getObject("todos")
a1.deleteObject('users', 2)
a1.deleteObject('posts', 2)
a1.deleteObject('comments', 2)
a1.deleteObject('todos', 2)
a1.postObject('users', values_users)
a1.postObject('posts', values_posts)
a1.postObject('comments', values_comments)
a1.postObject('todos', values_todos)
print(APIrequests.responses)
print(APIrequests.operations)
a1.cleanup(APIrequests.operations)

