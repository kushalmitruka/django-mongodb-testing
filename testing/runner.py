from django.test.runner import DiscoverRunner
from mongoengine import register_connection
from mongoengine.connection import disconnect
from .base import BaseTestCase
from django.conf import settings


class MongodbBaseDiscoverRunner(DiscoverRunner):

    reorder_by = (BaseTestCase,)

    rendered_document_info = {}

    rendered_suite_class_name = []

    @staticmethod
    def register_mongodb_connections():

        for key, database in settings.MONGO_DATABASE.items():

            if 'TEST' in database:

                register_connection(
                    alias=database['TEST']['DB_ALIAS'],
                    name=database['TEST']['NAME'],
                    host=database['HOST'],
                    port=database['PORT'],
                    username=database['USERNAME'],
                    password=database['PASSWORD'],
                    authentication_source=database['AUTH']
                )

            else:

                register_connection(
                    alias='test_' + database['DB_ALIAS'],
                    name='test_' + database['NAME'],
                    host=database['HOST'],
                    port=database['PORT'],
                    username=database['USERNAME'],
                    password=database['PASSWORD'],
                    authentication_source=database['AUTH']
                )

    def render_db_alias_for_suites(self, suites):

        suites_cls = type(suites)
        rendered_suites = suites_cls()

        original_db_alias = dict()
        for key, database in settings.MONGO_DATABASE.items():
            if 'TEST' in database:
                original_db_alias.update({database['DB_ALIAS']: database['TEST']['DB_ALIAS']})
            else:
                original_db_alias.update({database['DB_ALIAS']: 'test_' + database['DB_ALIAS']})

        for suite in suites:

            if suite.__class__.__name__ in self.rendered_suite_class_name:
                continue

            if original_db_alias.keys():
                self.rendered_document_info = suite.change_db_alias_to_test(self.rendered_document_info,
                                                                            db_alias=original_db_alias)
            else:
                raise ValueError('Settings for MONGO_DATABASE are not properly configured')

            self.rendered_suite_class_name = suite.setup_data_in_tables(self.rendered_suite_class_name)

            rendered_suites.addTest(suite)

        return rendered_suites

    def setup_databases(self, suite, **kwargs):
        """
        Steps overwritten to setup the database which would be based on the new settings file that we provide
        returns a list of databases which are setup for the testing
        """

        # Registers the Mongodb database connection to test databases
        self.register_mongodb_connections()

        rendered_suite = self.render_db_alias_for_suites(suites=suite)

        return rendered_suite

    def teardown_databases(self, old_config, **kwargs):
        """
        Steps overwritten to teardown the setup of database
        Args:
            old_config: this contains the info of testing database which were setup
        """
        for suite in old_config:

            suite.drop_data_in_tables()

            self.rendered_document_info = suite.change_db_alias_to_normal(self.rendered_document_info)

        disconnect()

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        Overwritten to handle mongoengine database shift
        """
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases(suite=suite)
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)
