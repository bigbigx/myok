#!/usr/bin/env python
#coding=utf-8
import call_inception

def test():
   data_select="select * from t_erp_sale_order t where t.bill_id='7029654';"
   data_ddl_dml="update t_erp_sale_order t set t.pay_status='N' where t.bill_id='7029654';"

   data = {'select': '', 'dml_ddl': ''}
   data1 = call_inception.Inception.BeautifySQL(sql=data_select)
   data2 = call_inception.Inception.BeautifySQL(sql=data_ddl_dml)
   data['select'] = data1
   data['dml_ddl'] = data2
   print(data)


#if __name__=='__main__':
if __name__ == '__main__':
    test()



