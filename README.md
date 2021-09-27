# Workbench Mitigation
To create input file for script run `grep -B2 ERROR workbench.log |grep -v 'INFO - Term' |grep -v 'INFO - Media' > missing.txt`
Move the newly created file to your script directory


Run `parseError.py --input missing.txt`
A csv file, with headers will now be created at `mediation.csv`
This csv file will be your input file when running a `Create Media` job.

If the Create Media job is not 100% successful, use that job's logfile as a secondary input and run `parseError.py --input missing.txt --secondary mitigation_log.txt`
to create a new csv, then re-run the `Create Media`job.

