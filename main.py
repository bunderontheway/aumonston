import spur
import psutil, datetime
import requests
import schedule
import time
shell = spur.SshShell(				#ssh connection
        hostname="139.59.112.115",
        port=443,
        username="root",
        password="krowteneroc",
        missing_host_key=spur.ssh.MissingHostKey.accept
)
with shell:
        result = shell.run(["ifconfig", "eth0"]) #getting ip 

        cpu = psutil.cpu_percent(interval=0.1) #cpu usage
        hdd = psutil.disk_usage('/') #disk usage
        inet = psutil.net_io_counters(pernic=False) #network
        ram = psutil.virtual_memory() #ram
        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
res = {
        "cpu" : float(cpu),
        "hdd.free" :  int(hdd.total - hdd.used),
        "hdd.total": int(hdd.total),
        "inet.packet.in":inet.packets_recv,
        "inet.packet.out":inet.packets_sent,
        "inet.bytes.in":inet.bytes_recv,
        "inet.bytes.out":inet.bytes_sent,
        "ram.free" :ram.free,
        "total":ram.total,
        "tx_date":str(time) 
}
print(result.output)
print(res)
def job():
        r = requests.post('http://139.59.112.115/stat',data = res)
schedule.every(2).seconds.do(job) #schedulling 
while True:
        schedule.run_pending() 
#       time.sleep(1)
