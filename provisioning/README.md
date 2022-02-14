# Creating a Remote Machine

The main purpose is to create a remote machine capable of running the airflow server and dealing with data files processing.
Here follows the steps to put everything up and running. Some of them require interaction with Google Cloud Platform (GCP Console or Gcloud SDK). You may find a detailed description about those tasks in the very Cloud documentation.

## Provisioning


### Set Up

The provisioning runs around Terraform, Packer, GCloud and SSH. Terraform and Packer are go-based tools and therefore you may
install them by downloading the binaries putting them in the path. SSH installation packages are available in any serious linux
distribution and it shouldn't be a problem to get in working in a tick.

To install GCloud SDK you can follow [install guide](https://cloud.google.com/sdk/docs/install) available on their site.
There's also an alternative if you don't want to install Gcloud directly in your distribution. You may run it as a dockerized
image. Here are the steps:

```sh
$ docker pull gcr.io/google.com/cloudsdktool/cloud-sdk:alpine

# Just to ease things
$ docker tag gcr.io/google.com/cloudsdktool/cloud-sdk:alpine cloud-sdk-alpine
$ docker run -ti --name gcloud-config cloud-sdk-alpine gcloud auth login
$ docker run --rm --volumes-from gcloud-config cloud-sdk-alpine gcloud config set project <project_id>

# Using alias
$ alias gcloud='docker run --rm --volumes-from gcloud-config cloud-sdk-alpine gcloud'
```

You may find more details regarding running Gcloud as a docker image [here](https://cloud.google.com/sdk/docs/downloads-docker)
.


### Workflow

_Enable GCloud APIs in Google Cloud_

- Compute Engine API (compute.googleapis.com)
- Identity and Access Management API (iam.googleapis.com)
- IAM Service Account Credentials API (iamcredentials.googleapis.com)
- Cloud Storage API (storage.googleapis.com)

You may do that in GCloud Console or using Gcloud SDK.

```sh
gcloud services enable iam.googleapis.com iamcredentials.googleapis.com \
    storage.googleapis.com compute.googleapis.com
```

_Create service account for Terraform, Packer, and for running airflow tasks in the VM_

```sh
gcloud iam service-accounts create packer-svc --display-name="Packer Service Account"
gcloud iam service-accounts create tf-svc --display-name="Terraform Service Account"
gcloud iam service-accounts create elt-svc --display-name="ELT Tasks Service Account"
```

Each account must have its set of roles assigned as well. Here are them:

- Packer
    - roles/compute.instanceAdmin.v1
    - roles/iam.serviceAccountUser
- Terraform
    - roles/compute.instanceAdmin.v1
    -roles/compute.admin
    -roles/storage.admin
    -roles/storage.objectAdmin
    -roles/bigquery.admin
- ELT
    - roles/storage.objectAdmin
    - roles/bigquery.admin

Use `add-iam-policy-binding` operation to do that via gcloud (you can also create a shell script to read a file with all
roles for each account and apply them).

```sh
    gcloud projects add-iam-policy-binding <project_id> \
        --member="serviceAccount:<account_email>" \
        --role="role identification"
```

_Create and download credentials files for each account_

```sh
$ gcloud iam service-accounts keys create path/to/key.json \
    --iam-account <account_email>
```

> **_NOTE:_** If you are using GCloud docker image, you should use a workaround. Here it is:
> ```sh
> $ docker run --rm --volumes-from gcloud-config -v path/to/dir:/tmp cloud-sdk-alpine gcloud \
>     iam service-accounts keys create /tmp/key.json \
>    --iam-account <account_email>
> $ sudo chown user:group path/to/dir/key.json
> ```

_Create an SSH Key and add it to project metadata_

```sh
$ ssh-keygen -t rsa -N "" -b 2048 -C <ssh_user> -f ~/.ssh/<key_file>
```

After creating the key, you should follow the instructions from 
[Google Cloud](https://cloud.google.com/compute/docs/connect/add-ssh-keys).

_Create the image_

- Configure Packer variables
- Run Packer

_Create the VM Instance

- Configure tf variables
- Run Terraform
