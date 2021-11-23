class APIobjects:

    usersKeys = ['name', 'email', 'gender', 'status']
    postsKeys = ['user_id', 'title', 'body']
    commentsKeys = ['post_id', 'name', 'email', 'body']
    todosKeys = ['user_id', 'title', 'due_on', 'status']
    objects = {'users': usersKeys, 'posts': postsKeys, 'comments': commentsKeys, 'todos': todosKeys}