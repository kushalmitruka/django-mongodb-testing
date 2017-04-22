# django-mongodb-testing
Testing app created for the purpose of writing tests in django framework without the hassle of integration and connection with database. It seamlessly integrates the mongodb related process in the django framework and make testing similiar to that of SQL database.

### Using the app and integrating in the project

In the `settings.py` file in django project - 
* `TEST_RUNNER = 'testing.base_test.MongodbBaseDiscoverRunner'`

* `Database Settings`

### Writing Tests 
`BaseTestCase` is the base class to inherit from to build class based tests. (`BaseTest`, `SimpleTest` in python and django).
Also need to specify 2 class variables - 

* `DOCUMENT_CLASS`

* `DATA_OBJECT`

### Running Tests
Run the tests using the command `./manage.py test` as one would do in django and can also specify app or specific test class which needs to run. This is exact similiar to django flow


