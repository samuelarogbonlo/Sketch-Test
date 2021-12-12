# Python Script to Move Files Between S3 Buckets

This script moves legacy assets to a production S3 bucket

## How to Run

- Clone the github repository by running `git clone <repo_url>` in your terminal
- Navigate to the folder containing the `move.py` file
- Install dependencies with `pip3 install -r requirements.txt`
- To seed dummy data into your database, make sure to set the environment variables defined in the `.env.example` file. Then, run the command `python3 seed/seeder.py <number_of_images>`. Set `<number_of_images>` to whatever number of images you want the seed script to create in your database.
- Run the command `python3 move.py` in your terminal to run the `move.py` script

## Development setup

Resources used in this script were created manually including S3 buckets and PostgreSQL databases. However, in a production environment, it is strongly advised to follow infrastructure as code best practices. Two S3 buckets were created on the AWS console and a PostgreSQL database called `proddatabase` was created. This database has a teble called `avatars` with a column called `path`

## Performance and Scalability

When testing the app initially, I discovered that the original synchronous solution I had wasn't going to scale. It waited for each file to get copied before moving to the next one. I decided to move to an asynchronous solution by running each copy operation on its own thread. This resulted in a tremendous improvement in performance.
