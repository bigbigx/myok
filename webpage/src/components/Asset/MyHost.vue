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
        我可访问的服务器清单：
        <Button  type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh">刷新</Button>

      </p>

      <Row>
        <Col span="24">
        <Table border :columns="columns6" :data="applytable" stripe size="small"></Table>
        </Col>
      </Row>
      <br>
      <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="20"></Page>
    </Card>

      <!--进入编辑按钮对话框-->
   <Modal v-model="showPublicSShModal" :width="1000" :mask-closable="false">
     <div>


     </div>
    <div slot="footer">
      <Button type="text" @click="showPublicSShModal = false">取消</Button>
      <Button type="primary" @click="delfilelink">删除</Button>
    </div>
  </Modal>
  </Row>
</div>
</template>
<script>
import Cookies from 'js-cookie'
import axios from 'axios'
import util from '../../libs/util'
export default {
  name: 'my-host',
  data () {
    return {
      columns6: [
        {
          title: '账号说明:',
          key: 'remark',
          sortable: true
        },
        {
          title: '外网IP:',
          key: 'publicip'
        },
        {
          title: '内网IP:',
          key: 'privateip',
          sortable: true
        },
        {
          title: '我的账号:',
          key: 'username',
          sortable: true
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
                  type: 'info'
                },
                on: {
                  click: () => {
                    this.showPublicSShModal = true
                  }
                }
              }, '公网访问'),
              h('Button', {
                props: {
                  size: 'small',
                  type: 'info'
                },
                style: {
                  marginLeft: '10px'
                },
                on: {
                  click: () => {
                    this.$router.push({
                      name: 'orderlist',
                      query: {workid: params.row.work_id, id: params.row.id, status: params.row.status, type: params.row.type}
                    })
                  }
                }
              }, '内网访问')
            ])
          }
        }
      ],
      sql: [],
      pagenumber: 1,
      computer_room: util.computer_room,
      applytable: [],
      openswitch: false,
      showPublicSShModal: false,
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
    axios.get(`${util.url}/host/?user=${Cookies.get('user')}&page=1`)
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
    axios.get(`${util.url}/host/myhost?user=${Cookies.get('user')}&page=1`)
      .then(res => {
        this.applytable = res.data
        // this.pagenumber = res.data.page.alter_number
      })
      .catch(error => {
        util.ajanxerrorcode(this, error)
      })
  }
}
</script>
