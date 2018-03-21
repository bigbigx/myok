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
        我的资产清单
        <Button  type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh">刷新</Button>

      </p>

      <Row>
        <Col span="24">
        <Table border :columns="columns6" :data="assettable" stripe size="small"></Table>
        </Col>
      </Row>
      <br>
      <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="20"></Page>
    </Card>
  </Row>
</div>
</template>
<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import util from '../../libs/util'
export default {
  name: 'asset-list',
  data () {
    return {
      columns6: [
        {
          type: 'selection',
          width: 60,
          align: 'center'
        },
        {
          title: '资产编号',
          key: 'work_id',
          sortable: true,
          sortType: 'desc',
          width: 200
        },
        {
          title: '资产名称',
          key: 'text'
        },
        {
          title: '资产位置',
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
          title: '指派审核人',
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
              label: '审核驳回',
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
            } else {
              return row.status === 5
            }
          }
        },
        {
          title: '审核备注',
          key: 'reject'
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
              }, '查看SQL')
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
      } else if (this.tmp[index].status === 3) {
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
    _Refresh () {
      this.mou_data()
    },
    out_button () {
      this.modal2 = false
      this.reject.reje = true
    },
    splicpage (page) {
      this.mou_data(page)
    },
    mou_data (vl = 1) {
      axios.get(`${util.url}/assets?page=${vl}&username=${Cookies.get('user')}`)
        .then(res => {
          if (res.data.status === 200) {
            this.assettable = res.data.data
          } else {
            this.$Notice.error({
                   title: '警告',
                   desc: '获取资产清单报错'
                 })
                 this.validate_gen_new = true
          }
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    delrecordList (vl) {
      this.delrecord = vl
    },
    delrecordData () {
      axios.post(`${util.url}/audit_sql`, {
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
