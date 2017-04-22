# django-mongodb-testing
Testing app created for the purpose of writing tests in django framework without the hassle of integration and connection with database. It seamlessly integrates the mongodb related process in the django framework and make testing similiar to that of SQL database.

### Using the app and integrating in the project

In the `settings.py` file in django project - 

`TEST_RUNNER = 'testing.runner.MongodbBaseDiscoverRunner'`

```
MONGO_DATABASE = {
    'default': {
        'NAME': 'database_1',
        'DB_ALIAS': 'database_1',
        'HOST': '0.0.0.0',
        'PORT': '27017',
        'USERNAME': 'user',
        'PASSWORD': 'pass',
        'AUTH': 'admin',
        'TEST': {
            'NAME': 'test_database_1',
            'DB_ALIAS': 'test_database_1'
        }
    }
}
```
In case of testing database name and alias not specified in `MONGO_DATABASE`, it will create test database with `test_` appended in the development database name and alias

### Writing Tests 
`BaseTestCase` is the base class to inherit from to build class based tests. (`BaseTest`, `SimpleTest` in python and django).
Also need to specify 2 class variables - 

* `DOCUMENT_CLASS`
A tuple containing all the document classes which will get affected from the test. Basically will change the database for these documents to test database.  

* `DATA_OBJECT`
A tuple containing the data as a `list` of `dict` objects. These will be stored in database in the begining of the test run.

`DATA_OBJECT` should contain the data elements list corresponding to the class in `DOCUMENT_CLASS`. In case of no initial data for a particular document, provide a empty list `[]`

### Running Tests
Run the tests using the command `./manage.py test` as one would do in django and can also specify app or specific test class which needs to run. This is exact similiar to django flow

### Things to remember
This app is configured in a manner that all the database connections and data updates happens in the begining of all the test. This is when collection of all the specified tests happens in django.

Also, only in the end it disconnects from database and drop it

