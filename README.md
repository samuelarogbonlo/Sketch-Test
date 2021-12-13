# Sketch Task

# Python Script to Move Files Between S3 Buckets
Opinionated project architecture and scripts for moving all images from the `legacy-s3` to the `production-s3` and updates their paths in the database. 

The architecture of operation can be found via the folder directed [here](https://github.com/samuelarogbonlo/sre-test/blob/master/ModelOfOperation.png)

## Operation Functionality
This script copies PNG images from a source bucket to a destination bucket. It renames the object's (PNG images) key prefix in the destination bucket and adds the PNG images in the destination bucket, and finally it updates a database containing a path (key prefix and object name i.e, PNG image file name) to the PNG images in the source bucket, to the new path (new key prefix and object name i.e, PNG image file name) of the PNG  images in the destination bucket. Example: `image/avatar-xx.png` is the old path in database and `avatar/avatar-xx.png` is the new updated path in database after copy operation. 
**NB:** Where `image` is the old key prefix, `avatar` is the new key prefix and `avatar-xx.png` is the PNG file name or object name. 

## Core Structure
    Mina Node Deployment
      │   ├── move.py   
      │   │
      │   └── requirements.txt
      ├── seed
      │   > seeder.py  
      │
      └── README.md (you are here)

## How To Run

- Clone the github repository by running `git clone <repo_url>` in your terminal
- Navigate to the folder containing the `move.py` file
- Install dependencies with `pip3 install -r requirements.txt`
- To seed dummy data into your database, make sure to set the environment variables defined in the `.env.example` file. Then, run the command `python3 seed/seeder.py <number_of_images>`. Set `<number_of_images>` to whatever number of images you want the seed script to create in your database.
- Run the command `python3 move.py` in your terminal to run the `move.py` script

## Development Setup

Resources used in this script were created manually including S3 buckets and PostgreSQL databases. However, in a production environment, it is strongly advised to follow infrastructure as code best practices. Two S3 buckets were created on the AWS console and a PostgreSQL database called `proddatabase` was created. This database has a table called `avatars` with a column called `path`

## Performance and Scalability

When testing the program initially, It was discovered that the original synchronous solution implemented was not going to be easy to scale. It waited for each PNG file to get copied before moving to the next one. An asynchronous approach was then implemented, which runs each copy operation on its own thread. This resulted in a tremendous improvement in performance.

## Authors
- Samuel Arogbonlo - [GitHub](https://github.com/samuelarogbonlo) · [Twitter](https://twitter.com/samuelarogbonlo)

## Collaborators
- [YOUR NAME HERE] - Feel free to contribute to the codebase by resolving any open issues, refactoring, adding new features, writing test cases or any other way to make the project better and helpful to the community. Feel free to fork and send pull requests.

## Resources and Inspirations
- Start learning by looking at sample codes on GitHub: [#LearnByExamples](https://github.com/topics/learn-by-examples)

## Hire me
Looking for an Infrastructure engineer to build your next infrastruture in O(1) Labs and work remotely? Get in touch: [sbayo971@gmail.com](mailto:sbayo971@gmail.com)

## License

The MIT License (http://www.opensource.org/licenses/mit-license.php)

