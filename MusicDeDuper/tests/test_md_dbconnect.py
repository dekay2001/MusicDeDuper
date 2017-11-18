import os
import md_test_base
import md_app.md_dbconnect

class test_musicDeduperDBManager(md_test_base.md_test_base):


    def setUp(self):
        self.db_manager = md_app.md_dbconnect.musicDeduperDBManager()
        self.db_path = os.path.dirname(__file__)
        self.db_test_name = os.path.join(self.db_path, 'test.sqlite')

    def tearDown(self):
        if os.path.exists(self.db_test_name):
            os.remove(self.db_test_name)

    def test_initialize(self):
        """Tests the creation of the test database.  It should exist 
        after initialization."""
        test_db = self.db_test_name
        self.db_manager.initialize(full_db_file_path=test_db)
        self.assertTrue(os.path.exists(test_db))
