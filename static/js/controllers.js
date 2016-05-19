
/**Controller for main page (home page)**/
/**This page includes general search by location (country or city)**/
TourGuideApp.controller('mainPageSearch', ['$scope', '$http', '$location', 'AuthenticationService', 
    function ($scope, $http, $location, AuthenticationService){ 
    $scope.searchData = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.search= function() {
        $location.path("/searchResults/" + $scope.searchData);
      };
}]);

/**Controller for main page search results**/
/**This page displays al guides that match the search, the user get start a new search by location**/
TourGuideApp.controller('searchResults', ['$scope', '$routeParams', '$location', 'AuthenticationService', 'searchGuides',
    function ($scope, $routeParams, $location, AuthenticationService, searchGuides){
    $scope.guides = '';
    $scope.searchData = $routeParams.searchData;
    $scope.searchFinished = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });
    // calling our submit function.
    $scope.search= function(data) {
        searchGuides.searchByLocation(data)
        .then(function(){
	    $scope.searchFinished = true;
            $scope.message = searchGuides.message;
            $scope.guides = searchGuides.guides;
        });  
    };

    $scope.search($routeParams.searchData);
    
    $scope.newSearch = function(){
        $location.path("/searchResults/" + $scope.searchData);
    };
    
}]);

/**Controller for advanced search**/
/**This page enables the user to search by dates, country, city and language**/
/**The dates are mandatory for the search**/
/**The system checks if the guide is availble in these dates**/ 
/**The guide can manage his avalibility in the app**/
TourGuideApp.controller('advancedSearch', ['$scope', '$location'
    ,'AuthenticationService', 'guideService', 'searchGuides',
     function ($scope, $location, AuthenticationService, guideService, searchGuides){
    $scope.message = '';
    $scope.searchFinished = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.open1 = function($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened1 = true;
            };

    $scope.open2 = function($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened2 = true;
            };

    $scope.newSearch = function(){
        var submitedLocation = ($scope.tourLocation ? $scope.tourLocation : 'noLocation') ;
        var submitedLanguage = ($scope.language ? $scope.language : 'noLanguage') ;
        $location.path("/advancedSearch/" + submitedLocation + '/' + submitedLanguage 
                + '/' + searchGuides.formattedDate($scope.fromDate) + 
                '/' + searchGuides.formattedDate($scope.toDate));
    };

}]);

/**Controller for advanced search results**/
/**This page displays the guides that match the search**/
/**The user can start a new search**/
TourGuideApp.controller('advancedSearchResults', ['$scope', '$location','$routeParams','AuthenticationService',
     'guideService', 'searchGuides', 
     function ($scope, $location, $routeParams, AuthenticationService, guideService, searchGuides){
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    if ($routeParams.location == 'noLocation'){
        $scope.tourLocation = '';    
    }
    else{
        $scope.tourLocation = $routeParams.location;
    }

    if ($routeParams.language == 'noLanguage'){
        $scope.language = '';    
    }
    else{
        $scope.language = $routeParams.language;
    }   

    $scope.fromDate = $routeParams.fromDate;
    $scope.toDate = $routeParams.toDate;

    $scope.clearSearchResults = function(){
        $scope.tourLocation = '';
        $scope.language = '';
        $scope.fromDate = '';
        $scope.toDate = '';        
    };

    $scope.open1 = function($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened1 = true;
            };

    $scope.open2 = function($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened2 = true;
            };

    $scope.newSearch = function(){
        var submitedLocation = ($scope.tourLocation ? $scope.tourLocation : 'noLocation') ;
        var submitedLanguage = ($scope.language ? $scope.language : 'noLanguage') ;
        $location.path("/advancedSearch/" + submitedLocation + '/' + submitedLanguage 
                + '/' + searchGuides.formattedDate($scope.fromDate) + 
                '/' + searchGuides.formattedDate($scope.toDate));
    };

    $scope.getSearchResults= function() {
        searchGuides.advancedSearchGuides($routeParams.location, $routeParams.language, 
            $routeParams.fromDate, $routeParams.toDate)
        .then(function(){
	    $scope.searchFinished = true;
            $scope.message = searchGuides.message;
            $scope.guides = searchGuides.guides;
        }); 
    };

    $scope.getSearchResults();
}]);

/**Controller for user registration for travellers only**/
TourGuideApp.controller('userRegister',['$scope', 'AuthenticationService', 'travellerService', 
    function ($scope, AuthenticationService, travellerService){
    $scope.message = '';
     $scope.showEmail = false;
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.submitUserForm = function() {
        travellerService.addNewUser($scope.firstName, $scope.lastName, 
        $scope.email, $scope.userName, $scope.password)
        .then(function(){
            $scope.message = travellerService.message;
        });
    };
    
}]);

/**Controller for login**/
/**If the user does not remeber his username or password he can enter his email**/
/**and get his credentials by email**/
TourGuideApp.controller('login', ['$scope', 'AuthenticationService',
    function ($scope, AuthenticationService){
    $scope.message = '';
    $scope.successMessage = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.loginForm = function() {
        AuthenticationService.logIn($scope.userName,$scope.password)
        .then(function(){
            $scope.message = AuthenticationService.message;
        });            
    };

    $scope.showEnterEmail = function(){
        $scope.showEmail = true;
    };

     $scope.hideEnterEmail = function(){
        $scope.showEmail = '';
    };

    $scope.sendCredentials = function(){
        AuthenticationService.sendMyCredentials($scope.email)
        .then(function(){
            $scope.successMessage = AuthenticationService.successMessage;
        });
    };
}]);     

/**Controller for logout**/
/**If the user was not logged in to the begin with, a message will appear to the user**/
TourGuideApp.controller('logout', ['$scope', 'AuthenticationService',
    function ($scope, AuthenticationService){
    $scope.message = '';
    AuthenticationService.logOut()
    .then(function(){
        $scope.message = AuthenticationService.message;
        AuthenticationService.getLoginStatus()
        .then(function(){
            $scope.loginUserId = AuthenticationService.loginUserId;
            $scope.userType = AuthenticationService.userType;
            $scope.loginUserName = AuthenticationService.userName;
        });    
    });
}]);

/**Controller for guide registrations**/
/**This page is the begining of the guide registration process**/
TourGuideApp.controller('guideRegister', ['$scope', 'AuthenticationService', 'guideService', 
    function ($scope, AuthenticationService, guideService){
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.submitGuideForm= function() {
        guideService.addNewGuide($scope.firstName, $scope.lastName, 
        $scope.email, $scope.userName, $scope.password)
        .then(function(){
            $scope.message = guideService.message;
        });
    };  
}]);

/**Controller for guide details**/
/**This user needs to enter more data about him, such as - guide certificate, age and photo**/
TourGuideApp.controller('guideDetails', ['$scope', '$routeParams', '$http', '$log', '$location', '$window', 'AuthenticationService', 
    'guideService', function ($scope, $routeParams, $http, $log, $location, $window, AuthenticationService, guideService){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    $scope.photoUploading = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    }); 
     $scope.uploadFile = function(files) {
        $scope.file = new FormData();
        $scope.file.append("file", files[0]);
    };
 
    $scope.submitGuideDetailsForm= function() {
        $scope.photoUploading = true;
	guideService.saveGuidePhoto($routeParams.userId ,$scope.file)
        .then(function(){
		$scope.photoUploading = '';
        	$scope.message2 = guideService.message2;
		if ($scope.message2 == 'success'){
			$location.path("/guideAddLanguange/"+$routeParams.userId);
		}
	});

        guideService.addNewGuideDetails($routeParams.userId ,$scope.age,
        $scope.certificate, $scope.yearsOfExperience, $scope.desc)
        .then(function(){

         	$scope.message = guideService.message;
        });

    };

}]);

/**Controller for guide language managment**/
/**This page enables the user to manage the language in which he can guide**/
TourGuideApp.controller('addLanguange', ['$scope', '$routeParams', 
    'AuthenticationService', 'guideService' 
    ,function ($scope, $routeParams, AuthenticationService, guideService){
    $scope.languages = '';
    $scope.language = 'English';
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.getLanguages= function(userId) {
        guideService.getGuideLanguages(userId)
        .then(function(){
            $scope.languages = guideService.languages;
        });
    };

    $scope.getLanguages($routeParams.userId);
    $scope.submitLanguages= function() { 

        guideService.addGuideLanguage($scope.language, $routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.getLanguages($routeParams.userId);
        });        
 
    };
    $scope.removeLanguage= function(languageName) {
    
        guideService.removeGuideLanguage(languageName, $routeParams.userId)
        .then(function(){
            $scope.message = AuthenticationService.message;
            $scope.getLanguages($routeParams.userId);
        });
    };

}]);

/**Controller for locations managment**/
/**This page enables the user to manage the location in which he can guide**/
TourGuideApp.controller('addCountiries', ['$scope', '$routeParams', 'AuthenticationService', 'guideService', 
    function ($scope, $routeParams, AuthenticationService, guideService){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    $scope.removeLocation= function(location) {
        guideService.removeGuideTourLocation(location, $routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.getLocations($routeParams.userId);
        });
    };

    $scope.getLocations= function(userId) {
        guideService.getGuideLocations(userId)
        .then(function(){
            $scope.locations = guideService.locations;
        });           
    };
    $scope.getLocations($routeParams.userId);

    $scope.submitCountryCity= function() {      
        if ($scope.finishSearch){
            guideService.addGuideLocations($scope.tourLocation, $routeParams.userId)
            .then(function(){
                $scope.message = guideService.message;
                $scope.getLocations($routeParams.userId);
            }); 
        };     
    };

}]);

/**Controller for guide profile**/
/**This page displays the guide profile that is visible to the users**/
/**Other users can write reviews for the guide in his profile page**/
/**Other users can write a private messgae to the guide**/ 
TourGuideApp.controller('guideProfile', ['$scope', '$location', '$routeParams', 'AuthenticationService','guideService',
    function ($scope, $location, $routeParams, AuthenticationService, guideService){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    $scope.file = '';
    $scope.photoUploading = '';
    $scope.showPhotoUpdate = '';

    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });
    
    $scope.loadGuideData = function(){
    	guideService.getGuideProfile($routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.firstName = guideService.firstName;
            $scope.lastName = guideService.lastName;
            $scope.age = guideService.age;
            $scope.years = guideService.years;
            $scope.certificate = guideService.certificate;
            $scope.desc = guideService.desc;
            $scope.photo = guideService.photo;
        });
    };

    $scope.loadGuideData();

    guideService.getGuideLanguages($routeParams.userId)
        .then(function(){
            $scope.languages = guideService.languages;
            $scope.message = guideService.message;
        });

    guideService.getGuideLocations($routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.locations = guideService.locations;
        });  
        
    $scope.getReviews = function(userId){
        guideService.getGuideReviews(userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.reviews = guideService.reviews;
	    $scope.users = guideService.users;
        });

    $scope.getGradeFullStars = function(grade) {
        return new Array(grade);  
        }; 

    $scope.getGradeEmptyStars = function(grade) {
        return new Array(5-grade);  
        };
    };
    
    $scope.getReviews($routeParams.userId);

    $scope.addReview= function() {
        guideService.writeGuideReviews($scope.review, $scope.reviewGrade, $routeParams.userId, $scope.loginUserId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.getReviews($routeParams.userId);
	    $scope.review = '';
	    $scope.reviewGrade = '';
        });
    };

    $scope.uploadFile = function(files) {
        $scope.file = new FormData();
        $scope.file.append("file", files[0]);
    };

    $scope.enableEditPhoto =  function(){
        $scope.showPhotoUpdate = true;
    };

    $scope.disableEditPhoto =  function(){
        $scope.showPhotoUpdate = '';
	console.log("I disabled");
	console.log($scope.showPhotoUpdate);
    };

    $scope.updatePhoto = function(){

        $scope.photoUploading = true;
        guideService.updateGuidePhoto($routeParams.userId ,$scope.file)
        .then(function(){
                $scope.photoUploading = '';
                $scope.showPhotoUpdate = '';
                $scope.message2 = guideService.message2;
		$scope.loadGuideData();

        });
    };


}]);

/**Controller for managing guide availability**/
/**This page enable the user to manage when he is busy**/
/**If a user is searching for a guide in specific date**/
/**The system will not show the guides which are busy in these dates**/
TourGuideApp.controller('guideAvailability', ['$scope', '$routeParams', 'AuthenticationService',
    'guideService', 'searchGuides',
    function ($scope, $routeParams, AuthenticationService, guideService, searchGuides){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });
    $scope.open1 = function($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened1 = true;
            };
    $scope.open2 = function($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened2 = true;
            };

    $scope.getGuideAvailability= function(userId) {
        guideService.guideAvailability(userId)
        .then(function(){
            $scope.availability = guideService.availability;
        });
    };
        
    $scope.getGuideAvailability($routeParams.userId);

    $scope.submitDates= function() {
        guideService.updateGuideAvailability($scope.fromDate, $scope.toDate, $routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.getGuideAvailability($routeParams.userId);
        });       
    };
    
    $scope.removeBusyDates= function(fromDate, toDate) {        
        guideService.removeGuideAvailability($scope.fromDate, $scope.toDate, $routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.getGuideAvailability($routeParams.userId);
        }); 
    };

}]);

/**Controller for all guides display**/
/**This page displays all the guides ti the user**/
TourGuideApp.controller('guidesData', ['$scope', '$routeParams', 'AuthenticationService', 'searchGuides',
    function ($scope, $routeParams, AuthenticationService, searchGuides){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
    });

    console.log("inside guides controller");
    searchGuides.getAllGuides()
    .then(function(){
        $scope.message = searchGuides.message;
        $scope.guides = searchGuides.guides;
	console.log("finish getting guides");
    });

}]);

/**Controller for managing guide details**/
/**This page enables the guide to edit the details that he defined**/
TourGuideApp.controller('editGuideDetails', ['$scope', '$routeParams', '$location',
    'AuthenticationService', 'guideService',
    function ($scope, $routeParams, $location, AuthenticationService, guideService){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
        if (!$scope.loginUserId){
            $location.path("/login");
        };
        if ($scope.loginUserId && $scope.loginUserId != $routeParams.userId){
            $location.path("/");
        };
    });

    guideService.getGuideProfile($routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;
            $scope.firstName = guideService.firstName;
            $scope.lastName = guideService.lastName;
            $scope.age = guideService.age;
            $scope.years = guideService.years;
            $scope.certificate = guideService.certificate;
            $scope.descrip = guideService.desc;
            $scope.email = guideService.email;
        });

    $scope.updateGuideDetails= function(){
        guideService.updateProfile($scope.firstName ,$scope.lastName 
                ,$scope.email, $scope.certificate,
                $scope.years, $scope.descrip, $scope.age, $routeParams.userId)
        .then(function(){
            $scope.message = guideService.message;      
	    if ($scope.message == 'success'){
	    	$location.path('/guideProfile/' + $routeParams.userId);
	    }
        });
    };
}]);

/**Controller for private chat**/
/**This page displays all the user that the logged in user had private chats with**/
/**The user can choose a conversation - see the conversation and continue it**/
TourGuideApp.controller('privateChat', ['$scope', '$routeParams', '$location',
 'AuthenticationService', 'privateChat',
    function ($scope, $routeParams, $location, AuthenticationService, privateChat){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
        if (!$scope.loginUserId){
            $location.path("/login");
        };
        if ($scope.loginUserId && $scope.loginUserId != $routeParams.userId){
            $location.path("/");
        };
    });

    privateChat.getAllUserChats($routeParams.userId)
    .then(function(){
        $scope.message = privateChat.message;
        $scope.users = privateChat.users;
    });

}]);

/**Controller for writing a private message for one user to another**/
/**Once a meesgae is sent, an email is sent to the reciever**/
/**The email says that there is a message waiting for him**/
TourGuideApp.controller('writeMessage', ['$scope', '$routeParams', '$location',
 'AuthenticationService', 'privateChat',
    function ($scope, $routeParams, $location, AuthenticationService, privateChat){
    $scope.userId = $routeParams.userId;
    $scope.message = '';
    AuthenticationService.getLoginStatus()
    .then(function(){
        $scope.message = AuthenticationService.message;
        $scope.loginUserId = AuthenticationService.loginUserId;
        $scope.userType = AuthenticationService.userType;
        $scope.loginUserName = AuthenticationService.userName;
        if (!$scope.loginUserName){
            $location.path("/login");
        };
        if ($scope.loginUserId && $scope.loginUserId != $routeParams.userId){
            $location.path("/");
        };
    });

    $scope.getMessages= function(userId, secondUserId) {
        privateChat.getChatBetweenTwoUsers(userId, secondUserId)
        .then(function(){
            $scope.message = privateChat.message;
            $scope.chat = privateChat.chat;
            $scope.user1 = privateChat.user1;
            $scope.user2 = privateChat.user2;
        });
    };

    $scope.getMessages($routeParams.userId, $routeParams.secondUserId);

    $scope.addMessage= function() {
        privateChat.AddPrivateMessage($scope.msgContent, $scope.msgTitle,$routeParams.userId, $routeParams.secondUserId)
        .then(function(){
            $scope.message = privateChat.message;
            $scope.getMessages($routeParams.userId, $routeParams.secondUserId);
	    $scope.successMessage = privateChat.successMessage;
        });
    };
}]);



