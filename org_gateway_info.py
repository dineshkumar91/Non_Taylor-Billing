import config
import requests
import json
billing_org = config.bill_org


def get_org_children(token):

    print("\n\nStep 2:Using the access token to get all information about a particular organization's children................")
    

    for index, elem in enumerate(billing_org):

        customer_name = config.bill_org.get(elem)
        print("The customer name is........................",customer_name)
        customer_no = config.cust_no.get(customer_name)
        print("Use the customer's orgID directly")
        gateway_info(elem,token,customer_name,customer_no)
        print("Now obtain children information")
        url = "https://parkerelevat-account.parker.com/org/"+elem 
        print(elem)
   
        querystring = {"children":"true"}

        headers = {
            'authorization': token,
            'cache-control': "no-cache"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        json_response = response.json()
        child = json_response['children']
        
        
        i = 0
        for child[i] in child:
          keys = child[i].keys()
          for key in child[i]:
            
            if key == '_id':              
              child_org_id = child[i][key]
              gateway_info(child_org_id,token,customer_name,customer_no)
                                          
            if key == 'parentId':              
              parent_org_id = child[i][key]
              gateway_info(parent_org_id,token,customer_name,customer_no)
              
            if key == 'gatewayCount':
              print(child[i][key])
          i+=1
          
        print("Done extracting information")
    return



def gateway_info(organization_id,token,customer_name,customer_no):

    gateway_list = open('gateway_needed_info_old.txt', 'a')

    url = "https://parkerelevat-gateway.parker.com/gateway/all"

    querystring = {"orgID":organization_id}

    headers = {
            'authorization': token,
            'cache-control': "no-cache"
            }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_response = response.json()

    #Extracting and storing 4 important information ---
    # orgID, gateway template, name and status

    
    j=0
    for json_response[j] in json_response:
        child = json_response[j]
        keys = child.keys()
                       
        if 'mastertag' in keys:
            if 'mastertag' == '':
              gateway_list.write("No Master Tag,")
            else:  
              gateway_list.write("%s," % child['mastertag'])
              gateway_list.flush()
              
        else:
            gateway_list.write("No Master Tag,")
            gateway_list.flush()
            
        if 'gtemplate' in keys:
            gchild = child['gtemplate']
            gkeys = gchild.keys()
           
            if 'name' in gkeys:  
                gateway_list.write(" %s," % gchild['name'])
                gateway_list.flush()
                
            else:
                gateway_list.write(" No gateway template name,")
                gateway_list.flush()
                
        if 'orgID' in keys:  
            gateway_list.write(" %s," % child['orgID'])
            gateway_list.write(" %s," % customer_name)
            gateway_list.write(" %s," % customer_no)
            gateway_list.flush()
           
        else:
            gateway_list.write(" No OrgID,")
            gateway_list.write(" %s," % customer_name)
            gateway_list.write(" %s," % customer_no)
            gateway_list.flush()
                            
                
        if 'status' in keys:  
            gateway_list.write(" %s\n" % child['status'])
            gateway_list.flush()
            
        else:
            gateway_list.write(" No status\n")
            gateway_list.flush()

    gateway_list.close()
    return


def clean():
    
    lines_seen = set() 
    outfile = open("gateway_needed_info.txt", "w")
    for line in open("gateway_needed_info_old.txt", "r"):
        if line not in lines_seen: 
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    print("\nGateway information corrected")

