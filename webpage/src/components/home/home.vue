<style lang="less">
@import "./home.less";
@import "../../styles/common.less";
.fuc {}

.fuc li {
    margin-top: 2%;
    margin-left: 15%;
}

.fuc h4 {
    margin-top: 2%;
    margin-left: 10%;
}
.fuc h3 {
    }
</style>
<template>
<div class="home-main">
  <Row>
    <Col span="8">
    <Row>
      <Card>
        <Row type="flex" class="user-infor">
          <Col span="8">
          <Row class-name="made-child-con-middle" type="flex" align="middle">
            <img class="avator-img" src="../../assets/bird-fast-v2.png" />
          </Row>
          </Col>
          <Col span="16" style="padding-left:6px;">
          <Row class-name="made-child-con-middle" type="flex" align="middle">
            <div>
              <b class="card-user-infor-name">{{username}}</b>
              <p>It's a nice day .</p>
            </div>
          </Row>
          </Col>
        </Row>
        <div class="line-gray"></div>
        <Row class="margin-top-8">
          <Col span="8">
          <p class="notwrap">登陆时间:</p>
          </Col>
          <Col span="16" class="padding-left-8">{{time}}</Col>
        </Row>
      </Card>
    </Row>
    <Row class="margin-top-10">
      <Card>
        <p slot="title" class="card-title">
          <Icon type="android-checkbox-outline"></Icon>
          ToDo List
        </p>
        <a type="text" slot="extra" @click.prevent="addNewToDoItem">
          <Icon type="plus-round"></Icon>
        </a>
        <Modal v-model="showAddNewTodo" title="添加新的待办事项" @on-ok="addNew" @on-cancel="cancelAdd">
          <Row type="flex" justify="center">
            <Input v-model="newToDoItemValue" icon="compose" placeholder="请输入..." style="width: 300px" />
          </Row>
          <Row slot="footer">
            <Button type="text" @click="cancelAdd">取消</Button>
            <Button type="primary" @click="addNew">确定</Button>
          </Row>
        </Modal>
        <div class="to-do-list-con">
          <div v-for="(item, index) in toDoList" :key="index" class="to-do-item">
            <to-do-list-item :content="item.title" @deltodo="deltodo"></to-do-list-item>
          </div>
        </div>
      </Card>
    </Row>
    </Col>

  </Row>
</div>
</template>

<script>
import axios from 'axios'
import util from '../../libs/util'
import Cookies from 'js-cookie'
import dataSourcePie from './components/dataSourcePie.vue';
import inforCard from './components/inforCard.vue';
import toDoListItem from './components/toDoListItem.vue';
export default {
  components: {
    dataSourcePie,
    inforCard,
    toDoListItem
  },
  data () {
    return {
      toDoList: [{
        title: ''
      }],
      count: {
        createUser: 0,
        order: 0,
        link: 0,
        dic: 0
      },
      showAddNewTodo: false,
      newToDoItemValue: '',
      username: Cookies.get('user'),
      time: '',
      board: {
        'title': ['1.SQL可视化自动生成', '2.数据库字典', '3.SQL审核', '4.流程化工单']
      }
    };
  },
  methods: {
    addNewToDoItem () {
      this.showAddNewTodo = true;
    },
    formatDate () {
      let date = new Date();
      let year = date.getFullYear();
      let month = date.getMonth() + 1;
      let day = date.getDate();
      let hour = date.getHours();
      let minute = date.getMinutes();
      let second = date.getSeconds();
      this.time = year + '/' + month + '/' + day + '  ' + hour + ':' + minute + ':' + second;
    },
    addNew () {
      if (this.newToDoItemValue.length !== 0) {
        axios.post(`${util.url}/homedata/todolist/`, {
            'username': Cookies.get('user'),
            'todo': this.newToDoItemValue
          })
          .then(() => {
            this.toDoList.unshift({
              title: this.newToDoItemValue
            });
            setTimeout(function () {
              this.newToDoItemValue = '';
            }, 200);
            this.showAddNewTodo = false;
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      } else {
        this.$Message.error('请输入待办事项内容');
      }
    },
    cancelAdd () {
      this.showAddNewTodo = false;
      this.newToDoItemValue = '';
    },
    deltodo (val) {
      axios.put(`${util.url}/homedata/deltodo`, {
          'username': Cookies.get('user'),
          'todo': val
        })
        .then(() => {
          this.gettodo()
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    gettodo () {
      axios.put(`${util.url}/homedata/todolist`, {
          'username': Cookies.get('user')
        })
        .then(res => {
          this.toDoList = res.data
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  },
  mounted () {
    axios.get(`${util.url}/homedata/infocard`)
      .then(res => {
        this.count.dic = res.data[0].dic_number
        this.count.createUser = res.data[1].user
        this.count.order = res.data[2].order
        this.count.link = res.data[3].link
      })
      .catch(error => {
        util.ajanxerrorcode(this, error)
      })
    this.gettodo()
    this.formatDate()
  }
};
</script>
