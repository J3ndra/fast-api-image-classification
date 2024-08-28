# How to use `.dvc`

1. Make sure MinIO has run successfully and bucket called `model` is created. Then create new `Access Key`, copy the `Access Key` and `Secret Key` to safe place.

    > If you want to use another bucket name, change the bucket name in `.dvc/config`. You need to change this line `url = s3://model` where you can change with your bucket name `url = s3://<bucket_name>`.

2. Run command `dvc config --local remote.minio-remote.access_key_id <Access Key>` and `dvc config --local remote.minio-remote.secret_access_key <Secret Key>`. It will generate file `.dvc/config.local` where it will contain MinIO Access key and Secret Key.
3. Then ran command `dvc push -r minio-remote` to push your model to MinIO.

### DVC Pipeline

If you want to try to use DVC Pipeline, you can download the dataset [here](https://www.kaggle.com/datasets/nodoubttome/skin-cancer9-classesisic).

1. Put all image from `train` and `test` to one `image` folder

   ![Screenshot](../screenshots/Screenshot%202024-08-28%20151538.png)

2. Then just run `dvc proc` and wait until all the process finish. Hashed dataset will be uploaded to minio bucket.