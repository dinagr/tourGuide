/**This service manages authentications - login, logout, check who is logged**/
TourGuideApp.service('AuthenticationService', ['$http', '$location',
 function ($http, $location) {
    var obj = {};
    obj.message = '';
    obj.loginUserId = '';

    /**Check if a user is logged in**/
    obj.userLoggedIn = function () {
        return $http.get('/checkLoginStatus')
            .success(function(data)
            {
                return data.result;
            })
            .error(function(data)
            {
                return false;
            });
        };

    /**Check if a user is logged in - if there is, get user data**/
    obj.getLoginStatus = function () {
        obj.message = '';
        obj.loginUserId = '';
        obj.userName = '';
        obj.userType = '';
        return $http.get('/getUserLogin')
            .success(function(data)
            {
                if (data.result=='true')
                {
                    obj.userName = data.userName;
                    obj.loginUserId = data.userId;
                    obj.userType = data.userType;
                }
            })
            .error(function(data)
            {
                obj.message = 'something went wrong! please try again later'
            });
        };

    /**Logout the current user**/
    obj.logOut = function () {
        obj.message = '';
        return  $http.get('/logout')
                .success(function(results) 
                {  
                    obj.message = results.result
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again later'
                });
        };

    /**Check if user name and password entered are correct - if yes, that loggin user**/
    obj.logIn = function (userName, password) {
        obj.message = '';
        return  $http.post('/loginUser', {userName : userName, password: password })
                .success(function(results) 
                {   
                    if (results.result == 'success')
                    {
                        $location.path("/");
                    }
                    else {
                        obj.message = results.result;
                    }
                }).
                error(function(error) 
                {
                    obj.message = 'something went wrong! please try again later'
                });
        };

    /**IF the user forgot his user name or password he can enter his email**/ 
    /**and gethis credential by email**/
    obj.sendMyCredentials = function (email) {
        obj.message = '';
        return  $http.post('/getMyCredentials', {email : email})
                .success(function(results) 
                {   
                    if (results.emailSent){
                        obj.message = 'An email with your credentials was sent to you';
                    }
                    if (results.result != 'success'){
                        obj.message = results.result;
                    }
                }).
                error(function(error) 
                {
                    obj.message = 'something went wrong! please try again later';
                });
        };


    return obj;
}]);

/**This service manages all the traveller details**/
TourGuideApp.service('travellerService', ['$http', '$location', 
    function ($http, $location) {
    var obj = {};
    obj.message = ''; 

    /**Add a new user of type traveller**/
    obj.addNewUser = function (firstName, lastName,email, userName, password) {
        obj.message = '';
        return $http.post('/newUser', 
                {firstName: firstName, lastName: lastName, email: email, 
                userName: userName, password: password})
                .success(function(results) 
                {   
                    if (results.result == 'success')
                    {
                        $location.path("/login");
                    }
                    else 
                    {
                        obj.message = results.result;
                    }
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
            };
    return obj;
}]);

/**This service manages all the guide details and actions**/
TourGuideApp.service('guideService', ['$http', '$location', 'searchGuides',
    function ($http, $location, searchGuides) {
    var obj = {};
    obj.message = '';
    obj.message2 = '';

    /**Add a new user of ype guide**/
    obj.addNewGuide = function (firstName, lastName,email, userName, password) {
        obj.message = '';
        return  $http.post('/newGuide', 
                {firstName: firstName, lastName: lastName, email: email, 
                userName: userName, password: password})
                .success(function(results) 
                {   
                    if (results.result == 'success')
                    {   
                        var userId = results.userId;
                        $location.path("/guideDetailsSignIn/" + userId);
                    }
                    else 
                    {
                        obj.message = results.result;
                    }
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
            };

    /**Add the guide details - age, certificate, years of experience and desc**/
    obj.addNewGuideDetails = function (userId, age, certificate, yearsOfExperience, desc) {
        obj.message = '';
        return  $http.post('/newGuideDetails', {userId: userId ,age: age, certificate: certificate,
                 yearsOfExperience: yearsOfExperience, description: desc})
                .success(function(results) 
                {   
                    if (results.result == 'success')
                    {
                        var userId = results.userId;
                        $location.path("/guideAddLanguange/"+userId);
                    }
                    else 
                    {
                        obj.message = results.result;
                    }
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
            };

    /**Add the guide photo**/
    obj.saveGuidePhoto = function (userId, file) {
        obj.message = '';
        return  $http.post('/uploadFile/' + userId, file, {
                            headers: {'Content-Type': undefined},
                            transformRequest: angular.identity
                }).success(function(results) 
                {   
                    obj.message2 = results.result;
                }).error(function(error) 
                {
                    obj.message2 = 'something went wrong while saving the photo! please try again';
                });
            };

    /**Update guide photo**/
    obj.updateGuidePhoto = function (userId, file) {
        obj.message = '';
        return  $http.post('/updateFile/' + userId, file, {
                            headers: {'Content-Type': undefined},
                            transformRequest: angular.identity
                }).success(function(results) 
                {   
                    obj.message2 = results.result;
                }).error(function(error) 
                {
                    obj.message2 = 'something went wrong while saving the photo! please try again';
                });
            };

    /**Get all the languages that the guide can guide in**/
    obj.getGuideLanguages = function (userId) {
        obj.message = '';
        return  $http.get('/getLanguanges/'+ userId)
                        .success(function(data)
                        {
                            obj.languages = data.languages;
                        }).error(function(data)
                        {
                            obj.message = 'something went wrong! please try again';
                        });
            };

    /**Add a new language to the list of languages that the guide knows**/
    obj.addGuideLanguage = function (language, userId) {
        obj.message = '';
        return  $http.post('/addLanguange', {language: language, userId: userId})
            .success(function(results) 
            {   
                if (results.result != 'success'){
                    obj.message = results.result;
                }
            }).error(function(error) 
            {
                obj.message = 'something went wrong! please try again';
            });
        };

    /**Remove a language from the list of languages that the guide knows**/
    obj.removeGuideLanguage = function (language, userId) {
        obj.message = '';
        return  $http.post('/removeLanguage', {language, userId})
            .success(function(results) 
            {   
                if (results.result != 'success'){
                    $scope.message = results.result;
                }
            }).error(function(error) 
            {
                obj.message = 'something went wrong! please try again'; 
            });
        };

    /**Get the list of all countries in the DB**/
    obj.getCountriesList = function () {
        obj.message = '';
        return  $http.get('/getAllCountries')
                .success(function(data)
                {
                    obj.countries = data.countries;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        };

    /**Get the full country details from the Country table for a specific country**/
    obj.getCountryObject = function (country) {
        obj.message = '';
        return  $http.get('/getCountry/' + country )
                .success(function(data)
                {
                    obj.country = data.country;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        };

    /**Get the full city details from the Cities table for a specific city**/
    obj.getCityObject = function (city) {
        obj.message = '';
        return  $http.get('/getCity/' + city )
                .success(function(data)
                {
                    obj.city = data.city;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        }; 

    /**Get all the cities from the DB for a specific country**/
    obj.getCitiesList = function (country) {
        obj.message = '';
        return  $http.get('/getCitiesByCountry/'+country)
                .success(function(data)
                {
                    obj.cities = data.cities;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        }; 

    /**Remove a location from the list of locations in which the guide can guide in**/
    obj.removeGuideTourLocation = function (country, city, userId) {
        obj.message = '';
        return  $http.post('/removeLocation', {country: country, city: city, userId: userId})
                .error(function(error) 
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        }; 

    /**Get the list of locations which the guide can guide in**/
    obj.getGuideLocations = function (userId) {
        obj.message = '';
        return  $http.get('/getGuideLocations/'+userId)
                .success(function(data)
                {
                    obj.locations = data.guideLocs;

                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        };    

    /**Add a new location to the list of locations in which the guide can guide in**/
    obj.addGuideLocations = function (country, city, userId) {
        obj.message = '';
        return  $http.post('/addCountriesCities',{country: country ,city: city ,userId: userId})
                .success(function(data)
                {
                    if (data.result != 'success'){
                        obj.message = data.result;
                    }

                })
                .error(function(error) 
                {
                    obj.message = 'something went wrong! please try again'; 
                });
        };

    /**Get all the data for guide profile**/
    obj.getGuideProfile = function (userId) {
        obj.message = '';
        return  $http.get('/getGuideProfile/'+ userId)
                .success(function(data)
                {
                    obj.firstName = data.firstName;
                    obj.lastName = data.lastName;
                    obj.age = data.age;
                    obj.years = data.years;
                    obj.certificate = data.certificate;
                    obj.desc = data.desc;
                    obj.photo = data.photo;
                    obj.email = data.email;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Get all the reviews that were written to a guide**/
     obj.getGuideReviews = function (userId) {
        obj.message = '';
        return  $http.get('/getReviews/'+userId)
                .success(function(data)
                {
                    obj.reviews = data.reviews;

                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again';
                });
        }; 

    /**Write a new review to a guide**/
    obj.writeGuideReviews = function (review, reviewGrade, recieverUserId, writerUserId) {
        obj.message = '';
        return  $http.post('/addReview',{review: review ,reviewGrade: reviewGrade,
                recieverUserId: recieverUserId, writerUserId: writerUserId})
                .error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Update guide details**/
    /**firstname, lastname, email, certificate, age, years of experience and description**/
    obj.updateProfile = function (firstName, lastName, email, certificate, age, year, descrip, userId) {
        obj.message = '';
        return  $http.post('/updateGuideDetails',{firstName: firstName ,lastName: lastName
                ,email: email, certificate: certificate, age: age, years: year,
                 descrip: descrip, userId: userId})
                .success(function(results) 
                {   
                    $location.path('/guideProfile/' + userId);
           
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Get all the dates in which the guide is busy**/   
    obj.guideAvailability = function (userId) {
        obj.message = '';
        return  $http.get('/getGuideAvailability/'+ userId)
                .success(function(data)
                {
                    obj.availability = data.guideAvail;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Add new dates to the list of dates in which the guide is busy**/
    obj.updateGuideAvailability = function (fromDate, toDate, userId) {
        obj.message = '';
        return  $http.post('/updateGuideAvailability', 
                {fromDate: searchGuides.formattedDate(fromDate), 
                 toDate: searchGuides.formattedDate(toDate), userId: userId})
                .success(function(results) 
                {   
                    if (results.result != 'success'){
                        obj.message = results.result;
                    }
                })
                .error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Remove dates from the list of dates in which the guide is busy**/
    obj.removeGuideAvailability = function (fromDate, toDate, userId) {
        obj.message = '';
        return  $http.post('/ClearBusyDates', {fromDate: searchGuides.formattedDate(fromDate),
         toDate: searchGuides.formattedDate(toDate), userId: userId})
                .success(function(results) 
                {   
                    if (results.result != 'success'){
                        obj.message = results.result;
                    }
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
        };
    return obj;
}]);

/**This service manages private chats betwen 2 users**/
TourGuideApp.service('privateChat', ['$http', function ($http) {
    var obj = {};
    obj.message = ''; 

    /**When a user clicks on 'Messages' in his menu, a list will open with all the user that**/
    /**he had chats with in the past - the user can click on a specific chat and see the conversation**/
    obj.getAllUserChats = function (userId) {
        obj.message = '';
        return  $http.get('/privateChat/' + userId)
                .success(function(data)
                {

                    obj.users = data.chatUsers;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Get all the messages written by 2 users to one another**/
    obj.getChatBetweenTwoUsers = function (userId, secondUserId) {
        obj.message = '';
        return $http.get('/getMessagesBetweenUsers/'+ userId + '/' + secondUserId)
                .success(function(data)
                {
                    obj.chat = data.chat;
                    obj.user1 = data.user1;
                    obj.user2 = data.user2;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Write a private message to a user**/
    obj.AddPrivateMessage = function (msgContent, msgTitle, writer, receiver) {
        obj.message = '';
        return  $http.post('/writeMessage',{msgContent: msgContent ,msgTitle: msgTitle 
                ,writer: writer, receiver: receiver})
                .success(function(data)
                {
                   if (data.emailSent){
                        obj.message = 'An email regarding the message was sent to the user!'
                   }
                })
                .error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    return obj;
}]);

/**This service manages the search in the app - regurlar search and advanced search**/
TourGuideApp.service('searchGuides', ['$http', function ($http) {
    var obj = {};
    obj.message = ''; 

    /**Get all the guides data**/
    obj.getAllGuides = function (userId) {
        obj.message = '';
        return  $http.get('/getGuides')
                .success(function(data)
                {
                    obj.guides = data.guides;
                }).error(function(data)
                {
                    obj.message = 'something went wrong! please try again';
                });
        };

    /**Get all the guides data that match the search - the user can enter a country or a city**/
    obj.searchByLocation = function (data) {
        obj.message = '';
        return  $http.get('/search/' + data)
                .success(function(results) 
                {   
                    obj.guides = results.guides;
                }).error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });  
        };

    /**Change the date format**/
    obj.formattedDate =  function (date) {
        var d = new Date(date || Date.now()),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        return [day, month, year].join('-');
    };

    /**Get all the guides that match the search**/
    /**The user can search by - country, city, dates and language**/
    obj.advancedSearchGuides = function (country, city, language, fromDate, toDate) {
        obj.message = '';
        return  $http.get('/advancedSearch/' + country + '/' + city + '/' + language 
                + '/' + fromDate + '/' + toDate)
                .success(function(results) 
                {   
                    obj.guides = results.guides;
                }).
                error(function(error) 
                {
                    obj.message = 'something went wrong! please try again';
                });
    };

    return obj;
}]);