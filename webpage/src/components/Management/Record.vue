<style lang="less">
@import '../../styles/common.less';
@import '../Order/components/table.less';
</style>
<template>
<div>
  <Row>
    <Card>
      <p slot="title">
        <Icon type="android-send"></Icon>
        历史工单执行记录
      </p>
      <Row>
        <Col span="24">
        <Table border :columns="tabcolumns" :data="TableDataNew" class="tabletop" style="background: #5cadff"></Table>
        <br>
        <Page :total="this.pagenumber" show-elevator @on-change="splicpage" :page-size="10" ref="page"></Page>
        </Col>
      </Row>
    </Card>
  </Row>
</div>
</template>
<script>
import axios from 'axios'
import util from '../../libs/util'
import Cookies from 'js-cookie'
export default {
  name: 'Record',
  data () {
    return {
      tabcolumns: [
        {
          title: '工单编号',
          key: 'workid'
        },
        {
          title: '工单标题',
          key: 'text'
        },
        {
          title: '执行时间',
          key: 'date',
          sortType: 'desc'
        },
        {
          title: '申请人',
          key: 'person'
        },
        {
          title: '执行人',
          key: 'reviewer'
        },
        {
          title: '执行区域',
          key: 'area'
        },
        {
          title: '连接名称',
          key: 'name'
        },
        {
          title: '库名',
          key: 'base'
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
                      query: {workid: params.row.workid, id: params.row.id, status: 1, type: params.row.type}
                    })
                  }
                }
              }, '详细信息')
            ])
          }
        }
      ],
      TableDataNew: [],
      pagenumber: 1
    }
  },
  methods: {
    getrecordinfo (vl = 1) {
      axios.get(`${util.url}/record?page=${vl}&username=${Cookies.get('user')}`)
        .then(res => {
          this.TableDataNew = res.data.data
          this.pagenumber = res.data.page
        })
        .catch(error => {
          this.$Notice.error({
            title: '警告',
            desc: error
          })
        })
    },
    splicpage (page) {
      this.getrecordinfo(page)
    }
  },
  mounted () {
    this.getrecordinfo()
  }
}
</script>
