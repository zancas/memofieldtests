import json
import pytest
import subprocess
import time
import uuid


#T_ADDRESS_LOCAL_0 = "tmQD1sgq1jqG9NZiyjeUFRwvLM3CBBnNevw" 
#Z_ADDRESS_LOCAL_0 = 

@pytest.fixture(scope="module")
def v1_1_0_containerid(request):
    MINORVERSION = 0
    REFCONTAINER = f"zcash-v1.1.{MINORVERSION}-tester:block256675"
    UNIQUESUFFIX = uuid.uuid4().urn[9:]
    IMAGETAG = f"zcash-v1.1.{MINORVERSION}-tester:{UNIQUESUFFIX}"
    tagrc = subprocess.call(f"docker tag {REFCONTAINER} {IMAGETAG}".split())
    so = open("zcashd.out", "w")
    ZCASHDCONTAINER = subprocess.Popen(f"docker run -t {IMAGETAG}".split(),
                                       stdout=so)
    increment = .00001
    total = 0
    while True:
        time.sleep(increment)
        total += increment
        containers = subprocess.getoutput("docker ps")
        if IMAGETAG in containers:
            for line in containers.split('\n'):
                if IMAGETAG in line:
                    container = line
                    break
            break
    containerID = container.split()[0]
    def cleaner():
        #  TODO: Check return codes.
        stopcode = subprocess.call(f"docker stop {containerID}".split())
        rmtagcode = subprocess.call(f"docker rmi {IMAGETAG}".split())
    request.addfinalizer(cleaner)
    return containerID

def _produce_command_prefix(containerid):
    Z_CLI_PATH = "/home/zcasher/zcash/src/zcash-cli -rpcwait"
    DOCKER_PREFIX_TEMPLATE = "docker exec {CONTAINERID}"
    DOCKER_PREFIX = DOCKER_PREFIX_TEMPLATE.format(CONTAINERID=containerid)
    return f"{DOCKER_PREFIX} {Z_CLI_PATH}"

def _obtain_TAZ_loaded_taddress(cmd_prefix):
    #return taddress

def test_zcashd_encoding_of_empty_memo(v1_1_0_containerid):
    command_prefix = _produce_command_prefix(v1_1_0_containerid)
    _obtain_TAZ_loaded_taddress(command_prefix)
