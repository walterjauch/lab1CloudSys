import exoscale
exo = exoscale.Exoscale()
import os
 
# export EXOSCALE_API_KEY="EXOb5d59624b13491ac662ef573" EXOSCALE_API_SECRET="5xy-ZybcGcb6xWiM1Y9JT3aE1vmDWZtLKLBmcSgPDpE"

print("creating back instance")
zone_gva = exo.compute.get_zone("ch-gva-2")

front_sg = exo.compute.get_security_group(id="00934966-8753-4bef-977f-3fb6ae38250a")


back_sg = exo.compute.get_security_group(id="00934966-8753-4bef-977f-3fb6ae38250a")

# Creation de l'instance du backend
back_instance = exo.compute.create_instance(
        name="backend",
        zone=zone_gva,
        type=exo.compute.get_instance_type("micro"),
        template= exo.compute.get_instance_template(zone_gva, "101866be-3894-4301-aa59-1c851ad1d23f"),
        security_groups=[back_sg],
        user_data="""
        #cloud-config
        
        runcmd:
        - cd ocr-back-end
        - sh run.sh

        """,
        ssh_key=exo.compute.get_ssh_key("hi"),
        )

print(back_instance.ipv4_address)

print("creating front instance")
#Creation de l'instance du frontend
front_instance = exo.compute.create_instance(
        name="front",
        zone=zone_gva,
        type=exo.compute.get_instance_type("micro"),
        template=list(
            exo.compute.list_instance_templates(zone_gva, "Linux Ubuntu 22.04 LTS 64-bit")
        )[0],
        security_groups=[front_sg],
        user_data="""
        #cloud-config

        package_update: true

        packages:
            - apache2
            - git
        
        runcmd:
            - cd /var/www/html
            - sudo git clone https://gitedu.hesge.ch/nikola.antonije/ocr-front-end.git
            - cd /var/www/html/ocr-front-end
            - sed -i 's/127.0.0.1/""" + back_instance.ipv4_address + """/' /var/www/html/ocr-front-end/canvas.js
            - cd /etc/apache2/sites-available/
            - sudo cp 000-default.conf ocr-front-end.conf
            - sudo nano ocr-front-end.conf
            - sed -i 's/DocumentRoot \/var\/www\/html/DocumentRoot \/var\/www\/html\/ocr-front-end\/' ocr-front-end.conf
            - sudo a2ensite ocr-front-end.conf
            - sudo service apache2 reload
        
        """)

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