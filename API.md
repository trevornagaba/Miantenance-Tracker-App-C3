FORMAT: 1A

# Maintenance Tracker App

Maintenance Tracker App is an application that provides users with the ability to create, update and monitor device repair or maintenance requests.

## Group Users

Resources related to users in the API.

## Authorization Collection [/v1/auth/{action}]

### Login [POST]

A user may login to his/her own account using this action. It takes a JSON object containing username and password.

+ username (string) - username of the user.

+ password (string) - password of the user.

+ Request (application/json)

            {
                "username":"Jackson",
                "password":"password"
            }

+ Response 201 (application/json)

    + Body
                {
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImNhM2MxM2IwLTcyMzgtMTFlOC04Yzc1LWE4YTc5NWI1OWI2NiIsImV4cCI6MTUyOTQxODA1Mn0.lPVhPRDOqDrfw2Nb7dDLkeJYIfFxHFDtNVc3bBZ_H98",
                    "user": {
                        "admin": false,
                        "id": "ca3c13b0-7238-11e8-8c75-a8a795b59b66",
                        "password": "sha256$SfAZtjZZ$7c781551f4c9de19ffe03d8cff31c4b5ea5fc35cefeb79697dc61afa1a3c09d3",
                        "username": "Jackson"
                    }
                }

### Signup [POST]

A user may create his/her own account using this action. It takes a JSON object containing 'username', 'password' and 'reenter_password'.

+ username (string) - The desired username of the user.

+ password (string) - The desired password of the user.

+ reenter_password (string) - The password is re-entered.

+ Request (application/json)

            {
                "username":"Jackson",
                "password":"password",
	            "reenter_password":"password"
            }

+ Response 201 (application/json)

    + Body
                {
                    "message": "User registered",
                    "status": "OK",
                    "username": {
                        "admin": false,
                        "id": "5a89abd2-72d4-11e8-b0e1-a8a795b59b66",
                        "password": "sha256$2axHCWU3$b106f9519ec507dcef526c35897029dfd61c649ce223feb2d4b58a89057e8160",
                        "username": "Jackson"
                    }
                }

## Group Requests

Resources related to requests in the API.

## Requests Collection [/v1/users/requests]

### Create Request [POST]

A user may create his/her own request using this action. It takes a JSON object containing 'device type' and 'fault description'.

+ device type (string) - The type of device for which repair is required.

+ fault description (string) - The issue that needs attention.

+ Request (application/json)

            {
                "device_type": "Laptop",
                "fault_description": "Battery not functioning"
            }

+ Response 201 (application/json)

    + Body
                {
                    "device-status": "Pending",
                    "device-type": "Laptop",
                    "message": "Request created successfully",
                    "request-id": "a94e2bb8-72d5-11e8-9636-a8a795b59b66",
                    "status": "OK"
                }

### View All Requests [GET]

A user may view all his/her requests. 

+ Response 200 (application/json)

    + Body

                {
                    "message": "successful",
                    "requests": [
                        {
                            "device_status": "Pending",
                            "device_type": "Laptop",
                            "fault_description": "Nosignal",
                            "id": "f1c59a61-7241-11e8-8a51-a8a795b59b66",
                            "user_id": "ca3c13b0-7238-11e8-8c75-a8a795b59b66"
                        },
                        {
                            "device_status": "Pending",
                            "device_type": "Laptop",
                            "fault_description": "Nosignal",
                            "id": "05b712b0-72d3-11e8-ad08-a8a795b59b66",
                            "user_id": "ca3c13b0-7238-11e8-8c75-a8a795b59b66"
                        },
                        {
                            "device_status": "Pending",
                            "device_type": "Laptop",
                            "fault_description": "Nosignal",
                            "id": "960eb9f6-72d5-11e8-bf9c-a8a795b59b66",
                            "user_id": "ca3c13b0-7238-11e8-8c75-a8a795b59b66"
                        },
                        {
                            "device_status": "Pending",
                            "device_type": "Laptop",
                            "fault_description": "Nosignal",
                            "id": "a94e2bb8-72d5-11e8-9636-a8a795b59b66",
                            "user_id": "ca3c13b0-7238-11e8-8c75-a8a795b59b66"
                        },
                        {
                            "device_status": "Pending",
                            "device_type": "Computer",
                            "fault_description": "Crackedscreen",
                            "id": "61fc5e4f-7241-11e8-9b11-a8a795b59b66",
                            "user_id": "ca3c13b0-7238-11e8-8c75-a8a795b59b66"
                        }
                    ],
                    "status": "OK"
                }

## Single Request Collection [/v1/users/requests/{id}]

### View Single Request [GET]

A user may view a single request.

+ id (string) - ID of the desired request.

+ Response 

    + Body
                {
                    "device-status": "Pending",
                    "device-type": "Laptop",
                    "fault description": "Nosignal",
                    "id": "f1c59a61-7241-11e8-8a51-a8a795b59b66",
                    "message": "successful",
                    "status": "OK"
                }        

### Modify single request [PUT]

+ Response 

## Admin Requests [/v1/requests]

+ Response 

## Admin Modify Requests [/v1/requests/{id}/{action}]

+ Response 


