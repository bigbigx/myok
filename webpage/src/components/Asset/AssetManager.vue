<style lang="less">
@import '../../styles/common.less';
@import '../common/table.less';
</style>

<template>
<div>
  <Row>
    <Col span="18" id="aliyun" class="padding-left-10">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        添加资产
      </p>
       <div class="edittable-test-con">
        <div id="show_Aliyun" class="margin-bottom-10" >
          <Form ref="formItem" :model="formItem"  :label-width="80">
            <FormItem label="机房:" prop="computer_room">
               <Tag  checkable color="blue" v-for="i in datalist.room_list" >{{i}}</Tag>
            </FormItem>
            <FormItem label="所在局域:" prop="area">
              <Tag  checkable color="blue" v-for="i in datalist.area_list" >{{i}}</Tag>
            </FormItem>

            <FormItem label="设备类型:" prop="device_type">
              <Select v-model="formItem.device_type"  filterable>
              <Option>dasds</Option>
            </Select>
            </FormItem>
          </Form>
         </div>
      </div>
      </Card>
    </Col>
    <Col span="6">
    <Card>
      <p slot="title">
        <Icon type="ios-redo"></Icon>
        请选择机房
      </p>
      <div class="edittable-test-con">
        <div id="showJifang" class="margin-bottom-10">

          <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="80">

            <FormItem>
              <Button type="warning" icon="android-search" @click.native="alive_check">检测</Button>
              <Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :disabled="this.validate_gen">添加</Button>
            </FormItem>
          </Form>
          <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="80">
          <FormItem>
            <Button type="warning" icon="android-search" @click.native="Onekey_search()">自动搜索</Button>
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
      room_name: '',
      datalist: {
        room_list: [],
        area_list: [],
        device_type: []
        // computer_roomlist: util.computer_room
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
    }
  },

  mounted () {
        axios.get(`${util.url}/assets?room=Aliyun`)
        .then(res => {
          this.datalist = res.data
          // this.formItem = res.data.data
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
}
</script>
