import os
from ROOT import TH1F
from test_histotoolsbase import TestHistoToolsBase
from varial.wrappers import FileServiceAlias
from varial import dbio
from varial import analysis


class TestDbio(TestHistoToolsBase):
    def setUp(self):
        super(TestDbio, self).setUp()
        if not os.path.exists('test_data'):
            os.mkdir('test_data')
        dbio._init('test_data/test.db')

    def tearDown(self):
        dbio._close()
        super(TestDbio, self).tearDown()
        
    def test_write(self):
        dbio.write(self.test_wrp)

        # file should exist
        c = dbio._db_conn.cursor()
        c.execute('SELECT data FROM analysis WHERE path=?', (self.test_wrp.name,))
        self.assertTrue(
            bool(c.fetchone())
        )

    def test_read(self):
        dbio.write(self.test_wrp)
        loaded = dbio.read(self.test_wrp.name)
        self.test_wrp.history = str(self.test_wrp.history)

        # check names
        self.assertEqual(
            self.test_wrp.all_writeable_info(),
            loaded.all_writeable_info()
        )

        # check histograms (same integral, different instance)
        self.assertEqual(self.test_wrp.histo.Integral(),loaded.histo.Integral())
        self.assertNotEqual(str(self.test_wrp.histo), str(loaded.histo))


import unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestDbio)
if __name__ == '__main__':
    unittest.main()