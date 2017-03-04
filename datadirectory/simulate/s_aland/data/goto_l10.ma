behavior_name=goto_list				
# GOTO_L10.MA for aland2017_1 mission				
# 20.2.2017 kimmo.tikka@fmi.fi  Lågskär söder-west				
<start:b_arg>				
b_arg: start_when(enum) 0				
b_arg: list_stop_when(enum) 007				
b_arg: initial_wpt(enum)  -1  # one after last one achieved				
b_arg: num_legs_to_run(nodim)   -2    #  traverse list once (stop at last in list)				
b_arg: num_waypoints(nodim) 6				
<end:b_arg>				
<start:waypoints>				
#WPT FORMAT: (DDmm.mmm)				
# longitude	latitude	koodi	nimi	
1959.3749	5947.1994	#   0	LÅGS_SN_A_1	
1956.9784	5946.1750	#   1	LÅGS_SN_A_2	
1953.5757	5946.1438	#   2	LÅGS_SN_A_3	
1949.4440	5946.5229	#   3	LÅGS_SN_A_4	
1945.8277	5946.3735	#   4	LÅGS_SN_A_5	
1941.9557	5947.3173	#   5	LÅGS_SN_A_6		
<end:waypoints>				
