# How to use `.dvc`

1. Make sure MinIO has run successfully. Then create new `Access Key`, copy the `Access Key` and `Secret Key` to safe place.
2. Run command `dvc config --local remote.minio-remote.access_key_id <Access Key>` and `dvc config --local remote.minio-remote.secret_access_key <Secret Key>`. It will generate file `.dvc/config.local` where it will contain MinIO Access key and Secret Key.
3. Then ran command `dvc push -r minio-remote` to push your model to MinIO.