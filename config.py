
db1_host = "10.38.177.21"
db1_port = "13306"
db1_user = "sltadm"
db1_password = "SltAdmin%401234"
db1_name = "SltDB"
db1 = {
    "host": db1_host,
    "port": db1_port,
    "user": db1_user,
    "password": db1_password,
    "name": db1_name
}

# Database 2 (destination) connection parameters
db2_host = "den-slt-01.amperecomputing.com"
db2_port = "3306"
db2_user = "sltadm"
db2_password = "SltAdmin%401234"
db2_name = "Slt_VDC_DEV"
db2 = {
    "host": db2_host,
    "port": db2_port,
    "user": db2_user,
    "password": db2_password,
    "name": db2_name
}


# Remote server parameters
remote_ip = "10.38.177.23"
remote_user = "root"
remote_password = "Ampere@4655"
remote_log_dir = "/slt_logs_local/Logs"
remote_report_dir = "/slt_logs_local/Reports"
remote_summary_dir = "/slt_logs_local/Summary"
remote_final_log_dir = "/slt_logs_local/Reports"
remote_server = {
    "ip": remote_ip,
    "user": remote_user,
    "password": remote_password,
    "log_dir": remote_log_dir,
    "report_dir": remote_report_dir,
    "summary_dir": remote_summary_dir,
    "final_log_dir": remote_final_log_dir
}
# Local directory to copy files to
root_local_dir = "/slt_logs"
local_log_dir = f"{root_local_dir}/Logs"
local_report_dir = f"{root_local_dir}/Reports"
local_summary_dir =f"{root_local_dir}/Summary"
local_final_log_dir = f"{root_local_dir}/Reports"
local_server = {
    "log_dir": local_log_dir,
    "report_dir": local_report_dir,
    "summary_dir": local_summary_dir,
    "final_log_dir": local_final_log_dir
}

