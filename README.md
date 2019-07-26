# codechefGalleryServer
Simple photo viewing and storing app with album containing features.

Requirements:
Python Version: 3.6.7
Modules: [django, boto3, bson, json]

Database:
  Name: mongo 4.0.9
  Database Name: "gallery"
Collections: 
   1: "album": Schema:
       {
        "name" : String,
        "access" : enum("public","private"),
        "likes" : [mixed],
        "url" : String,
        "desc" : String,
        "datetime" : ISODate,
        "location" : String,
        "owner" : String
        }
   2: "photos": Schema:
       {
        "access" : enum("public","private"),
        "likes" : [mixed],
        "url" : String,
        "albumId" : String,
        "desc" : String,
        "datetime" : ISODate,
        "location" : String,
        "owner" : String
        }
   3: "users": Schema:
       {
        "username" : String,
        "first_name" : String,
        "last_name" : String,
        "gender" : enum("M","F"),
        "email" : String,
        "dp" : String,
        "password" : String
        }

Steps:
1: Clone the App
2: Install all python modules
3: Run Mongo [Mongo will run on http://127.0.0.1:27017/
4: Go to <Downloaded Path>/codechefGalleryServer/codechefGallery
5: run python3 manage.py runserver 8000 [Server will run on http://127.0.0.1:8000/ ]
6: Open the URL and you are good to go. The main webpage will open up

Setting up AWS Bucket 
  Bucket Name: codechefgallery
  Bucket Permissions:
    1: Go to bucket's Permission > Access Control List and set public access to everyone (List objects : yes, Read bucket     permissions : yes)
    2: Go to bucket's Permission > Bucket Policy and paste this Code and click save
          {
            "Version": "2008-10-17",
            "Statement": [
            {
              "Sid": "AllowPublicRead",
              "Effect": "Allow",
              "Principal": {
                  "AWS": "*"
              },
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::codechefgallery/*"
            }
            ]
          }

AWS Changes [Required to upload a file to AWS]:
Installing awscli
  1:sudo pip3 install awscli
Configuring it to access S3 bucket
  2: AWS configure
  3: (Upadte your credentials)
