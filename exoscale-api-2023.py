# Creator: Francisco Mendonca (francisco.mendonca@hesge.ch)
import exoscale
import os
import time


# Before using, please install exoscale-cli, and do:
#  exo c0onfig
#  Follow the instruction to create API keys.
#  And follow the instruction on how to use exoscale on python from:
#  https://www.exoscale.c/syslog/official-python-bindings-for-the-exoscale-api/


# Creates Exoscale Object
exo = exoscale.Exoscale()
print("API_KEY : " + exo.api_key)
# Create the zone object
zone_gva2 = exo.compute.get_zone("ch-gva-2")
elastic_ip = exo.compute.create_elastic_ip(zone_gva2)

# If the security group hasn't yet been created uncomment the following:

# if the security group has been crated uncomment the following:
# and comment out the previous one
security_group_web = exo.compute.get_security_group("default")

if not security_group_web:
    security_group_web = exo.compute.create_security_group("default")
    for rule in [
        exoscale.api.compute.SecurityGroupRule.ingress(
            description="HTTP",
            network_cidr="0.0.0.0/0",
            port="80",
            protocol="tcp",
        ),
        exoscale.api.compute.SecurityGroupRule.ingress(
            description="HTTPS",
            network_cidr="0.0.0.0/0",
            port="443",
            protocol="tcp",
        ),
        exoscale.api.compute.SecurityGroupRule.ingress(
            description="SSH",
            network_cidr="0.0.0.0/0",
            port="22",
            protocol="tcp",
        )
        ]:
        security_group_web.add_rule(rule)

print("Creating Instance...")


# BACKEND
back_instance = exo.compute.create_instance(
    name="Backend",
    zone=zone_gva2,
    type=exo.compute.get_instance_type("small"),
    template=list(
        exo.compute.list_instance_templates(
            zone_gva2,
            "Linux Ubuntu 20.04 LTS 64-bit"))[0],
    volume_size=50,
    security_groups=[security_group_web],
    user_data="""#cloud-config
    package_upgrade: true
    packages:
        - nginx
        - python3-pip
        - fastapi
        - uvicorn
        - git
    write_files:
        - path: /etc/nginx/sites_enabled/fastapi_nginx
        content: server {
            listen 80;
            server_name: {eip}
            location / {
                proxy_pass http://127.0.0.1:8000
            }
        }

    runcmd:
        - sudo service nginx restart
        - git clone https://github.com/walterjauch/lab1CloudSys.git
        - cd lab1CloudSys
        - python3 -m uvicorn api:app
    """.format(
    eip=elastic_ip.address)
)

input("Backend is ready")

#FONTEND
front_instance = exo.compute.create_instance(
     name="Frontend",
     zone=zone_gva2,
     type=exo.compute.get_instance_type("small"),
     template=list(
         exo.compute.list_instance_templates(
             zone_gva2,
             "Linux Ubuntu 20.04 LTS 64-bit"))[0],
     volume_size=50,
     security_groups=[security_group_web]
     )


input("Frontend is ready")


print("Instance:")
print("ID: ", back_instance.id)

print("Name:", back_instance.name)

print("IP Address: ", back_instance.ipv4_address)

# Delete Image

print("Deleted VM")
back_instance.delete()



## S3 Bucket

bucket = exo.storage.create_bucket("exoscale-bucket", zone="ch-gva-2")

# # Create empty file
if not os.path.isfile("localfile.txt"):
    open("localfile.txt", "a")


# Insert file in bucket
print("Writing Item to Bucket")
file_index = bucket.put_file("localfile.txt","file-in-bucket.txt")

# List files in bucket
print(bucket.list_files())

input('File has been uploaded. Please check, then press any button.')

# Download file to folder
print("Downloading file from Bucket")
f = bucket.get_file('file-in-bucket.txt')

# There is no Download procedure. So we have to create our own.
with open('downloaded-file.txt', "a") as df:
    for entry in f.content.read():
        f.append(entry)


# Delete all files
print("Deleting all items in Bucket")
for f in bucket.list_files():
    print("Deleting: ", f)
    f.delete()

# Delete Bucket
print("Deleting Bucket\n")
bucket.delete()
