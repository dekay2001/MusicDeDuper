import md_test_base
import md_app.music_deduper

class test_musicDeduper(md_test_base.md_test_base):
	def setUp(self):
		self.de_duper = md_app.music_deduper.musicDeDuper()

	def test_get_similar_file_names(self):
		self.assertGreater(self.de_duper.get_similar_file_names(start_index = 1100),0)

	def test_get_similar_count_top_folder(self):
		"""Tests the the top level directory has more similar
		directories than 0"""
		self.assertGreater(self.de_duper.get_similar_count_top_folder(),0)

class testSimilarNames(md_test_base.md_test_base):
	def setUp(self):
		self.similar_names = md_app.music_deduper.similarNames('Dan1', 'Dan2')

	def test_name1(self):
		self.similar_names.name1 = 'Sam'
		name1 = self.similar_names.name1
		self.assertEqual('Sam', name1)

	def test_name2(self):
		self.similar_names.name2 = 'Sam'
		name2 = self.similar_names.name2
		self.assertEqual('Sam', name2)

	def test_different_names(self):
		name1 = self.similar_names.name1
		name2 = self.similar_names.name2
		self.assertNotEqual(name1, name2)