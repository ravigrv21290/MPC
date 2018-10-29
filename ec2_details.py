mport boto3
import mysql.connector
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Atmecs@123",
        database="ec2"
        )

mycursor = mydb.cursor()
#mycursor2 = mydb.cursor()
delq = "DELETE FROM ec2details"
mycursor.execute(delq)
mydb.commit()
try:
	ec2client = boto3.client('ec2')
	response = ec2client.describe_instances()
	#print response
        
	for reservation in response["Reservations"]:
    		for instance in reservation["Instances"]:
        		# This sample print will output entire Dictionary object
        
        		# This will print will output the value of the Dictionary key 'InstanceId'
        		id = instance["InstanceId"]
        		os_type = instance["InstanceType"]
        		region = instance["Placement"].get('AvailabilityZone')
        		state = instance["State"].get('Name')
                        if state == 'terminated':
                           elastic_ip = "NA"
                        else:
                           elastic_ip = instance["PublicIpAddress"]
		
        		image_id = instance["ImageId"]
        		launch_time = instance["LaunchTime"]
        		key_name = instance["KeyName"]
			if state == 'terminated':
                        	vpc_id = "NA"
                        else:
                        	vpc_id = instance["VpcId"]
			
			if state == 'terminated':
                                sg_name = "NA"
                        else:
                                for sg in  instance["SecurityGroups"]:
                                
            				sg_name=sg['GroupName']

        		#print id,os_type,state,region,image_id,key_name,sg_name,elastic_ip,launch_time,vpc_id 
              
                	sql = "INSERT IGNORE INTO ec2details(id,os_name,region,state,elastic_ip,image_id,launch_time,key_name,vpc_id,sg_name) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
                	val = (id, os_type, region, state, elastic_ip, image_id, launch_time, key_name, vpc_id, sg_name)
                	mycursor.execute(sql, val)
                	mydb.commit()
                	print(mycursor.rowcount, "record inserted.")

except Exception as error:
    
	print error	


