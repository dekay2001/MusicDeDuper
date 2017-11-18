import os

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import md_app.music_deduper

simple_page = Blueprint( 'simple_page', __name__,
						template_folder='templates')


file_directory, file_name = os.path.split(__file__)

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show_songs(page):
	try:
		page_file = os.path.join(file_directory, 'static\{}.html'.format(page))
		print(page_file)
		#C:\Dev\MusicDeDuper\md_app\static
		md = md_app.music_deduper.musicDeDuper()
		similar_songs = []
		#similar_songs = md.get_similar_top_folder_names()
		print(os.path.exists(page_file))
		return render_template(page_file, similar_songs=similar_songs )
	except TemplateNotFound:
		abort(404)

@simple_page.route('/similar_songs/')
def show_similar_songs():
	try:
		md = md_app.music_deduper.musicDeDuper()
		similar_songs = md.get_similar_file_names()
		return render_template('{}.html'.format('index'), similar_songs=similar_songs )
	except TemplateNotFound:
		abort(404)