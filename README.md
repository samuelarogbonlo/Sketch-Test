# Python Script to Move Files Between S3 Buckets

This script copies PNG images from a source bucket to a destination bucket. It renames the object's (PNG images) key prefix in the destination bucket and adds the PNG images in the destination bucket, and finally it updates a database containing a path (key prefix and object name i.e, PNG image file name) to the PNG images in the source bucket, to the new path (new key prefix and object name i.e, PNG image file name) of the PNG  images in the destination bucket. Example: `image/avatar-xx.png` is the old path in database and `avatar/avatar-xx.png` is the new updated path in database after copy operation. 
**NB:** Where `image` is the old key prefix, `avatar` is the new key prefix and `avatar-xx.png` is the PNG file name or object name. 

### Model of Operation of move.py Script
Below is a diagram describing the operation of the `move.py` script contained in this repository.
![Model of Operation](/samuelarogbonlo/sre-test/blob/master/ModelOfOperation.png)


## How to Run

- Clone the github repository by running `git clone <repo_url>` in your terminal
- Navigate to the folder containing the `move.py` file
- Install dependencies with `pip3 install -r requirements.txt`
- To seed dummy data into your database, make sure to set the environment variables defined in the `.env.example` file. Then, run the command `python3 seed/seeder.py <number_of_images>`. Set `<number_of_images>` to whatever number of images you want the seed script to create in your database.
- Run the command `python3 move.py` in your terminal to run the `move.py` script

## Development Setup

Resources used in this script were created manually including S3 buckets and PostgreSQL databases. However, in a production environment, it is strongly advised to follow infrastructure as code best practices. Two S3 buckets were created on the AWS console and a PostgreSQL database called `proddatabase` was created. This database has a table called `avatars` with a column called `path`

## Performance and Scalability

When testing the program initially, It was discovered that the original synchronous solution implemented was not going to be easy to scale. It waited for each PNG file to get copied before moving to the next one. An asynchronous approach was then implemented, which runs each copy operation on its own thread. This resulted in a tremendous improvement in performance.
