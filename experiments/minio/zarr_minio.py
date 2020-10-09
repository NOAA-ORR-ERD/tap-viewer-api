"""
a test of minio
"""

import json
from pathlib import Path

import s3fs
import zarr

credentials = json.load(open("minio_credentials.json"))

tap_path = Path(credentials['bucket'])

fs = s3fs.S3FileSystem(anon=False,
                       key=credentials["user"],
                       secret=credentials["password"],
                       client_kwargs={
                           'endpoint_url': credentials["endpoint"],
                           }
                       )


# # Using the zarr lru cache

# store = fs.S3Map(root='zarr-demo/store', s3=s3, check=False)
# cache = zarr.LRUStoreCache(store, max_size=2**28)
# root = zarr.group(store=cache)
# z = root['foo/bar/baz']

# from timeit import timeit
# >>> # first data access is relatively slow, retrieved from store
# ... timeit('print(z[:].tostring())', number=1, globals=globals())
# b'Hello from the cloud!'
# 0.1081731989979744
# >>> # second data access is faster, uses cache
# ... timeit('print(z[:].tostring())', number=1, globals=globals())
# b'Hello from the cloud!'
# 0.0009490990014455747


