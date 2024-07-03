import json
import xmltodict
from bs4 import BeautifulSoup

xmlstr="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<tenants>
    <name>IHU</name>
</tenants>
"""

jsonString = json.dumps(xmltodict.parse(xmlstr), indent=4)
print(jsonString)

json_data = json.loads(jsonString)
print(json_data['tenants']['name'])

with open('user_data.html') as f:
    html = f.read()

# print(html)

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', {'class': 'filterSortPageTableData tableExpand'})
tbody = table.select_one('tbody')
# print(tbody)
trs = soup.select('tr')
# print(trs)
user_list = list()
for tr in trs:
    name=tr.select('td')[0].text.strip()
    if not name == '':
        user_list.append(name)
print(user_list)

xmlStr = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ecTopology>
    <description>Erasure coding topology for the US, Europe, Canada, and
        Africa-North divisions.</description>
    <erasureCodedObjects>3289</erasureCodedObjects>
    <erasureCodingDelay>10</erasureCodingDelay>
    <fullCopy>false</fullCopy>
    <hcpSystems>
        <name>hcp-an.example.com</name>
        <name>hcp-ca.example.com</name>
        <name>hcp-eu.example.com</name>
        <name>hcp-us.example.com</name>
    </hcpSystems>
    <id>faa9b2e5-a8b0-4211-ac83-6a25dff50800</id>
    <minimumObjectSize>4096</minimumObjectSize>
    <name>ex-corp-4</name>
    <protectionStatus>HEALTHY</protectionStatus>
    <readStatus>HEALTHY</readStatus>
    <replicationLinks>
        <replicationLink>
            <hcpSystems>
                <name>hcp-ca.example.com</name>
                <name>hcp-eu.example.com</name>
            </hcpSystems>
            <name>eu-ca</name>
            <pausedTenantsCount>0</pausedTenantsCount>
            <state>HEALTHY</state>
            <uuid>7ae4101c-6e29-426e-ae71-9a7a529f019d</uuid>
        </replicationLink>
        <replicationLink>
            <hcpSystems>
                <name>hcp-eu.example.com</name>
                <name>hcp-us.example.com</name>
            </hcpSystems>
            <name>us-eu</name>
            <pausedTenantsCount>0</pausedTenantsCount>
            <state>HEALTHY</state>
            <uuid>32871da5-2355-458a-90f5-1717aa684d6f</uuid>
        </replicationLink>
        <replicationLink>
            <hcpSystems>
                <name>hcp-an.example.com</name>
                <name>hcp-us.example.com</name>
            </hcpSystems>
            <name>us-an</name>
            <pausedTenantsCount>0</pausedTenantsCount>
            <state>HEALTHY</state>
            <uuid>c8c875ad-dbfe-437d-abd3-862a6c719894</uuid>
        </replicationLink>
        <replicationLink>
            <hcpSystems>
                <name>hcp-an.example.com</name>
                <name>hcp-ca.example.com</name>
            </hcpSystems>
            <name>ca-an</name>
            <pausedTenantsCount>0</pausedTenantsCount>
            <state>HEALTHY</state>
            <uuid>a1f21e03-fb46-48cc-967e-b0cedf80bb20</uuid>
        </replicationLink>
    </replicationLinks>
    <restorePeriod>5</restorePeriod>
    <state>ACTIVE</state>
    <tenants>
        <name>research-dev</name>
        <name>sales-mktg</name>
        <name>exec</name>
        <name>finance</name>
    </tenants>
    <type>RING</type>
</ecTopology>"""
jsonString = json.dumps(xmltodict.parse(xmlStr), indent=4)
print(jsonString)

json_data = json.loads(jsonString)
#
# xmlStr="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <licenses>
# <license>
#          <localCapacity>10000000000000</activeCapacity>
#          <expirationDate>Jan 1, 2021</expirationDate>
#          <extendedCapacity>0</extendedCapacity>
#          <licenseType>Premium</licenseType>
#          <serialNumber>12345</serialNumber>
#          <uploadDate>Aug 14, 2016</uploadDate>
# </license>
# </licenses>"""
# jsonString = json.dumps(xmltodict.parse(xmlStr), indent=4)
# print(jsonString)
#
# json_data = json.loads(jsonString)


xmlStr="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<nodeStatistics>
     <requestTime>1528292517330</requestTime>
     <nodes>
          <node>
               <nodeNumber>17</nodeNumber>
               <frontendIpAddresses>
                    <ipAddress>172.20.35.17</ipAddress>
                    <ipAddress>2001:623:0:0:222:11ff:fec7:6584</ipAddress>
               </frontendIpAddresses>
               <backendIpAddress>172.35.14.17</backendIpAddress>
               <managementIpAddresses>
                    <ipAddress>172.20.45.17</ipAddress>
                    <ipAddress>2001:623:0:0:222:11ff:fec7:6585</ipAddress>
               </managementIpAddresses>
               <openHttpConnections>0</openHttpConnections>
               <openHttpsConnections>0</openHttpsConnections>
               <maxHttpConnections>255</maxHttpConnections>
               <maxHttpsConnections>254</maxHttpsConnections>
               <cpuUser>0.16</cpuUser>
               <cpuSystem>0.08</cpuSystem>
               <cpuMax>24</cpuMax>
               <ioWait>0.02</ioWait>
               <swapOut>0.0</swapOut>
               <maxFrontEndBandwidth>1024000</maxFrontEndBandwidth>
               <frontEndBytesRead>0.3</frontEndBytesRead>
               <frontEndBytesWritten>0.2</frontEndBytesWritten>
               <maxBackEndBandwidth>1024000</maxBackEndBandwidth>
               <backEndBytesRead>7.22</backEndBytesRead>
               <backEndBytesWritten>3.87</backEndBytesWritten>
               <maxManagementPortBandwidth>1024000</maxManagementPortBandwidth>
               <managementBytesRead>.75</managementBytesRead>
               <managementBytesWritten>.7</managementBytesWritten>
               <collectionTimestamp>1528292472000</collectionTimestamp>
               <volumes>
                    <volume>
                         <id>example090</id>
                         <blocksRead>0.0</blocksRead>
                         <blocksWritten>24.8</blocksWritten>
                         <diskUtilization>0.0</diskUtilization>
                         <transferSpeed>0.57</transferSpeed>
                    </volume>
                    <volume>
                         <id>example091</id>
                         <blocksRead>138.93</blocksRead>
                         <blocksWritten>34.0</blocksWritten>
                         <diskUtilization>0.48</diskUtilization>
                         <transferSpeed>7.82</transferSpeed>
                    </volume>
               </volumes>
          </node>
          <node>
               <nodeNumber>173</nodeNumber>
               <frontendIpAddresses>
                    <ipAddress>172.20.35.16</ipAddress>
                    <ipAddress>2001:623:0:0:222:11ff:fec7:6574</ipAddress>
               </frontendIpAddresses>
               <backendIpAddress>172.35.14.16</backendIpAddress>
               <managementIpAddresses>
                    <ipAddress>172.20.45.16</ipAddress>
                    <ipAddress>2001:623:0:0:222:11ff:fec7:6575</ipAddress>
               </managementIpAddresses>
               <openHttpConnections>0</openHttpConnections>
               <openHttpsConnections>0</openHttpsConnections>
               <maxHttpConnections>255</maxHttpConnections>
               <maxHttpsConnections>254</maxHttpsConnections>
               <cpuUser>0.06</cpuUser>
               <cpuSystem>0.06</cpuSystem>
               <cpuMax>24</cpuMax>
               <ioWait>0.0</ioWait>
               <swapOut>0.0</swapOut>
               <maxFrontEndBandwidth>1024000</maxFrontEndBandwidth>
               <frontEndBytesRead>0.17</frontEndBytesRead>
               <frontEndBytesWritten>0.1</frontEndBytesWritten>
               <maxBackEndBandwidth>1024000</maxBackEndBandwidth>
               <backEndBytesRead>5.2</backEndBytesRead>
               <backEndBytesWritten>2.7</backEndBytesWritten>
               <maxManagementPortBandwidth>1024000</maxManagementPortBandwidth>
               <managementBytesRead>.32</managementBytesRead>
               <managementBytesWritten>.27</managementBytesWritten>
               <collectionTimestamp>1528292486000</collectionTimestamp>
               <volumes>
                    <volume>
                         <id>example092</id>
                         <blocksRead>0.0</blocksRead>
                         <blocksWritten>6.8</blocksWritten>
                         <diskUtilization>0.0</diskUtilization>
                         <transferSpeed>0.27</transferSpeed>
                    </volume>
                    <volume>
                         <id>example093</id>
                         <blocksRead>13.93</blocksRead>
                         <blocksWritten>28.0</blocksWritten>
                         <diskUtilization>0.08</diskUtilization>
                         <transferSpeed>1.82</transferSpeed>
                    </volume>
               </volumes>
          </node>
     </nodes>
</nodeStatistics>"""
jsonString = json.dumps(xmltodict.parse(xmlStr), indent=4)
print(jsonString)

json_data = json.loads(jsonString)
print(json_data)
json_data
#
#
# xmlStr="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <serviceStatistics>
#      <requestTime>1524773822369</requestTime>
#      <services>
#           <service>
#                <name>StorageTieringService</name>
#                <state>RUNNING</state>
#                <startTime>1524773425</startTime>
#                <endTime>-1</endTime>
#                <performanceLevel>MEDIUM</performanceLevel>
#                <objectsExamined>0</objectsExamined>
#                <objectsServiced>0</objectsServiced>
#                <objectsUnableToService>0</objectsUnableToService>
#           </service>
#           <service>
#                <name>GarbageCollection</name>
#                <state>READY</state>
#                <startTime>1523624400</startTime>
#                <endTime>1523624748</endTime>
#                <objectsExamined>29530</objectsExamined>
#                <objectsServiced>27570</objectsServiced>
#                <objectsUnableToService>5</objectsUnableToService>
#           </service>
#           <service>
#                <name>RetirementPolicy</name>
#                <state>DISABLED</state>
#                <startTime>-1</startTime>
#                <endTime>-1</endTime>
#                <objectsExamined>0</objectsExamined>
#                <objectsServiced>0</objectsServiced>
#                <objectsUnableToService>0</objectsUnableToService>
#           </service>
#      </services>
# </serviceStatistics>"""
# jsonString = json.dumps(xmltodict.parse(xmlStr), indent=4)
# print(jsonString)
#
# json_data = json.loads(jsonString)
#
# xmlStr="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <tenant>
#     <name>Finance</name>
#     <systemVisibleDescription>Created for the Finance department at Example
#         Company by P.D. Grey on 2/9/2017.</systemVisibleDescription>
#     <hardQuota>100 GB</hardQuota>
#     <softQuota>90</softQuota>
#     <namespaceQuota>5</namespaceQuota>
#     <authenticationTypes>
#         <authenticationType>LOCAL</authenticationType>
#         <authenticationType>EXTERNAL</authenticationType>
#     </authenticationTypes>
#     <complianceConfigurationEnabled>true</complianceConfigurationEnabled>
#     <versioningConfigurationEnabled>true</versioningConfigurationEnabled>
#     <searchConfigurationEnabled>true</searchConfigurationEnabled>
#     <replicationConfigurationEnabled>true</replicationConfigurationEnabled>
#     <erasureCodingSelectionEnabled>true</erasureCodingSelectionEnabled>
#     <tags>
#         <tag>Example Company</tag>
#         <tag>pdgrey</tag>
#     </tags>
#     <servicePlanSelectionEnabled>false</servicePlanSelectionEnabled>
#     <servicePlan>Short-Term-Activity</servicePlan>
#     <dataNetwork>net127</dataNetwork>
#     <managementNetwork>net004</managementNetwork>
# </tenant>"""
# jsonString = json.dumps(xmltodict.parse(xmlStr), indent=4)
# print(jsonString)
# json_data = json.loads(jsonString)
# print(json_data['tenant']['name'])
#
# xmlStr="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <namespace>
#     <name>Accounts-Receivable</name>
#     <description>Created for the Finance department at Example Company by Lee
#         Green on 2/9/2017.</description>
#     <hashScheme>SHA-256</hashScheme>
#     <enterpriseMode>true</enterpriseMode>
#     <hardQuota>50 GB</hardQuota>
#     <softQuota>75</softQuota>
#     <servicePlan>Short-Term-Activity</servicePlan>
#     <optimizedFor>CLOUD</optimizedFor>
#     <versioningSettings>
#         <enabled>true</enabled>
#         <prune>true</prune>
#         <pruneDays>10</pruneDays>
#     </versioningSettings>
#     <multipartUploadAutoAbortDays>10</multipartUploadAutoAbortDays>
#     <searchEnabled>true</searchEnabled>
#     <indexingEnabled>true</indexingEnabled>
#     <customMetadataIndexingEnabled>true</customMetadataIndexingEnabled>
#     <customMetadataValidationEnabled>true</customMetadataValidationEnabled>
#     <replicationEnabled>true</replicationEnabled>
#     <allowErasureCoding>true</allowErasureCoding>
#     <readFromReplica>true</readFromReplica>
#     <serviceRemoteSystemRequests>true</serviceRemoteSystemRequests>
#     <tags>
#         <tag>Billing</tag>
#         <tag>lgreen</tag>
#     </tags>
# </namespace>"""
# print('#'*50)
# jsonString = json.dumps(xmltodict.parse(xmlStr), indent=4)
# print(jsonString)
# json_data = json.loads(jsonString)
#
# xml_dict = xmltodict.parse(xmlStr)
# print(type(xml_dict))
