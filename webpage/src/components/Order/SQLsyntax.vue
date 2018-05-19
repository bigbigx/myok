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
              <Input  v-model="formItem.connection_name" disabled ></input>
            </FormItem>

            <FormItem label="库名:" prop="basename" v-if="!this.choose_db">
              <Select v-model="formItem.basename">
              <Option v-for="item in datalist.basenamelist" :value="item">{{ item }}</Option>
            </Select>
            </FormItem>
            <FormItem label="库名:" prop="basename" v-else="this.choose_db">
              <Input  v-model="formItem.basename" disabled ></input>
            </FormItem>

            <FormItem label="快速选库: ">
                  <RadioGroup v-model="formItem.quick_choose">
                              <Radio label="laimi_online" @click.native="ChooseDatabase({'url':'114.215.28.111','basename':'laimi','port':'32112'})" ><Icon type="social-android"></Icon><span>线上laimi库</span></Radio>
                              <Radio label="activity_online" @click.native="ChooseDatabase({'url':'114.215.28.111','basename':'laimi_activity','port':'32021'})"><Icon type="social-android"></Icon><span>线上activity库</span></Radio>
                              <Radio label="erp_online" @click.native="ChooseDatabase({'url':'114.215.28.111','basename':'laimi_erp','port':'32453'})"><Icon type="social-android"></Icon><span>线上erp库</span></Radio>
                              <Radio label="new_salesman_online" @click.native="ChooseDatabase({'url':'114.215.28.111','basename':'salesman','port':'13306'})"><Icon type="social-android"></Icon><span>线上新salesman库</span></Radio>
                              <Radio label="shopcart" @click.native="ChooseDatabase({'url':'114.215.28.111','basename':'laimi_shopcart','port':'32454'})"><Icon type="social-android"></Icon><span>线上shopcart库</span></Radio>
                              <!--<Radio label="old_salesman_online"  @click.native="ChooseDatabase({'url':'114.215.28.111','basename':'laimi_salesman','port':'23764'})"><Icon type="social-android"></Icon><span>线上老供应商salesman库</span></Radio>-->
                              <Radio label="laimi_test" @click.native="ChooseDatabase({'url':'101.236.45.42','basename':'laimi_test','port':'3306'})" ><Icon type="social-android"></Icon><span>美团云测试库</span></Radio>
                              <Radio label="my_laimi_test" @click.native="ChooseDatabase({'url':'101.236.41.66 ','basename':'laimi_test','port':'3306'})" ><Icon type="social-android"></Icon><span>我的测试库</span></Radio>
                              <!--<Radio label="custom" @click.native="ReChooseDB()"><Icon type="social-android"></Icon><span>自定义选库</span></Radio>-->
                  </RadioGroup>
              <!--<Button type="default" icon="ios-redo" @click.native="ChooseLaimiOnline()"  :enabled="this.validate_gen1">线上laimi库</Button>-->
              <!--<Button type="default" icon="ios-redo" @click.native="ChooseActivityOnline()"  style="margin-left: 10%"  :enabled="this.validate_gen1">线上activity库</Button>-->
              <!--<Button type="default" icon="ios-redo" @click.native="ChooseMylaimi()"  :enabled="this.validate_gen1">我的测试库</Button>-->
              <!--<Button type="default" icon="ios-redo" @click.native="ReChooseDB()"   style="margin-left: 10%" :enabled="this.validate_gen1">重新选择</Button>-->
          </FormItem>
            <FormItem label="是否备份: " prop="backup">
              <RadioGroup v-model="formItem.backup">
                <Radio label="1">是(默认)</Radio>
                <Radio label="0">否</Radio>
              </RadioGroup>
            </FormItem>
            <FormItem label="工单说明:" prop="text">
              <Input type="textarea" :rows="6" v-model="formItem.text" placeholder="请输入"></Input>
            </FormItem>
            <FormItem label="应用系统名称:" prop="system">
              <Tooltip placement="top">
                <Input type="textarea" :rows="1" v-model="formItem.system" placeholder="请输入"></Input>
                <div slot="content">
                  <p>请填写受影响的应用系统内容</p>
                  <p><i>如erp、tms、wms、salesman等系统</i></p>
              </div>
              </Tooltip>
            </FormItem>
            <FormItem label="指定审核人:" prop="approve_man" >
              <Select v-model="formItem.approve_man" v-if="person==2" >
                <Option v-for="i in this.approve_man" :value="i.username" :key="i.username">{{i.username}}</Option>
              </Select>
                <Input type="text"  v-model="formItem.approve_man"  disabled  v-if="person==0 || person==1"  ></Input>
               <RadioGroup v-model="person" >
                <Tooltip placement="top">
                <div slot="content">
                  <p>将提交给刘艳审核</p>
                 </div>
                 <Radio label="0" @click.native="chooseapprover('0')"><Icon type="social-apple"></Icon><span>常规审核人</span></Radio>
                 </Tooltip>
                 <Tooltip placement="top">
                <div slot="content">
                  <p>将紧急提交江理彬执行,不经过paul审核</p>
                 </div>
                 <Radio label="1" @click.native="chooseapprover('1')"><Icon type="social-apple"></Icon><span>紧急审核人</span></Radio>
                 </Tooltip>
                   <Radio label="2" @click.native="chooseapprover('2')"><Icon type="social-apple"></Icon><span>手工选人</span></Radio>
              </RadioGroup>
            </FormItem>

            <FormItem label="邮件抄送人:" >
              <Tooltip placement="top">
              <Checkbox v-model="cc_mail"  >选择(请点击)</Checkbox><p></p>
                <div slot="content">
                  <p>点击选择邮件抄送人</p>
                  <p><i>勾选选人</i></p>
              </div>
              </Tooltip>
              <p></p>
               <!--<Button type="default" icon="ios-redo" size="small" @click.native="checkbox_test()" v-if="this.cc_mail" >确定</Button>-->
              <!--<Button type="default" icon="ios-redo" size="small" @click.native="checkbox_all()" style="margin-left: 20%" v-if="this.cc_mail" >全选</Button>-->
                  <CheckboxGroup v-if="this.cc_mail" v-model="social">
                      <Checkbox v-for="k in this.cc_mail_list" :label="k.mail">
                          <Icon type="social-twitter"></Icon>
                          <span >{{k.username}}</span>
                      </Checkbox>
                  </CheckboxGroup>
            </FormItem>


            <FormItem label="SQL检查: ">
              <Tooltip placement="top">
              <Button type="default" icon="paintbucket" @click.native="beautify()">美化</Button>
                <div slot="content">
                  <p>对SQL语句进行排版</p>
              </div>
              </Tooltip>
              <Tooltip placement="top">
              <Button type="default" icon="android-search" style="margin-left: 10%" @click.native="test_sql_1()">检测</Button>
                <div slot="content">
                  <p>检测SQL语句</p>
              </div>
              </Tooltip>
            </FormItem>


            <FormItem label="工单提交: ">
              <Button type="success" icon="ios-redo" @click.native="SubmitSQL()"   :disabled="this.validate_gen">工单提交</Button>
            </FormItem>
            <FormItem label="选项: ">
              <Tooltip placement="top">
              <Checkbox v-model="single"  @click.native="show_explain_div()" >高级</Checkbox><p></p>
                <div slot="content">
                  <p>检测无法通过</p>
                  <p>可点击此高级按钮</p>
                  <p>然后点击explain按钮</p>
                  <p>只要explain正常,则工单可提交</p>
              </div>
              </Tooltip>
              <p></p>
              <Button type="primary" icon="ios-redo" @click.native="explain_test()"    v-if="this.single">explain</Button>
              <!--<Button type="primary" icon="android-search" style="margin-left: 10%" @click.native="sqladvisor()" v-if="this.single">优化</Button>-->
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
        system: '',
        text: '',
        backup: '1',
        // approve_man: 'liuyan',
        approve_man: '',
        cc_mail_list: [],
        default_ccmail: [],
        quick_choose: 'custom',
        hang_choose: false
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
        system: [{
            required: true,
            message: '受影响的应用系统不得为空',
            trigger: 'blur'
          },
          {
            type: 'string',
            max: 50,
            message: '最多50个字符，最多25个汉字(不含逗号分号)',
            trigger: 'blur'
          }
        ],
        approve_man: [{
            required: true,
            message: '请选择审核人',
            trigger: 'blur'
          }
        ],
        backup: [{
            required: true,
            message: '请选择是否备份',
            trigger: 'blur'
          }
        ],
        text: [{
            required: true,
            message: '请填写工单说明',
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
      approve_man: [],
      flag: false,
      single: false,
      cc_mail: false,
      person: '2',
      validate_result: false,
      validate_cc_mail: false,
      choose_db: false,
      cc_address_list: [],
      social: [],
      run_type: 0  //  0 -- inception方式提交和执行sql  1-- 直接连接数据库提交和执行
    }
  },
  methods: {
    chooseapprover (val) {
     if (val === '0') {
        this.formItem.approve_man = 'liuyan';
     } else if (val === '1') {
       this.formItem.approve_man = 'paul';
     } else {
       this.formItem.approve_man = '';
     }
    },
    show_ccmail_div () {
      if (this.cc_mail) {
        this.validate_cc_mail = true
      } else {
        this.validate_cc_mail = false
      }
    },
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
      // if (this.flag) return;
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
    ChooseDatabase (param) {
        axios.put(`${util.url}/workorder/quickbasename`, param)
          .then(res => {
              this.flag = true;
              this.choose_db = true;
              this.formItem.computer_room = res.data['computer_room_custom'];
              this.formItem.connection_name = res.data['connection_name_custom'];
              this.formItem.basename = res.data['laimi_db'];
              this.id = [res.data['id']];
              this.datalist.connection_name_list = [];
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
      this.formItem.computer_room = null;
      this.formItem.connection_name = null;
      this.formItem.basename = null;
      this.datalist.basenamelist = [];
      this.datalist.connection_name_list = [];
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
            let tmpddl2 = ''
            // let tmpddl = ''
            // let tmpbak = ''
            let tmpbak2 = ''
            if (this.formItem.textarea_backup) {
              tmpbak2 = this.formItem.textarea_backup.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
              // tmpbak = this.formItem.textarea_backup.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
              // tmpbak = ''
            }
            if (this.formItem.textarea_ddl_dml) {
              tmpddl2 = this.formItem.textarea_ddl_dml.replace(/--.*\n/g, '').replace(/\n/g, ' ').replace(/(;|；)$/gi, '').replace(/；/g, ';')
              // tmpddl = this.formItem.textarea_ddl_dml.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            } else {
              // tmpddl = ''
            }
            console.log(this.formItem)
            axios.put(`${util.url}/sqlsyntax/explain`, {
              'id': this.id[0].id,
              'base': this.formItem.basename,
              'type': 1,
              'sql': tmpddl2 + '&&&' + tmpbak2
            })
              .then(res => {
                console.log(res.data)
                if (res.data.status === 200) {
                  this.Testresults_explain = res.data.result_ddl_explain
                  this.Testresults_backup_explain = res.data.result_bak_explain
                  this.Testresults_backup_explain_error = '';
                  this.Testresults_explain_error = '';
                  this.validate_gen = false;
                  this.run_type = 1;
                } else if (res.data.status === 202) {
                    this.$Notice.error({
                    title: '执行语句错误',
                    desc: res.data.data_ddl,
                    duration: 15
                 })
                   this.Testresults_explain = '';
                   this.Testresults_explain_error = res.data.err_msg;
                   this.Testresults_backup_explain_error = '';
                   this.validate_gen = true;
                } else if (res.data.status === 203) {
                  this.$Notice.error({
                    title: '备份语句错误',
                    desc: res.data.data_bak,
                    duration: 15
                 })
                   this.Testresults_backup_explain = '';
                   this.Testresults_backup_explain_error = res.data.err_msg;
                   this.Testresults_explain_error = '';
                   this.validate_gen = true;
                } else {
                  this.$Notice.error({
                   title: '错误-1',
                   desc: '未知的错误'
                 })
                  this.validate_gen = true;
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
                 this.run_type = 0;
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
                'apply_man': Cookies.get('user'),
                'type': 1,
                'run_type': this.run_type,
                'cc_list': this.social,
                'id': this.id[0].id
              })
              .then(res => {
                this.$Notice.success({
                  title: '成功',
                  desc: res.data.ret
                })
                // this.validate_gen = !this.validate_gen
                this.validate_gen = true
                console.log('jianglb', res.data)
                this.cc_address_list = res.data.cc_address_list
                this.ClearForm()
                this.person = '2'
                this.cc_mail = false
                this.formItem.quick_choose = ''
                this.choose_db = false
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
      this.Testresults_backup = '';
      this.social = [];
      this.Testresults_backup_explain = '';
      this.Testresults_explain = '';
      // this.formItem.system='';
      // this.formItem.text='';
    }
  },
  mounted () {
    axios.put(`${util.url}/workorder/connection`)
      .then(res => {
        // console.log('ddddd', res.data)
        this.item = res.data['connection'];
        this.approve_man = res.data['person'];
        this.cc_mail_list = res.data['cc_mail_list'];
      })
      .catch(error => {
        util.ajanxerrorcode(this, error)
      });
    window.vm = this;
    }
}
</script>
