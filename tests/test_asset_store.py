import os
import tempfile
from typing import Iterator

import cv2
import numpy
import pytest

from facefusion.apis import asset_store


@pytest.fixture(scope = 'function', autouse = True)
def before_each() -> None:
	asset_store.clear()


@pytest.fixture(scope = 'function')
def temp_file() -> Iterator[str]:
	fd, path = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd)
	image = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path, image)
	yield path
	if os.path.exists(path):
		os.remove(path)


@pytest.fixture(scope = 'function')
def session_id() -> str:
	return 'test-session-123'


def test_create_source_asset(temp_file : str, session_id : str) -> None:
	asset = asset_store.create_asset(session_id, 'source', temp_file)

	assert asset is not None
	assert isinstance(asset.get('id'), str)
	assert len(asset.get('id')) == 36
	assert asset.get('type') == 'source'
	assert asset.get('path') == temp_file
	assert asset.get('size') > 0
	assert asset.get('created_at')


def test_create_target_asset(temp_file : str, session_id : str) -> None:
	asset = asset_store.create_asset(session_id, 'target', temp_file)

	assert asset is not None
	assert asset.get('type') == 'target'


def test_get_asset(temp_file : str, session_id : str) -> None:
	created_asset = asset_store.create_asset(session_id, 'source', temp_file)
	asset_id = created_asset.get('id')

	asset = asset_store.get_asset(session_id, asset_id)
	assert asset is not None
	assert asset.get('id') == asset_id
	assert asset.get('type') == 'source'


def test_get_asset_not_found(session_id : str) -> None:
	asset = asset_store.get_asset(session_id, 'non-existent-id')
	assert asset is None


def test_get_asset_wrong_session(temp_file : str, session_id : str) -> None:
	created_asset = asset_store.create_asset(session_id, 'source', temp_file)
	asset_id = created_asset.get('id')

	asset = asset_store.get_asset('different-session', asset_id)
	assert asset is None


def test_get_assets_empty(session_id : str) -> None:
	assets = asset_store.get_assets(session_id)
	assert assets is None


def test_get_assets_with_multiple(temp_file : str, session_id : str) -> None:
	fd1, path1 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd1)
	image1 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path1, image1)

	fd2, path2 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd2)
	image2 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path2, image2)

	try:
		asset_store.create_asset(session_id, 'source', path1)
		asset_store.create_asset(session_id, 'source', path2)
		asset_store.create_asset(session_id, 'target', temp_file)

		assets = asset_store.get_assets(session_id)
		assert assets is not None
		assert len(assets) == 3
	finally:
		if os.path.exists(path1):
			os.remove(path1)
		if os.path.exists(path2):
			os.remove(path2)


def test_get_assets_session_scoped(temp_file : str) -> None:
	session1_id = 'session-1'
	asset1 = asset_store.create_asset(session1_id, 'source', temp_file)
	asset1_id = asset1.get('id')

	session2_id = 'session-2'

	fd, path2 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd)
	image2 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path2, image2)

	try:
		asset2 = asset_store.create_asset(session2_id, 'source', path2)
		asset2_id = asset2.get('id')

		assets_session2 = asset_store.get_assets(session2_id)
		assert assets_session2 is not None
		assert len(assets_session2) == 1
		assert asset2_id in assets_session2

		assets_session1 = asset_store.get_assets(session1_id)
		assert assets_session1 is not None
		assert len(assets_session1) == 1
		assert asset1_id in assets_session1
	finally:
		if os.path.exists(path2):
			os.remove(path2)


def test_delete_assets(session_id : str) -> None:
	fd1, path1 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd1)
	image1 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path1, image1)

	fd2, path2 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd2)
	image2 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path2, image2)

	try:
		asset1 = asset_store.create_asset(session_id, 'source', path1)
		asset2 = asset_store.create_asset(session_id, 'source', path2)
		asset1_id = asset1.get('id')
		asset2_id = asset2.get('id')

		asset_store.delete_assets(session_id, [asset1_id])

		assets = asset_store.get_assets(session_id)
		assert assets is not None
		assert len(assets) == 1
		assert asset2_id in assets
		assert asset1_id not in assets
	finally:
		if os.path.exists(path1):
			os.remove(path1)
		if os.path.exists(path2):
			os.remove(path2)


def test_delete_assets_not_found(session_id : str) -> None:
	asset_store.delete_assets(session_id, ['non-existent-id'])


def test_clear() -> None:
	fd1, path1 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd1)
	image1 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path1, image1)

	fd2, path2 = tempfile.mkstemp(suffix = '.jpg')
	os.close(fd2)
	image2 = numpy.zeros((100, 100, 3), dtype = numpy.uint8)
	cv2.imwrite(path2, image2)

	try:
		session1_id = 'session-1'
		session2_id = 'session-2'

		asset_store.create_asset(session1_id, 'source', path1)
		asset_store.create_asset(session2_id, 'source', path2)

		asset_store.clear()

		assert asset_store.get_assets(session1_id) is None
		assert asset_store.get_assets(session2_id) is None
	finally:
		if os.path.exists(path1):
			os.remove(path1)
		if os.path.exists(path2):
			os.remove(path2)
