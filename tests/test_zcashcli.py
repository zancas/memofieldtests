import subprocess
import time
import uuid

MINORVERSION = 0
REFCONTAINER = f"zcash-v1.1.{MINORVERSION}-tester:latest"
UNIQUESUFFIX = uuid.uuid4().urn[9:]
IMAGETAG = f"zcash-v1.1.{MINORVERSION}-tester:{UNIQUESUFFIX}"
tagrc = subprocess.call(f"docker tag {REFCONTAINER} {IMAGETAG}".split())
print(f"IMAGETAG is {IMAGETAG}")
print(f"tagrc is: {tagrc}")
so = open("zcashd.out", "w")
ZCASHDCONTAINER = subprocess.Popen(f"docker run -t {IMAGETAG}".split(),
                                   stdout=so)
container = ''
increment = .00001
total = 0
while True:
    time.sleep(increment)
    total += increment
    containers = subprocess.getoutput("docker ps")
    if IMAGETAG in containers:
        for line in containers.split('\n'):
            if IMAGETAG in line:
                print(line)
                container = line
                break
        break
print(f"total: {total}")
containerID = container.split()[0]
print(containerID)

def test_run_hello_world():
    print("hello")
    #print(subprocess.getoutput(f"{ZCASH_CLI} help"))
    #print(subprocess.getoutput(f"{ZCASH_CLI} z_getnewaddress"))
    #print(subprocess.getoutput(f"{ZCASH_CLI} z_getoperationstatus"
    #    " '[\"opid-a377a0b0-3ffd-4c2b-95c8-4aef3b2def8a\"]'"))
    #print(subprocess.getoutput(f"docker stop {IMAGETAG}"))
    

    

