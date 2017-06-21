'use strict';
angular.module('myApp.searchView', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/search-view', {
            templateUrl: 'search-view/search-view.html',
            controller: 'searchCtrl'
        });
    }])
    .controller('searchCtrl', [ '$scope', '$http', function($scope, $http) {
        $scope.onPhotoChange = function(photos) {
            $scope.selectedPhoto = photos[0];
            $scope.selectedPhotos = [];
            for (let photo of photos) {
                let reader = new FileReader();

                reader.onload = function (e) {
                    $scope.$evalAsync(function () {
                        $scope.selectedPhotos.push(e.target.result);
                    });
                };

                reader.readAsDataURL(photo);
            }
            
        };
        $scope.uploadFile = function() {
            let formData = new FormData();
            formData.append('file', $scope.selectedPhoto);

            $http({
                method: 'POST',
                url: 'http://localhost:4000/image',
                data: formData,
                headers: {
                    'Content-Type': undefined
                }
            })
            .success(function (data) {
                $scope.$evalAsync(function () {
                    $scope.message = "Uploaded successfully";
                });
                data.forEach((id)=>{
                    $scope.retrieveFiles(id);
                });
            })
            .error(function (data, status) {
                $scope.$evalAsync(function () {
                    $scope.message = status + " Upload unsuccessful";
                });
            });
        };
        $scope.retrieveFiles = function(data) {
            $scope.retrievedPhotos = [];
            $http({
                method : "GET",
                url : "http://localhost:4000/image/"+data
            }).then(function mySuccess(response) {
                $scope.retrievedPhotos.push("data:image/png;base64, "+response.data);
            }, function myError(response) {
                $scope.$evalAsync(function () {
                    $scope.message = "Failed! "+response.statusText;
                });
            });
        };
    }]);