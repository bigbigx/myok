<style lang="less">
@import '../../styles/common.less';
@import '../common/table.less';
</style>

<template>
<div>
  <Row>
    <Col span="6">
    <Card>
      <p slot="title">
        <Icon type="ios-redo"></Icon>
        资产配置
      </p>
      <div class="edittable-test-con">
        <div id="showJifang" class="margin-bottom-10">

          <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="机房:" prop="computer_room">
              <Select v-model="formItem.computer_room" @on-change="show_tab_and_quyu">
              <Option v-for="i in datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="所在局域:" prop="connection_name">
              <Select v-model="formItem.area_name"  filterable>
              <Option v-for="i in datalist.area_list" :value="i.area_name" :key="i.area_name">{{ i.area_name }}</Option>
            </Select>
            </FormItem>

            <FormItem label="设备类型:" prop="device_type">
              <Select v-model="formItem.device_type"  filterable>
              <Option v-for="i in datalist.area_list" :value="i.device_type" :key="i.device_type">{{ i.device_type }}</Option>
            </Select>
            </FormItem>


            <FormItem>
              <Button type="warning" icon="android-search" @click.native="alive_check">检测</Button>
              <Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :disabled="this.validate_gen">添加</Button>
            </FormItem>

          </Form>
          <Alert style="height: 90px">
            "添加" 按钮
            <template slot="desc">
                <p>1、在填写完整信息后此按钮才可用</p>

                <p></p>
              </template>
          </Alert>
          <Alert style="height: 130px">
            "自动搜索" 按钮
            <template slot="desc">
                <p>1、自动检查存活而且没有添加的服务器</p>
                <p>2、点击按钮前请选择机房和区域</p>
                <p>3、点击按钮后在右边会出现搜索到的服务器</p>
                <p></p>
              </template>
          </Alert>
          <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="80">
          <FormItem>
            <Button type="warning" icon="android-search" @click.native="Onekey_search()">自动搜索</Button>
          </FormItem>
          </Form>
        </div>
      </div>
    </Card>
    </Col>
    <Col span="18" id="aws" class="padding-left-10" v-if="this.formItem.computer_room==='AWS'">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        细节配置--美团云机房
      </p>
       <div class="edittable-test-con" >
        <div id="show_AWS" class="margin-bottom-10" >
          <Form ref="formItem_aws" :model="formItem_ali"  :label-width="80">
            <FormItem label="CPU型号:" prop="computer_room">
              <Select v-model="formItem.computer_room">
              <Option v-for="i in datalist.cpu_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="内存:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.mem_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>


            <FormItem label="硬盘:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
          </Form>
         </div>
       </div>
      </Card>
    </Col>

    <Col span="18" id="aliyun" class="padding-left-10"  v-else-if="this.formItem.computer_room==='Aliyun'">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        细节配置--阿里云机房
      </p>
       <div class="edittable-test-con">
        <div id="show_Aliyun" class="margin-bottom-10" >
          <Form ref="formItem_ali" :model="formItem_ali"  :label-width="80">

            <FormItem label="资产名称:" prop="computer_room">
              <Select v-model="formItem.computer_room">
              <Option v-for="i in datalist.cpu_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="CPU型号:" prop="computer_room">
              <Select v-model="formItem.computer_room">
              <Option v-for="i in datalist.cpu_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="内存:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.mem_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>


            <FormItem label="硬盘:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
            <FormItem label="硬盘11:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
          </Form>
         </div>
      </div>
      </Card>
    </Col>

    <Col span="18"  class="padding-left-10"  v-else-if="this.formItem.computer_room==='Own'">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        细节配置--独立机房
      </p>
       <div class="edittable-test-con">
        <div id="show_Own" class="margin-bottom-10" >
          <Form ref="formItem_own" :model="formItem_own"  :label-width="80">

            <FormItem label="资产名称:" prop="asset_name">
              <Input v-model="formItem.text" placeholder="请输入"></Input>
            </FormItem>

            <FormItem label="CPU型号:" prop="computer_room">
              <Select v-model="formItem.computer_room">
              <Option v-for="i in datalist.cpu_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="内存:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.mem_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>


            <FormItem label="硬盘:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
            <FormItem label="硬盘11:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
          </Form>
         </div>
      </div>
      </Card>
    </Col>



    <Col span="18"  class="padding-left-10"  v-else-if="this.formItem.computer_room==='Other'">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        细节配置--其他机房
      </p>
       <div class="edittable-test-con">
        <div id="show_Other" class="margin-bottom-10" >
          <Form ref="formItem_ali" :model="formItem_ali"  :label-width="80">
            <FormItem label="CPU型号:" prop="computer_room">
              <Select v-model="formItem.computer_room">
              <Option v-for="i in datalist.cpu_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="内存:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.mem_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>


            <FormItem label="硬盘:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
            <FormItem label="硬盘11:" prop="computer_room">
              <Select v-model="formItem.computer_room" >
              <Option v-for="i in datalist.disk_version" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>
          </Form>
         </div>
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
  name: 'asset-manager',
  data () {
    return {
      validate_gen: true,
      formItem: {
        textarea: '',
        computer_room: '',
        area_name: '',
        device_type: '',
        text: ''
      },
      columnsName: [
        {
          title: 'ID',
          key: 'ID',
          width: '50'
        },
        {
          title: '阶段',
          key: 'stage',
          width: '100'
        },
        {
          title: '错误等级',
          key: 'errlevel',
          width: '100'
        },
        {
          title: '阶段状态',
          key: 'stagestatus',
          width: '150'
        },
        {
          title: '错误信息',
          key: 'errormessage'
        },
        {
          title: '当前检查的sql',
          key: 'sql'
        },
        {
          title: '预计影响的SQL',
          key: 'affected_rows',
          width: '130'
        }
      ],
      Testresults: [],
      Testresults_backup: [],
      item: {},
      datalist: {
        connection_name_list: [],
        area_list: [],
        device_type: [],
        computer_roomlist: util.computer_room
      },
      ruleValidate: {
        computer_room: [{
          required: true,
          message: '机房地址不得为空',
          trigger: 'change'
        }],
        area_name: [{
          required: true,
          message: '所属区域不得为空',
          trigger: 'change'
        }],
        device_type: [{
          required: true,
          message: '设备类型不得为空',
          trigger: 'change'
        }],
        asset_name: [{
          required: true,
          message: '资产名称不得为空',
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
    show_tab_and_quyu (val) {
      if (val) {
        this.ScreenConnection(val)
        return
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
    SubmitSQL () {
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          if (this.formItem.textarea_ddl_dml || this.formItem.textarea_backup) {
            this.validate_gen = true
            axios.post(`${util.url}/assets/add`, {
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
    axios.put(`${util.url}/assets/area`)
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
