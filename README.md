# Django Rest backend server with Firebase token auth mechanism and Docker containerization
<h2>Pre-Installation</h2>
<p>[!] Important thing - to use this project you will need to fill two json files: firebase_service_account_creds.json for service account credentials and firebase_app_creds.json for app credentials. Also, do not forgot to let users sign-in via email and password - it can be done in : firebase dashboard -> build -> authentication -> "Sign-in method" -> enable email and password auth</p>
<p>[*] How to fill firebase_app_creds:<br> firebase console -> create project -> start register web app by clicking on "< />" button -> end creating this web app by clicking on "Continue to console" button -> click on Realtime Database in Build tab -> Create Database -> Next -> Start in test mode -> after creating database in Realtime Database, in Data tab create any "key: data" pair -> click on gear icon -> Project Settings -> Reload page -> scroll down and get dictionary value from firebaseConfig (only part in {} with that brackets) and paste it to firebase_app_creds.json -> cover keys in quotes</p>
<p>[*] How to fill firebase_service_account_creds:<br> in firebase console click on gear icon -> Project settings -> Service accounts tab -> Select Python in Admin SDK configuration snippet -> click on "Generate new private key" button -> Generate Key -> Copy everything from downloaded file and paste it to firebase_service_account_creds.json</p>
<h2>Everything About Project</h2>
<p>Project is made by using django, drf, firebase-admin, pyrebase and drf-swagger</p>
<ul><p style="color: green">There is an opportunity to:</p>
    <li>generate Firebase token and  with authenticate with it</li>
    <li>create user(in local DB and firebase authenticated users list simultaneously)</li>
    <li>see the info of current authenticated user</li>
    <li>change the info of some user if you have admin permissions</li>
    <li>delete user from local DB and firebase authenticated users list in one click if you have admin permissions</li>
    <li>see the list of users in local DB or in firebase users list</li>
    <li>create custom super user via command 'python manage.py createcustomsuperuser'</li>
    <li>on the start of docker image the command 'python manage.py firstadminuser' will be executed so you can log in as super user(email=admin@example.com, password=1mytestuser!)</li>
</ul>
<br><hr>
<ol type="1"><p style="color: green">What work has been done:</p>
    <li>Connected Firebase project(and app) with my django project by using Firebase credentials in json files</li>
    <li>Set Firebase Token Authentication as standart authentication method for my project</li>
    <li>Overwritten default django user model</li>
    <li>Upgraded default django management command 'createsuperuser' and set it as 'createcustomsuperuser' command</li>
    <li>Added swagger and overwtitten it a little(button 'Authorize') for better presentation of this project</li>
    <li>Implemented CRUD operations for User model instances</li>
    <li>Created views to generate firebase token and authorize/authenticate with it</li>
    <li>Dokerized this project so it is easy to reproduce.</li>
</ol>
<br><hr>
<ol type="1"><p style="color: green">Algorithm to test all the possibilities of this project</p>
    <li>Use "git clone" for this repo</li>
    <li>Run command "docker-compose build --no-cache && docker-compose up" from the directory with Dockerfile and docker-compose.yml</li>
    <li>Go to http://0.0.0.0:8000/</li>
    <li>Use route "/auth/get_token/" and pass email 'admin@example.com' and password '1mytestuser!'. Copy the firebase token from response.</li>
    <li>Authorize via button "Authorize" by passing copied token in format "Token copied_token"</li>
    <li>See info about current authorized user with /auth/current_user_info/ </li>
    <li>See the list of local DB users with /auth/users_list/ </li>
    <li>See the list of Firebase users with /auth/users_list_firebase/ </li>
    <li>Create new user with help of /auth/register/ </li>
    <li>See the list of local DB users and Firebase user with /auth/users_list/ and /auth/users_list_firebase/ . As you see, new user has been added.</li>
    <li>Change new user data  with PATCH request to /auth/user/{id}. (For example, you can change nickname)</li>
    <li>Delete the user with DELETE request to /auth/user/{id} </li>
    <li>See the user lists - there is no user object there</li>
    <li>(Optionally) You can get token with credits of user created by /auth/register/  and see that you have not permissions to make CRUD operations and see the lists of all users - just because you are not an admin user.</li>
    <li>(Optionally) You can create custom super user via command in new terminal tab(but in same dir as docker-compose file) while "docker-compose up" is active: docker-compose run --rm app sh -c "python manage.py createcustomsuperuser". Than you can try to log in to admin panel and see the list of users.</li>
    <li> That's all for now, thanks for using this project!</li>
</ol>
<hr>
