# event
signup:signup using username,password,name,email,phonenumber and add username and password to the auth User model,name,email,phonenumber add to the
Profile model  also generate jwt token

login:login using username and password

editprofile:user can edit own profile,permission required

createevent:create an event for user,fields included eventname,about,place,start_date,end_date,image,.image can not be multiple and format must be png,jpg,
jpeg .and save to the Event model.user can create many events.eventname must be unique

editevent: user can edit event 

viewprofile:view profile datas

viewmyevents:view user events

viewallevents:view all events

deleteevent:delete event
