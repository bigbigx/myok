<style lang="less">
  @import '../../styles/common.less';
  @import '../Order/components/table.less';
  .top{
    padding: 10px;
    background: rgba(0, 153, 229, .7);
    color: #fff;
    text-align: center;
    border-radius: 2px;
  }
</style>
<template>
  <div>
    <Row>
      <Card>
        <p slot="title" style="height: 45px">
          <Icon type="android-send"></Icon>
          工单{{ this.$route.query.workid }}详细信息
          <br>
          <Button type="text" v-if="this.$route.query.status === 0 && this.$route.query.type === 1" @click.native="PutData()">修改工单SQL</Button>
          <Button type="text" v-if="this.$route.query.status === 0" @click.native="delorder()">工单撤销</Button>
          <Button type="text" v-if="this.$route.query.status === 2" @click.native="delorder()">撤销</Button>
          <Button type="text"  @click.native="$router.go(-1)">返回</Button>
        </p>
        <Row>
          <Col span="24">
            <Table border :columns="tabcolumns" :data="TableDataNew" class="tabletop" style="background: #5cadff" size="large"></Table>
          </Col>
        </Row>
      </Card>
    </Row>
    <BackTop :height="100" :bottom="200">
      <div class="top">返回顶端</div>
    </BackTop>

    <Modal v-model="reloadsql" width="800">
      <Row>
        <Card>
          <div class="step-header-con">
            <h3 style="margin-left: 35%">蜜罐运维平台SQL审核工单</h3>
          </div>
          <p class="step-content"></p>
          <Form  ref="formItem" :model="formItem" :rules="ruleValidate"  class="step-form" :label-width="100">
            <FormItem label="工单ID:">
              <p>{{formItem.id}}</p>
            </FormItem>
            <FormItem label="受影响应用系统:">
              <p>{{formItem.system}}</p>
            </FormItem>
            <FormItem label="提交人:">
              <p>{{formItem.username}}</p>
            </FormItem>
            <FormItem label="审核人:">
              <p>{{formItem.approve_man}}</p>
            </FormItem>
            <FormItem label="机房:">
              <p>{{formItem.computer_room}}</p>
            </FormItem>
            <FormItem label="连接名:">
              <p>{{formItem.connection_name}}</p>
            </FormItem>
            <FormItem label="数据库库名:">
              <p>{{formItem.basename}}</p>
            </FormItem>
            <FormItem label="数据库编号:">
              <p>{{formItem.base_id}}</p>
            </FormItem>
            <FormItem label="执行SQL:" prop="sql">
              <template v-if="sqltype===0">
              <Input v-model="sql" type="textarea" :rows="8"></Input>
              </template>
              <template v-else>
                <p v-for="i in ddlsql">{{i}}</p>
              </template>
            </FormItem>
            <FormItem label="备份SQL:">
              <template v-if="sqltype===0">
              <Input v-model="backup_sql" type="textarea" :rows="8"></Input>
              </template>
              <template v-else>
                <p v-for="j in baksql">{{j}}</p>
              </template>
            </FormItem>
            <FormItem label="工单提交说明:">
              <Input v-model="formItem.text" placeholder="最多不超过20个字"></Input>
            </FormItem>
            <!--<FormItem label="是否备份">-->
              <!--<RadioGroup v-model="formItem.backup">-->
                <!--<Radio label="1">是</Radio>-->
                <!--<Radio label="0">否</Radio>-->
              <!--</RadioGroup>-->
            <!--</FormItem>-->
          </Form>
        </Card>
      </Row>
      <div>
         <p align:center>执行SQL 检测结果</p>
         <Table :columns="columnsName" :data="Testresults_ddl" highlight-row></Table>
      </div>
      <div>
         <p align:center>执行SQL Explain结果</p>
         <Table :columns="columnsName_explain" :data="Testresults_ddl_explain" highlight-row></Table>
      </div>
      <div>
         <p align:center>备份SQL 检测结果</p>
         <Table :columns="columnsName" :data="Testresults_backup" highlight-row></Table>
      </div>
      <div>
         <p align:center>备份SQL Explain结果</p>
         <Table :columns="columnsName_explain" :data="Testresults_backup_explain" highlight-row></Table>
      </div>

      <div slot="footer">
         <Row>
            <Col span="12" style="text-align: left;">
                 <Button type="default" @click="cancel_button">取消</Button>
           <Button type="default" icon="trash-a" @click.native="_Beauty" style="margin-left: 10%">美化</Button>
            </Col>
            <Col span="12">

                <Button type="warning" icon="android-search" @click.native="_Test" style="margin-left: 10%">检测</Button>
                <Button type="warning" icon="android-search" @click.native="_Explain" style="margin-left: 10%">Explain</Button>
                <Button type="success" icon="ios-redo" @click.native="_Putorder" style="margin-left: 10%"  :disabled="this.validate_gen_new">提交</Button>
            </Col>
         </Row>
       </div>


    </Modal>
  </div>
</template>

<script>
import util from '../../libs/util'
import axios from 'axios'
import Cookies from 'js-cookie'
export default {
  name: 'myorder-list',
  data () {
    return {
      validate_gen_new: true,
      tabcolumns: [
        {
          title: 'sql语句',
          key: 'sql',
          width: 550
        },
        {
          title: '备份语句',
          key: 'backup_sql',
          width: 550
        }
      ],
      columnsName_explain: [
        {
          title: 'SelectType',
          key: 'select_type'
        },
        {
          title: 'Table',
          key: 'table'
        },
        {
          title: 'Type',
          key: 'type'
        },
        {
          title: 'Possiblekeys',
          key: 'possiblekeys'
        },
        {
          title: 'Key',
          key: 'key'
        },
        {
          title: 'KeyLen',
          key: 'key_len'
        },
        {
          title: 'Ref',
          key: 'ref'
        },
        {
          title: 'Rows',
          key: 'rows'
        },
        {
          title: 'Extra',
          key: 'extra'
        }
      ],
      TableDataNew: [],
      sql: '',
      ruleValidate: {
        sql: [{
          required: true,
          message: '执行SQL不得为空',
          trigger: 'blur'
        }]
      },
      backup_sql: '',
      openswitch: false,
      single: false,
      reloadsql: false,
      formItem: {
        computer_room: '',
        connection_name: '',
        basename: '',
        username: '',
        approve_man: '',
        bundle_id: null
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
      Testresults_ddl: [],
      Testresults_ddl_explain: [],
      Testresults_backup_explain: [],
      ddlsql: [],
      baksql: [],
      sqltype: null,
      dmlorddl: null,
      run_type: 0
    }
  },
  methods: {
     DelOrder () { // 删除已经被驳回的工单
      axios.delelte(`${util.url}/detail`, {'id': this.$route.query.id})
        .then(res => {
            this.$Notice.info({
              title: '通知',
              desc: '工单已撤销成功'
            })
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    cancel_button () {
      this.reloadsql = false
    },
    _Explain () {
      this.$refs['formItem'].validate((valid) => {
        console.log(valid, 'jianglb')
        if (valid) {
          if (this.formItem.backup_sql || this.formItem.sql) {
            let tmpddl2 = ''
            // let tmpddl = ''
            // let tmpbak = ''
            let tmpbak2 = ''
            if (this.formItem.backup_sql) {
              tmpbak2 = this.formItem.backup_sql.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
              // tmpbak = this.formItem.textarea_backup.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
              // tmpbak = ''
            }
            if (this.formItem.sql) {
              tmpddl2 = this.formItem.sql.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
              // tmpddl = this.formItem.textarea_ddl_dml.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
              // tmpddl = ''
            }
            // console.log(tmpddl2 + '&&&' + tmpbak2, 'test')
            axios.put(`${util.url}/sqlsyntax/explain`, {
              'id': this.formItem.base_id,
              'base': this.formItem.basename,
              'type': 1,
              'sql': tmpddl2 + '&&&' + tmpbak2
            }).then(res => {
                console.log(res.data, 'newtest')
                if (res.data.status === 200) {
                  this.Testresults_ddl_explain = res.data.result_ddl_explain
                  this.Testresults_backup_explain = res.data.result_bak_explain
                  this.Testresults_backup_explain_error = '';
                  this.Testresults_explain_error = '';
                  this.validate_gen_new = false;
                  this.run_type = 1;
                } else if (res.data.status === 202) {
                   console.log(res.data, 'new1')
                    this.$Notice.error({
                    title: '执行语句错误',
                    desc: res.data.data_ddl,
                    duration: 15
                 })
                   // this.Testresults_explain = '';
                   this.Testresults_explain_error = res.data.err_msg;
                   // this.Testresults_backup_explain_error = '';
                   this.validate_gen_new = true;
                } else if (res.data.status === 203) {
                  // console.log(res.data, 'new1')
                  this.$Notice.error({
                    title: '备份语句错误',
                    desc: res.data.data_bak,
                    duration: 15
                 })
                   this.Testresults_backup_explain = '';
                   this.Testresults_backup_explain_error = res.data.err_msg;
                   this.Testresults_explain_error = '';
                   this.validate_gen_new = true;
                } else {
                  this.$Notice.error({
                   title: '错误-1',
                   desc: '未知的错误'
                 })
                  this.validate_gen_new = true;
               }
              })
              .catch((error) => {
                alert('error')
                  this.$Notice.error({
                    title: '错误',
                    desc: error
                  })
              })
          } else {
            this.$Message.error('请填写sql语句后再测试!');
          }
        }
      })

    },
    _Beauty () {
      axios.put(`${util.url}/sqlsyntax/beautify`, {
          'data1': this.sql || '',
          'data2': this.backup_sql || ''
        })
        .then(res => {
          this.sql = res.data.select
          this.backup_sql = res.data.dml_ddl
        })
        .catch(error => {
          this.$Notice.error({
            title: '警告',
            desc: error
          })
        })
    },
    _Test () {
          if (this.sql || this.backup_sql) {
            console.log(this.validate_gen_new, '...')
            let tmpddl2 = ''
            let tmpddl = ''
            let tmpbak = ''
            let tmpbak2 = ''
            if (this.backup_sql) {
                tmpbak2 = this.backup_sql.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
                tmpbak = this.backup_sql.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
                tmpbak = ''
            }
            if (this.sql) {
                tmpddl2 = this.sql.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
                tmpddl = this.sql.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
                tmpddl = ''
            }
            axios.put(`${util.url}/sqlsyntax/test`, {
                'id': this.formItem.id,
                'base': this.formItem.basename,
                'type': 2,
                'base_id': this.formItem.base_id,
                'sql': tmpddl + '&&&' + tmpbak,
                'check_sql': tmpddl2 + '&&&' + tmpbak2
              })
              .then(res => {
               if (res.data.status === 200) {
                 this.Testresults_ddl = res.data.result_ddl
                 this.Testresults_backup = res.data.result_bak
                 let gen1 = 0
                 let gen11 = 0
                 this.Testresults_ddl.forEach(vl => {
                   if (vl.errlevel !== 0) {
                     gen1 += 1
                   }
                 })
                 this.Testresults_backup.forEach(v2 => {
                   if (v2.errlevel !== 0) {
                     gen11 += 1
                   }
                 })
                 if (gen1 === 0 && gen11 === 0) {
                   this.validate_gen_new = false
                 } else {
                   this.validate_gen_new = true
                 }
               } else if (res.data.status === 202) {
                 this.$Notice.error({
                   title: '警告',
                   desc: res.data.result
                 })
                 this.validate_gen_new = true
               } else {
                 this.$Notice.error({
                   title: '警告',
                   desc: 'ddl-dml-无法连接到Inception!'
                 })
                 this.validate_gen_new = true
               }
              })
              .catch(error => {
               util.ajanxerrorcode(this, error)
              })
          } else {
            this.$Message.error('请填写sql语句后再测试!');
          }
          console.log(this.validate_gen_new, '...22222')
    },
    PutData () {
      this.validate_gen_new = true
      axios.put(`${util.url}/detail`, {
       'id': this.$route.query.id
       })
        .then(res => {
          this.formItem = res.data.data
          this.sql = res.data.sql
          this.backup_sql = res.data.backup_sql
          this.sqltype = res.data.type
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
      this.reloadsql = true
    },
    _Putorder () {
      if (this.sqltype === 0) {
        let _tmpsql = this.sql.replace(/(;|；)$/gi, '').replace(/\s/g, ' ').replace(/；/g, ';').split(';')
        let _tmpsqlbak = this.backup_sql.replace(/(;|；)$/gi, '').replace(/\s/g, ' ').replace(/；/g, ';').split(';')
        axios.post(`${util.url}/sqlsyntax/`, {
          'data': JSON.stringify(this.formItem),
          'sql': JSON.stringify(_tmpsql),
          'backup_sql': JSON.stringify(_tmpsqlbak),
          'apply_man': Cookies.get('user'),
          'type': this.dmlorddl,
          'run_type': this.run_type,
          'cc_list': [],
          'id': this.formItem.bundle_id
        })
          .then(() => {
            this.$Notice.info({
              title: '通知',
              desc: '工单已提交成功'
            })
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
          this.delorder()
          this.reloadsql = false
      } else {
        axios.post(`${util.url}/sqlsyntax/`, {
          'data': JSON.stringify(this.formItem),
          'sql': JSON.stringify(this.ddlsql),
          'backup_sql': JSON.stringify(this.baksql),
          'apply_man': Cookies.get('user'),
          'type': this.dmlorddl,
          'id': this.formItem.bundle_id
        })
          .then(() => {
            this.$Notice.info({
              title: '通知',
              desc: '工单已提交成功'
            })
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
          this.delorder()
          this.reloadsql = false
      }
    },
    delorder () {
      let _list = []
      _list.push({'status': this.$route.query.status, 'id': this.$route.query.id})
      axios.post(`${util.url}/audit_sql`, {
        'id': JSON.stringify(_list)
      })
        .then(res => {
          this.$Notice.info({
            title: '信息',
            desc: res.data
          })
          this.$router.go(-1)
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  },
  mounted () {
   axios.get(`${util.url}/detail?workid=${this.$route.query.workid}&status=${this.$route.query.status}&id=${this.$route.query.id}`)
     .then(res => {
       this.TableDataNew = res.data.data
       this.dmlorddl = res.data.type
     })
     .catch(error => {
       this.$Notice.error({
         title: '警告',
         desc: error
       })
     })
  }
}
</script>
