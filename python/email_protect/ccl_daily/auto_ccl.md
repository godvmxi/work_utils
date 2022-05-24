```mermaid
graph TD;
    ResetCurJob[Reset Current Job]
    SendLogAbortReport[Save Log and Report]
    StartRegression[Start Ctest Regression]
    CheckNewDeploy{Check New Deploy}
    CheckUnfinishedJob{Check Unfinished Job, Exist Done flag?}
    NewBoot([Test Board New Boot])
    Deploy[Deploy To Test Board]
    ExitProgram([Exit Current Job])
    CollectTestResult[Collect Test Result]
    SendLogDoneReport[Send Job Done Report]
    SendLogAbortReport[Send Job Abort Report]
    SaveLogInterruptReport[Send Job Interrupt Report]
    CheckFailReachThresHold{Check Fail Reach Threshold}
    SetDoneFlag[Set Done Flag]
    SetAbortFlag[Set Abort Flag]
    CheckAbortFlag{Check Abort Flag}
    CleanUpOldTests[Clean Up Old Tests]


    Diag[[Diag Portal]]
    Diag-->Deploy
    CheckSingleInstance{Check Single Instance}
    
    NewBoot-->CronJob
    CronJob-->CheckSingleInstance
    CheckSingleInstance --Yes--> ExitProgram
    CheckSingleInstance--No-->CleanUpOldTests
    CleanUpOldTests-->CheckNewDeploy
    Deploy-->CheckNewDeploy
    CheckUnfinishedJob--No--> CheckAbortFlag
    CheckAbortFlag --No--> CheckFailReachThresHold
    CheckAbortFlag --Yes--> ExitProgram
    CheckFailReachThresHold --Yes--> SendLogAbortReport
    CheckFailReachThresHold --No--> StartRegression
    SendLogAbortReport-->SetAbortFlag
    SetAbortFlag-->ExitProgram
    CheckNewDeploy--Yes--> ResetCurJob
    ResetCurJob-->SaveLogInterruptReport
    SaveLogInterruptReport-->StartRegression
    CheckNewDeploy--No-->CheckUnfinishedJob
    CheckUnfinishedJob--Yes-->ExitProgram
    StartRegression-->CollectTestResult
    CollectTestResult --> SendLogDoneReport
    SendLogDoneReport --> SetDoneFlag
    SetDoneFlag --> ExitProgram

```

## Report Detail


| key | detail | comment |
| --- | --- | --- |
| ReportType | Report Type | Abort/Interrupt/Done |
| MotherBoard | mother board type | |
| BiosVersion | | |
| TsBuildTime | | |
| TsBuildVersion | | |
| StartTime | | |
| EndTime | | |
| ClkStatus | | |
