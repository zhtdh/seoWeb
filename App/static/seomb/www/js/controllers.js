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
          lo_json = {"fun":"typelist", "exp": aType};
          break;
        case 'contact':
        case 'corpinfo':
          lo_json = {"fun":"getfirst", "exp": aType};
          break;
        case 'artlist':     // aEx = { pid: xxx, loc :{"pn":1,"pr":10,"pall":0} }
          if (aEx.pid == 'custom') aEx.pid = 'C67B827ABA30000162DB157B90C560';
          lo_json = {"fun":"artlist", "exp": aEx };
          break;
        case 'getart':     // aEx = {pid: xxx }
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

  $scope.article = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/singArticle.html', {
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

  var lp = $scope;
  lp.showArticle = function(aId){
    blacAccess.getJsonp('getart', { pid:aId } )
      .then(function (aRtn) {
        if( aRtn.exObj.data.length > 0) {
          $scope.article = aRtn.exObj.data[0];
          $scope.modal.show(); }
        else
          alert('数据检索失败。')
      },
      function (err) {
        console.log('err', err)
        alert('访问服务器失败。')
      })
  }

  lp.$on("showArticle", function(event, aInfo){
    console.log('get broadcast ', event, aInfo);
    lp.showArticle(aInfo);

  });

})

.controller('topCtrl', function($rootScope, $scope, $state) {
    $scope.clickDiv = function(aArg){
      // alert(aArg)
      switch(aArg) {
        case 1: // 公司
          $state.go('app.atype', { atype : 'corp' });
          break;
        case 2:
          $state.go('app.atype', { atype : 'product' });
          break;
        case 3:
          $state.go('app.atype', { atype : 'industry' });
          break;
        case 4:
          $state.go('app.artlist', { atype : 'custom' });
          break;
        case 5:
          $rootScope.$broadcast('showArticle', 'C6843ABD76400001A9521DC180BF30')
          break;
      }
    };
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
    blacAccess.getJsonp('artlist', {pid:lType, loc:lp.loc} )
      .then(function (aRtn) {
        lp.txtReturn = JSON.stringify( aRtn.rtnInfo );
        Array.prototype.push.apply(lp.artLists, aRtn.exObj.data)
        lp.loc.pa = aRtn.exObj.loc.pa;
        if (lp.loc.pa < (lp.loc.pn * lp.loc.pr)) lp.nomore = true; else lp.nomore = false;
      },
      function (err) {
        lp.txtReturn = JSON.stringify(err);
      }
    );
  }
  // 如果是公司简介的话，就直接不用列出来。
  lp.getMore();
})
;
