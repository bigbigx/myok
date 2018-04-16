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
      <div id="showImage" class="margin-bottom-10">
      <Form ref="formFileItem" :model="formFileItem" :rules="ruleValidate" :label-width="100" >


        <Form-item label="云环境:" prop="computer_room">
          <Select v-model="formFileItem.computer_room" placeholder="请选择" @on-change="Computer_Room">
            <Option v-for="i in datalist.yun_env_list" :key="i" :value="i" >{{i}}</Option>
          </Select>
        </Form-item>
        <Form-item label="区域:" prop="area">
          <Select v-model="formFileItem.area" placeholder="请选择" @on-change="Area" filterable>
            <Option v-for="i in datalist.area_list" :value="i.area_name" :key="i.area_name">{{ i.area_name }}</Option>
          </Select>
        </Form-item>
        <Form-item label="服务器实例:" prop="server_instance_name">
          <Select v-model="formFileItem.server_instance_name" placeholder="请选择" @on-change="Server_instance" filterable>
            <Option v-for="item in datalist.server_instance_list" :value="item.name" :key="item.name">{{ item.name }}</Option>
          </Select>
        </Form-item>
        <Form-item label="主机公网IP:" prop="publicip">
          <Input v-model="formFileItem.publicip" disabled placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="主机内网IP:" prop="privateip">
          <Input v-model="formFileItem.privateip" disabled placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="主机状态:" prop="serverstatus">
          <Input v-model="formFileItem.serverstatus" disabled placeholder="请输入"></Input>
        </Form-item>

        <!--<Form-item label="机房:" prop="computer_room">-->
          <!--<Select v-model="formFileItem.computer_room" placeholder="请选择" @on-change="Computer_Room">-->
            <!--<Option v-for="i in datalist.idc_env_list" :key="i" :value="i" >{{i}}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->
        <!--<Form-item label="机柜:" prop="area">-->
          <!--<Select v-model="formFileItem.area" placeholder="请选择" @on-change="Area" filterable>-->
            <!--<Option v-for="i in datalist.area_list" :value="i.area_name" :key="i.area_name">{{ i.area_name }}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->
        <!--<Form-item label="服务器编号:" prop="server_instance_name">-->
          <!--<Select v-model="formFileItem.server_instance_name" placeholder="请选择" @on-change="Server_instance" filterable>-->
            <!--<Option v-for="item in datalist.server_instance_list" :value="item.name" :key="item.name">{{ item.name }}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->

      <Tabs value="yun_env_init" @on-click="ClearForm">
        <TabPane label="固定文件"  name="yun-env" >
        <!--<Form-item label="主机公网IP:" prop="publicip">-->
          <!--<Input v-model="formFileItem.publicip" disabled placeholder="请输入"></Input>-->
        <!--</Form-item>-->
        <!--<Form-item label="主机内网IP:" prop="pricateip">-->
          <!--<Input v-model="formFileItem.privateip" disabled placeholder="请输入"></Input>-->
        <!--</Form-item>-->
        <!--<Form-item label="主机状态:" prop="serverstatus">-->
          <!--<Input v-model="formFileItem.serverstatus" disabled placeholder="请输入"></Input>-->
        <!--</Form-item>-->
        <Form-item label="文件标题:" prop="file_title">
          <Input v-model="formFileItem.file_title" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件路径:" prop="file_path">
          <Input v-model="formFileItem.file_path" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件备注:" prop="file_remark">
          <Input v-model="formFileItem.file_remark" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件类型:" prop="file_type">
          <Select v-model="formFileItem.file_type" placeholder="请选择">
            <Option v-for="type in file_type" :value="type" :key="type">{{ type }}</Option>
          </Select>
        </Form-item>
        </TabPane>
      <TabPane label="动态文件"  name="idc-env" >
        <Form-item label="文件标题:" prop="file_title">
          <Input v-model="formFileItem.file_title" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="选择命令:" prop="file_path">
          <Input v-model="formFileItem.file_path" placeholder="请输入"></Input>
        </Form-item>
      <Form-item label="指定文件路径:" prop="file_path">
          <Input v-model="formFileItem.file_path" placeholder="请输入"></Input>
        </Form-item>

      </TabPane>
     </Tabs>
        <!--<Form-item label="文件归属:" prop="file_owner">-->
          <!--<Select v-model="formFileItem.file_owner" placeholder="请选择">-->
            <!--<Option v-for="list in item_user" :value="list.username" :key="list.username">{{ list.username }}</Option>-->
          <!--</Select>-->
        <!--</Form-item>-->

        <FormItem label="所属群组:" prop="group">
              <Select v-model="formFileItem.group" placeholder="请选择">
            <Option v-for="group in group_list" :value="group.name" :key="group.name">{{ group.name }}</Option>
          </Select>
            </FormItem>
        <p></p>
        <p></p>
        <Button type="info" @click="filetest()">文件检测</Button>
        <Button type="success" @click="add_file()" style="margin-left: 5%">确定</Button>
        <Button type="warning" @click="del_file()" style="margin-left: 30%">重填</Button>

      </Form>
      </div>
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
      <Table :columns="columns" :data="file_list" height="550"></Table>
    </div>
    <br>
    <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
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


  <Modal v-model="editFileModal" :width="500">
    <h3 slot="header" style="color:#2D8CF0">编辑文件</h3>
    <Form ref="formFileItem" :model="formFileItem" :rules="ruleValidate" :label-width="100" >

        <Form-item label="环境或机房:" prop="computer_room">
          <Input v-model="formFileItem.computer_room" disabled placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="区域或机柜:" prop="area">
          <Input v-model="formFileItem.area" disabled placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="服务器实例:" prop="server_instance_name">
          <Input v-model="formFileItem.server_instance_name" disabled placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="主机公网IP:" prop="publicip">
          <Input v-model="formFileItem.publicip" disabled placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="主机内网IP:" prop="privateip">
          <Input v-model="formFileItem.privateip" disabled placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="主机状态:" prop="serverstatus">
          <Input v-model="formFileItem.serverstatus" disabled placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="文件标题:" prop="file_title">
          <Input v-model="formFileItem.file_title" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件路径:" prop="file_path">
          <Input v-model="formFileItem.file_path" placeholder="请输入"></Input>
        </Form-item>
        <Form-item label="文件类型:" prop="file_type">
          <Input v-model="formFileItem.file_type" placeholder="没数据"></Input>
        </Form-item>
        <Form-item label="文件备注:" prop="file_remark">
          <Input v-model="formFileItem.file_remark" placeholder="请输入"></Input>
        </Form-item>

        <FormItem label="文件归属:" prop="group">
            <Select v-model="formFileItem.group" placeholder="请选择">
              <Option v-for="group in group_list" :value="group.name" :key="group.name">{{ group.name }}</Option>
            </Select>
            </FormItem>
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
import util from '../../libs/util'
import ICol from '../../../node_modules/iview/src/components/grid/col'
export default {
  components: {
    ICol
  },
  name: 'logger-manager',
  data () {
    return {
      social: [],
      file_owern_list: [],
      columns: [
        {
          title: '主机名',
          key: 'server_hostname',
          width: 150,
          fixed: 'left',
          sortable: true
        },
        {
          title: '文件标题',
          key: 'file_title',
          width: 150,
          fixed: 'left'
        },
        {
          title: '文件路径',
          key: 'file_path',
          width: 180,
          fixed: 'left'
        },
        {
          title: '文件类型',
          key: 'file_type',
          width: 80
        },
        {
          title: '区域',
          key: 'region_name',
          width: 150
        },
        {
          title: '环境',
          key: 'room_name',
          width: 150
        },
        {
          title: '公网IP',
          key: 'public_server_ip',
          width: 150
        },

        {
          title: '内网IP',
          key: 'private_server_ip',
          width: 150
        },
        {
          title: '文件归属',
          key: 'file_owner',
          width: 150
        },
        {
          title: '操作',
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
        },
        {
          title: '是否允许全量查看文件',
          key: 'switch',
          align: 'center',
          fixed: 'right',
          width: 70,
          render: (h, params) => {
            // console.log(Boolean(params.row.full_file_status), 'jianglibin')
            if (params.row.full_file_status === 'false') {
              return h('div', [
                h('i-switch', { // 数据库1是已处理，0是未处理
                  props: {
                    type: 'primary',
                    value: false// 控制开关的打开或关闭状态，官网文档属性是value
                    // value: params.row.status // 控制开关的打开或关闭状态，官网文档属性是value
                    // value: params.row.switch === params.row.full_file_status  // 控制开关的打开或关闭状态，官网文档属性是value
                    // value: params.row.full_file_status // 控制开关的打开或关闭状态，官网文档属性是value
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
                }, '')
              ])
            } else {
               return h('div', [
                h('i-switch', { // 数据库1是已处理，0是未处理
                  props: {
                    type: 'primary',
                    value: true// 控制开关的打开或关闭状态，官网文档属性是value
                    // value: params.row.status // 控制开关的打开或关闭状态，官网文档属性是value
                    // value: params.row.switch === params.row.full_file_status  // 控制开关的打开或关闭状态，官网文档属性是value
                    // value: params.row.full_file_status // 控制开关的打开或关闭状态，官网文档属性是value
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
                }, '')
              ])
            }
          }
        }
      ],
      rowdata: [],
      file_list: [],
      group_list: [],
      editFileModal: false,
      delFileModal: false,
      delfilename: '',
      delconfirmfilename: '',
      full_file_status: 0,
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
      ruleValidate: {
        computer_room: [{
          required: true,
          message: '机房地址不得为空',
          trigger: 'change'
        }],
        area: [{
          required: true,
          message: '区域不得为空',
          trigger: 'change'
        }],
        server_instance_name: [{
          required: true,
          message: '服务器名称不得为空',
          trigger: 'change'
        }],
        privateip: [{
          required: true,
          message: '主机内网IP不得为空',
          trigger: 'change'
        }],
        serverstatus: [{
          required: true,
          message: '主机运行状态不得为空',
          trigger: 'change'
        }],
        file_title: [{
          required: true,
          message: '文件标题不得为空',
          trigger: 'change'
        }],
        file_path: [{
          required: true,
          message: '文件路径不得为空',
          trigger: 'change'
        }],
        file_type: [{
          required: true,
          message: '文件类型不得为空',
          trigger: 'change'
        }],
        file_remark: [{
          required: true,
          message: '文件说明不得为空',
          trigger: 'change'
        }],
        group: [{
          required: true,
          message: '文件归属群组不得为空',
          trigger: 'change'
        }]
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
     // 通过开关状态判断值然后传值进行更新
     switch (index) {
      // 打开是true,已经处理1
        console.log(this.file_list[index], 'hehe')
        if (this.file_list[index].full_file_status === 'true') {
            this.file_list[index].switch = false
            this.updateFeedbackMessage(this.file_list[index].id, 'false')
        } else {
          this.file_list[index].switch = true
            this.updateFeedbackMessage(this.file_list[index].id, 'true')
        }
     },
     // 更新反馈信息某一字段
     updateFeedbackMessage (id, value) {
       axios.put(`${util.url}/filemanager/save_status`, {
        'full_file_status': value,
        'file_id': id
      }).then(res => {
          this.$Notice.success({
                  title: '成功',
                  desc: res.data
                })
        }).catch(() => {
          this.$Notice.error({
            title: '警告',
            desc: '无法连接数据库!请检查网络'
          })
        })
     },
     // // 获取所有反馈信息列表
     // getFeedbackMessages() {
     //  var vm = this
     //  var url = '/v1/suggestions?'
     //  url = url + "pageNum=" + this.pageNum + '&pageSize=' + this.pageSize
     //  if (this.createByValue !== '') {
     //    url = url + '&createBy=' + this.createByValue
     //  }
     //  if (this.dealModelValue !== '') {
     //      url = url + '&treatment=' + this.dealModelValue
     //  }
     //  axios.get(util.url + '/filemanager/' + this.delbasename).then(response => {
     //    if (response.data.code === '000000') {
     //       vm.data1 = response.data.data
     //       vm.pageTotal = parseInt(response.data.message)
     //    }
     //  }).catch(error => {
     //    console.log(error)
     //  })
     // },
    add_file () {
       axios.post(`${util.url}/filemanager/`, {
        'room_name': this.formFileItem.computer_room,
        'area_name': this.formFileItem.area,
        'server_name': this.formFileItem.server_instance_name,
        'server_status': this.formFileItem.serverstatus,
        'publicip': this.formFileItem.publicip,
        'privateip': this.formFileItem.privateip,
        'file_path': this.formFileItem.file_path,
        'file_remark': this.formFileItem.file_remark,
        // 'file_owner': this.formFileItem.file_owner,
        'file_owner': this.formFileItem.group,
        'file_title': this.formFileItem.file_title,
        'file_type': this.formFileItem.file_type
      }).then(res => {
          this.$Notice.success({
                  title: '成功',
                  desc: res.data
                })
          this.ClearForm()
        })
        .catch(() => {
          this.$Notice.error({
            title: '警告',
            desc: '无法连接数据库!请检查网络'
          })
        })
    },
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
          // console.log(res.data.aliyun, 'jianglb')
          this.item = res.data.area
          this.item_user = res.data.user
          this.file_list = res.data.file_list
          this.group_list = res.data.group
          console.log(res.data.file_list, 'jianglb')
          // this.datalist_init.aliyun_area_list = res.data.aliyun
          // this.datalist_init.meituanyun_area_list = res.data.meituanyun
          // this.datalist_init.huaweiyun_area_list = res.data.huaweiyun
          // this.datalist_init.
          // this.datalist_init.own_cabinet_list = res.data.own
          // this.datalist_init.
          // console.log(res.data, 'jianglb')
          // this.datalist_init.yun_area_list = res.data.aliyun.data
          // this.datalist_init.idc_room_list = res.data
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
