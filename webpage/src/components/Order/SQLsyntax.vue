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
            <FormItem label="机房:" prop="computer_room" v-if="!this.choose_db">
              <Select v-model="formItem.computer_room" @on-change="Connection_Name">
              <Option v-for="i in datalist.computer_roomlist" :value="i">{{i}}</Option>
            </Select>
            </FormItem>
            <FormItem label="机房:" prop="computer_room" v-else="this.choose_db">
              <Input  v-model="formItem.computer_room" disabled></Input>
            </FormItem>
            <FormItem label="连接名:" prop="connection_name" v-if="!this.choose_db">
              <Select v-model="formItem.connection_name" @on-change="DataBaseName"  filterable>
              <Option v-for="i in datalist.connection_name_list" :value="i.connection_name">{{ i.connection_name }}</Option>
              </Select>
            </FormItem>
            <FormItem label="连接名:" prop="connection_name" v-else="this.choose_db">
              <Input  v-model="formItem.connection_name" disabled></input>
            </FormItem>

            <FormItem label="库名:" prop="basename" v-if="!this.choose_db">
              <Select v-model="formItem.basename">
              <Option v-for="item in datalist.basenamelist" :value="item">{{ item }}</Option>
            </Select>
            </FormItem>
            <FormItem label="库名:" prop="basename" v-else="this.choose_db">
              <Input  v-model="formItem.basename" disabled></input>
            </FormItem>


            <FormItem label="工单说明:" prop="text">
              <Input type="textarea" :rows="8" v-model="formItem.text" placeholder="请输入"></Input>
            </FormItem>

            <FormItem label="指定审核人:" prop="text">
              <Select v-model="formItem.assigned">
                <Option v-for="i in this.assigned" :value="i.username" :key="i.username">{{i.username}}</Option>
              </Select>
            </FormItem>

            <!--<FormItem label="指定邮件抄送人:" prop="text">-->
              <!--<Select v-model="formItem.assigned">-->
                <!--<Option v-for="i in this.assigned" :value="i.username" :key="i.username">{{i.username}}</Option>-->
              <!--</Select>-->
            <!--</FormItem>-->

            <FormItem label="是否备份: ">
              <RadioGroup v-model="formItem.backup">
                <Radio label="1" default>是</Radio>
                <Radio label="0">否</Radio>
              </RadioGroup>
            </FormItem>
            <FormItem label="快速选库: ">
              <Button type="default" icon="ios-redo" @click.native="ChooseLaimiOnline()"  :enabled="this.validate_gen1">线上laimi库</Button>
              <Button type="default" icon="ios-redo" @click.native="ChooseActivityOnline()"  :enabled="this.validate_gen1">线上activity库</Button>
              <Button type="default" icon="ios-redo" @click.native="ChooseMylaimi()"  :enabled="this.validate_gen1">我的测试库</Button>
              <Button type="default" icon="ios-redo" @click.native="ReChooseDB()"  :enabled="this.validate_gen1">重新选择</Button>
          </FormItem>
            <br>
            <FormItem label="SQL检查: ">
              <Button type="default" icon="paintbucket" @click.native="beautify()">美化</Button>
              <Button type="default" icon="android-search" style="margin-left: 10%" @click.native="test_sql_1()">检测</Button>
            </FormItem>


            <FormItem label="工单提交: ">
              <Button type="success" icon="ios-redo" @click.native="SubmitSQL()"   :disabled="this.validate_gen">工单提交</Button>
            </FormItem>
            <FormItem label="选项: ">
              <Checkbox v-model="single"  @click.native="show_explain_div()" >高级</Checkbox><p></p>
              <Button type="primary" icon="ios-redo" @click.native="explain_test()"    v-if="this.single">explain</Button>
              <Button type="primary" icon="android-search" style="margin-left: 10%" @click.native="sqladvisor()" v-if="this.single">优化</Button>
            </FormItem>

          </Form>
          <Alert style="height: 250px">
            检测表字段提示信息
            <template slot="desc">
                <p>1.错误等级 0正常,1警告,2错误。</p>
                <p>2.阶段状态 审核成功,Audit completed</p>
                <p>3.错误信息 用来表示出错错误信息</p>
                <p>4.当前检查的sql</p>
                <p>5.选项"高级":</p>
                <p>     1).有对SQL的explain和优化检查,可以作为参考项检查，特别针对复杂SQL的语法检查</p>
                <p>     2).通过检测检查SQL报错，可以执行explain按钮进行检查</p>
                <p>注:只有错误等级等于0时提交按钮才会激活</p>
              </template>
          </Alert>
        </div>
      </div>
    </Card>
    </Col>
    <Col span="18" class="padding-left-10" v-if="formItem.backup == 1">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        填写备份SQL语句 (备份SQL编辑框)
      </p>
      <Input v-model="formItem.textarea_backup" type="textarea" :autosize="{minRows: 10,maxRows: 15}" placeholder="请输入需要提交的SQL语句,多条sql请用;分隔" autocomplete="on"></Input>
      <Table :columns="columnsName" :data="Testresults_backup" highlight-row></Table>
      <Table :columns="columnsName_explain" :data="Testresults_backup_explain" highlight-row></Table>
      <!--<Table :columns="columnsName_explain_error" :data="Testresults_backup_explain_error" highlight-row></Table>-->
      <br>
    </Card>
       <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        填写执行SQL语句 (执行SQL编辑框)
      </p>
      <Input v-model="formItem.textarea_ddl_dml" type="textarea" :autosize="{minRows: 15,maxRows: 15}" placeholder="请输入需要提交的SQL语句,多条sql请用;分隔" autocomplete="on"></Input>
      <Table :columns="columnsName" :data="Testresults" highlight-row></Table>
      <Table :columns="columnsName_explain" :data="Testresults_explain" highlight-row></Table>
      <!--<Table :columns="columnsName_explain_error" :data="Testresults_explain_error" highlight-row></Table>-->

    </Card>
  </Col>
    <Col span="18" class="padding-left-10" v-if="formItem.backup == 0">
    <Card>
      <p slot="title">
        <Icon type="ios-crop-strong"></Icon>
        填写执行SQL语句 (执行SQL编辑框)
      </p>
      <Input v-model="formItem.textarea_ddl_dml" type="textarea" :autosize="{minRows: 15,maxRows: 15}" placeholder="请输入需要提交的SQL语句,多条sql请用;分隔" autocomplete="on"></Input>
      <Table :columns="columnsName" :data="Testresults" highlight-row></Table>
      <Table :columns="columnsName_explain" :data="Testresults_explain" highlight-row></Table>
      <!--<Table :columns="columnsName_explain_error" :data="Testresults_explain_error" highlight-row></Table>-->
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
      validate_gen1: true,
      formItem: {
        textarea: '',
        computer_room: '',
        connection_name: '',
        basename: '',
        text: '',
        backup: 1,
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
      //  columnsName_explain_error: [
      //  {
      //     title: 'SQL报错信息',
      //     key: 'err_msg',
      //     width: '350'
      //   }
      // ],
      columnsName_explain: [
        {
          title: 'SelectType',
          key: 'select_type',
          width: '100'
        },
        {
          title: 'Table',
          key: 'table',
          width: '100'
        },
        {
          title: 'Type',
          key: 'type',
          width: '100'
        },
        {
          title: 'Possiblekeys',
          key: 'possiblekeys',
          width: '150'
        },
        {
          title: 'Key',
          key: 'key',
          width: '80'
        },
        {
          title: 'KeyLen',
          key: 'key_len'
        },
        {
          title: 'Ref',
          key: 'ref',
          width: '130'
        },
        {
          title: 'Rows',
          key: 'rows',
          width: '80'
        },
        {
          title: 'Extra',
          key: 'extra',
          width: '130'
        }
      ],
      Testresults: [],
      Testresults_backup: [],
      Testresults_explain: [],
      Testresults_backup_explain: [],
      Testresults_backup_explain_error: [],
      Testresults_explain_error: [],
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
      assigned: [],
      flag: false,
      single: false,
      validate_result: false,
      choose_db: false
    }
  },
  methods: {
    show_explain_div () {
      if (this.single) {
        this.validate_result = true
      } else {
        this.validate_result = false
      }
    },
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
      if (val) {
        this.ScreenConnection(val)
      } else {
        this.datalist.connection_name_list = [];
      }
      if (this.flag) return;
      this.datalist.basenamelist = [];
      this.formItem.connection_name = '';
      this.formItem.basename = '';
    },
    ScreenConnection (val) {
      this.datalist.connection_name_list = this.item.filter(item => {
        if (item.computer_room === val) {
          return item
        }
      })
    },
    ChooseMylaimi () {
          axios.put(`${util.url}/workorder/quickbasename`, {
            'url': '101.236.41.66',
            'basename': 'laimi_test'
          })
          .then(res => {
              console.log(res.data)
              this.flag = true;
              this.choose_db = true;
              this.formItem.computer_room = res.data['computer_room'];
              this.formItem.connection_name = res.data['connection_name'];
              this.formItem.basename = res.data['laimi_db'];
              this.id = [res.data['id']];
              this.$nextTick(() => {
                this.flag = false;
              });
            if (res.data.status === 202) {
              this.$Notice.error({
              title: '警告',
              desc: res.data['msg']
            })
            }
          })
          .catch((error) => {
            this.$Notice.error({
              title: '警告',
              desc: error
            })
          })
    },
    ChooseActivityOnline () {
        axios.put(`${util.url}/workorder/quickbasename`, {
            'url': 'rm-m5eb3mg98au6s55xpo.mysql.rds.aliyuncs.com',
            'basename': 'laimi_activity'
          })
          .then(res => {
              console.log(res.data)
              this.flag = true;
              this.choose_db = true;
              this.formItem.computer_room = res.data['computer_room'];
              this.formItem.connection_name = res.data['connection_name'];
              this.formItem.basename = res.data['laimi_db'];
              this.id = [res.data['id']];
              this.$nextTick(() => {
                this.flag = false;
              });
            if (res.data.status === 202) {
              this.$Notice.error({
              title: '警告',
              desc: res.data['msg']
            })
            }
          })
          .catch((error) => {
            this.$Notice.error({
              title: '警告',
              desc: error
            })
          })
    },
    ReChooseDB () {
      this.choose_db = false;
      this.id = null;
    },
    ChooseLaimiOnline (val) {
        axios.put(`${util.url}/workorder/quickbasename`, {
            'url': 'rds6qxe126phmtspwi72o.mysql.rds.aliyuncs.com',
            'basename': 'laimi'
          })
          .then(res => {
              console.log(res.data)
              this.flag = true;
              this.choose_db = true;
              this.formItem.computer_room = res.data['computer_room'];
              this.formItem.connection_name = res.data['connection_name'];
              this.formItem.basename = res.data['laimi_db'];
              this.id = [res.data['id']];
              this.$nextTick(() => {
                this.flag = false;
              });
            if (res.data.status === 202) {
              this.$Notice.error({
              title: '警告',
              desc: res.data['msg']
            })
            }
          })
          .catch((error) => {
            this.$Notice.error({
              title: '警告',
              desc: error
            })
          })
    },
    DataBaseName (index) {
      if (index) {
        this.id = this.item.filter(item => {
          if (item.connection_name === index) {
            return item
          }
        });
        axios.put(`${util.url}/workorder/basename`, {
            'id': this.id[0].id
          })
          .then(res => {
            console.info(res.data)
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
    //  sql 的explain执行输出
    explain_test: function () {
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          if (this.formItem.textarea_ddl_dml || this.formItem.textarea_backup) {
            let tmpddl2 = '';
            let tmpddl = '';
            let tmpbak = '';
            let tmpbak2 = '';
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
            console.log(this.formItem)
            axios.put(`${util.url}/sqlsyntax/explain`, {
              'id': this.id[0].id,
              'base': this.formItem.basename,
              'type': 1,
              'sql': tmpddl + '&&&' + tmpbak,
              'check_sql': tmpddl2 + '&&&' + tmpbak2
            })
              .then(res => {
                console.log(res.data)
                if (res.data.status === 200) {
                  this.Testresults_explain = res.data.result_ddl_explain
                  this.Testresults_backup_explain = res.data.result_bak_explain
                  this.Testresults_backup_explain_error = '';
                  this.Testresults_explain_error = '';
                } else if (res.data.status === 202) {
                    this.$Notice.error({
                    title: '执行语句错误',
                    desc: res.data.err_msg
                 })
                   this.Testresults_explain = '';
                   this.Testresults_explain_error = res.data.err_msg;
                   this.Testresults_backup_explain_error = '';
                } else if (res.data.status === 203) {
                  this.$Notice.error({
                    title: '备份语句错误',
                    desc: res.data.err_msg
                 })
                   this.Testresults_backup_explain = '';
                   this.Testresults_backup_explain_error = res.data.err_msg;
                   this.Testresults_explain_error = '';
                } else {
                  this.$Notice.error({
                   title: '错误-1',
                   desc: '未知的错误'
                 })
               }
              })
              .catch((error) => {
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
    // 同时检查  备份栏只能是select语句，ddl栏只能是非select语句
    test_sql_1 () {
      this.$refs['formItem'].validate((valid) => {
        console.log(valid)
        if (valid) {
          console.log(this.formItem.textarea_ddl_dml)
          console.log(this.formItem.textarea_backup)
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
            console.log('this id value', this.id)
            // debugger
            // console.log('axios.put', `${util.url}/sqlsyntax/test`, axios.put)

            // axios.put(`${util.url}/sqlsyntax/test`, { 'id': '1' })
            // debugger
            // console.log('this.id[0].id ---------------584', this  )
            // console.log('this.id[0].id ---------------583', this.id[0].id)
            var param = {
                'id': this.id[0].id,
                'base': this.formItem.basename,
                'type': 1,
                'sql': tmpddl + '&&&' + tmpbak,
                'check_sql': tmpddl2 + '&&&' + tmpbak2
              };
            console.log('string param  591', param)
            axios.put(`${util.url}/sqlsyntax/test`, param)
              .then(res => {
               console.log(res.data)
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
            console.log('end')
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
      });
    window.vm = this;
    }
}
</script>
