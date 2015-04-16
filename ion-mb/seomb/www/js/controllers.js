app = angular.module('starter.controllers', []);

app.factory('blacAccess', function($http,$q){

    var getJsonp = function(aType, aEx){
      var deferred = $q.defer();
      var ls_url = 'http://127.0.0.1:8000/mbjp/?callback=JSON_CALLBACK';
      var lo_json = {};  // var lo_json = {"fun":"typelist", "type": lType, "loc":{"pn":1,"pr":10,"pall":0} };
      switch(aType)
      {
        case 'corp':       // ,corp-1,
        case 'product':    // ,corp-1,
        case 'industry':   // ,corp-1,
        case 'custom':     // ,corp-1,
          lo_json = {"fun":"typelist", "exp": aType};
          break;
        case 'contact':
        case 'corpinfo':
          lo_json = {"fun":"getfirst", "exp": aType};
          break;

        case 'artlist':     // aEx = {pid: xxx, loc :{"pn":1,"pr":10,"pall":0} }
          lo_json = {"fun":"artlist", "exp": aEx };
          break;
        case 'article':     // aEx = {pid: xxx }
          lo_json = {"fun":"getart", "exp": aEx};
          break;
        default:
          break;
      }

      $http.jsonp(ls_url + '&&jpargs=' + JSON.stringify(lo_json))
        .success(function (data, status, headers, config) {
          console.log('sucess', data);
          deferred.resolve(data || []);
        })
        .error(function (data, status, headers, config) {
          console.log('fail', data);
          deferred.reject(data);
        });

      return deferred.promise;
    }

    return {
      getJsonp: getJsonp  // getJsonp('data').then(function(data){}, function(err){})
    } ;
  });

app.controller('AppCtrl', function($scope, blacAccess, $ionicModal, $timeout) {
  // Form data for the login modal
  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('topCtrl', function($scope) {
    $scope.clickDiv = function(aArg){alert(aArg) };
})

.controller('typeListCtrl', function($scope, blacAccess, $stateParams, $http) {

  var lType = $stateParams.atype;
  var lp = $scope;
  lp.typeLists = [];

  blacAccess.getJsonp(lType)
    .then(function (aRtn) {
      lp.txtReturn = JSON.stringify( aRtn.rtnInfo );
      lp.typeLists = aRtn.exObj.data;
    },
    function (err) {
      lp.txtReturn = JSON.stringify(err);
    }
  );
})

.controller('artListCtrl', function($scope, blacAccess, $stateParams, $http) {

  var lType = $stateParams.atype;  // articletype 's id.
  var lp = $scope;
  lp.artLists = [];
  lp.loc = {pn:0, pr:10, pa:-1 };
  lp.nomore = false;

  lp.getMore = function(){
    lp.loc.pn = lp.loc.pn + 1;
    blacAccess.getJsonp(lType, {pid:lType, loc:lp.loc} )
      .then(function (aRtn) {
        lp.txtReturn = JSON.stringify( aRtn.rtnInfo );
        lp.artLists.concat(aRtn.exObj.data);
        lp.loc.pa = aRtn.exObj.loc.pa;
        if (lp.loc.pa < (lp.loc.pn * lp.loc.pr)) lp.nomore = false; else lp.nomore = true;
      },
      function (err) {
        lp.txtReturn = JSON.stringify(err);
      }
    );
  }



})

.controller('PlaylistCtrl', function($scope, $stateParams) {


});
