// import env from '../../config/env';
import Notice from 'iview/src/components/notice'
import {appRouter} from '../router'
let util = {};
util.title = function (title) {
  title = title || '蜜罐运维平台';
  window.document.title = title;
};

// util.url = 'http://' + document.domain + ':8000/api/v1'
util.url = '/api/v1'

util.auth = '/api-token-auth/'

util.computer_room = ['AWS', 'Aliyun', 'Own', 'Other']
// util.yun_dev = ['Aliyun', 'Meituanyun', 'Huaweiyun']
// util.idc_dev = ['zskx', 'gzIDC']
util.yun_room_list = ['阿里云', '美团云', '华为云']
util.own_room_list = ['独立机房', '广州IDC']
util.yun_area_list = ['华北1', '华北2', '华东1', '华南1']
util.yun_instance_type_list = ['ECS', 'RDS', 'SLB', 'MongDB', 'Redis']

util.ajanxerrorcode = function (vm, error) {
  if (error.response) {
    if (error.response.status === 401) {
      vm.$router.push({name: 'error_401'})
    } else if (error.response.status === 400) {
      Notice.error({title: '警告', desc: '账号密码错误,请重新输入!'})
    } else if (error.response.status === 500) {
      vm.$router.push({name: 'error_500'})
    } else if (error.response.status === 404) {
      vm.$router.push({name: 'error_404'})
    } else {
      Notice.error({title: '警告', desc: error.response})
    }
  }
};

util.showThisRoute = function (itAccess, currentAccess) {
  if (typeof itAccess === 'object' && itAccess.isArray()) {
    return util.oneOf(currentAccess, itAccess);
  } else {
    return itAccess === currentAccess;
  }
};

util.openPage = function (vm, name) {
  vm.$router.push({name: name});
  vm.$store.commit('Breadcrumbset', name)
  vm.$store.state.currentPageName = name
  util.taglist(vm, name)
};

util.taglist = function (vm, name) {
  vm.$store.state.pageOpenedList.forEach((vl, index) => {
    if (vl.name === name) {
      vm.$store.state.pageOpenedList.splice(index, 1)
    }
  })

  appRouter.forEach((val) => {
    for (let i of val.children) {
      if (i.name === name) {
        vm.$store.state.pageOpenedList.push({'title': i.title, 'name': i.name})
      }
    }
  })
  localStorage.setItem('pageOpenedList', JSON.stringify(vm.$store.state.pageOpenedList))
}

export default util;
