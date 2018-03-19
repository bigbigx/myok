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
        我的日志工单
        <Button  type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh_myorder()">刷新</Button>
        <Button type="primary"  shape="circle"  style="margin-left: 92%" @click.native="Apply()">申请工单</Button>
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
   <Modal v-model="apply_file" width="800">
      <Row>
        <Card>
          <div class="step-header-con">
            <h3 style="margin-left: 35%">蜜罐运维平台---日志工单</h3>
          </div>
          <p class="step-content"></p>
          <Form  ref="formItem" :model="formItem" class="step-form" :label-width="100">
            <FormItem label="分组:">
              <p>{{formItem.id}}</p>
            </FormItem>
            <FormItem label="机房:">
              <p>{{formItem.username}}</p>
            </FormItem>
            <FormItem label="服务器:">
              <p>{{formItem.computer_room}}</p>
            </FormItem>
            <FormItem label="文件路径:">
              <Input v-model="formItem.fileremark" placeholder="最多不超过50个字"></Input>
            </FormItem>
            <FormItem label="工单提交说明:">
              <Input v-model="formItem.text" placeholder="最多不超过150个字"></Input>
            </FormItem>
            <FormItem label="指定审核人:" prop="text">
              <Select v-model="formItem.assigned">
                <Option v-for="i in this.assigned" :value="i.username" :key="i.username">{{i.username}}</Option>
              </Select>
            </FormItem>
          </Form>
        </Card>
      </Row>
      <div>
         <p align:center>检测结果</p>
         <Table :columns="columnsName" :data="Testresults_file_path" highlight-row></Table>
      </div>
      <div slot="footer">
         <Row>
            <Col span="12" style="text-align: left;">
                 <Button type="default" @click="cancel_button">取消</Button>
            </Col>
            <Col span="12">
                <Button type="warning" icon="android-search" @click.native="_Test_file_path" style="margin-left: 10%">检测</Button>
                <Button type="success" icon="ios-redo" @click.native="Apply_Put_Data" style="margin-left: 10%"  :disabled="this.validate_gen_new">提交</Button>
            </Col>filepa
         </Row>
       </div>


    </Modal>

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
          title: '工单编号:',
          key: 'work_id',
          sortable: true
        },
        {
          title: '工单标题:',
          key: 'text'
        },
        {
          title: '提交时间:',
          key: 'date',
          sortable: true
        },
        {
          title: '提交人',
          key: 'username',
          sortable: true
        },
        {
          title: '指派审核人',
          key: 'assigned',
          sortable: true
        },
        {
          title: '状态',
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
              label: '已配置',
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
              }, '查看详情')
            ])
          }
        }
      ],
      file_path: [],
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
    Apply_Main () {
      this.validate_gen_new = true
    },
    Apply_Put_Data () {
        axios.post(`${util.url}/filecontent/`, {
          'data': JSON.stringify(this.formItem),
          'filepath': this.formItem.file_path,
          'work_text': this.formItem.text,
          'user': Cookies.get('user'),
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
    },
    cancel_button () {
      this.apply_file = false
    },
    _Test_file_path () {
      if (this.formItem.fileremark || this.formItem.assigned || this.formItem.text) {
        alert('dads')
      } else {
        this.$Message.error('请填写好文件路径、指派审核人和工单说明再检测!');
      }
    },
    _Refresh_myorder () {
    axios.get(`${util.url}/filecontent/?user=${Cookies.get('user')}&page=1`)
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
