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
        我的查看文件清单
        <Button  type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh_log_full">刷新</Button>
      </p>

      <Row>
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
          title: '日志说明',
          key: 'log_title',
          sortable: true
        },
        {
          title: '日志路径',
          key: 'log_path',
          sortable: true
        },
        {
          title: '搜索关键字',
          key: 'hostname',
          sortable: true
        },
        {
          title: '上下行数',
          key: 'hostname',
          sortable: true
        },
        {
          title: 'IP地址',
          key: 'IP',
          sortable: true
        },
        {
          title: '主机名',
          key: 'hostname',
          sortable: true
        },
        {
          title: '审核备注',
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
              }, '查看实时内容')
            ])
          }
        },
        {
          title: '编辑管理',
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
              }, '编辑')
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
    _Refresh_full () {
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
