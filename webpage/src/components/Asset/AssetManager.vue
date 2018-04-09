<style lang="less">
@import '../../styles/common.less';
@import '../common/table.less';
</style>

<template>
<div>
  <Row>

    <Col span="7">


        <Card>
              <p slot="title">
      <Icon type="ios-crop-strong"></Icon>新增资产
    </p>
          <Tabs value="name1" >
        <TabPane label="云环境" icon="load-b" name="parent_tab_yun">
          <div class="edittable-test-con">
          <div id="showImage" class="margin-bottom-10">

            <Form ref="formYunItem" :model="formYunItem" :rules="ruleValidate" :label-width="80">
              <!--<FormItem label="云环境:" prop="computer_room">-->
                <!--<Select v-model="formYunItem.computer_room" @on-change="Computer_room">-->
                <!--<Option v-for="i in yun_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>-->
              <!--</Select>-->
              <!--</FormItem>-->

              <!--<FormItem label="所在区域:" prop="area">-->
                <!--<Select v-model="formYunItem.area_name" filterable>-->
                <!--<Option v-for="i in yun_datalist.area_list" :value="i" :key="i">{{ i }}</Option>-->
              <!--</Select>-->
              <!--</FormItem>-->


              <!--<FormItem label="实例类型:" prop="instance_type">-->
                <!--<Select v-model="formYunItem.instance_type" filterable>-->
                <!--<Option v-for="i in yun_datalist.instance_type_list" :value="i" :key="i">{{ i }}</Option>-->
              <!--</Select>-->
              <!--</FormItem>-->

              <!--<FormItem label="实例名称:" prop="instance_name">-->
                <!--<input type="text" size="small"></input>-->
              <!--</FormItem>-->

              <!--<FormItem label="实例ID:" prop="instance_id">-->
                 <!--<input type="text" size="small"></input>-->
              <!--</FormItem>-->

              <!--<FormItem>-->
                <!--<Button type="warning" icon="android-search" @click.native="test_sql()">检测</Button>-->
                <!--<Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :disabled="this.validate_gen">添加</Button>-->
              <!--</FormItem>-->
            <!--</Form>-->
             <Alert style="height: 145px">
              云环境资产更新说明
              <template slot="desc">
                  <p>1) 本平台可通过阿里云的SDK获取资产信息i</p>
                  <p>2) 可以手工更新资产</p>
                  <p>3) 可以设置定时更新资产，每天只能更新一次</p>
                </template>
            </Alert>
            </Form>
            <Card>
              <Tabs value="refresh_tab" style="height: 180px;">
                <TabPane label="手工更新"  name="handle_refresh_assets" >
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click="confirm"  size="large">手工更新资产</Button>
                  </TabPane>
                <TabPane label="定时更新"  name="crontab_refresh_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="large">设置定时更新资产</Button>
                </TabPane>
                <TabPane label="导出资产清单"  name="crontab_export_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="large">导出云资产</Button>
                <Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="large">查看资产更新日志</Button>
                </TabPane>
              </Tabs>
            </Card>
              <Card>
                <p slot="title">
                  <Icon type="ios-crop-strong"></Icon>资产操作记录
                </p>
                <!--<Tabs value="name_history" >-->
                    <!--<TabPane label="目录" icon="load-b" name="asset_operation_melu">-->
                         <div class="edittable-con-0">
                   <Table  border :columns="columns_refresh_log" :data="yun_diff_list" stripe height="300"></Table>
                  <!--<Page :total="pagenumber-asset" show-elevator @on-change="splicpage" :page-size="10"></Page>-->

                </div>
                    <!--</TabPane>-->
                     <!--<TabPane label="ECS" icon="load-b" name="asset_ecs_detail">-->
                       <!--<Table border :columns="columns_ecs_diff_detail" style="overflow-y: scroll;" :data="ecs_diff_detail" stripe height="300"></Table>-->
                    <!--</TabPane>-->
                     <!--<TabPane label="RDS" icon="load-b" name="asset_rds_detail">-->
                       <!--<Table border :columns="columns_rds_diff_detail" :data="rds_diff_detail" stripe height="300"></Table>-->
                    <!--</TabPane>-->
                <!--</Tabs>-->
                <!--<Modal-->
                  <!--v-model="diff_detail_model"-->
                  <!--title="Common Modal dialog box title"-->
                  <!--@on-ok="ok"-->
                  <!--@on-cancel="cancel"></Modal>-->
                  <!--<Modal v-model="diff_detail_model"  width="75%" scrollable="true" closable="false">-->
                      <!--<h3 slot="header" style="color:#2D8CF0">查看资产差异详情</h3>-->
                      <!--<p>ECS</p>-->
                    <!--&lt;!&ndash;<Button type="primary" style="margin-left: 25%;margin-top: 5%;" @click.native="orderswitch" size="small">查看资产更新日志</Button>&ndash;&gt;-->
                      <!--<Table   stripe   border :columns="columns_change_name" :data="ecs_diff_detail"    size="small" ></Table>-->
                      <!--<br>-->
                      <!--<h2>RDS</h2>-->
                      <!--<Table border  stripe :columns="columns_change_name" :data="rds_diff_detail"   size="small"></Table>-->
                      <!--<div slot="footer">-->
                        <!--<Button type="text" @click="diff_detail_model = false">取消</Button>-->
                        <!--<Button type="primary" @click="add2asset">同步到数据库</Button>-->
                      <!--</div>-->
                   <!--</Modal>-->
              </Card>

          </div>
        </div>
        </TabPane>

        <TabPane label="物理机房" icon="load-d" name="parent_tab_own">
            <div class="edittable-test-con">
          <div id="showImage" class="margin-bottom-10">

            <Form ref="formOwnItem" :model="formOwnItem" :rules="ruleValidate" :label-width="80">
              <FormItem label="机房:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>

              <FormItem label="机柜:" prop="connection_name">
                <Select v-model="formOwnItem.connection_name" @on-change="DataBaseName" filterable>
                <Option v-for="i in own_datalist.connection_name_list" :value="i.connection_name" :key="i.connection_name">{{ i.connection_name }}</Option>
              </Select>
              </FormItem>


              <FormItem label="所属资产:" prop="connection_name">
                <Select v-model="formOwnItem.connection_name" @on-change="DataBaseName" filterable>
                <Option v-for="i in formOwnItem.connection_name_list" :value="i.connection_name" :key="i.connection_name">{{ i.connection_name }}</Option>
              </Select>
              </FormItem>

              <FormItem label="主机名:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>

              <FormItem label="IP地址:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>


              <FormItem label="硬盘:" prop="computer_room">
                <Select v-model="formOwnItem.computer_room" @on-change="Connection_Name">
                <Option v-for="i in own_datalist.computer_roomlist" :key="i" :value="i" >{{i}}</Option>
              </Select>
              </FormItem>

              <FormItem>
                <Button type="warning" icon="android-search" @click.native="test_sql()">检测</Button>
                <Button type="success" icon="ios-redo" @click.native="SubmitSQL()" style="margin-left: 10%"  :enabled="this.validate_gen">添加</Button>
              </FormItem>
            </Form>
            <Alert style="height: 145px">
              物理机房如何自动CMDB
              <template slot="desc">
                  <p>1) 巡风系统估计值</p>
                </template>
            </Alert>
             <Card>
              <Tabs value="refresh_tab" style="height: 150px;">
                <TabPane label="手工更新"  name="handle_refresh_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 10%;" @click.native="orderswitch" size="large">手工更新资产</Button>
                </TabPane>
                <TabPane label="定时更新"  name="crontab_refresh_assets">
                  <Button type="primary" style="margin-left: 25%;margin-top: 10%;" @click.native="orderswitch" size="large">设置定时更新资产</Button>
                </TabPane>
              </Tabs>
            </Card>
          </div>
        </div>
        </TabPane>
      </Tabs>
        </Card>

    </Col>

<Col span="17" class="padding-left-10">
  <Card>
    <p slot="title">
      <Icon type="ios-crop-strong"></Icon>资产清单
<Button type="primary" style="margin-left: 85%;" @click.native="test" size="small">刷新清单</Button>
    </p>

    <div class="edittable-con-0">
      <Card>
        <Tabs value="name1">
          <TabPane label="云环境" icon="social-hackernews" name="parent_right_tab_yun">

            <div class="edittable-test-con">
                <div class="edittable-testauto-con">
                  <Card>
                    <Tabs value="name999">
                      <TabPane    label="阿里云" name="child_right_tab_aliyun">
                        <Tabs value="aliyun-fenlei">
                          <TabPane :label="ecs_label" name="aliyun-ecs">
                            <div class="edittable-con-0">
                              <Table :columns="columns_ecs_diff_detail" :data="this.aliyun_result_list.aliyun_ECS_assets" height="500"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                          </TabPane>
                          <TabPane :label="rds_label"  name="aliyun-rds">
                            <div class="edittable-con-0">
                              <Table :columns="columns_rds_diff_detail" :data="this.aliyun_result_list.aliyun_RDS_assets" height="500"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                          </TabPane>
                          <TabPane label="SLB"  name="aliyun-slb">
                            <div class="edittable-con-0">
                              <Table :columns="columns_slb_diff_detail" :data="this.aliyun_result_list.aliyun_SLB_assets" height="500"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                          </TabPane>
                        </Tabs>

                      </TabPane>
                      <TabPane label="美团云"  name="child_right_tab_meituanyun">
                            <div class="edittable-con-0">
                              <Table :columns="yun_columnsName1" :data="meituanyun_assets" height="500"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                      <TabPane label="华为云" name="child_right_tab_huaweiyun">
                            <div class="edittable-con-0">
                              <Table :columns="yun_columnsName1" :data="huaweiyun_assets" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                    </Tabs>
                  </Card>
                </div>
              <!--<Table :columns="columns" :data="rowdata" height="550"></Table>-->
            </div>
          </TabPane>
          <TabPane label="物理机房" icon="nuclear" name="parent_right_tab_own">
            <div class="edittable-test-con">
            <div id="showImage" class="margin-bottom-10">
              <Card>
                    <Tabs value="name999">
                      <TabPane label="公司机房"  name="companry-idc">
                            <div class="edittable-con-1">
                              <Table :columns="columns" :data="rowdata" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                       <TabPane label="广州IDC"  name="gz-idc">
                            <div class="edittable-con-1">
                              <Table :columns="columns" :data="rowdata" height="550"></Table>
                            </div>
                            <br>
                            <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
                      </TabPane>
                    </Tabs>
              </Card>
            </div>
            </div>
          </TabPane>
        </Tabs>
      </Card>
    </div>

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
  name: 'host-manager',
  data () {
    return {

       ecs_label: (h) => {
                    return h('div', [
                        h('span', 'ECS'),
                        h('Badge', {
                            props: {
                                count: this.coutlist.aliyun_ecs_count
                            }
                        })
                    ])
                },
       rds_label: (h) => {
                    return h('div', [
                        h('span', 'RDS'),
                        h('Badge', {
                            props: {
                                count: this.coutlist.aliyun_rds_count
                            }
                        })
                    ])
                },
      validate_gen: true,
      coutlist: {
        aliyun_ecs_count: 0,
        aliyun_rds_count: 0,
        aliyun_slb_count: 0,
        meituanyun_ecs_count: 0,
        meituanyun_rds_count: 0
      },
      formYunItem: {
        textarea: '',
        computer_room: '',
        area_name: '',
        instance_type: '',
        instance_name: ''
      },
      formOwnItem: {
        textarea: '',
        computer_room: '',
        connection_name: '',
        basename: '',
        text: '',
        backup: 0,
        assigned: ''
      },
      columns_rds_diff_detail: [
        {
          title: 'DBInstanceDescription',
          key: 'DBInstanceDescription',
          fixed: 'left',
          width: 160
        },
        {
          title: 'LockMode',
          key: 'LockMode',
          width: 160
        },
        {
          title: 'DBInstanceNetType',
          key: 'DBInstanceNetType',
          width: 160
        },
        {
          title: 'DBInstanceClass',
          key: 'DBInstanceClass',
          width: 160
        },
        {
          title: 'ResourceGroupId',
          key: 'ResourceGroupId',
          width: 160
        },
        {
          title: 'DBInstanceId',
          key: 'DBInstanceId',
          width: 160
        },
        {
          title: 'VpcCloudInstanceId',
          key: 'VpcCloudInstanceId',
          width: 160
        },
        {
          title: 'ZoneId',
          key: 'ZoneId',
          width: 160
        },
        {
          title: 'InstanceNetworkTypes',
          key: 'InstanceNetworkType',
          width: 160
        },
        {
          title: 'ConnectionMode',
          key: 'ConnectionMode',
          width: 160
        },
        {
          title: 'Engine',
          key: 'Engine',
          width: 160
        },
        {
          title: 'MutriORsignle',
          key: 'MutriORsignle',
          width: 160
        },
        {
          title: 'InsId',
          key: 'InsId',
          width: 160
        },
        {
          title: 'ExpireTime',
          key: 'ExpireTime',
          width: 160
        },
        {
          title: 'CreateTime',
          key: 'CreateTime',
          width: 160
        },
        {
          title: 'DBInstanceType',
          key: 'DBInstanceType',
          width: 160
        },
        {
          title: 'RegionId',
          key: 'RegionId',
          width: 160
        },
        {
          title: 'EngineVersion',
          key: 'EngineVersion',
          width: 160
        },
        {
          title: 'LockReason',
          key: 'LockReason',
          width: 160
        },
        {
          title: 'DBInstanceStatus',
          key: 'DBInstanceStatus',
          width: 160
        },
        {
          title: 'PayType',
          key: 'PayType',
          width: 160
        }
      ],
      columns_change_name: [
        {
          title: '变动实例ID',
          key: 'id_count',
          width: 150
        },
        {
          title: '变动实例名字',
          key: 'id_count',
          width: 150
        },
        {
          title: '变动项目数',
          key: 'item_count',
          width: 150
        },
        {
          title: '操作',
          key: 'item_count',
          width: 150
        }
      ],
      columns_ecs_diff_detail: [
        {
          title: '实例名称',
          key: 'InstanceName',
          fixed: 'left',
          width: 160
        },
        {
          title: '实例ID',
          key: 'InstanceId',
          width: 120
        },
        {
          title: '内网IP',
          key: 'InnerIpAddress',
          width: 120
        },
        {
          title: '公网IP',
          key: 'PublicIpAddress',
          width: 120
        },
        {
          title: '主机名',
          key: 'HostName',
          width: 100
        },
        {
          title: 'IO',
          key: 'IoOptimized',
          width: 100
        },
        {
          title: '内存',
          key: 'Memory',
          width: 100
        },
        {
          title: 'Cpu',
          key: 'Cpu',
          width: 100
        },
        {
          title: '镜像ID',
          key: 'ImageId',
          width: 100
        },
        {
          title: 'InstanceTypeFamily',
          key: 'InstanceTypeFamily',
          width: 100
        },
        {
          title: 'VlanId',
          key: 'VlanId',
          width: 100
        },
        {
          title: 'EipAddress',
          key: 'EipAddress',
          width: 300
        },
        {
          title: '公网入带宽',
          key: 'InternetMaxBandwidthIn',
          width: 100
        },
        {
          title: 'ZoneId',
          key: 'ZoneId',
          width: 100
        },
        {
          title: 'InternetChargeType',
          key: 'InternetChargeType',
          width: 100
        },
        {
          title: 'SpotStrategy',
          key: 'SpotStrategy',
          width: 100
        },
        {
          title: '停止模式',
          key: 'StoppedMode',
          width: 100
        },
        {
          title: 'VPC',
          key: 'VpcAttributes',
          width: 100
        },
        {
          title: '公网出带宽',
          key: 'InternetMaxBandwidthOut',
          width: 100
        },
        {
          title: '设备可用性',
          key: 'DeviceAvailable',
          width: 100
        },
        {
          title: '安全组',
          key: 'SecurityGroupIds',
          width: 100
        },
        {
          title: 'SaleCycle',
          key: 'SaleCycle',
          width: 100
        },
        {
          title: 'SpotPriceLimit',
          key: 'SpotPriceLimit',
          width: 100
        },
        {
          title: 'AutoReleaseTime',
          key: 'AutoReleaseTime',
          width: 100
        },
        {
          title: 'StartTime',
          key: 'StartTime',
          width: 100
        },
        {
          title: '描述',
          key: 'Description',
          width: 100
        },
        {
          title: '资源组ID',
          key: 'ResourceGroupId',
          width: 100
        },
        {
          title: 'OS类型',
          key: 'OSType',
          width: 100
        },
        {
          title: 'OSName',
          key: 'OSName',
          width: 100
        },
        {
          title: 'InstanceNetworkType',
          key: 'InstanceNetworkType',
          width: 100
        },
        {
          title: 'InstanceType',
          key: 'InstanceType',
          width: 100
        },
        {
          title: 'CreationTime',
          key: 'CreationTime',
          width: 100
        },
        {
          title: 'Status',
          key: 'Status',
          width: 100
        },
        {
          title: 'ClusterId',
          key: 'ClusterId',
          width: 100
        },
        {
          title: 'Recyclable',
          key: 'Recyclable',
          width: 100
        },
        {
          title: 'RegionId',
          key: 'RegionId',
          width: 100
        },
        {
          title: 'GPUSpec',
          key: 'GPUSpec',
          width: 100
        },
        {
          title: 'OperationLocks',
          key: 'OperationLocks',
          width: 100
        },
        {
          title: 'InstanceChargeType',
          key: 'InstanceChargeType',
          width: 100
        },
        {
          title: 'GPUAmount',
          key: 'GPUAmount',
          width: 100
        },
        {
          title: 'xpiredTime',
          key: 'xpiredTime',
          width: 100
        }
      ],
      columns_refresh_log: [
        {
          title: '时间',
          key: 'cur_time',
          width: ''
        },
        {
          title: '差异条数',
          key: 'diff_count',
          width: ''
        },
        {
          title: '操作人',
          key: 'cur_person',
          width: ''
        },
        {
          title: '操作',
          key: 'diff_detail',
          width: 80,
          align: 'center',
          render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.show_diif_detail(params.index)
                    }
                  }
                }, '详情')
              ])
          }
        }
      ],
      yun_columnsName: [
        {
          title: '实例ID',
          key: 'ID',
          width: '150'
        },
        {
          title: '实例名称',
          key: 'name',
          width: '150'
        },
        {
          title: '实例类型',
          key: 'type',
          width: '100'
        },
        {
          title: '域名/IP',
          key: 'yuming_or_ip',
          width: '150'
        },
        {
          title: '基本配置',
          key: 'basic_config'
        }
      ],
      ecsdata: [],
      pagenumber_asset: 1,
      rdsdata: [],
      Testresults: [],
      yun_diff_list: [],
      asset_diff_detail: [],
      data_asset_list: {
        ecs_diff_detail: [],
        rds_diff_detail: []
      },
      diff_detail_model: false,
      Testresults_backup: [],
      item: {},
      yun_datalist: {
        connection_name_list: [],
        instance_type_list: util.yun_instance_type_list,
        area_list: util.yun_area_list,
        computer_roomlist: util.yun_room_list
      },
      own_datalist: {
        connection_name_list: [],
        basenamelist: [],
        sqllist: [],
        computer_roomlist: util.own_room_list
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
      aliyun_result_list: {
        aliyun_ECS_assets: [],
        aliyun_RDS_assets: [],
        aliyun_SLB_assets: []
      },
      meituanyun_result_list: {
        meituanyun_ECS_assets: [],
        meituanyun_RDS_assets: []
      },
      huaweiyun_result_list: {
        huaweiyun_ECS_assets: [],
        huaweiyun_RDS_assets: []
      }
    }
  },
  methods: {
    confirm () {
      // this.diff_detail_model = true
      this.$Modal.confirm({
                    title: '准备写入变动到资产数据表(后期会添加校验码功能)',
                    content: '<p>预备</p><p>开始</p>',
                    loading: true,
                    onOk: () => {
                       setTimeout(() => {
                            this.$Modal.remove();
                            // this.$Message.info('关闭');
                            // this.diff_detail_model = true;
                            this.add2asset();
                        }, 2000);
                    },
                    onCancel: () => {
                        this.$Message.info('Clicked cancel');
                    }
                });
    },
    handleSelectAll (status) {
      this.$refs.selection.selectAll(status);
    },
    add2asset () {  //  添加数据到数据库
             axios.put(`${util.url}/yunassets/showdiff`)
                  .then(res => {
                      this.data_asset_list.ecs_diff_detail = res.data.diff_detail.ecs
                      this.data_asset_list.rds_diff_detail = res.data.diff_detail.rds
                      console.log(this.data_asset_list.rds_diff_detail, 'rds')
                      console.log(this.data_asset_list.ecs_diff_detail, 'ecs')
                  })
                  .catch(error => {
                  util.ajanxerrorcode(this, error)
                })
              axios.post(`${util.url}/yunassets/`, {
                'user': Cookies.get('user'),
                'ecs_data': JSON.stringify(this.data_asset_list.ecs_diff_detail),
                'rds_data': JSON.stringify(this.data_asset_list.rds_diff_detail)
                // 'ecs_data': this.ecs_diff_detail,
                // 'rds_data': this.rds_diff_detail
              })
              .then(res => {
                this.$Notice.success({
                  title: '成功',
                  desc: '更新资产成功'
                })
                // 添加记录到 资产操作记录栏目理
                this.yun_diff_list = res.data
              })
              .catch(error => {
                util.ajanxerrorcode(this, error)
              })
    },
    show_diif_detail (index) {
      this.diff_detail_model = true

      // this.username = this.data5[index].username
    }
  },
  mounted () {
     axios.put(`${util.url}/yunassets/showdiff`)
          .then(res => {
              this.data_asset_list.ecs_diff_detail = res.data.diff_detail.ecs
              this.data_asset_list.rds_diff_detail = res.data.diff_detail.rds
              console.log(this.data_asset_list.rds_diff_detail, 'rds')
              console.log(this.data_asset_list.ecs_diff_detail, 'ecs')
          })
          .catch(error => {
          util.ajanxerrorcode(this, error)
        })
     axios.get(`${util.url}/yunassets/`)
          .then(res => {
              this.aliyun_result_list.aliyun_ECS_assets = res.data.ecs_data.data
              this.aliyun_result_list.aliyun_RDS_assets = res.data.rds_data.data
              this.coutlist.aliyun_ecs_count = res.data.ecs_data.data.length
              this.coutlist.aliyun_rds_count = res.data.rds_data.data.length
              console.log(this.aliyun_result_list.aliyun_ECS_assets, 'aliyunassets')
              // this.data_asset_list.rds_diff_detail = res.data.diff_detail.rds
          })
          .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
}
</script>
