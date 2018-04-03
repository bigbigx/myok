<style lang="less">
@import '../../styles/common.less';
@import '../Order/components/table.less';
.demo-spin-icon-load {
    animation: ani-demo-spin 1s linear infinite;
}
</style>
<template>
<div>
  <Col span="6">
  <Card>
    <p slot="title">
      <Icon type="load-b"></Icon>
      添加关注文件(日志和配置文件等)
    </p>
    <div class="edittable-testauto-con">
      <Form ref="formValidate" :model="formFileItem" :label-width="100" :rules="ruleInline">
        <Form-item label="机房:" prop="room">
          <Select v-model="formFileItem.computer_room" placeholder="请选择" @on-change="Computer_Room">
            <Option v-for="i in computer_room_set" :key="i" :value="i" >{{i}}</Option>
          </Select>
        </Form-item>
        <Form-item label="机柜或区域:" prop="cabinet">
          <Select v-model="formFileItem.cabinet" placeholder="请选择" @on-change="Cabinet">
            <Option v-for="i in datalist.cabinet_list" :value="i.connection_name" :key="i.connection_name">{{ i.connection_name }}</Option>
          </Select>
        </Form-item>
        <Form-item label="服务器实例:">
          <Select v-model="formFileItem.server_instance" placeholder="请选择" @on-change="Server_instance">
            <Option v-for="item in datalist.server_instance_list" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </Form-item>
        <Form-item label="主机IP:" prop="username">
          <Input v-model="formFileItem.serverip" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="主机名:" prop="username">
          <Input v-model="formFileItem.serverhost" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件标题:" prop="name">
          <Input v-model="formFileItem.file_title" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件路径:" prop="ip">
          <Input v-model="formFileItem.file_path" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件类型:" prop="ip">
          <Select v-model="formFileItem.file_type" placeholder="请选择">
            <Option v-for="type in file_type" :value="type" :key="type">{{ type }}</Option>
          </Select>
        </Form-item>
        <Form-item label="文件备注:" prop="ip">
          <Input v-model="formFileItem.file_remark" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件归属:" prop="ip">
          <Select v-model="formFileItem.file_owner" placeholder="请选择">
            <Option v-for="list in dataset" :value="list" :key="list">{{ list }}</Option>
          </Select>
        </Form-item>
        <p></p>
        <p></p>
        <Button type="info" @click="testlink()">测试连接</Button>
        <Button type="success" @click="add()" style="margin-left: 5%">确定</Button>
        <Button type="warning" @click="del()" style="margin-left: 30%">重填</Button>

      </Form>
    </div>
  </Card>

  </Col>
  <Col span="18" class="padding-left-10">
  <Card>
    <p slot="title">
      <Icon type="ios-crop-strong"></Icon>
      文件配置清单
    </p>
    <div class="edittable-con-1">
      <Table :columns="columns" :data="rowdata" height="550"></Table>
    </div>
    <br>
    <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
  </Card>
  </Col>
  <Modal v-model="delbaseModal" :width="500">
    <h3 slot="header" style="color:#2D8CF0">删除数据库</h3>
    <Form :label-width="100" label-position="right">
      <FormItem label="数据库连接名">
        <Input v-model="delbasename" readonly="readonly"></Input>
      </FormItem>
      <FormItem label="请输入数据库连接名">
        <Input v-model="delconfirmbasename" placeholder="请确认数据库连接名"></Input>
      </FormItem>
    </Form>
    <div slot="footer">
      <Button type="text" @click="delbaseModal = false">取消</Button>
      <Button type="primary" @click="delbaselink">删除</Button>
    </div>
  </Modal>
  <Modal v-model="addDingding" :width="500">
    <h3 slot="header" style="color:#2D8CF0">添加钉钉推送接口</h3>
    <Form :label-width="100" label-position="right">
      <FormItem label="数据库连接名">
        <Input v-model="dingname" readonly="readonly"></Input>
      </FormItem>
      <FormItem label="钉钉Webhook:">
        <Input v-model="dingurl"></Input>
      </FormItem>
      <FormItem label="提交工单推送的消息内容:">
        <Input v-model="dingdingbeforetext" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
      </FormItem>
      <FormItem label="审核成功后推送的消息内容:">
        <Input v-model="dingdingaftertext" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
      </FormItem>
    </Form>
    <div slot="footer">
      <Button type="text" @click="addDingding = false">取消</Button>
      <Button type="primary" @click="savedingding()">添加</Button>
    </div>
  </Modal>
</div>
</template>
<script>
import '../../assets/tablesmargintop.css'
import axios from 'axios'
import util from '../../libs/util'
import ICol from '../../../node_modules/iview/src/components/grid/col'
export default {
  components: {
    ICol
  },
  name: 'sqlist',
  data () {
    return {
      columns: [
        {
          title: '文件标题',
          key: 'file_title'
        },
        {
          title: '文件类型',
          key: 'file_type'
        },
        {
          title: '主机名',
          key: 'serverhost'
        },
        {
          title: '主机IP',
          key: 'serverip'
        },
        {
          title: '文件路径',
          key: 'file_path'
        },
        {
          title: '文件归属',
          key: 'file_owner'
        },
        {
          title: '操作',
          key: 'action',
          width: 120,
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  size: 'small',
                  type: 'info'
                },
                on: {
                  click: () => {
                    this.edit_tab(params.index)
                  }
                }
              }, '查看信息'),
              h('Button', {
                style: {
                  marginLeft: '8px'
                },
                props: {
                  type: 'warning',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.delFile(params.index)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      rowdata: [],
      modal: false,
      // 添加数据库信息
      formFileItem: {
        computer_room: '',
        cabinet: '',
        server_instance: '',
        serverip: '',
        serverhost: '',
        file_title: '',
        file_path: '',
        file_remark: '',
        file_owner: '',
        file_type: 0  //  0 -- 日志类型  1--配置文件类型
      },
      // 添加表单验证规则
      ruleInline: {
        serverip: [{
          required: true,
          message: '请填写主机IP',
          trigger: 'blur'
        }],
        serverhost: [{
          required: true,
          message: '请填写主机名',
          trigger: 'blur'
        }],
        file_title: [{
          required: true,
          message: '请填写文件标题',
          trigger: 'blur'
        }],
        file_path: [{
          required: true,
          message: '请填写文件路径',
          trigger: 'blur'
        }],
        file_type: [{
          required: true,
          message: '请选择文件类型',
          trigger: 'blur'
        }],
        file_owner: [{
          required: true,
          message: '请选择文件归属人',
          trigger: 'blur'
        }]
      },

      Generate: {
        textarea: '',
        add: '',
        name: ''
      },
      file_type: ['Log', 'Config', 'Other'],
      computer_room_set: util.computer_room,
      datalist: {
        computer_room_list: [],
        cabinet_list: [],
        server_instance_list: [],
        serverhost_list: [],
        serverip_list: []
      },
      delbaseModal: false,
      delbasename: '',
      delconfirmbasename: '',
      pagenumber: 1,
      tmp_id: null,
      diclist: [],
      mail_switch: false,
      dingding_switch: false
    }
  },
  methods: {
    del () {
      this.modal = false
      this.formFileItem = {}
    },
    Computer_Room (val) {
      this.dataset.cabinet = ''
      this.dataset.server = ''
      this.dataset.serverhost = ''
      this.dataset.serverip = ''
      if (val) {
        this.ScreenComputer(val)
      }
    },
    ScreenComputer (val) {
      this.datalist.computer_roomlist = this.item.filter(item => {
        if (item.computer_room === val) {
          return item
        }
      })
    },
    Cabinet (index) {
      if (index) {
        this.id = this.item.filter(item => {
          if (item.computer_room === index) {
            return item
          }
        })
        axios.put(`${util.url}/assets/cabinet`, {
            'id': this.id[0].id
          })
          .then(res => {
            this.datalist.cabinet_list = res.data
          })
          .catch(() => {
            this.$Notice.error({
              title: '警告',
              desc: '无法连接数据库!请检查网络'
            })
          })
      }
    },
    Server_instance () {
      this.formFileItem.serverip = ''
      this.formFileItem.serverhost = ''
    },
    add () {
      for (let i of this.rowdata) {
        if (i.computer_room === this.formFileItem.name) {
          this.$Notice.error({
            title: '警告',
            desc: '连接名称重复,请更改为其他！'
          })
          return
        }
      }
      this.$refs['formValidate'].validate((valid) => {
        if (valid) {
          let data = {
            'computer_room': this.formFileItem.computer_room,
            'cabinet': this.formFileItem.cabinet,
            'server_instance': this.formFileItem.server_instance,
            'serverhost': this.formFileItem.serverhost,
            'serverip': this.formFileItem.serverip,
            'file_path': this.formFileItem.file_path,
            'file_owner': this.formFileItem.file_owner,
            'file_remark': this.formFileItem.file_remark,
            'file_title': this.formFileItem.file_title,
            'file_type': this.formFileItem.file_type
          }
          axios.post(util.url + '/mamagement_sql/', {
              'data': JSON.stringify(data)
            })
            .then(() => {
              this.$Notice.success({
                title: '通知',
                desc: '数据库信息添加成功!'
              })
            })
            .catch(error => {
              this.$Notice.error({
                title: '警告',
                desc: error
              })
            })
          this.del()
          this.mountdata()
        }
      })
    },
    edit_tab (index) {
      this.$Modal.info({
        title: '数据库连接信息',
        content: `机房: ${this.rowdata[index].computer_room}<br> 连接名称：${this.rowdata[index].connection_name}<br>
                  数据库地址：${this.rowdata[index].ip}<br>端口: ${this.rowdata[index].port}<br>用户名: ${this.rowdata[index].username}`
      })
    },
    // 删除数据库
    delFile (index) {
      this.delbaseModal = true
      this.delbasename = this.rowdata[index].computer_room
    },
    // 生成数据库全部库名
    BaseList (vl) {
      if (vl.length === 0) {
        return
      }
      this.tmp_id = vl
      axios.put(`${util.url}/workorder/basename`, {
          'id': vl
        })
        .then(res => {
          this.dictionary.databasesList = res.data
        })
        .catch(() => {
         this.$Notice.error({
           title: '警告',
           desc: '数据库信息获取失败,请检查网络状态.'
         })
        })
    },
    // 全选
    dicCheckAll () {
      if (this.dictionary.indeterminate) {
        this.dictionary.checkAll = false;
      } else {
        this.dictionary.checkAll = !this.dictionary.checkAll;
      }
      this.dictionary.indeterminate = false;

      if (this.dictionary.checkAll) {
        this.dictionary.databases = this.dictionary.databasesList;
      } else {
        this.dictionary.databases = [];
      }
    },
    // 重置
    cleardata () {
      this.dictionary.databases = []
      this.dictionary.databasesList = []
      this.dictionary.getdellist = []
      this.dictionary.getdel = []
    },
    delbaselink () {
      if (this.delbasename === this.delconfirmbasename) {
        axios.delete(util.url + '/mamagement_sql/' + this.delbasename)
          .then(res => {
            this.$Notice.success({
              title: '通知',
              desc: res.data
            })
            this.delbaseModal = false
            this.delconfirmbasename = ''
            this.mountdata()
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      } else {
        this.$Message.error({
          content: '请确认输入的连接名称一致！'
        })
      }
    },
    splicpage (page) {
      this.mountdata(page)
    },
    mountdata (vl = 1) {
      axios.get(`${util.url}/mamagement_sql?page=${vl}`)
        .then(res => {
          this.rowdata = res.data.data
          this.pagenumber = parseInt(res.data.page.alter_number)
          this.diclist = res.data.diclist
          this.mail_switch = res.data.mail_switch
          this.dingding_switch = res.data.ding_switch
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    mailchange (status) {
      let id = null
      status ? id = 1 : id = 0
      axios.post(`${util.url}/globalpermissions`, {
        'type': '1',
        'id': id
      })
        .then(res => {
          this.$Notice.info({
            title: '信息',
            desc: res.data
          })
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    dingdingchange (status) {
      let id = null
      status ? id = 1 : id = 0
      axios.post(`${util.url}/globalpermissions`, {
        'type': '0',
        'id': id
      })
        .then(res => {
          this.$Notice.info({
            title: '信息',
            desc: res.data
          })
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  },
  mounted () {
    this.mountdata()
  }
}
</script>
