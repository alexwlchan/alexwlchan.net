# -*- encoding: utf-8

import boto3
from moto import mock_s3
import pytest

from matching_s3_objects import get_matching_s3_keys


@pytest.fixture
def s3_buckets():
    with mock_s3():
        boto3.setup_default_session(region_name='eu-west-1')

        client = boto3.client('s3')

        client.create_bucket(Bucket='empty-bucket')

        client.create_bucket(Bucket='busy-bucket')
        for key in [
            'key1',
            'key2',
            'key3',
            'longkey1',
            'longkey2',
            'longkey3_suffix',
            'longkey4_suffix',
            'miscellaneous',
        ]:
            client.put_object(Bucket='busy-bucket', Key=key, Body=b'')

        yield


def test_empty_bucket_has_no_keys(s3_buckets):
    assert list(get_matching_s3_keys(bucket='empty-bucket')) == []


def test_getting_prefixes(s3_buckets):
    assert list(get_matching_s3_keys(bucket='busy-bucket', prefix='key')) == [
        'key1', 'key2', 'key3'
    ]


def test_getting_suffixes(s3_buckets):
    assert list(get_matching_s3_keys(
        bucket='busy-bucket',
        prefix='longkey',
        suffix='_suffix')) == ['longkey3_suffix', 'longkey4_suffix']
