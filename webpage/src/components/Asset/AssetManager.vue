<style lang="less">
@import '../../styles/common.less';
@import '../common/table.less';
</style>

<template>
<div>
  <Row>

    <Col span="7">


        <Card>
              <p slot="title">
      <Icon type="ios-crop-strong"></Icon>新增资产
    </p>
          <Tabs value="name1" >
        <TabPane label="云环境" icon="load-b" name="parent_tab_yun">
          <div class="edittable-test-con">
          <div id="showImage" class="margin-bottom-10">

            <Form ref="formYunItem" :model="formYunItem" :rules="ruleValidate" :label-width="80">
              <!--<FormItem label="云环境:" prop="computer_room">-->
                <!--<Select v-model="formYunItem.computer_room" @on-change="Computer_room">-->
                <!--<Option v-for="i in yun_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>-->
              <!--</Select>-->
              <!--</FormItem>-->

              <!--<FormItem label="所在区域:" prop="area">-->
                <!--<Select v-model="formYunItem.area_name" filterable>-->
                <!--<Option v-for="i in yun_datalist.area_list" :value="i" :key="i">{{ i }}</Option>-->
              <!--</Select>-->
              <!--</FormItem>-->


              <!--<FormItem label="实例类型:" prop="instance_type">-->
                <!--<Select v-model="formYunItem.instance_type" filterable>-->
                <!--<Option v-for="i in yun_datalist.instance_type_list" :value="i" :key="i">{{ i }}</Option>-->
              <!--</Select>-->
              <!--</FormItem>-->

              <!--<FormItem label="实例名称:" prop="instance_name">-->
                <!--<input type="text" size="small"></input>-->
              <!--</FormItem>-->

              <!--<FormItem label="实例ID:" prop="instance_id">-->
                 <!--<input type="text" size="small"></input>-->
              <!--</FormItem>-->

              <!--<FormItem>-->
                <!--<Button type="warning" icon="android-search" @click.native="test_sql()">检测</Button>-->
                <!--<Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :disabled="this.validate_gen">添加</Button>-->
              <!--</FormItem>-->
            <!--</Form>-->
             <Alert style="height: 145px">
              云环境资产更新说明
              <template slot="desc">
                  <p>1) 本平台可通过阿里云的SDK获取资产信息i</p>
                  <p>2) 可以手工更新资产</p>
                  <p>3) 可以设置定时更新资产，每天只能更新一次</p>
                </template>
            </Alert>
            </Form>
            <Card>
              <Tabs value="refresh_tab" style="height: 180px;">
                <TabPane label="手工更新"  name="handle_refresh_assets" >
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="handle_yun_assets" size="large">手工更新资产</Button>
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="handle_yun_assets" size="large">刷新云资产清单</Button>
                </TabPane>
                <TabPane label="定时更新"  name="crontab_refresh_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="large">设置定时更新资产</Button>
                </TabPane>
                <TabPane label="导出资产"  name="crontab_export_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="large">导出云资产</Button>
                <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="large">查看资产更新日志</Button>
                </TabPane>
              </Tabs>
            </Card>
              <Card>
                <p slot="title">
                  <Icon type="ios-crop-strong"></Icon>最近资产动作
                </p>
                <div class="edittable-con-0">
                   <Table :columns="columns_refresh_log" :data="yun_diff_list" height="300"></Table>
                  <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                </div>
              </Card>
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
          </div>
        </div>
        </TabPane>

        <TabPane label="物理机房" icon="load-d" name="parent_tab_own">
            <div class="edittable-test-con">
          <div id="showImage" class="margin-bottom-10">

            <Form ref="formOwnItem" :model="formOwnItem" :rules="ruleValidate" :label-width="80">
              <FormItem label="机房:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>

              <FormItem label="机柜:" prop="connection_name">
                <Select v-model="formOwnItem.connection_name" @on-change="DataBaseName" filterable>
                <Option v-for="i in own_datalist.connection_name_list" :value="i.connection_name" :key="i.connection_name">{{ i.connection_name }}</Option>
              </Select>
              </FormItem>


              <FormItem label="所属资产:" prop="connection_name">
                <Select v-model="formOwnItem.connection_name" @on-change="DataBaseName" filterable>
                <Option v-for="i in formOwnItem.connection_name_list" :value="i.connection_name" :key="i.connection_name">{{ i.connection_name }}</Option>
              </Select>
              </FormItem>

              <FormItem label="主机名:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>

              <FormItem label="IP地址:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>


              <FormItem label="硬盘:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>

              <FormItem>
                <Button type="warning" icon="android-search" @click.native="test_sql()">检测</Button>
                <Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :enabled="this.validate_gen">添加</Button>
              </FormItem>
            </Form>
            <Alert style="height: 145px">
              物理机房如何自动CMDB
              <template slot="desc">
                  <p>1) 巡风系统估计值</p>
                </template>
            </Alert>
             <Card>
              <Tabs value="refresh_tab" style="height: 150px;">
                <TabPane label="手工更新"  name="handle_refresh_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 10%;" @click.native="orderswitch" size="large">手工更新资产</Button>
                </TabPane>
                <TabPane label="定时更新"  name="crontab_refresh_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 10%;" @click.native="orderswitch" size="large">设置定时更新资产</Button>
                </TabPane>
              </Tabs>
            </Card>
          </div>
        </div>
        </TabPane>
      </Tabs>
        </Card>

    </Col>
<Col span="17" class="padding-left-10">
  <Card>
    <p slot="title">
      <Icon type="ios-crop-strong"></Icon>资产清单

    </p>

    <div class="edittable-con-0">
      <Card>
        <Tabs value="name1">
          <TabPane label="云环境" icon="social-hackernews" name="parent_right_tab_yun">

            <div class="edittable-test-con">
                <div class="edittable-testauto-con">
                  <Card>
                    <Tabs value="name999">
                      <TabPane label="阿里云"  name="child_right_tab_aliyun">
                            <div class="edittable-con-0">
                              <Table :columns="yun_columnsName" :data="aliyun_assets" height="550"></Table>
                            </div>
                            <br>
                        <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                      <TabPane label="美团云"  name="child_right_tab_meituanyun">
                            <div class="edittable-con-0">
                              <Table :columns="yun_columnsName" :data="meituanyun_assets" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                      <TabPane label="华为云" name="child_right_tab_huaweiyun">
                            <div class="edittable-con-0">
                              <Table :columns="yun_columnsName" :data="huaweiyun_assets" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                    </Tabs>
                  </Card>
                </div>
              <!--<Table :columns="columns" :data="rowdata" height="550"></Table>-->
            </div>
          </TabPane>
          <TabPane label="物理机房" icon="nuclear" name="parent_right_tab_own">
            <div class="edittable-test-con">
            <div id="showImage" class="margin-bottom-10">
              <Card>
                    <Tabs value="name999">
                      <TabPane label="公司机房"  name="companry-idc">
                            <div class="edittable-con-1">
                              <Table :columns="columns" :data="rowdata" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                       <TabPane label="广州IDC"  name="gz-idc">
                            <div class="edittable-con-1">
                              <Table :columns="columns" :data="rowdata" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                    </Tabs>
              </Card>
            </div>
            </div>
          </TabPane>
        </Tabs>
      </Card>
    </div>

  </Card>
  </Col>
  </Row>
</div>
</template>
<script>
import ICol from '../../../node_modules/iview/src/components/grid/col.vue'
import axios from 'axios'
import Cookies from 'js-cookie'
import util from '../../libs/util'
export default {
  components: {
    ICol
  },
  name: 'host-manager',
  data () {
    return {
      validate_gen: true,
      formYunItem: {
        textarea: '',
        computer_room: '',
        area_name: '',
        instance_type: '',
        instance_name: ''
      },
      formOwnItem: {
        textarea: '',
        computer_room: '',
        connection_name: '',
        basename: '',
        text: '',
        backup: 0,
        assigned: ''
      },
      columns_refresh_log: [
        {
          title: '时间',
          key: 'cur_time',
          width: ''
        },
        {
          title: '差异条数',
          key: 'diff_count',
          width: ''
        },
        {
          title: '操作人',
          key: 'cur_person',
          width: ''
        },
        {
          title: '详情',
          key: 'action',
          width: 400,
          align: 'center',
          render: (h, params) => {
            if (params.row.username !== this.data5[0].username) {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.edituser(params.index)
                    }
                  }
                }, '更改密码')
              ])
            } else {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.edituser(params.index)
                    }
                  }
                }, '更改密码')
              ])
            }
          }
        }
      ],
      yun_columnsName: [
        {
          title: '实例ID',
          key: 'ID',
          width: '150'
        },
        {
          title: '实例名称',
          key: 'name',
          width: '150'
        },
        {
          title: '实例类型',
          key: 'type',
          width: '100'
        },
        {
          title: '域名/IP',
          key: 'yuming_or_ip',
          width: '150'
        },
        {
          title: '基本配置',
          key: 'basic_config'
        }
      ],
      ecsdata: [],
      rdsdata: [],
      Testresults: [],
      yun_diff_list: [],
      Testresults_backup: [],
      item: {},
      yun_datalist: {
        connection_name_list: [],
        instance_type_list: util.yun_instance_type_list,
        area_list: util.yun_area_list,
        computer_roomlist: util.yun_room_list
      },
      own_datalist: {
        connection_name_list: [],
        basenamelist: [],
        sqllist: [],
        computer_roomlist: util.own_room_list
      },
      ruleValidate: {
        computer_room: [{
          required: true,
          message: '机房地址不得为空',
          trigger: 'change'
        }],
        connection_name: [{
          required: true,
          message: '连接名不得为空',
          trigger: 'change'
        }],
        basename: [{
          required: true,
          message: '数据库名不得为空',
          trigger: 'change'
        }],
        text: [{
            required: true,
            message: '说明不得为空',
            trigger: 'blur'
          },
          {
            type: 'string',
            max: 150,
            message: '最多150个字',
            trigger: 'blur'
          }
        ]
      },
      id: null,
      assigned: []
    }
  },
  methods: {
    show_diif_detail (index) {
      // this.editPasswordModal = true
      // this.username = this.data5[index].username
    },
    handle_yun_assets () { // 手工更新资产 按钮，显示所有ecs和rds的差异
      axios.put(`${util.url}/yunassets/showdiff`, {
        'user': Cookies.get('user')
      })
          .then(res => {
              // this.ecsdata = res.data.ecs
              // this.rdsdata = res.data.rds
              // this.time = res.data.cur_time
              // this.person = res.data.cur_person
              this.yun_diff_list = res.data
              console.log(res.data.ecs, 'ecs')
              console.log(res.data.rds, 'rds')
              // this.formItem
          })
          .catch(() => {
            this.$Notice.error({
              title: '错误',
              desc: '无法连接阿里云API，请检查',
              duration: 10
            })
          })
    },
    Connection_Name (val) {
      this.datalist.connection_name_list = []
      this.datalist.basenamelist = []
      this.formItem.connection_name = ''
      this.formItem.basename = ''
      if (val) {
        this.ScreenConnection(val)
      }
    },
    ScreenConnection (val) {
      this.datalist.connection_name_list = this.item.filter(item => {
        if (item.computer_room === val) {
          return item
        }
      })
    },
    DataBaseName (index) {
      if (index) {
        this.id = this.item.filter(item => {
          if (item.connection_name === index) {
            return item
          }
        })
        axios.put(`${util.url}/workorder/basename`, {
            'id': this.id[0].id
          })
          .then(res => {
            this.datalist.basenamelist = res.data
          })
          .catch(() => {
            this.$Notice.error({
              title: '警告',
              desc: '无法连接数据库!请检查网络'
            })
          })
      }
    },
    //  sql 优化建议
    sqladvisor () {

    },
    // 同时检查  备份栏只能是select语句，ddl栏只能是非select语句
    test_sql () {
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          if (this.formItem.textarea_ddl_dml || this.formItem.textarea_backup) {
            let tmpddl2 = ''
            let tmpddl = ''
            let tmpbak = ''
            let tmpbak2 = ''
            if (this.formItem.textarea_backup) {
                tmpbak2 = this.formItem.textarea_backup.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
                tmpbak = this.formItem.textarea_backup.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
                tmpbak = ''
            }
            if (this.formItem.textarea_ddl_dml) {
                tmpddl2 = this.formItem.textarea_ddl_dml.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
                tmpddl = this.formItem.textarea_ddl_dml.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
                tmpddl = ''
            }
            axios.put(`${util.url}/sqlsyntax/test`, {
                'id': this.id[0].id,
                'base': this.formItem.basename,
                'type': 1,
                'sql': tmpddl + '&&&' + tmpbak,
                'check_sql': tmpddl2 + '&&&' + tmpbak2
              })
              .then(res => {
               if (res.data.status === 200) {
                 this.Testresults = res.data.result_ddl
                 this.Testresults_backup = res.data.result_bak
                 let gen = 0
                 let gen1 = 0
                 this.Testresults.forEach(vl => {
                   if (vl.errlevel !== 0) {
                     gen += 1
                   }
                 })
                 this.Testresults_backup.forEach(v2 => {
                   if (v2.errlevel !== 0) {
                     gen1 += 1
                   }
                 })
                 if (gen === 0 && gen1 === 0) {
                   this.validate_gen = false
                 } else {
                   this.validate_gen = true
                 }
               } else if (res.data.status === 202) {
                 this.$Notice.error({
                   title: '警告',
                   desc: res.data.result
                 })
                 this.validate_gen = true
               } else {
                 this.$Notice.error({
                   title: '警告',
                   desc: 'ddl-dml-无法连接到Inception!'
                 })
                 this.validate_gen = true
               }
              })
              .catch(error => {
               util.ajanxerrorcode(this, error)
              })
          } else {
            this.$Message.error('请填写sql语句后再测试!');
          }
       }
      })
    },
    SubmitSQL () {
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          if (this.formItem.textarea_ddl_dml || this.formItem.textarea_backup) {
            this.validate_gen = true
            this.datalist.sqllist_ddl = ''
            this.datalist.sqllist_backup = ''
            if (this.formItem.textarea_ddl_dml) {
                this.datalist.sqllist_ddl = this.formItem.textarea_ddl_dml.replace(/--.*\n/g, '').replace(/(;|；)$/gi, '').replace(/\s/g, ' ').replace(/；/g, ';').split(';')
            }
            if (this.formItem.textarea_backup) {
                this.datalist.sqllist_backup = this.formItem.textarea_backup.replace(/--.*\n/g, '').replace(/(;|；)$/gi, '').replace(/\s/g, ' ').replace(/；/g, ';').split(';')
            }
            axios.post(`${util.url}/sqlsyntax/`, {
                'data': JSON.stringify(this.formItem),
                'sql': JSON.stringify(this.datalist.sqllist_ddl),
                'backup_sql': JSON.stringify(this.datalist.sqllist_backup),
                'user': Cookies.get('user'),
                'type': 1,
                'id': this.id[0].id
              })
              .then(res => {
                this.$Notice.success({
                  title: '成功',
                  desc: res.data
                })
                // this.validate_gen = !this.validate_gen
                this.validate_gen = true
                this.ClearForm()
              })
              .catch(error => {
                util.ajanxerrorcode(this, error)
              })
          } else {
            this.$Message.error('请填写sql语句后再提交!');
          }
        } else {
          this.$Message.error('表单验证失败!');
        }
      })
    },
    ClearForm () {
      this.$refs['formItem'].resetFields();
      this.formItem.textarea_ddl_dml = '';
      this.formItem.textarea_backup = '';
      this.Testresults = '';
      this.Testresults_backup = ''
    }
  },
  mounted () {
    axios.put(`${util.url}/workorder/connection`)
      .then(res => {
        this.item = res.data['connection']
        this.assigned = res.data['person']
      })
      .catch(error => {
        util.ajanxerrorcode(this, error)
      })
    }
}
</script>
