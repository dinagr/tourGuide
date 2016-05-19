
TourGuideApp.directive("navigationMenu", function() {
   return {
       restrict: 'E',
       templateUrl: '../static/directivesTemplates/navMenu.html' 
   }
});

TourGuideApp.directive("message", function() {
   return {
       restrict: 'E',
       templateUrl: '../static/directivesTemplates/message.html' 
   }
});

TourGuideApp.directive("successMessage", function() {
   return {
       restrict: 'E',
       templateUrl: '../static/directivesTemplates/successMessage.html'
   }
});


TourGuideApp.directive('googleplace', function() {
    return {
        link: function(scope, element, attrs) {
                    var options = {
                        types: ['(regions)']
                    };
                    scope.finishSearch = '';
                    scope.gPlace = new google.maps.places.Autocomplete(element[0], options);
                    element.blur(function(e) {
                        window.setTimeout(function() {
                            angular.element(element).trigger('input');
                            scope.finishSearch = true;
                        }, 0);
                    });
                }

    }
});

