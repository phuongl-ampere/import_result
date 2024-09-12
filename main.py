import os
import traceback
import paramiko
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import db1, db2, remote_server, local_server  # Import configuration
from sqlalchemy.sql import text  # Ensure this import is present

# Define the base for SQLAlchemy models
Base = declarative_base()

from db import Result

def get_database_session(config):
    print(f"Connecting to database: {config['name']} at {config['host']}:{config['port']}")
    fengine = f'mysql+mysqlconnector://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["name"]}'
    print(f"Engine: {fengine}")
    engine = create_engine(fengine)
    Session = sessionmaker(bind=engine)
    return Session()

def fetch_data():
    print("Fetching data from database...")
    session = get_database_session(db1)
    results = session.query(Result).all() # Fetch full Result records
    # results = session.query(Result).filter(Result.LogFile.like('%202404%.zip')).limit(1).all()
    session.close()
    print(f"Fetched {len(results)} records.")
    return results

from sqlalchemy.sql import text  # Ensure this import is present

from sqlalchemy.sql import text
from sqlalchemy import insert
def insert_into_database2(result, dry_run):
    global count_error, count_success
    if dry_run:
        print(f"[DRY RUN] Would insert record into database2: {result}")
    else:
        print(f"Inserting record into database2: {result}")

        # Prepare parameters
        params = {
            'ECID': result.ECID,
            'Serial': result.Serial,
            'PartId': result.PartId,
            'LotNumber': result.LotNumber,
            'Cores': result.Cores,
            'Frequency': result.Frequency,
            'AVS': result.AVS,
            'TDP': result.TDP,
            'TesterNumber': result.TesterNumber,
            'ScreeningMode': result.ScreeningMode,
            'TestCase': result.TestCase,
            'Operator': result.Operator,
            'BoardSerial': result.BoardSerial,
            'SocketSerial': result.SocketSerial,
            'Environments': result.Environments,
            'StartTime': result.StartTime,
            'RunTime': result.RunTime,
            'Result': result.Result,
            'BinLabel': result.BinLabel,
            'HBin': result.HBin,
            'SBin': result.SBin,
            'LogFile': result.LogFile,
            'ReportFile': result.ReportFile,
            'SummaryFile': result.SummaryFile,
            'LastModified': result.LastModified,
            'CpuType': result.CpuType,
            'HandlerID': result.HandlerID,
            'TestStep': result.TestStep,
            'COM_ECID': result.COM_ECID,
            'IO_ECID': result.IO_ECID,
            'BinFailed': result.BinFailed,
            'FinalLogFile': result.FinalLogFile,
        }

        # Print parameter types for debugging
        # for key, value in params.items():
            # print(f"Parameter: {key}, Value: {value}, Type: {type(value)}")

        sql = text("""
            INSERT INTO slt_ws_result (
                ECID, Serial, PartId, LotNumber, Cores, Frequency, AVS, TDP,
                TesterNumber, ScreeningMode, TestCase, Operator, BoardSerial,
                SocketSerial, Environments, StartTime, RunTime, Result,
                BinLabel, HBin, SBin, LogFile, ReportFile, SummaryFile,
                LastModified, CpuType, HandlerID, TestStep, COM_ECID,
                IO_ECID, BinFailed, FinalLogFile
            ) VALUES (
                :ECID, :Serial, :PartId, :LotNumber, :Cores, :Frequency, :AVS, :TDP,
                :TesterNumber, :ScreeningMode, :TestCase, :Operator, :BoardSerial,
                :SocketSerial, :Environments, :StartTime, :RunTime, :Result,
                :BinLabel, :HBin, :SBin, :LogFile, :ReportFile, :SummaryFile,
                :LastModified, :CpuType, :HandlerID, :TestStep, :COM_ECID,
                :IO_ECID, :BinFailed, :FinalLogFile
            )
        """)

        try:
        # session.execute(sql, params)
            session = get_database_session(db2)
            stmt = insert(Result).values(**params)
            # stmt = sql.bindparams(params)
            session.execute(stmt)
            session.commit()
            count_success += 1
            print(f"Inserted record into count_success: {count_success}")
        except Exception as e:
            print(f"Error during insertion: {e}")
            count_error += 1
        finally:
            session.close()

def ensure_local_directory_exists(local_path, dry_run):
    """Ensure that the local directory exists."""
    directory = os.path.dirname(local_path)
    if not os.path.exists(directory):
        if dry_run:
            print(f"[DRY RUN] Would create directory: {directory}")
        else:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
def check_existed(session, logfile):
    exists = session.query(Result).filter(Result.LogFile == logfile).first() is not None
    if exists:
        return True
    return False
def copy_files(results, dry_run):
    try:
        print("Connecting to the remote server...")
        # Connect to the remote server
        transport = paramiko.Transport((remote_server["ip"], 22))
        transport.connect(username=remote_server["user"], password=remote_server["password"])
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        session = get_database_session(db2)
        for result in results:
            if check_existed(session, result.LogFile):
                print(f"File {result.LogFile} existed in database")
                continue
            # Copy log files
            if result.LogFile:
                remote_log_path = os.path.join(remote_server["log_dir"], result.LogFile)
                local_log_path = os.path.join(local_server["log_dir"], result.LogFile)
                ensure_local_directory_exists(local_log_path, dry_run)  # Ensure directory exists
                if dry_run:
                    print(f"[DRY RUN] Would copy log file from {remote_log_path} to {local_log_path}")
                else:
                    print(f"Copying log file from {remote_log_path} to {local_log_path}")
                    sftp.get(remote_log_path, local_log_path)

            # Copy report files
            if result.ReportFile:
                remote_report_path = os.path.join(remote_server["report_dir"], result.ReportFile)
                local_report_path = os.path.join(local_server["report_dir"], result.ReportFile)
                ensure_local_directory_exists(local_report_path, dry_run)  # Ensure directory exists
                if dry_run:
                    print(f"[DRY RUN] Would copy report file from {remote_report_path} to {local_report_path}")
                else:
                    print(f"Copying report file from {remote_report_path} to {local_report_path}")
                    sftp.get(remote_report_path, local_report_path)

            # Copy final log files
            if result.FinalLogFile:
                remote_final_log_path = os.path.join(remote_server["final_log_dir"], result.FinalLogFile)
                local_final_log_path = os.path.join(local_server["final_log_dir"], result.FinalLogFile)
                ensure_local_directory_exists(local_final_log_path, dry_run)  # Ensure directory exists
                if dry_run:
                    print(f"[DRY RUN] Would copy final log file from {remote_final_log_path} to {local_final_log_path}")
                else:
                    print(f"Copying final log file from {remote_final_log_path} to {local_final_log_path}")
                    sftp.get(remote_final_log_path, local_final_log_path)

            insert_into_database2(result, dry_run)

    except Exception as e:
        print(f"Error copying files: {e}")
        traceback.print_exc()
    finally:
        session.close()
        transport.close()
        print("Disconnected from the remote server.")

if __name__ == "__main__":
    count_error = 0
    count_success = 0
    # Command-line argument for dry run with default value set to True
    parser = argparse.ArgumentParser(description='File copy script with dry run option.')
    parser.add_argument('--dry-run', action='store_false', help='Simulate the operations without making any changes.')
    args = parser.parse_args()

    os.makedirs(local_server["log_dir"], exist_ok=True)
    os.makedirs(local_server["report_dir"], exist_ok=True)
    
    results = fetch_data()
    copy_files(results, args.dry_run)
    print(f"Errors: {count_error}")
    print(f"count_success: {count_success}")