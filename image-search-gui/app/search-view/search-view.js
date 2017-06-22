let Config = {
    ApiBaseUrl:'http://localhost:4000'
};

'use strict';
angular.module('myApp.searchView', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/search-view', {
            templateUrl: 'search-view/search-view.html',
            controller: 'searchCtrl'
        });
    }])
    .controller('searchCtrl', [ '$scope', '$http', function($scope, $http) {
        $scope.isBusy = false;
        $scope.onPhotoChange = function(photos) {
            $scope.originalPhoto = photos[0];
            let imgPreview = document.getElementById('imgPreview');
            let reader = new FileReader();
            reader.onload = function (e) {
                let image = new Image();
                image.onload = function (imageEvent) {
                    let canvas = document.createElement('canvas'),
                        max_size = 600,
                        width = image.width,
                        height = image.height;
                    if (width > height) {
                        if (width > max_size) {
                            height *= max_size / width;
                            width = max_size;
                        }
                    } else {
                        if (height > max_size) {
                            width *= max_size / height;
                            height = max_size;
                        }
                    }
                    canvas.width = width;
                    canvas.height = height;
                    canvas.getContext('2d').drawImage(image, 0, 0, width, height);
                    let dataURI = canvas.toDataURL("image/png");
                    imgPreview.src = dataURI;
                    let blob = $scope.dataUrlToBlob(dataURI);
                    $scope.selectedPhoto = $scope.blobToFile(blob, photos[0].name);
                };
                image.src = e.target.result;
            };

            reader.readAsDataURL(photos[0]);
        };
        $scope.uploadFile = function() {
            $scope.isBusy = true;
            let formData = new FormData();
            formData.append('file', $scope.selectedPhoto);
            // formData.append('file', $scope.originalPhoto);

            $http({
                method: 'POST',
                url: Config.ApiBaseUrl+'/image',
                data: formData,
                headers: {
                    'Content-Type': undefined
                }
            })
            .success(function (data) {
                $scope.$evalAsync(function () {
                    $scope.message = "Uploaded successfully";
                });
                $scope.retrievedPhotoCount = 0;
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
                url : Config.ApiBaseUrl+"/image/"+data
            }).then(function mySuccess(response) {
                $scope.$evalAsync(function () {
                    $scope.retrievedPhotos.push("data:image/png;base64, " + response.data);
                    $scope.retrievedPhotoCount++;
                    if ($scope.retrievedPhotoCount === 3) $scope.isBusy = false;
                });
            }, function myError(response) {
                $scope.$evalAsync(function () {
                    $scope.message = "Failed! "+response.statusText;
                });
            });
        };
        $scope.dataUrlToBlob = function(dataURI) {

            // convert base64 to raw binary data held in a string
            // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
            let byteString = atob(dataURI.split(',')[1]);

            // separate out the mime component
            let mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

            // write the bytes of the string to an ArrayBuffer
            let ab = new ArrayBuffer(byteString.length);

            // create a view into the buffer
            let ia = new Uint8Array(ab);

            // set the bytes of the buffer to the correct values
            for (let i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }

            // write the ArrayBuffer to a blob, and you're done
            return new Blob([ab], {type: mimeString});
        }
        $scope.blobToFile = function(blob, fileName) {
            return new File([blob], fileName, new Date());
        }
    }]);
