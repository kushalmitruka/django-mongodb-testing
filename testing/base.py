from django.test import TestCase


class BaseTestCase(TestCase):

    DOCUMENT_CLASS = ()

    DATA_OBJECT = ()

    def setup_data_in_tables(self, rendered_suite_class_name):
        """
        This will insert the test data required for this Base class and correspondingly
        whichever tests it runs
        """

        for index, data_obj in enumerate(self.DATA_OBJECT):
            current_document = self.DOCUMENT_CLASS[index]

            for data in data_obj:
                document = current_document(**data)
                document.save()

        rendered_suite_class_name.append(self.__class__.__name__)

        return rendered_suite_class_name

    def drop_data_in_tables(self):

        for document in self.DOCUMENT_CLASS:
            document.drop_collection()

    def change_db_alias_to_test(self, rendered_document_info, db_alias):

        for document in self.DOCUMENT_CLASS:
            document_name = document.__name__
            if document_name not in rendered_document_info:
                collection = document._get_collection()
                original_db_alias = document._meta['db_alias']

                if original_db_alias in db_alias:
                    document._meta['db_alias'] = db_alias[original_db_alias]
                    document._collection = None
                else:
                    raise AttributeError("Specify the db_alias properly in MONGO_DATABASE under `original_db_alias`")

                rendered_document_info.update({document_name: {
                    'collection': collection, 'original_db_alias': original_db_alias}
                })

        return rendered_document_info

    def change_db_alias_to_normal(self, rendered_document_info):

        if len(rendered_document_info.keys()) == 0:
            return True

        for document in self.DOCUMENT_CLASS:
            document_name = document.__name__
            if document_name in rendered_document_info:
                document_details = rendered_document_info.pop(document_name)
                collection = document_details.get('collection', None)

                original_db_alias = document_details.get('original_db_alias', None)

                document._meta['db_alias'] = original_db_alias
                document._collection = collection

        return rendered_document_info
