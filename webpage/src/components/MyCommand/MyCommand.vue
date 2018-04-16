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
      新增服务器管理命令
    </p>
    <div class="edittable-testauto-con">
      <div id="showImage" class="margin-bottom-10">
      <Form ref="formFileItem" :model="formFileItem" :rules="ruleValidate" :label-width="100" >

        <!--<Form-item label="云环境:" prop="computer_room">-->
          <!--<Select v-model="formFileItem.computer_room" placeholder="请选择" @on-change="Computer_Room">-->
            <!--<Option v-for="i in datalist.yun_env_list" :key="i" :value="i" >{{i}}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->
        <!--<Form-item label="区域:" prop="area">-->
          <!--<Select v-model="formFileItem.area" placeholder="请选择" @on-change="Area" filterable>-->
            <!--<Option v-for="i in datalist.area_list" :value="i.area_name" :key="i.area_name">{{ i.area_name }}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->
        <!--<Form-item label="服务器实例:" prop="server_instance_name">-->
          <!--<Select v-model="formFileItem.server_instance_name" placeholder="请选择" @on-change="Server_instance" filterable>-->
            <!--<Option v-for="item in datalist.server_instance_list" :value="item.name" :key="item.name">{{ item.name }}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->
        <!--<Form-item label="主机公网IP:" prop="publicip">-->
          <!--<Input v-model="formFileItem.publicip" disabled placeholder="请输入"></Input>-->
        <!--</Form-item>-->
        <!--<Form-item label="主机内网IP:" prop="privateip">-->
          <!--<Input v-model="formFileItem.privateip" disabled placeholder="请输入"></Input>-->
        <!--</Form-item>-->
        <!--<Form-item label="主机状态:" prop="serverstatus">-->
          <!--<Input v-model="formFileItem.serverstatus" disabled placeholder="请输入"></Input>-->
        <!--</Form-item>-->
        <!--<Form-item label="选择用户:" prop="file_title">-->
          <!--<Input v-model="formFileItem.ssh_user" placeholder="请输入"></Input>-->
        <!--</Form-item>-->

        <Form-item label="添加命令:" prop="file_title">
          <Input v-model="formFileItem.ssh_pwd" type="textarea" :row="10"  placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="命令说明:" prop="file_title">
          <Input v-model="formFileItem.ssh_user_remark" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="命令分类:" prop="file_title">
          <Input v-model="formFileItem.ssh_pwd"  placeholder="请输入"></Input>
        </Form-item>
        <p></p>
        <Button type="default" @click="test_ssh()" style="margin-left: 5%">连接测试</Button>
        <Button type="success" @click="add_sshuser()" style="margin-left: 19%" :disabled="this.validate_gen">确定</Button>
        <Button type="warning" @click="del_sshuser()" style="margin-left: 10%">重填</Button>

      </Form>
      </div>
    </div>
  </Card>

  </Col>
  <Col span="18" class="padding-left-10">
  <Card>
    <Tabs value="主机控制" style="height: 660px;">
      <TabPane label="数据库命令" icon="load-b" name="rds_command">
          <!--<p slot="title">-->
            <!--<Icon type="ios-crop-strong"></Icon>-->
            <!--主机SSH账号清单-->
          <!--</p>-->
          <div class="edittable-con-3">
            <Table :columns="columns" :data="command_list" height="550"></Table>
          </div>
          <br>
          <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
      </TabPane>


      <TabPane label="主机命令" icon="load-b" name="ecs_command">
        <!--<p slot="title">-->
          <!--<Icon type="ios-crop-strong"></Icon>-->
          <!--主机访问控制-->
        <!--</p>-->
        <div class="edittable-con-3">
          <Table :columns="columns_server" :data="host_list_server" height="550"></Table>
        </div>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
      </TabPane>

      <TabPane label="网络命令" icon="load-b" name="">
        <!--<p slot="title">-->
          <!--<Icon type="ios-crop-strong"></Icon>-->
          <!--主机访问控制-->
        <!--</p>-->
        <div class="edittable-con-3">
          <Table :columns="columns_server" :data="host_list_server" height="550"></Table>
        </div>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
      </TabPane>


    </Tabs>

  </Card>

  </Col>

  <!--进入编辑按钮对话框-->
   <Modal v-model="delFileModal" :width="500">
    <h3 slot="header" style="color:#2D8CF0">编辑</h3>
    <Form :label-width="100" label-position="right">
      <FormItem label="文件名称">
        <Input v-model="delbasename" readonly="readonly"></Input>
      </FormItem>
      <FormItem label="请输入文件名称">
        <Input v-model="delconfirmfilename" placeholder="请确认数据库连接名"></Input>
      </FormItem>
    </Form>
    <div slot="footer">
      <Button type="text" @click="delbaseModal = false">取消</Button>
      <Button type="primary" @click="delfilelink">删除</Button>
    </div>
  </Modal>


  <Modal v-model="editGroupModal" :width="800" :mask-closable="false">
    <h3 slot="header" style="color:#2D8CF0">编辑群组</h3>
    <Form ref="formFileItem" :model="formFileItem" :rules="ruleValidate" :label-width="120" >

        <Form-item label="群组:" prop="computer_room">
          <Select v-model="formFileItem.area" placeholder="请选择" @on-change="Group" filterable>
            <Option v-for="i in datalist.area_list" :value="i.area_name" :key="i.area_name">{{ i.area_name }}</Option>
          </Select>
        </Form-item>
        <Form-item label="区域或机柜:" prop="area">
            <Transfer
                    :data="data2"
                    :target-keys="targetKeys2"
                    filterable
                    :filter-method="filterMethod"
                    @on-change="handleChange2"></Transfer>
            </Form-item>
        <p></p>
        <p></p>
        <!--<Button type="success" @click="add_file()" style="margin-left: 5%">确定</Button>-->

      </Form>
  </Modal>
</div>
</template>
<script>
import '../../assets/tablesmargintop.css'
import axios from 'axios'
// import Cookies from '../js-cookie'
import util from '../../libs/util'
import ICol from '../../../node_modules/iview/src/components/grid/col'
export default {
  components: {
    ICol
  },
  name: 'my-command',
  data () {
    return {
      validate_gen: true,
      social: [],
      file_owern_list: [],
      host_list_server: [],
      host_list_group: [],
      editGroupModal: false,
      columns_server: [
        {
          title: '外网IP',
          key: 'publicip'
        },
        {
          title: '内网IP',
          key: 'privateip'
        },
        {
          title: '是否进制普通用户访问',
          key: 'switch_server',
          width: 150,
          render: (h, params) => {
            return h('div', [
              h('i-switch', { // 数据库1是已处理，0是未处理
                props: {
                  type: 'primary',
                  value: params.row.treatment === 1  // 控制开关的打开或关闭状态，官网文档属性是value
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  'on-change': (value) => { // 触发事件是on-change,用双引号括起来，
                    // 参数value是回调值，并没有使用到
                    this.switch(params.index) // params.index是拿到table的行序列，可以取到对应的表格值
                  }
                }
              }, 'bb')
            ])
          }
        }
      ],
      columns_visit_group: [
        {
          title: '外网IP',
          key: 'publicip'
        },
        {
          title: '内网IP',
          key: 'privateip'
        },
        {
          title: '访问群组',
          key: 'workgroup'
        },
        {
          title: '操作',
          key: 'switch_group',
          width: 180,
          render: (h, params) => {
            return h('div', [
               h('Button', {
                props: {
                  size: 'small',
                  type: 'info'
                },
                on: {
                  click: () => {
                    this.edit_File(params.index)
                  }
                }
              }, '编辑'),
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
                    this.def_File(params.index)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      columns: [
        {
          title: '命令说明',
          key: 'room_name'
        },
        {
          title: '命令内容',
          key: 'region_name'
        },
        {
          title: '附件',
          key: 'privateip'
        },
        {
          title: '创建人',
          key: 'workgroup'
        },
        {
          title: '账号编辑',
          key: 'action',
          width: 200,
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  size: 'small',
                  type: 'info'
                },
                on: {
                  click: () => {
                    this.edit_File(params.index)
                  }
                }
              }, '编辑账号'),
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
                    this.def_File(params.index)
                  }
                }
              }, '删除')
            ])
          }
        },
        {
          title: '编辑群组',
          key: 'action',
          width: 130,
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  size: 'small',
                  type: 'info'
                },
                on: {
                  click: () => {
                    this.editGroupModal = true
                  }
                }
              }, '选择群组')
            ])
          }
        },
        {
          title: '允许此账号SSH访问',
          key: 'switch',
          width: 70,
          render: (h, params) => {
            return h('div', [
              h('i-switch', { // 数据库1是已处理，0是未处理
                props: {
                  type: 'primary',
                  value: params.row.treatment === 1  // 控制开关的打开或关闭状态，官网文档属性是value
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  'on-change': (value) => { // 触发事件是on-change,用双引号括起来，
                    // 参数value是回调值，并没有使用到
                    this.switch(params.index) // params.index是拿到table的行序列，可以取到对应的表格值
                  }
                }
              }, 'aa')
            ])
          }
        }
      ],
      rowdata: [],
      host_list: [],
      group_list: [],
      editFileModal: false,
      delFileModal: false,
      delfilename: '',
      delconfirmfilename: '',
      modal: false,
      // 添加数据库信息
      formFileItem: {
        computer_room: '',
        cabinet: '',
        server_instance_name: '',
        serverip: '',
        publicip: '',
        privateip: '',
        serverstatus: '',
        ssh_user: '',
        ssh_pwd: '',
        ssh_user_remark: ''
      },
      // 添加表单验证规则
      ruleValidate: {
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
        ssh_user: [{
          required: true,
          message: '请填写登录账号',
          trigger: 'blur'
        }],
        ssh_pwd: [{
          required: true,
          message: '请填写登录账号密码',
          trigger: 'blur'
        }],
        ssh_user_remark: [{
          required: true,
          message: '请填写登录账号说明',
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
      item: {},
      item_user: {},
      // datalist_init: {
      //   yun_room_list: [],
      //   idc_room_list: [],
      //   // cabinet_list: [],
      //   own_cabinet_list:[],
      //   gzidc_cabinet_list: [],
      //   aliyun_area_list: [],
      //   meituanyun_area_list: [],
      //   huaweiyun_area_list: [],
      //   area_list: [],
      //   server_instance_name_list: [],
      //   server_id_name_list: [],
      //   serverhost_list: [],
      //   serverip_list: []
      // },
      datalist: {
        yun_env_list: util.yun_room_list,
        idc_env_list: util.own_room_list,
        area_list: [],
        server_instance_list: []
      },
      server_host_ip: {
        name: '',
        publicip: '',
        privateip: '',
        status: ''
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
    test_ssh () {
      axios.put(`${util.url}/host/test`, {
        'publicip': this.formFileItem.publicip,
        'privateip': this.formFileItem.privateip,
        'ssh_user': this.formFileItem.ssh_user,
        'ssh_pwd': this.formFileItem.ssh_pwd
      }).then(res => {
        if (res.data.status === 200) {
          this.$Notice.success({
            title: '成功',
            desc: res.data.data
          })
          this.validate_gen = false
        } else {
          this.$Notice.success({
            title: '失败',
            desc: res.data.data
          })
        }
        })
        .catch(() => {
          this.$Notice.error({
            title: '警告',
            desc: '无法连接数据库!请检查网络'
          })
        })
    },
    add_sshuser () {
       axios.post(`${util.url}/host/`, {
        // 'room_name': this.formFileItem.computer_room,
        // 'area_name': this.formFileItem.area,
        // 'server_name': this.formFileItem.server_instance_name,
        // 'server_status': this.formFileItem.serverstatus,
        'publicip': this.formFileItem.publicip,
        'privateip': this.formFileItem.privateip,
        'ssh_user': this.formFileItem.ssh_user,
        'ssh_pwd': this.formFileItem.ssh_pwd,
        'remark': this.formFileItem.ssh_user_remark
      })
        .then(res => {
          this.$Notice.success({
                  title: '成功',
                  desc: res.data.msg
                })
          this.host_list = res.data.data
        })
        .catch(() => {
          this.$Notice.error({
            title: '警告',
            desc: '无法连接数据库!请检查网络'
          })
        })
    },
    del_sshuser () {},
    ClearForm () {
      this.formFileItem.publicip = ''
      this.formFileItem.privateip = ''
      this.formFileItem.serverstatus = ''
      this.formFileItem.file_type = ''
      this.formFileItem.file_title = ''
      this.formFileItem.file_remark = ''
      this.formFileItem.file_owner = ''
      this.formFileItem.area = ''
      this.formFileItem.file_path = ''
      this.formFileItem.serverip = ''
      this.formFileItem.server_instance_name = ''
      // this.formFileItem.server_instance = ''
      this.formFileItem.cabinet = ''
      this.formFileItem.computer_room = ''
      this.datalist.area_list = []
      // this.Computer_Room
    },
    // del () {
    //   this.modal = false
    //   this.formFileItem = {}
    // },
    Computer_Room (val) {
      this.formFileItem.server_instance = '';
      this.formFileItem.server_instance_name = '';
      this.formFileItem.cabinet = '';
      // this.datalist.area_list = [];
      this.formFileItem.cabinet = '';
      this.formFileItem.server_instance = '';
      if (val) {
        // alert(val)
        this.ScreenComputer(val)
      }
    },
    ScreenComputer (val) {
      this.datalist.area_list = this.item.filter(item => {
        if (item.room_name === val) {
          // alert(item.room_name)
          return item
        }
        // console.log(item, 'yes')
      })
      // console.log(this.datalist.area_list, 'hello')
    },
    delfilelink () {
      if (this.delfilename === this.delconfirmfilename) {
        axios.delete(util.url + '/filemanager/' + this.delbasename)
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
    Area () {
      axios.put(`${util.url}/filemanager/instance`, {
        'room_name': this.formFileItem.computer_room,
        'area_name': this.formFileItem.area
      })
        .then(res => {
          this.datalist.server_instance_list = res.data
          console.log(res.data, 'jiangtest')
        })
        .catch(() => {
          this.$Notice.error({
            title: '警告',
            desc: '无法连接数据库!请检查网络'
          })
        })
    // }
    },
    Server_instance (val) {
      this.server_host_ip = this.datalist.server_instance_list.filter(item => {
        if (item.name === val) {
          return item
        }
      })
      console.log(this.server_host_ip, 'jack')
      console.log(this.server_host_ip[0].publicip, 'jack1')
      console.log(this.server_host_ip[0].privateip, 'jack2')
      console.log(this.server_host_ip[0].status, 'jack3')
      this.formFileItem.publicip = this.server_host_ip[0].publicip
      this.formFileItem.privateip = this.server_host_ip[0].privateip
      this.formFileItem.serverstatus = this.server_host_ip[0].status
    },
    edit_File (index) {
      this.editFileModal = true
    },
    def_File (index) {
      this.delFileModal = true
      this.delfiilename = this.rowdata[index].file_title
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
    splicpage (page) {
      this.mountdata(page)
    },
    mountdata (vl = 1) {
      axios.put(`${util.url}/filemanager/init`)
        .then(res => {
          this.item = res.data.area
          // this.host_list = res.data.host_list
          // console.log(res.data.host_list, 'jianglb')
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })

      axios.get(`${util.url}/host/`)
        .then(res => {
          this.host_list = res.data.data
          this.host_list_server = res.data.distinct_data
          this.host_list_group = res.data
          // console.log(res.data.host_list, 'jianglb')
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
