/**
 * Created by Administrator on 2015/1/15.
 */
var app = angular.module('blacapp', ['ui.router', 'blac-util', 'ui.tree']);

app.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/login"); // For any unmatched url, redirect.
  $stateProvider
    .state('login', {
      url: "/login",
      templateUrl: "partials/login.html"
    })
    .state('acadmin', {
      url: "/acadmin",
      templateUrl: "partials/acadminleft.html"
    })
    .state('acadmin.cover', {
      url: "/cover",
      templateUrl: "partials/acadmincover.html",
      controller: function($scope) {
          $scope.items = ["acAc", "Listac", "acOf", "acItems"];
      }
    })
    .state('acadmin.word', {
      url: "/word",
      templateUrl: "partials/acadminword.html",
      controller:function($scope, blacStore, blacAccess){
        $scope.saveWord = function(){
          if ($scope.newword == $scope.confirmword && $scope.newword != $scope.oldword)  {
            blacAccess.userChange(blacStore.localUser(), $scope.oldword, $scope.newword).then(
              function(data){ if (data.rtnCode ==1) window.alert("更改成功"); else window.alert("保存失败"); }
            );
          }
        }
      }
    })
    .state('acadmin.selflist', {
      url: "/selflist/:nodeId",
      templateUrl: "partials/acadmincolselfedit.html"
    })
    .state('acadmin.listart', {
      url: "/listart/:columnId/:linkPrefix",
      templateUrl: "partials/acadminlistart.html"
    })
    .state('acadmin.user', {
      url: "/listuser",
      templateUrl: "partials/acadminlistuser.html"
    })
    .state('extools', {
      url: "/extools",
      templateUrl: "partials/exTools.html"
    }) ;
});
app.controller("ctrlExtools",function($scope,blacAccess,blacUtil){
  var lp = $scope;
  lp.md5String = blacUtil.md5String;

  lp.postReq = function() {
    var l_param = { sql: lp.txtReq, word: blacUtil.md5String(lp.addPass) };
    blacAccess.extoolsPromise(l_param)
      .then(function (aRtn) {
        lp.txtReturn = JSON.stringify(aRtn);
      },
      function (err) {
        lp.txtReturn = JSON.stringify(err);
      }
    );
  }
});
app.controller("ctrlAdminTop",function($location,$scope,blacStore,blacAccess) {
  var lp = $scope;
  lp.loginedUser = blacStore.localUser();
  lp.$on(blacAccess.gEvent.login, function(){
    lp.loginedUser = blacStore.localUser();
  });
  lp.$on(blacAccess.gEvent.broadcast, function(event, aInfo){
    lp.broadInfo = aInfo;
  });
  lp.logout = function(){
    lp.loginedUser = null
    blacAccess.userLogOutQ().then( function(data) {
        $location.path('/login')
    }, function (error) {  lp.rtnInfo = JSON.stringify(error); });
  }

});
app.controller("ctrlLogin",function($rootScope,$scope,$location,blacStore,blacAccess) {
  var lp = $scope;
  lp.rtnInfo = "";
  lp.lUser = {rem:blacStore.localRem(), username:blacStore.localUser(), pw:blacStore.localWord()  };

  lp.userLogin = function () {
    blacAccess.userLoginQ(lp.lUser).then( function(data) {
      if (data.rtnCode > 0) {
        blacStore.localUser(lp.lUser.username);
        blacStore.localWord(lp.lUser.pw);
        blacStore.localRem(lp.lUser.rem);
        $rootScope.$broadcast(blacAccess.gEvent.login);
        $location.path('/acadmin/cover');
      }
      else{
        lp.rtnInfo = data.rtnInfo;
      }
    }, function (error) {  lp.rtnInfo = JSON.stringify(error); });
  };
});
app.controller("ctrlAdminLeft", function($scope,blacUtil,blacStore,blacAccess,$location,$http) {
  var lp = $scope;

  lp.isAdmin = blacStore.localUser() == "Admin"? true : false;

  // 后台管理端：栏目设置。
  {
    lp.treeData = [{"id":0,"title":"根","items":[], deleteId:[]}];
    lp.wrapConfirm = blacUtil.wrapConfirm;

    lp.initColumDefTree = function() {
      blacAccess.getAdminColumn({type:"admin"}).then(   // 管理员设置录入。
        function (data) {
          if (data.rtnCode == 1) lp.treeData[0].items = data.exObj.columnTree.items;
            else console.log(data);
        }, function (data) {
            console.log(data);
        });
    };
    lp.wrapRemove = function (aNode) {
      var nodeData = aNode.$modelValue;
      if (nodeData.id == 0) return;
      if (window.confirm("确认删除他和所有的子记录么？"))
        if (blacAccess.getDataState(nodeData) == blacAccess.dataState.new)
          aNode.remove();
        else {
          lp.treeData[0].deleteId.push(nodeData.id);
          aNode.remove();
        }

    };
    lp.newSubItem = function (aNode) {
      var nodeData = aNode.$modelValue;
      if (aNode.collapsed) { // console.log('when insert into a colapsed node, should expand it.');
        aNode.expand();
      };
      var l_tmp = { id: blacUtil.createUUID(), // nodeData.id * 10 + nodeData.items.length,
        parent_id: nodeData.id,
        title: '新节点', // nodeData.title + '.' + (nodeData.items.length + 1),
        items: []
      };
      blacAccess.setDataState(l_tmp, blacAccess.dataState.new);
      nodeData.items.push(l_tmp);
    };
    lp.nodeClick = function (aNode) {
      if (aNode.$modelValue.id == 0) return;
      lp.clickNode = aNode.$modelValue;
      $location.path('/acadmin/selflist/' + lp.clickNode.id);
    };
    lp.nodeTitleChanged = function (aCurNode) {
      if (blacAccess.getDataState(aCurNode) != blacAccess.dataState.new) blacAccess.setDataState(aCurNode, blacAccess.dataState.dirty);
    };
    lp.treeExpandAll = function(){
      angular.element(document.getElementById("tree-root")).scope().expandAll();
    };
    lp.saveTree = function(){
      blacAccess.setAdminColumn( lp.treeData[0]).then(
        function (data) {
          if (data.rtnCode == 1) {
            console.log('save ok. ');
            lp.initColumDefTree();
          }
          else console.log(data);
        },
        function (data) {
          console.log(data);
        });
    }
    lp.treeExpandCol = function(){
      angular.element(document.getElementById("tree-content-root")).scope().expandAll();
    }
  }

  // 后台管理端：  用户录入内容。
  {
    blacAccess.getAdminColumn({type:"user"}).then(
      function (data) {
          console.log(data);
        if (data.rtnCode == 1) lp.treeContentData = data.exObj.columnTree.items;
        else console.log(data);
      },
      function (err) {
        console.log(err);
      });
    // 点击用户栏目，列出下级文章。
    lp.clickContentNode = { id: 0 };  // init;

    lp.clickCol4ConList = function (aNode) {
      if (aNode.$modelValue.id == 0) return;
      if (lp.clickContentNode.id != aNode.$modelValue.id) {
        lp.clickContentNode = aNode.$modelValue;
        lp.psContentInfo = { pageCurrent: 1, pageRows: 10, pageTotal: 0  };
        $location.path('/acadmin/listart/' + lp.clickContentNode.id + "/" + window.btoa(lp.clickContentNode.link));
      }
    };
  }
});
app.controller("ctrlAdminListArt", function($scope,blacUtil,blacAccess,blacStore,blacPage,$window,$location,$http,$stateParams) {
  var lp = $scope;
  var lColumnId = $stateParams.columnId;
  lp.linkPrefix = window.atob($stateParams.linkPrefix);
  var lEditorId = "uEditor";
  lp.clickContentNode = { id : 0 };  // init;

  // 查询。
  lp.psContentInfo = { pageCurrent: 1, pageRows: 10, pageTotal: 0  }; // init;
  lp.contentList = [];
  lp.psGetContent = function (aOffset) {
    blacPage.psGetContent(blacAccess.getArticleList,[lp.psContentInfo, lColumnId], aOffset
      ,function(aErr, aRtn){
        lp.contentList = aRtn.exObj.contentList;
        lp.psContentInfo = aRtn.psInfo;
        lp.contentHasLast = (lp.psContentInfo.pageCurrent == lp.psContentInfo.pageTotal)?false:true;
        lp.contentHasPrior = (lp.psContentInfo.pageCurrent == 1)?false:true;
      });
  };

  // 编辑和录入内容
  lp.singArticle = {};
  lp.closeArticle = function(){
    $('#myModal').modal('toggle');
  };
  lp.editArticle = function(aArg){
    if (aArg == -1 ) {  // 在当前的父栏目下面增加新的内容。
      lp.singArticle = {id: blacUtil.createUUID(), parent_id:lColumnId, kind:"", title:"", content:"",
        imglink:"", videolink:"", recname:blacStore.localUser(), rectime:blacUtil.strDateTime()};
      blacAccess.setDataState(lp.singArticle, blacAccess.dataState.new);
      UE.getEditor(lEditorId).setContent('');
    }
    else {  // 根据点击的articleID，搞到他的内容。
      blacAccess.getArticleCont(aArg).then(
        function(data){
          if (data.rtnCode == 1) {
            lp.singArticle = data.exObj.article;
             UE.getEditor(lEditorId).setContent(lp.singArticle.content); // 获得uEditor的内容。保存到数据字段。
          }
          else console.log("竟然会没有这个id？");
        }
      );
    };
    $('#myModal').modal( { backdrop: "static" } );
  };
  lp.saveArticle = function(){
    // 如果是增加，就增加到 lp.contentList 的最前面。如果是edit，就直接更新。
    // 远程保存成功否？

    lp.singArticle.content = UE.getEditor(lEditorId).getContent(); // 获得uEditor的内容。保存到数据字段。
    if (blacAccess.getDataState(lp.singArticle) != blacAccess.dataState.new) blacAccess.setDataState(lp.singArticle, blacAccess.dataState.dirty);// 设置保存。

    blacAccess.setArticleCont(lp.singArticle).then(
      function(data){
        if (data.rtnCode == 1){
          if (blacAccess.getDataState(lp.singArticle) == blacAccess.dataState.new) {
            blacAccess.setDataState(lp.singArticle, blacAccess.dataState.clean);
            lp.contentList.unshift(lp.singArticle);
          }
          else{
            for (i=0;i<lp.contentList.length;i++){
              if (lp.singArticle.id ==lp.contentList[i].id ) {
                lp.contentList[i] = lp.singArticle;
                break;
              }
            }
          }
          lp.closeArticle();
        }
        else{
          if (data.alertType == 1) alert(data.rtnInfo);
        }
      }
    )
  };
  lp.deleteArticle = function(){
    if (blacAccess.getDataState(lp.singArticle) == blacAccess.dataState.new) { // 直接删掉
      lp.singArticle = {};
    }
    else {
      blacAccess.deleteArticleCont(lp.singArticle.id).then(
        function(data){
          if (data.rtnCode == 1){
            for (i=0;i<lp.contentList.length;i++){
              if (lp.singArticle.id ==lp.contentList[i].id ) {
                lp.contentList.splice(i, 1);
                break;
              }
            }
          }
        }
      );
    }
    lp.closeArticle();
  };

  // 默认显示第一页。
  lp.psGetContent(1);

});
app.controller("ctrlAdminListUser", function($scope,blacAccess,blacPage,blacUtil) {
  var lp = $scope;
  lp.wrapConfirm = blacUtil.wrapConfirm;
  lp.clickContentNode = { id : 0 };  // init;
  // 查询。
  lp.psContentInfo = { pageCurrent: 1, pageRows: 10, pageTotal: 0  }; // init;
  lp.contentList = []; // user list
  lp.psGetContent = function (aOffset) {
    blacPage.psGetContent(blacAccess.getUserList,[lp.psContentInfo], aOffset
      ,function(aErr, aRtn){
        lp.contentList = aRtn.exObj.userList;
        lp.psContentInfo = aRtn.psInfo;
        lp.contentHasLast = (lp.psContentInfo.pageCurrent == lp.psContentInfo.pageTotal)?false:true;
        lp.contentHasPrior = (lp.psContentInfo.pageCurrent == 1)?false:true;
        if (lp.contentList) blacAccess.setDataState(lp.contentList, blacAccess.dataState.clean); else lp.contentList = [];
      });
  };
  lp.singleRec = {username:"newUser", pw: "", usertype:""};

  lp.addRecord = function(){
    lp.singleRec = {username:"newUser", pw:"", usertype:"norm"};
    $('#userModal').modal( { backdrop: "static" } );
  };

  lp.saveRecord = function(){
    var lAdd = { username:lp.singleRec.username, pw: blacUtil.md5String(lp.singleRec.username + lp.singleRec.pw),
                  usertype:lp.singleRec.usertype   };
    blacAccess.setDataState(lAdd, blacAccess.dataState.new);
    console.log(lAdd);
    blacAccess.setUserCont(lAdd).then(   // here we go . not finished
      function(data){
        if (data.rtnCode == 1){
          lp.contentList.unshift(lp.singleRec);
          blacAccess.setDataState(lp.singleRec, blacAccess.dataState.clean );
          lp.closeRec();
        }
      }
    )

  };
  lp.deleteRec = function(aName) {
    console.log('del',aName);
    for (var i = 0; i < lp.contentList.length; i++)
      if (lp.contentList[i].username == aName) {
        if (blacAccess.getDataState(lp.contentList[i]) == blacAccess.dataState.new) { // 直接删掉
          lp.contentList.splice(i, 1);
        }
        else {
          blacAccess.deleteUserCont(aName).then(
            function (data) {
              if (data.rtnCode == 1) {
                lp.contentList.splice(i, 1);
              }
            }
          );
        }
        break;
      }
  };
  lp.closeRec = function(){
    $('#userModal').modal('toggle');
  };
  // 默认显示第一页。
  lp.psGetContent(1);

});

