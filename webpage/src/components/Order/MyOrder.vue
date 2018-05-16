<style lang="less">
@import '../../styles/common.less';
@import '../Order/components/table.less';
</style>
<template>
<div>
  <Row>
    <Card>
      <p style="height: 30px;" slot="title">
        <Icon size="20" type="person"></Icon>
        我的工单
        <Button  type="primary" shape="circle" style="margin-left: 80%" @click="_Refresh_1">刷新</Button>
      </p>

      <Row>
        <!--<Col class="demo-spin-col" span="8">-->
            <!--<Spin fix>-->
                <!--<Icon type="load-c" size=18 class="demo-spin-icon-load"></Icon>-->
                <!--<div>Loading</div>-->
            <!--</Spin>-->
        <!--</Col>-->
        <Col span="24">
        <Table border :columns="columns6" :data="applytable" stripe size="small"></Table>
        </Col>
      </Row>
      <br>
      <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="20"></Page>
    </Card>
  </Row>
</div>
</template>
<script>
import Cookies from 'js-cookie'
import axios from 'axios'
import util from '../../libs/util'
export default {
  name: 'put',
  data () {
    return {
      columns6: [
        {
          title: '工单编号',
          key: 'work_id',
          sortable: true,
          width: 160
        },
        {
          title: '工单标题',
          key: 'text',
          width: 200
        },
        {
          title: '应用系统',
          key: 'affectd_system',
          sortable: true,
          width: 130
        },
        {
          title: '提交时间',
          key: 'date',
          sortable: true,
          width: 145
        },
        {
          title: '提交人',
          key: 'username',
          sortable: true,
          width: 100
        },
        {
          title: '审核人',
          key: 'assigned',
          sortable: true,
          width: 100
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
              text = '被驳回'
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
              label: '已同意',
              value: 1
            },
            {
              label: '已驳回',
              value: 0
            },
            {
              label: '待审核',
              value: 2
            },
            {
              label: '已执行',
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
            } else if (value === 0) {
              return row.status === 0
            } else if (value === 2) {
              return row.status === 2
            } else if (value === 3) {
              return row.status === 3
            } else if (value === 4) {
              return row.status === 4
            } else if (value === 5) {
              return row.status === 5
            }
          }
        },
        {
          title: '审核备注',
          key: 'reject',
          width: 155
        },
        {
          title: '审核时间',
          key: 'approvetime',
          width: 150,
        },
        {
          title: '执行时间',
          key: 'runtime',
          width: 150,
        },
        {
          title: '操作',
          key: 'action',
          align: 'center',
          fixed: 'right',
          width: 100,
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  size: 'small',
                  type: 'primary'
                  // color:'blue'
                },
                on: {
                  click: () => {
                    this.$router.push({
                      name: 'orderlist',
                      query: {workid: params.row.work_id, id: params.row.id, status: params.row.status, type: params.row.type}
                    })
                  }
                }
              }, '查看SQL')
            ])
          }
        }
      ],
      sql: [],
      pagenumber: 1,
      computer_room: util.computer_room,
      applytable: [],
      openswitch: false,
      modaltext: {},
      editsql: ''
    }
  },
  methods: {
    currentpage (vl) {
      axios.get(`${util.url}/workorder/?user=${Cookies.get('user')}&page=${vl}`)
        .then(res => {
          this.applytable = res.data.data
          this.pagenumber = parseInt(res.data.page.alter_number)
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    _Refresh_1 () {
      axios.get(`${util.url}/workorder/?user=${Cookies.get('user')}&page=1`)
        .then(res => {
          this.applytable = res.data.data
          this.pagenumber = res.data.page.alter_number
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  },

  mounted () {
    axios.get(`${util.url}/workorder/?user=${Cookies.get('user')}&page=1`)
      .then(res => {
        this.applytable = res.data.data
        this.pagenumber = res.data.page.alter_number
      })
      .catch(error => {
        util.ajanxerrorcode(this, error)
      })
  }
}
</script>
<!-- remove delete request -->
<style>
    .demo-spin-icon-load{
        animation: ani-demo-spin 1s linear infinite;
    }
    @keyframes ani-demo-spin {
        from { transform: rotate(0deg);}
        50%  { transform: rotate(180deg);}
        to   { transform: rotate(360deg);}
    }
    .demo-spin-col{
        height: 100px;
        position: relative;
        border: 1px solid #eee;
    }
</style>
