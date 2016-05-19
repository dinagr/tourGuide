
var TourGuideApp = angular.module('TourGuideApp', ['ngRoute', 'ui.bootstrap']);

TourGuideApp.config(function($routeProvider) {
    $routeProvider.
        when('/', {
            templateUrl: 'static/mainPage.html',
            controller: 'mainPageSearch'
        }).

        when('/guides', {
            templateUrl: 'static/guides.html',
            controller: 'guidesData'
        }).
            
        when('/userSignIn', {
            templateUrl: 'static/userSignIn.html',
            controller: 'userRegister'
        }).
            
        when('/guideSignIn', {
            templateUrl: 'static/guideSignIn.html',
            controller: 'guideRegister'
        }).

        when('/guideAddLanguange/:userId', {
            templateUrl: 'static/guideAddLanguange.html',
            controller: 'addLanguange'
        }).

        when('/guideAddCountries/:userId', {
            templateUrl: 'static/guideAddCountries.html',
            controller: 'addCountiries'
        }).

        when('/guideDetailsSignIn/:userId', {
            templateUrl: 'static/guideDetailsSignIn.html',
            controller: 'guideDetails'
        }).

        when('/guideDetailsPhotoSignIn/:userId', {
            templateUrl: 'static/guideDetailsPhotoSignIn.html',
            controller: 'guideDetails'
        }).
        
        when('/editGuideDetails/:userId', {
            templateUrl: 'static/editGuideDetails.html',
            controller: 'editGuideDetails'
        }).

        when('/guideProfile/:userId', {
            templateUrl: 'static/guideProfile.html',
            controller: 'guideProfile'
        }).
            
        when('/login', {
            templateUrl: 'static/login.html',
            controller: 'login'
        }).

        when('/logout', {
            templateUrl: 'static/logout.html',
            controller: 'logout'
        }).

        when('/privateChat/:userId', {
            templateUrl: 'static/privateChat.html',
            controller: 'privateChat'
        }).

        when('/writeMessage/:userId/:secondUserId', {
            templateUrl: 'static/writeMessage.html',
            controller: 'writeMessage'
        }).

        when('/updateGuideAvailability/:userId', {
            templateUrl: 'static/guideAvailability.html',
            controller: 'guideAvailability'
        }).

        when('/searchResults/:searchData', {
            templateUrl: 'static/searchResults.html',
            controller: 'searchResults'
        }).

        when('/advancedSearch', {
            templateUrl: 'static/advancedSearch.html',
            controller: 'advancedSearch'
        }).

        when('/advancedSearch/:location/:language/:fromDate/:toDate', {
            templateUrl: 'static/advancedSearch.html',
            controller: 'advancedSearchResults'
        }).

        otherwise({
            redirectTo: '/'
        });
    });

