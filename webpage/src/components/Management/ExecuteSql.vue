<style lang="less">
@import '../../styles/common.less';
@import '../Order/components/table.less';
</style>
<template>
<div>
  <Row>
    <Card>
      <p slot="title">
        <Icon type="person"></Icon>
        执行工单
        <Button  type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh_3">刷新</Button>
      </p>
      <Row>
        <Col span="24">
        <Poptip
          confirm
          title="您确认删除这些工单信息吗?"
          @on-ok="delrecordData"
          >
        <Button type="text" style="margin-left: -1%">删除记录</Button>
        </Poptip>
        <Table border :columns="columns6" :data="tmp" stripe ref="selection" @on-selection-change="delrecordList"></Table>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="20" ref="page"></Page>
        </Col>
      </Row>
    </Card>
  </Row>
  <Modal v-model="modal2" width="800">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>SQL工单详细信息</span>
    </p>
    <Form label-position="right">
      <FormItem label="id:">
        <span>{{ formitem.id }}</span>
      </FormItem>
      <FormItem label="工单编号:">
        <span>{{ formitem.work_id }}</span>
      </FormItem>
      <FormItem label="工单说明:">
        <span>{{ formitem.text }}</span>
      </FormItem>
      <FormItem label="提交时间:">
        <span>{{ formitem.date }}</span>
      </FormItem>
      <FormItem label="提交人:">
        <span>{{ formitem.username }}</span>
      </FormItem>
      <FormItem label="审核时间:">
        <span>{{ formitem.approve_time }}</span>
      </FormItem>
      <FormItem label="审核人:">
        <span>{{ formitem.assigned }}</span>
      </FormItem>
      <FormItem label="机房:">
        <span>{{ formitem.computer_room }}</span>
      </FormItem>
      <FormItem label="连接名称:">
        <span>{{ formitem.connection_name }}</span>
      </FormItem>
      <FormItem label="数据库库名:">
        <span>{{ formitem.basename }}</span>
      </FormItem>
      <FormItem label="备份SQL:">
        <p v-for="j in backup_sql">{{ j }}</p>
      </FormItem>
      <FormItem label="执行SQL:">
        <p v-for="i in sql">{{ i }}</p>
      </FormItem>
    </Form>

    <div slot="footer">

      <Button @click="cancel_button">取消</Button>
      <!-- <Button type="error" @click="out_button_1()" :enabled="summit">驳回</Button> -->
      <Button type="success" @click="put_button_exe()" :enabled="summit">备份和执行</Button>
    </div>
  </Modal>


  <Modal v-model="reject.reje" @on-ok="rejecttext">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>SQL工单执行驳回理由说明</span>
    </p>
    <Input v-model="reject.textarea" type="textarea" :autosize="{minRows: 15,maxRows: 15}" placeholder="请填写执行驳回说明"></Input>
  </Modal>
</div>
</template>
<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import util from '../../libs/util'
export default {
  name: 'Sqltable',
  data () {
    return {
      columns6: [
        {
          type: 'selection',
          width: 60,
          align: 'center'
        },
        {
          title: '工单编号:',
          key: 'work_id',
          sortable: true,
          sortType: 'desc',
          width: 250
        },
        {
          title: '工单标题:',
          key: 'text'
        },
        {
          title: '提交时间:',
          key: 'date',
          sortable: true,
          width: 150
        },
        {
          title: '提交人',
          key: 'username',
          sortable: true,
          width: 150
        },

        {
          title: '审核时间:',
          key: 'approve_time',
          sortable: true,
          width: 150
        },
        {
          title: '审核人',
          key: 'assigned',
          sortable: true,
          width: 150
        },

        {
          title: '状态',
          key: 'status',
          width: 150,
          render: (h, params) => {
            const row = params.row
            let color = ''
            let text = ''
            if (row.status === 2) {
              color = 'blue'
              text = '待审核'
            } else if (row.status === 0) {
              color = 'red'
              text = '已驳回'
            } else if (row.status === 1) {
              color = 'orange'
              text = '已同意'
            } else if (row.status === 4) {
              color = 'green'
              text = '已执行'
            } else {
              color = 'yellow'
              text = '进行中'
            }
            return h('Tag', {
              props: {
                type: 'dot',
                color: color
              }
            }, text)
          },
          sortable: true,
          filters: [{
              label: '审核同意',
              value: 1
            },
            {
              label: '审核拒绝',
              value: 0
            },
            {
              label: '待审核',
              value: 2
            },
            {
              label: '执行驳回',
              value: 3
            },
            {
              label: '执行成功',
              value: 4
            },
            {
              label: '进行中',
              value: 5
            },
            {
              label: '备份中',
              value: 6
            }
          ],
          //            filterMultiple: false 禁止多选,
          filterMethod (value, row) {
            if (value === 1) {
              return row.status === 1
            } else if (value === 2) {
              return row.status === 2
            } else if (value === 0) {
              return row.status === 0
            } else if (value === 3) {
              return row.status === 3
            } else if (value === 4) {
              return row.status === 4
            } else if (value === 6) {
              return row.status === 6
            } else {
              return row.status === 5
            }
          }
        },
        {
          title: '审核备注',
          key: 'action'
        },
        {
          title: '操作',
          key: 'action',
          width: 100,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  size: 'small',
                  type: 'text'
                },
                on: {
                  click: () => {
                    this.edit_tab(params.index)
                  }
                }
              }, '执行SQL')
            ])
          }
        }
      ],
      modal2: false,
      sql: null,
      backup_sql: null,
      formitem: {
        workid: '',
        date: '',
        username: '',
        dataadd: '',
        database: '',
        att: '',
        assigned: '',
        approve_time: '',
        id: null
      },
      summit: false,
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
          width: '85'
        },
        {
          title: '阶段状态',
          key: 'stagestatus'
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
          key: 'affected_rows'
        }
      ],
      dataId: [],
      reject: {
        reje: false,
        textarea: ''
      },
      tmp: [],
      pagenumber: 1,
      delrecord: [],
      togoing: null
    }
  },
  methods: {
    edit_tab: function (index) {
      this.togoing = index
      this.dataId = []
      this.modal2 = true
      if (this.tmp[index].status === 2) {
        this.summit = false
        this.formitem = this.tmp[index]
        this.sql = this.tmp[index].sql.split(';')
        this.backup_sql = this.tmp[index].backup_sql.split(';')
      } else if (this.tmp[index].status === 6) {
        this.summit = false
        this.formitem = this.tmp[index]
        this.sql = this.tmp[index].sql.split(';')
        this.backup_sql = this.tmp[index].backup_sql.split(';')
      } else {
        this.formitem = this.tmp[index]
        this.sql = this.tmp[index].sql.split(';')
        this.backup_sql = this.tmp[index].backup_sql.split(';')
        this.summit = true
      }
    },
    cancel_button () {
      this.modal2 = false
    },
    put_backup () {  //  数据库备份查询
      this.modal2 = false // 保留窗口显示状
    },
    put_button_exe () {
      this.modal2 = false
      this.tmp[this.togoing].status = 5
      axios.put(`${util.url}/execute_sql`, {
          'type': 1,
          'from_user': Cookies.get('user'),
          'to_user': this.formitem.assigned,
          'apply_man': this.formitem.username,
          'id': this.formitem.id
        })
        .then(res => {
          this.$Notice.success({
            title: '执行成功',
            desc: res.data
          })
          this.mou_data()
          this.$refs.page.currentPage = 1
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    out_button_1 () {
      this.modal2 = false
      this.reject.reje = true
    },
    rejecttext () {
      axios.put(`${util.url}/execute_sql`, {
          'type': 0,
          'from_user': Cookies.get('user'),
          'text': this.reject.textarea,
          'to_user': this.formitem.assigned,
          'id': this.formitem.id
        })
        .then(res => {
          this.$Notice.warning({
            title: res.data
          })
          this.mou_data()
          this.$refs.page.currentPage = 1
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    test_button () {
      //  ddl& dml语句检测显示
      axios.put(`${util.url}/execute_sql`, {
          'type': 'test',
          'base': this.formitem.basename,
          'id': this.formitem.id
        })
        .then(res => {
          if (res.data.status === 200) {
            this.dataId = res.data.result
          } else {
            this.$Notice.error({
              title: '警告',
              desc: '无法连接到Inception!'
            })
          }
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    splicpage (page) {
      this.mou_data(page)
    },
    mou_data (vl = 1) {
      axios.get(`${util.url}/execute_sql?page=${vl}&username=${Cookies.get('user')}`)
        .then(res => {
          this.tmp = res.data.data
          this.pagenumber = res.data.page.alter_number
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    _Refresh_3 () {
    },
    delrecordList (vl) {
      this.delrecord = vl
    },
    delrecordData () {
      axios.post(`${util.url}/execute_sql`, {
        'id': JSON.stringify(this.delrecord)
      })
        .then(res => {
          this.$Notice.info({
            title: '信息',
            desc: res.data
          })
          this.mou_data()
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  },
  mounted () {
    this.mou_data()
  }
}
</script>
<!-- remove delete request -->
