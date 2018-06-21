FORMAT: 1A

# Maintenance Tracker App

Maintenance Tracker App is an application that provides users with the ability to create, update and monitor device repair or maintenance requests.

## Group Users

Resources related to users in the API.

## Authorization Collection [/v1/auth/{action}]

+ Parameters
    + action (string) - Either login or signup

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

+ Parameters
    + id (string) - ID of the desired request.

### View Single Request [GET]

A user may view a single request.

+ Response 200 (application/json)

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

A user may modify a pending request. It takes JSON object containing 'device type' and fault description. 

+ device type (string) - The type of device for which repair is required.

+ fault description (string) - The issue that needs attention.

+ id (string) - ID of the desired request.

+ Request (application/json)

        {
            "device_type": "Computer",
            "fault_description": "Crackedscreen"
        }

+ Response 200 (application/json) 

    + Body 

            {
                "device-status": "Pending",
                "device-type": "Computer",
                "fault-description": "Crackedscreen",
                "message": "A request was modified",
                "request-id": "61fc5e4f-7241-11e8-9b11-a8a795b59b66",
                "status": "OK"
            }

## Admin Requests [/v1/requests]

An admin can view all requests registered.

+ Response 200 (application/json)
    
    + Body 

            {
                "message": "successful",
                "requests": [
                    {
                        "device_status": "Approved",
                        "device_type": "Edgars Phone",
                        "fault_description": "Dead battery",
                        "id": "84935fc0-6a32-11e8-bb85-caca35d9aa6d",
                        "user_id": "a9115521-6a30-11e8-8d13-caca35d9aa6d"
                    },
                    {
                        "device_status": "Pending",
                        "device_type": "Edgars Phone",
                        "fault_description": "Dead battery",
                        "id": "2ac1c5f0-6a45-11e8-9e31-caca35d9aa6d",
                        "user_id": "fda80ecf-6a44-11e8-afb1-caca35d9aa6d"
                    },
                    {
                        "device_status": "Pending",
                        "device_type": "   ",
                        "fault_description": "   ",
                        "id": "58fddd00-6a45-11e8-b7e9-caca35d9aa6d",
                        "user_id": "fda80ecf-6a44-11e8-afb1-caca35d9aa6d"
                    },
                    {
                        "device_status": "Pending",
                        "device_type": "@#$%^&&&&&",
                        "fault_description": "@#$%^&",
                        "id": "66b1188f-6a45-11e8-86dc-caca35d9aa6d",
                        "user_id": "fda80ecf-6a44-11e8-afb1-caca35d9aa6d"
                    }
                ],
                "status": "OK"
            }

## Admin Modify Requests [/v1/requests/{id}/{action}]

An admin can either approve, disaaprove or resolve a request. Only pending requests can be approved.

+ Parameters
    + id (string) - ID of the desired request.
    + action (string) - Either approve, disapprove or resolve.

+ Response 200 (application/json)\

    + Body 

            {
                "device-status": "Disapproved",
                "device-type": "Edgars Phone",
                "fault-description": "Dead battery",
                "message": "A request was modified",
                "request-id": "2ac1c5f0-6a45-11e8-9e31-caca35d9aa6d",
                "status": "OK"
            }

