# Python script to move files between S3 buckets

This script moves legacy assets to a production S3 bucket

## How to run

- Clone the github repository by running `git clone <repo_url>` in your terminal
- Navigate to the folder containing the `move.py` file
- Install dependencies with `pip3 install -r requirements.txt`
- To seed dummy data into your database, make sure to set the environment variables defined in the `.env.example` file. Then, run the command `python3 seed/seeder.py <number_of_images>`. Set `<number_of_images>` to whatever number of images you want the seed script to create in your database.
- Run the command `python3 move.py` in your terminal to run the `move.py` script

## Development setup

Resources used in this script were created manually including S3 buckets and PostgreSQL databases. However, in a production environment, it is strongly advised to follow infrastructure as code best practices.
