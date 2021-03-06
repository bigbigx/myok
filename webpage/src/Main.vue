<style lang="less">
@import "./main.less";
</style>
<template>
<div id="main" class="main" :class="{'main-hide-text': hideMenuText}">
  <div class="sidebar-menu-con" :style="{width: hideMenuText?'60px':'200px', overflow: hideMenuText ? 'visible' : 'auto', background: $store.state.menuTheme === 'dark'?'#495060':'white'}">
    <div class="logo-con">
    </div>
    <sidebar-menu v-if="!hideMenuText" :menuList="menuList" :iconSize="14" />
    <sidebar-menu-shrink :icon-color="menuIconColor" v-else :menuList="menuList" />
  </div>
  <div class="main-header-con" :style="{paddingLeft: hideMenuText?'60px':'200px'}">
    <div class="main-header">
      <div class="navicon-con">
        <Button :style="{transform: 'rotateZ(' + (this.hideMenuText ? '-90' : '0') + 'deg)'}" type="text" @click="toggleClick">
            <Icon type="navicon" size="32"></Icon>
          </Button>
      </div>
      <div class="header-middle-con">
        <div class="main-breadcrumb">
          <breadcrumb-nav :currentPath="currentPath"></breadcrumb-nav>
        </div>
      </div>
      <div class="header-avator-con">

        <div @click="handleFullScreen" v-if="showFullScreenBtn" class="full-screen-btn-con">
          <Tooltip :content="isFullScreen ? '退出全屏' : '全屏'" placement="bottom">
            <Icon :type="isFullScreen ? 'arrow-shrink' : 'arrow-expand'" :size="23"></Icon>
          </Tooltip>
        </div>
        <div @click="lockScreen" class="lock-screen-btn-con">
          <Tooltip content="锁屏" placement="bottom">
            <Icon type="locked" :size="20"></Icon>
          </Tooltip>
        </div>
        <div @click="showMessage" class="message-con">
          <Tooltip :content="messageCount > 0 ? '有' + messageCount + '条未读消息' : '无未读消息'" placement="bottom">
            <Badge :count="messageCount" dot>
              <Icon type="ios-bell" :size="22"></Icon>
            </Badge>
          </Tooltip>
        </div>
        <div class="switch-theme-con">
          <Row class="switch-theme" type="flex" justify="center" align="middle">
            <theme-dropdown-menu></theme-dropdown-menu>
          </Row>
        </div>
        <div class="user-dropdown-menu-con">
          <Row type="flex" justify="end" align="middle" class="user-dropdown-innercon">
            <Dropdown trigger="click" @on-click="handleClickUserDropdown">
              <a href="javascript:void(0)">
                  <span class="main-user-name">{{ userName }}</span>
                  <Icon type="arrow-down-b"></Icon>
                </a>
              <DropdownMenu slot="list">
                <DropdownItem name="ownSpace">个人中心</DropdownItem>
                <DropdownItem name="loginout" divided>退出登录</DropdownItem>
              </DropdownMenu>
            </Dropdown>
            <Avatar :src="avatorPath" style="background: #ffffff;margin-left: 10px;"></Avatar>
          </Row>
        </div>
      </div>
    </div>
    <div class="tags-con">
      <tags-page-opened :pageTagsList="pageTagsList"></tags-page-opened>
    </div>
  </div>
  <div class="single-page-con" :style="{paddingLeft: hideMenuText?'60px':'200px'}">
    <div class="single-page">
      <router-view></router-view>
    </div>
  </div>
</div>
</template>
<script>
import sidebarMenu from './main_components/sidebarMenu.vue';
import tagsPageOpened from './main_components/tagsPageOpened.vue';
import breadcrumbNav from './main_components/breadcrumbNav.vue';
import themeDropdownMenu from './main_components/themeDropdownMenu.vue';
import sidebarMenuShrink from './main_components/sidebarMenuShrink.vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import util from './libs/util.js';
export default {
  components: {
    sidebarMenu,
    tagsPageOpened,
    breadcrumbNav,
    themeDropdownMenu,
    sidebarMenuShrink
  },
  data () {
    return {
      spanLeft: 4,
      spanRight: 20,
      currentPageName: '',
      hideMenuText: false,
      userName: Cookies.get('user'),
      showFullScreenBtn: window.navigator.userAgent.indexOf('MSIE') < 0,
      isFullScreen: false,
      lockScreenSize: 0,
      avatorPath: 'static/bird-fast-v2.png'
    };
  },
  computed: {
    menuList () {
      return this.$store.state.menuList;
    },
    pageTagsList () {
      return this.$store.state.pageOpenedList; // 打开的页面的页面对象
    },
    currentPath () {
      return this.$store.state.currentPath; // 当前面包屑数组
    },
    menuIconColor () {
      return this.$store.state.menuTheme === 'dark' ? 'white' : '#495060';
    },
    messageCount () {
      return this.$store.state.messageCount
    }
  },
  methods: {
    // 导航栏收缩
    toggleClick () {
      this.hideMenuText = !this.hideMenuText;
    },
    // 个人中心
    handleClickUserDropdown (name) {
      if (name === 'ownSpace') {
        util.openPage(this, 'ownspace_index', '个人中心');
      } else if (name === 'loginout') {
        // 退出登录
        Cookies.remove('user');
        Cookies.remove('password');
        Cookies.remove('hasGreet');
        Cookies.remove('access');
        localStorage.clear()
        this.$router.push({
          name: 'login'
        });
      }
    },
    // 全屏
    handleFullScreen () {
      let main = document.getElementById('main');
      if (this.isFullScreen) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      } else {
        if (main.requestFullscreen) {
          main.requestFullscreen();
        } else if (main.mozRequestFullScreen) {
          main.mozRequestFullScreen();
        } else if (main.webkitRequestFullScreen) {
          main.webkitRequestFullScreen();
        } else if (main.msRequestFullscreen) {
          main.msRequestFullscreen();
        }
      }
    },
    // 消息中心
    showMessage () {
      util.openPage(this, 'message_index', '消息中心');
    },
    // 锁屏
    lockScreen () {
      let lockScreenBack = document.getElementById('lock_screen_back');
      lockScreenBack.style.transition = 'all 3s';
      lockScreenBack.style.zIndex = 10000;
      lockScreenBack.style.boxShadow = '0 0 0 ' + this.lockScreenSize + 'px #667aa6 inset';
      this.showUnlock = true;
      this.$store.commit('lock');
      Cookies.set('last_page_name', this.$route.name); // 本地存储锁屏之前打开的页面以便解锁后打开
      setTimeout(() => {
        lockScreenBack.style.transition = 'all 0s';
        this.$router.push({
          name: 'locking'
        });
      }, 800);
    },
    init () {
      // 全屏相关
      document.addEventListener('fullscreenchange', () => {
        this.isFullScreen = !this.isFullScreen;
      });
      document.addEventListener('mozfullscreenchange', () => {
        this.isFullScreen = !this.isFullScreen;
      });
      document.addEventListener('webkitfullscreenchange', () => {
        this.isFullScreen = !this.isFullScreen;
      });
      document.addEventListener('msfullscreenchange', () => {
        this.isFullScreen = !this.isFullScreen;
      });
      // 锁屏相关
      let lockScreenBack = document.getElementById('lock_screen_back');
      let x = document.body.clientWidth;
      let y = document.body.clientHeight;
      let r = Math.sqrt(x * x + y * y);
      let size = parseInt(r);
      this.lockScreenSize = size;
      window.addEventListener('resize', () => {
        let x = document.body.clientWidth;
        let y = document.body.clientHeight;
        let r = Math.sqrt(x * x + y * y);
        let size = parseInt(r);
        this.lockScreenSize = size;
        lockScreenBack.style.transition = 'all 0s';
        lockScreenBack.style.width = lockScreenBack.style.height = size + 'px';
      });
      lockScreenBack.style.width = lockScreenBack.style.height = size + 'px';
      // 问候信息相关
      if (!Cookies.get('hasGreet')) {
        let now = new Date();
        let hour = now.getHours();
        let greetingWord = {
          title: '',
          words: ''
        };
        let userName = Cookies.get('user');
        if (hour < 6) {
          greetingWord = {
            title: '凌晨好~' + userName,
            words: '早起的鸟儿有虫吃~'
          };
        } else if (hour >= 6 && hour < 9) {
          greetingWord = {
            title: '早上好~' + userName,
            words: '来一杯咖啡开启美好的一天~'
          };
        } else if (hour >= 9 && hour < 12) {
          greetingWord = {
            title: '上午好~' + userName,
            words: '工作要加油哦~'
          };
        } else if (hour >= 12 && hour < 14) {
          greetingWord = {
            title: '中午好~' + userName,
            words: '午饭要吃饱~'
          };
        } else if (hour >= 14 && hour < 17) {
          greetingWord = {
            title: '下午好~' + userName,
            words: '下午也要活力满满哦~'
          };
        } else if (hour >= 17 && hour < 19) {
          greetingWord = {
            title: '傍晚好~' + userName,
            words: '下班没事问候下爸妈吧~'
          };
        } else if (hour >= 19 && hour < 21) {
          greetingWord = {
            title: '晚上好~' + userName,
            words: '工作之余品一品书香吧~'
          };
        } else {
          greetingWord = {
            title: '深夜好~' + userName,
            words: '夜深了，注意休息哦~'
          };
        }
        this.$Notice.config({
          top: 130
        });
        this.$Notice.info({
          title: greetingWord.title,
          desc: greetingWord.words,
          duration: 4,
          name: 'greeting'
        });
        Cookies.set('hasGreet', 1);
      }
    }
  },
  mounted () {
    this.$store.commit('Breadcrumbset', this.$route.matched[1].name)
    this.$store.state.currentPageName = this.$route.matched[1].name
    if (localStorage.getItem('pageOpenedList')) {
      this.$store.state.pageOpenedList = JSON.parse(localStorage.getItem('pageOpenedList'))
    } else {
      this.$store.state.pageOpenedList = [{
        title: '首页',
        path: '',
        name: 'home_index'
      }]
    }
    this.init()
    axios.get(`${util.url}/homedata/messages?username=${Cookies.get('user')}`)
      .then(res => {
        this.$store.state.messageCount = res.data.messagecount
      })
  },
  created () {
    // 权限菜单过滤相关
    this.$store.commit('Menulist');
    axios.defaults.headers.common['Authorization'] = Cookies.get('jwt')
  }
};
</script>
