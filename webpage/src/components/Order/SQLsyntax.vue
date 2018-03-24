<style lang="less">
@import '../../styles/common.less';
@import 'components/table.less';
</style>

<template>
<div>
  <Row>
    <Col span="6">
    <Card>
      <p slot="title">
        <Icon type="ios-redo"></Icon>
        选择数据库
      </p>
      <div class="edittable-test-con">
        <div id="showImage" class="margin-bottom-10">

          <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="机房:" prop="computer_room">
              <Select v-model="formItem.computer_room" @on-change="Connection_Name">
              <Option v-for="i in datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
            </Select>
            </FormItem>

            <FormItem label="连接名:" prop="connection_name">
              <Select v-model="formItem.connection_name" @on-change="DataBaseName" filterable>
              <Option v-for="i in datalist.connection_name_list" :value="i.connection_name" :key="i.connection_name">{{ i.connection_name }}</Option>
            </Select>
            </FormItem>

            <FormItem label="库名:" prop="basename">
              <Select v-model="formItem.basename" filterable>
              <Option v-for="item in datalist.basenamelist" :value="item" :key="item">{{ item }}</Option>
            </Select>
            </FormItem>

            <FormItem label="工单说明:" prop="text">
              <Input v-model="formItem.text" placeholder="请输入"></Input>
            </FormItem>

            <FormItem label="指定审核人:" prop="text">
              <Select v-model="formItem.assigned">
                <Option v-for="i in this.assigned" :value="i.username" :key="i.username">{{i.username}}</Option>
              </Select>
            </FormItem>

            <FormItem label="是否备份">
              <RadioGroup v-model="formItem.backup">
                <Radio label="1">是</Radio>
                <Radio label="0">否</Radio>
              </RadioGroup>
            </FormItem>

            <FormItem>
              <Button type="default" icon="paintbucket" @click.native="beautify()">美化</Button>
            </FormItem>

            <FormItem>
              <Button type="warning" icon="android-search" @click.native="test_sql()">检测</Button>
              <Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :disabled="this.validate_gen">提交</Button>
            </FormItem>

          </Form>
          <Alert style="height: 145px">
            检测表字段提示信息
            <template slot="desc">
                <p>1.错误等级 0正常,1警告,2错误。</p>
                <p>2.阶段状态 审核成功,Audit completed</p>
                <p>3.错误信息 用来表示出错错误信息</p>
                <p>4.当前检查的sql</p>
                <p>注:只有错误等级等于0时提交按钮才会激活</p>
              </template>
          </Alert>
        </div>
      </div>
    </Card>
    </Col>
    <Col span="18" class="padding-left-10">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        填写备份SQL语句 (备份SQL编辑框)
      </p>
      <Input v-model="formItem.textarea_backup" type="textarea" :autosize="{minRows: 10,maxRows: 15}" placeholder="请输入需要提交的SQL语句,多条sql请用;分隔" autocomplete="on"></Input>
      <br>
      <Table :columns="columnsName" :data="Testresults_backup" highlight-row></Table>
    </Card>

        <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        填写执行SQL语句 (执行SQL编辑框)
      </p>
      <Input v-model="formItem.textarea_ddl_dml" type="textarea" :autosize="{minRows: 15,maxRows: 15}" placeholder="请输入需要提交的SQL语句,多条sql请用;分隔" autocomplete="on"></Input>
      <br>
      <br>
      <Table :columns="columnsName" :data="Testresults" highlight-row></Table>
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
  name: 'SQLsyntax',
  data () {
    return {
      validate_gen: true,
      formItem: {
        textarea: '',
        computer_room: '',
        connection_name: '',
        basename: '',
        text: '',
        backup: 0,
        assigned: ''
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
        basenamelist: [],
        sqllist: [],
        computer_roomlist: util.computer_room
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
    beautify () {
      axios.put(`${util.url}/sqlsyntax/beautify`, {
          'data1': this.formItem.textarea_backup || '',
          'data2': this.formItem.textarea_ddl_dml || ''
        })
        .then(res => {
          // console.log(res)
          // console.log(res.data.select)
          // console.log(res.data.dml_ddl)
          this.formItem.textarea_backup = res.data.select
          this.formItem.textarea_ddl_dml = res.data.dml_ddl
        })
        .catch(error => {
          this.$Notice.error({
            title: '警告',
            desc: error
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
