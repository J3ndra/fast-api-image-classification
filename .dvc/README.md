# How to use `.dvc`

1. Make sure MinIO has run successfully. Then create new `Access Key`, copy the `Access Key` and `Secret Key` to safe place.
2. Run command `dvc config --local remote.minio-remote.access_key_id <Access Key>` and `dvc config --local remote.minio-remote.secret_access_key <Secret Key>`. It will generate file `.dvc/config.local` where it will contain MinIO Access key and Secret Key.
3. Then ran command `dvc push -r minio-remote` to push your model to MinIO.

### DVC Pipeline

```bash
# preprocess_image.py
dvc run -n preprocess \
    -d datasets/images/ \
    -o datasets/preprocessed/ \
    python scripts/preprocess_images.py
```

```bash
# train.py
dvc run -n train \
    -d datasets/preprocessed/ \
    -d scripts/train.py \
    -o models/ \
    python scripts/train.py --data-dir datasets/preprocessed/ --model-dir models/
```


