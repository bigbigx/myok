<style>
.Menu span {
  color: #ffffff;
  font-weight: bold;
  margin-left: 10%;
}

.MenuIcon {
  margin-left: 10%;
  margin-top: 0.1%;
  color: #5cadff;
}
</style>
<template>
<Menu width="auto" :theme="theme" @on-select="currentPageTab" :active-name="currentPageName" accordion>
  <MenuItem name="main">
  <Icon type="cube" size="50" class="MenuIcon"></Icon>
  <br>
  <span>蜜罐运维平台</span>
  </MenuItem>
  <MenuItem name="home_index">
  <Icon type="home" :size="iconSize"></Icon>
  <span class="layout-text">首页</span>
  </MenuItem>
  <template v-for="item in menuList">
      <Submenu v-if="item.children.length>=1 && item.name !== 'main'" :name="item.name" :key="item.path">
        <template slot="title">
          <Icon :type="item.icon" :size="iconSize"></Icon>
          <span class="layout-text">{{ item.title }}</span>
        </template>
        <template v-for="child in item.children">
          <MenuItem :name="child.name" :key="child.name" style="margin-left: -5%">
            <Icon :type="child.icon" :size="iconSize" :key="child.name"></Icon>
            <span class="layout-text" :key="child.name">{{ child.title }}</span>
          </MenuItem>
        </template>
  </Submenu>
  </template>
  <Menu-item name="login">
    <Icon type="log-out" :size="iconSize"></Icon>
    <span class="layout-text">退出</span>
  </Menu-item>
</Menu>
</template>
<script>
import Cookies from 'js-cookie'
import util from '../libs/util'
export default {
  name: 'sidebarMenu',
  props: {
    menuList: Array,
    iconSize: Number
  },
  computed: {
    theme () {
      return this.$store.state.menuTheme
    },
    currentPageName () {
      return this.$store.state.currentPageName
    }
  },
  methods: {
    currentPageTab (val) {
      if (val === 'login') {
        Cookies.remove('user');
        Cookies.remove('password');
        Cookies.remove('hasGreet');
        Cookies.remove('access');
        localStorage.clear()
        this.$router.push({
          name: val
        })
      } else {
        util.openPage(this, val)
      }
    }
  },
  mounted () {}
}
</script>
