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
        运维步骤
        <Button  type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh">刷新</Button>

      </p>

      <Row>
        <Col span="24">
        <Table border :columns="columns6" :data="ops_step_config_list" stripe size="small"></Table>
        </Col>
      </Row>
      <br>
      <Button type="primary" shape="circle" style="margin-left: 80%" @click="_Refresh_log">下一步</Button>
    </Card>
  </Row>
</div>
</template>

<script>
    import Cookies from 'js-cookie'
    import axios from 'axios'
    import util from '../../libs/util'
    export default {
        name: 'manage-step',
        data () {
    return {
      columns6: [
        {
          title: '编号:',
          key: 'step_id',
          sortable: true
        },
        {
          title: '步骤分类:',
          key: 'text'
        },
        {
          title: '步骤小类:',
          key: 'date',
          sortable: true
        },
        {
          title: '实施内容',
          key: 'username',
          sortable: true
        },
        {
          title: '实施对象',
          key: 'assigned',
          sortable: true
        },
        {
          title: '步骤编号',
          key: 'assigned',
          sortable: true
        },
        {
          title: '步骤细节',
          key: 'assigned',
          sortable: true
        },
        {
          title: '执行时间',
          key: 'assigned',
          sortable: true
        },
        {
          title: '审核人',
          key: 'assigned',
          sortable: true
        },
        {
          title: '审核状态',
          key: 'status',
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
          title: '执行人',
          key: 'reject'
        },
        {
          title: '操作',
          key: 'action',
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
                    this.$router.push({
                      name: 'orderlist',
                      query: {workid: params.row.work_id, id: params.row.id, status: params.row.status, type: params.row.type}
                    })
                  }
                }
              }, '查看SQL')
            ])
          }
        },
        {
          title: '回滚编号',
          key: 'reject'
        }
      ],
      ops_step_config_list: [],
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
    _Refresh () {
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

<style scoped>

</style>
